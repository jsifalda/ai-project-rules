"""
render-report.py
================
Reads a code-review run directory and writes a single self-contained HTML report.

Usage
-----
    python3 render-report.py --run-dir <dir> --out <path/to/report.html>

Input contract
--------------
The run directory must contain exactly one file: ``report.json``.

Shape of report.json
~~~~~~~~~~~~~~~~~~~~
{
  "meta": {
    "source": str,               # e.g. "MR !1234" or "branch feat/x"
    "source_url": str | null,
    "generated_at": str,         # ISO timestamp
    "reviewers_run": [str],
    "reviewers_skipped": [{"name": str, "reason": str}],
    "diff_stats": {"files": int, "insertions": int, "deletions": int},
    "council_convened": bool,
    "pipeline": {                # OPTIONAL — when present, an ASCII chart is rendered
                                 # at the top of the report (after the header, before
                                 # the verdict). All keys inside are optional too.
      "invocation": str,         # e.g. "/code-review-full MR !1234"
      "sources": [               # what was fetched and from where
        {"what": str,            # "GitLab MR !1234"
         "from": str,            # "glab api"
         "detail": str}          # "12 files, +340/-58"
      ],
      "reviewers": [
        {"role": str,            # "correctness" | "structural" | "direct-read" | "spec-conformance"
         "delegate": str,        # "code-review agent" | "code-review-nuclear" | "this agent"
         "model": str,           # "claude-opus-5", or "" when not applicable
         "mode": str,            # "delegated" | "inline"
         "tool_calls": int|null,
         "duration_s": int|null,
         "findings": int|null}
      ],
      "stages": [                # free-form pipeline steps between review and verdict.
                                 # ONLY steps that have no key of their own. Never put
                                 # sources, reviewers, the council or the verdict here,
                                 # they each have a dedicated key and a stage duplicate
                                 # renders the branch twice.
        {"name": str,            # "MERGE + VERIFY"
         "detail": str|[str]}    # "14 raw -> 9 deduped" (list of str also accepted)
      ],
      "council": {"mode": str, "model": str, "advisors": int, "peer_reviews": int,
                  "kept": int, "overflow": int},
      "outcome": str             # "2 FIX BEFORE MERGE, 1 FOLLOW-UP TICKET"
    }
  },
  "verdict": {
    "headline": str,
    "summary": str               # markdown
  },
  "findings": [
    {
      "id": str,
      "verdict": str,            # "FIX BEFORE MERGE" | "FOLLOW-UP TICKET" | ...
      "severity": str,           # "high" | "medium" | "low"
      "origins": [str],
      "file": str,               # exactly one file path; must not contain commas
      "lines": str,              # exactly one line number (e.g. "122") or range (e.g. "196-197");
                                 # may have leading "L"; must not contain commas or semicolons
      "claim": str,              # markdown
      "consequence": str,        # markdown
      "fix_direction": str,      # markdown
      "evidence": str,           # markdown
      "comment": str             # paste-ready plain text, multi-line, newlines permitted
    }
  ],

  # All fields below are OPTIONAL. Missing keys degrade gracefully.

  "overflow": [
    {"id": str, "verdict": str, "file": str, "lines": str,
     "claim": str, "reason_cut": str}
  ],
  "dropped": [
    {"id": str, "file": str, "lines": str, "claim": str,
     "disproof": str}              # markdown
  ],
  "corrections": [
    {"target": str, "claim": str, "correction": str}
  ],
  "record": {
    "original_request": str,       # OPTIONAL markdown — the user's original request as
                                   # received; rendered as a collapsed block titled
                                   # "Original request", placed first before framed_question
    "framed_question": str,        # markdown
    "advisors": [
      {"name": str, "letter": str, "response": str}  # response is markdown
    ],
    "peer_reviews": [
      {"probe": str, "response": str}               # response is markdown
    ],
    "anonymization_mapping": {str: str},            # {"A": "The Executor"}
    "ranked_list": str,            # OPTIONAL markdown — the full ranked finding list before
                                   # the cap was applied; rendered as a collapsed block titled
                                   # "Ranked list (before cap)", placed immediately before synthesis
    "synthesis": str,              # markdown
    "process_notes": str           # markdown
  }
}

Validation behavior
~~~~~~~~~~~~~~~~~~~
Malformed findings (where file contains a comma, or lines is not a single number/range)
are flagged in stderr but still rendered in the HTML with an inline "ANCHOR NOT POSTABLE"
badge. Exit code remains 0 to surface the flaw without withholding the report.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Malformed finding detection
# ---------------------------------------------------------------------------

def validate_findings_and_collect_malformed(
    findings_list: List[Dict[str, Any]], section_name: str
) -> Dict[str, str]:
    """
    Validate findings in a list (findings/overflow/dropped).
    Returns {finding_id: reason_str} for malformed findings.
    """
    malformed = {}
    for finding in findings_list:
        fid = finding.get("id", "?")
        file_val = finding.get("file", "")
        lines_val = finding.get("lines", "")

        # file must not contain comma
        if "," in str(file_val):
            malformed[fid] = f"file contains comma"
            continue

        # file must not be empty if lines is present
        if not file_val and lines_val:
            malformed[fid] = f"file is empty but lines is present"
            continue

        # lines must be a single number or single range (allow leading L, strip whitespace)
        if lines_val:
            lines_clean = str(lines_val).strip()
            if lines_clean.startswith("L"):
                lines_clean = lines_clean[1:]

            # invalid if contains comma or semicolon (multiple ranges/values)
            if "," in lines_clean or ";" in lines_clean:
                malformed[fid] = f"lines contains comma or semicolon"
                continue

            # must be single number or single range (N or N-M)
            if "-" in lines_clean:
                parts = lines_clean.split("-")
                if len(parts) != 2 or not all(p.isdigit() for p in parts):
                    malformed[fid] = f"lines is not a valid range"
                    continue
            elif not lines_clean.isdigit():
                malformed[fid] = f"lines is not a valid number or range"
                continue

    return malformed


# ---------------------------------------------------------------------------
# Markdown -> HTML (subset only)
# ---------------------------------------------------------------------------

def md_to_html(text: str) -> str:
    """
    Convert a small markdown subset to HTML.
    Handles: fenced code blocks, inline code, bold, unordered lists, paragraphs.
    Everything else is rendered as escaped text.
    """
    if not text:
        return ""

    # 1. Fenced code blocks (``` ... ```) -- extract before anything else.
    fence_pattern = re.compile(r"```(?:[^\n]*)?\n(.*?)```", re.DOTALL)
    code_blocks: List[str] = []

    def _store_code(m: re.Match) -> str:  # type: ignore[type-arg]
        code_blocks.append(html.escape(m.group(1)))
        return f"\x00CODE{len(code_blocks) - 1}\x00"

    text = fence_pattern.sub(_store_code, text)

    # 2. Split into lines for list / paragraph handling.
    lines = text.split("\n")
    output: List[str] = []
    in_list = False

    for line in lines:
        # Restore code block placeholders inside lines (shouldn't split mid-block).
        stripped = line.rstrip()

        # Unordered list items: "- " or "* ".
        if re.match(r"^[\-\*] ", stripped):
            if not in_list:
                output.append("<ul>")
                in_list = True
            item = stripped[2:]
            output.append(f"<li>{_inline_md(item)}</li>")
        else:
            if in_list:
                output.append("</ul>")
                in_list = False
            if stripped == "":
                output.append("<br>")
            else:
                output.append(f"<p>{_inline_md(stripped)}</p>")

    if in_list:
        output.append("</ul>")

    result = "\n".join(output)

    # 3. Restore fenced code blocks.
    for i, code in enumerate(code_blocks):
        result = result.replace(f"\x00CODE{i}\x00", f"<pre><code>{code}</code></pre>")

    return result


def _inline_md(text: str) -> str:
    """Apply inline markdown transforms (bold, inline code) to already-escaped text."""
    # Escape HTML first.
    text = html.escape(text)
    # Inline code: `...`
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Bold: **...**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def e(value: Any) -> str:
    """Escape a value for safe HTML output."""
    return html.escape(str(value) if value is not None else "")


SEVERITY_COLOR = {
    "high": "#c0392b",
    "medium": "#e67e22",
    "low": "#2980b9",
}

VERDICT_COLOR = {
    "BLOCK MERGE": "#8e1616",
    "FIX BEFORE MERGE": "#c0392b",
    "FOLLOW-UP TICKET": "#e67e22",
    "DROP": "#7f8c8d",
    "INFORMATIONAL": "#2980b9",
}


def severity_badge(severity: str) -> str:
    color = SEVERITY_COLOR.get(severity.lower(), "#555")
    return (
        f'<span style="background:{color};color:#fff;padding:2px 8px;'
        f'border-radius:4px;font-size:0.8em;font-weight:600">'
        f'{e(severity.upper())}</span>'
    )


def verdict_badge(verdict: str) -> str:
    color = VERDICT_COLOR.get(verdict.upper(), "#555")
    return (
        f'<span style="background:{color};color:#fff;padding:2px 8px;'
        f'border-radius:4px;font-size:0.8em;font-weight:600">'
        f'{e(verdict)}</span>'
    )


def malformed_badge(reason: str) -> str:
    return (
        f'<span style="background:#d32f2f;color:#fff;padding:2px 8px;'
        f'border-radius:4px;font-size:0.8em;font-weight:600" '
        f'title="Not postable to code review: {e(reason)}">'
        f'ANCHOR NOT POSTABLE</span>'
    )


def copy_button(finding_id: str) -> str:
    return (
        f'<button onclick="copyComment(\'{e(finding_id)}\')" '
        f'style="font-size:0.8em;padding:3px 10px;cursor:pointer;'
        f'border:1px solid #ccc;border-radius:4px;background:#f5f5f5">'
        f'Copy comment</button>'
    )


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def _fmt_duration(seconds: Any) -> str:
    """Format a duration in seconds as '6m40s' or '12s'. Returns '' for None/null."""
    if seconds is None:
        return ""
    try:
        s = int(seconds)
    except (TypeError, ValueError):
        return ""
    if s >= 60:
        return f"{s // 60}m{s % 60:02d}s"
    return f"{s}s"


def _plural(count: Any, noun: str) -> str:
    """Render '1 finding' / '3 findings'. Returns '' when count is None."""
    if count is None:
        return ""
    try:
        n = int(count)
    except (TypeError, ValueError):
        return ""
    return f"{n} {noun}" if n == 1 else f"{n} {noun}s"


def _dot_pad(text: str, width: int) -> str:
    """Pad non-empty text to width using dot leaders: 'foo .....'"""
    if len(text) >= width:
        return text
    return text + " " + "." * (width - len(text) - 1)


def _pad_col(text: str, width: int) -> str:
    """
    Pad a column to width.
    Uses dot leaders when text is non-empty (value on both sides of the leader).
    Uses spaces when text is empty so no spurious dot run appears.
    """
    if not text:
        return " " * width
    return _dot_pad(text, width)


def _wrap_pre(chart_plain: str) -> str:
    """Wrap a plain-text chart string in the standard <section>/<pre> block."""
    return (
        '<section style="margin-bottom:28px">'
        '<h2 style="font-size:1.2em;margin-bottom:8px">How this review ran</h2>'
        f'<pre style="background:#f8f8f8;border:1px solid #ddd;padding:12px 16px;'
        f'border-radius:4px;overflow-x:auto;font-family:&quot;SFMono-Regular&quot;,Consolas,'
        f'monospace;font-size:0.82em;line-height:1.5">{e(chart_plain)}</pre>'
        "</section>"
    )


def build_pipeline_chart(pipeline: Dict[str, Any]) -> str:
    """
    Build an ASCII pipeline chart from the structured pipeline data.
    Returns '' when pipeline is falsy.

    The chart is built entirely as plain text (no per-field HTML escaping).
    Column widths are computed from raw string lengths so dot leaders align
    correctly regardless of HTML-special characters in values.
    e() is called exactly once, on the finished plain-text string, in _wrap_pre.
    """
    if not pipeline:
        return ""

    invocation: str = pipeline.get("invocation") or ""
    sources: List[Dict[str, Any]] = pipeline.get("sources") or []
    reviewers: List[Dict[str, Any]] = pipeline.get("reviewers") or []
    stages: List[Dict[str, Any]] = pipeline.get("stages") or []
    council: Optional[Dict[str, Any]] = pipeline.get("council")
    outcome: str = pipeline.get("outcome") or ""

    def _child_conn(i: int, total: int) -> str:
        return "`- " if i == total - 1 else "+- "

    # Build branches as (title_line, child_lines) tuples — plain text only.
    branches: List[tuple] = []

    # ---- SOURCES ----
    if sources:
        what_w = max(len(s.get("what") or "") for s in sources) + 2
        from_w = max(len(s.get("from") or "") for s in sources) + 2
        children: List[str] = []
        for i, src in enumerate(sources):
            what_str = _pad_col(src.get("what") or "", what_w)
            from_str = _pad_col(src.get("from") or "", from_w)
            detail_str = src.get("detail") or ""
            children.append(
                f"{_child_conn(i, len(sources))}{what_str} {from_str} {detail_str}".rstrip()
            )
        branches.append(("SOURCES", children))

    # ---- REVIEWERS ----
    if reviewers:
        def _delegate_display(rev: Dict[str, Any]) -> str:
            d = rev.get("delegate") or ""
            return f"{d} (inline)" if (rev.get("mode") or "") == "inline" else d

        role_w = max(len(r.get("role") or "") for r in reviewers) + 2
        delegate_w = max(len(_delegate_display(r)) for r in reviewers) + 2
        model_w = max(len(r.get("model") or "") for r in reviewers) + 2

        rev_children: List[str] = []
        for i, rev in enumerate(reviewers):
            role_str = _pad_col(rev.get("role") or "", role_w)
            delegate_str = _pad_col(_delegate_display(rev), delegate_w)
            model_val = rev.get("model") or ""
            model_str = _pad_col(model_val, model_w)
            tc = rev.get("tool_calls")
            dur = rev.get("duration_s")
            findings_n = rev.get("findings")
            tc_str = _plural(tc, "call") if tc is not None else ""
            dur_str = _fmt_duration(dur)
            findings_str = _plural(findings_n, "finding") if findings_n is not None else ""
            tail = "  ".join(p for p in [tc_str, dur_str, findings_str] if p)
            rev_children.append(
                f"{_child_conn(i, len(reviewers))}{role_str} {delegate_str} {model_str} {tail}".rstrip()
            )
        rev_title = (
            f"REVIEWERS ({len(reviewers)}, parallel)"
            if len(reviewers) > 1
            else "REVIEWERS (1)"
        )
        branches.append((rev_title, rev_children))

    # ---- FREE-FORM STAGES ----
    for stage in stages:
        stage_name = stage.get("name") or ""
        detail = stage.get("detail") or ""
        stage_children: List[str] = []
        if detail:
            detail_items: List[str] = detail if isinstance(detail, list) else [str(detail)]
            for i, item in enumerate(detail_items):
                stage_children.append(f"{_child_conn(i, len(detail_items))}{item}")
        branches.append((stage_name, stage_children))

    # ---- COUNCIL ----
    if council:
        mode = council.get("mode") or ""
        model = council.get("model") or ""
        advisors = council.get("advisors")
        peer_reviews_n = council.get("peer_reviews")
        kept = council.get("kept")
        c_overflow = council.get("overflow")
        header_parts = [p for p in [mode, model] if p]
        council_title = f"COUNCIL ({', '.join(header_parts)})" if header_parts else "COUNCIL"
        c_detail_parts: List[str] = []
        if advisors is not None:
            c_detail_parts.append(_plural(advisors, "advisor"))
        if peer_reviews_n is not None:
            c_detail_parts.append(_plural(peer_reviews_n, "peer review"))
        c_detail_parts.append("chairman")
        ko_parts: List[str] = []
        if kept is not None:
            ko_parts.append(f"{kept} kept")
        if c_overflow is not None:
            ko_parts.append(f"{c_overflow} overflow")
        if ko_parts:
            c_detail_parts.append(", ".join(ko_parts))
        council_detail = " -> ".join(c_detail_parts)
        branches.append((council_title, [f"`- {council_detail}"] if council_detail else []))

    # ---- VERDICT ----
    if outcome:
        branches.append((f"VERDICT  {outcome}", []))

    if not branches:
        return _wrap_pre(invocation) if invocation else ""

    # Emit the full chart as plain text.
    # - invocation line only when present (Fix 4)
    # - "|" spacer only BETWEEN branches, never after the last one (Fix 2)
    # - last branch uses "`- " connector; its children use "   " prefix (Fix 2)
    # - strip trailing whitespace from every line (Fix 4)
    plain_lines: List[str] = []
    if invocation:
        plain_lines.append(invocation)
        plain_lines.append("|")

    n = len(branches)
    for idx, (title, children) in enumerate(branches):
        last = idx == n - 1
        branch_conn = "`- " if last else "+- "
        child_prefix = "   " if last else "|  "
        plain_lines.append(f"{branch_conn}{title}")
        for child in children:
            plain_lines.append(f"{child_prefix}{child}")
        if not last:
            plain_lines.append("|")

    chart_plain = "\n".join(line.rstrip() for line in plain_lines)
    return _wrap_pre(chart_plain)


def build_header(meta: Dict[str, Any]) -> str:
    source = meta.get("source", "")
    source_url = meta.get("source_url")
    generated_at = meta.get("generated_at", "")
    reviewers_run: List[str] = meta.get("reviewers_run") or []
    reviewers_skipped: List[Dict[str, str]] = meta.get("reviewers_skipped") or []
    diff_stats: Dict[str, Any] = meta.get("diff_stats") or {}

    source_html = (
        f'<a href="{e(source_url)}">{e(source)}</a>'
        if source_url
        else e(source)
    )

    skipped_warning = ""
    if reviewers_skipped:
        items = "".join(
            f'<li><strong>{e(s.get("name","?"))}</strong>: {e(s.get("reason",""))}</li>'
            for s in reviewers_skipped
        )
        skipped_warning = (
            '<div style="background:#fff3cd;border-left:4px solid #e67e22;'
            'padding:12px 16px;margin:16px 0;border-radius:4px">'
            '<strong>Warning: some reviewers were skipped</strong>'
            f'<ul style="margin:6px 0 0 0">{items}</ul></div>'
        )

    run_tags = " ".join(
        f'<code style="background:#e8f5e9;padding:1px 6px;border-radius:3px">'
        f'{e(r)}</code>'
        for r in reviewers_run
    )

    stats_parts: List[str] = []
    if diff_stats:
        if "files" in diff_stats:
            stats_parts.append(f'{e(diff_stats["files"])} files')
        if "insertions" in diff_stats:
            stats_parts.append(
                f'<span style="color:#27ae60">+{e(diff_stats["insertions"])}</span>'
            )
        if "deletions" in diff_stats:
            stats_parts.append(
                f'<span style="color:#c0392b">-{e(diff_stats["deletions"])}</span>'
            )
    stats_html = " &nbsp; ".join(stats_parts)

    return f"""
<header style="border-bottom:2px solid #ddd;padding-bottom:16px;margin-bottom:24px">
  <h1 style="margin:0 0 6px 0;font-size:1.6em">Code Review Report</h1>
  <div style="color:#555;margin-bottom:8px">
    Source: {source_html} &nbsp;|&nbsp; Generated: {e(generated_at)}
  </div>
  {f'<div style="margin-bottom:6px">Diff: {stats_html}</div>' if stats_html else ''}
  <div>Reviewers: {run_tags}</div>
  {skipped_warning}
</header>
"""


def build_verdict(verdict: Dict[str, Any]) -> str:
    headline = verdict.get("headline", "")
    summary = verdict.get("summary", "")
    return f"""
<section style="background:#f0f4ff;border-left:5px solid #3498db;
  padding:16px 20px;border-radius:4px;margin-bottom:28px">
  <h2 style="margin:0 0 10px 0;font-size:1.3em">Verdict</h2>
  <div style="font-size:1.15em;font-weight:700;margin-bottom:10px">{e(headline)}</div>
  <div>{md_to_html(summary)}</div>
</section>
"""


def build_corrections(corrections: List[Dict[str, Any]]) -> str:
    if not corrections:
        return ""
    rows = "".join(
        f"""<tr>
          <td style="padding:8px;border:1px solid #f5c6cb;vertical-align:top">
            {e(c.get("target",""))}
          </td>
          <td style="padding:8px;border:1px solid #f5c6cb;vertical-align:top">
            {e(c.get("claim",""))}
          </td>
          <td style="padding:8px;border:1px solid #f5c6cb;vertical-align:top">
            {e(c.get("correction",""))}
          </td>
        </tr>"""
        for c in corrections
    )
    return f"""
<section style="background:#fdf2f2;border:2px solid #e74c3c;border-radius:6px;
  padding:16px 20px;margin-bottom:28px">
  <h2 style="margin:0 0 12px 0;font-size:1.2em;color:#c0392b">
    Pipeline Self-Corrections
  </h2>
  <table style="width:100%;border-collapse:collapse;font-size:0.9em">
    <thead>
      <tr style="background:#fadbd8">
        <th style="padding:8px;border:1px solid #f5c6cb;text-align:left">Target</th>
        <th style="padding:8px;border:1px solid #f5c6cb;text-align:left">Original claim</th>
        <th style="padding:8px;border:1px solid #f5c6cb;text-align:left">Correction</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</section>
"""


def build_findings_table(findings: List[Dict[str, Any]], malformed: Dict[str, str] | None = None) -> str:
    if malformed is None:
        malformed = {}
    if not findings:
        return "<p>No findings.</p>"
    rows = "".join(
        f"""<tr>
          <td style="padding:8px;border:1px solid #ddd">
            <a href="#{e(f.get('id',''))}">{e(f.get('id',''))}</a>
            {malformed_badge(malformed[f.get('id','')]) if f.get('id','') in malformed else ''}
          </td>
          <td style="padding:8px;border:1px solid #ddd">
            {verdict_badge(f.get('verdict',''))}
          </td>
          <td style="padding:8px;border:1px solid #ddd">
            {severity_badge(f.get('severity',''))}
          </td>
          <td style="padding:8px;border:1px solid #ddd;font-size:0.85em">
            {e(', '.join(f.get('origins') or []))}
          </td>
          <td style="padding:8px;border:1px solid #ddd;font-family:monospace;font-size:0.85em">
            {e(f.get('file',''))} :{e(f.get('lines',''))}
          </td>
        </tr>"""
        for f in findings
    )
    return f"""
<section style="margin-bottom:28px">
  <h2 style="font-size:1.2em">Findings summary</h2>
  <table style="width:100%;border-collapse:collapse;font-size:0.9em">
    <thead>
      <tr style="background:#f5f5f5">
        <th style="padding:8px;border:1px solid #ddd;text-align:left">ID</th>
        <th style="padding:8px;border:1px solid #ddd;text-align:left">Verdict</th>
        <th style="padding:8px;border:1px solid #ddd;text-align:left">Severity</th>
        <th style="padding:8px;border:1px solid #ddd;text-align:left">Origins</th>
        <th style="padding:8px;border:1px solid #ddd;text-align:left">Location</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</section>
"""


def build_finding_detail(finding: Dict[str, Any], malformed: Dict[str, str] | None = None) -> str:
    if malformed is None:
        malformed = {}
    fid = finding.get("id", "")
    comment = finding.get("comment", "")
    # Store comment text in a data attribute so JS can read it without re-escaping.
    comment_attr = html.escape(comment, quote=True)
    malformed_html = malformed_badge(malformed[fid]) if fid in malformed else ""
    return f"""
<section id="{e(fid)}" style="border:1px solid #ddd;border-radius:6px;
  padding:16px 20px;margin-bottom:20px">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;flex-wrap:wrap">
    <h3 style="margin:0;font-size:1.1em">{e(fid)}</h3>
    {verdict_badge(finding.get('verdict',''))}
    {severity_badge(finding.get('severity',''))}
    {malformed_html}
    <span style="font-family:monospace;font-size:0.85em;color:#555">
      {e(finding.get('file',''))} :{e(finding.get('lines',''))}
    </span>
    <span style="font-size:0.85em;color:#777">
      {e(', '.join(finding.get('origins') or []))}
    </span>
  </div>

  <div style="margin-bottom:12px">
    <strong>Claim</strong>
    <div style="margin-top:4px">{md_to_html(finding.get('claim',''))}</div>
  </div>

  <div style="margin-bottom:12px">
    <strong>Consequence</strong>
    <div style="margin-top:4px">{md_to_html(finding.get('consequence',''))}</div>
  </div>

  <div style="margin-bottom:12px">
    <strong>Fix direction</strong>
    <div style="margin-top:4px">{md_to_html(finding.get('fix_direction',''))}</div>
  </div>

  <div style="margin-bottom:14px">
    <strong>Evidence</strong>
    <div style="margin-top:4px">{md_to_html(finding.get('evidence',''))}</div>
  </div>

  <div>
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
      <strong>Paste-ready comment</strong>
      <span id="copy-ok-{e(fid)}" style="color:green;font-size:0.85em;display:none">
        Copied!
      </span>
      {copy_button(fid)}
    </div>
    <pre data-comment="{comment_attr}" id="comment-{e(fid)}"
      style="background:#f8f8f8;border:1px solid #ddd;padding:12px;
      border-radius:4px;overflow-x:auto;white-space:pre-wrap;word-break:break-word;
      font-size:0.85em">{e(comment)}</pre>
  </div>
</section>
"""


def build_dropped(dropped: List[Dict[str, Any]], malformed: Dict[str, str] | None = None) -> str:
    if malformed is None:
        malformed = {}
    if not dropped:
        return ""
    rows = "".join(
        f"""<tr>
          <td style="padding:8px;border:1px solid #ddd">{e(d.get('id',''))} {malformed_badge(malformed[d.get('id','')]) if d.get('id','') in malformed else ''}</td>
          <td style="padding:8px;border:1px solid #ddd;font-family:monospace;font-size:0.85em">
            {e(d.get('file',''))} :{e(d.get('lines',''))}
          </td>
          <td style="padding:8px;border:1px solid #ddd">{e(d.get('claim',''))}</td>
          <td style="padding:8px;border:1px solid #ddd">
            {md_to_html(d.get('disproof',''))}
          </td>
        </tr>"""
        for d in dropped
    )
    return f"""
<section style="margin-bottom:28px">
  <h2 style="font-size:1.2em">Dropped findings</h2>
  <table style="width:100%;border-collapse:collapse;font-size:0.9em">
    <thead>
      <tr style="background:#f5f5f5">
        <th style="padding:8px;border:1px solid #ddd;text-align:left">ID</th>
        <th style="padding:8px;border:1px solid #ddd;text-align:left">Location</th>
        <th style="padding:8px;border:1px solid #ddd;text-align:left">Claim</th>
        <th style="padding:8px;border:1px solid #ddd;text-align:left">Disproof</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</section>
"""


def build_overflow_details(overflow: List[Dict[str, Any]], malformed: Dict[str, str] | None = None) -> str:
    if malformed is None:
        malformed = {}
    if not overflow:
        return ""
    rows = "".join(
        f"""<tr>
          <td style="padding:8px;border:1px solid #ddd">{e(o.get('id',''))} {malformed_badge(malformed[o.get('id','')]) if o.get('id','') in malformed else ''}</td>
          <td style="padding:8px;border:1px solid #ddd">
            {verdict_badge(o.get('verdict',''))}
          </td>
          <td style="padding:8px;border:1px solid #ddd;font-family:monospace;font-size:0.85em">
            {e(o.get('file',''))} :{e(o.get('lines',''))}
          </td>
          <td style="padding:8px;border:1px solid #ddd">{e(o.get('claim',''))}</td>
          <td style="padding:8px;border:1px solid #ddd">{e(o.get('reason_cut',''))}</td>
        </tr>"""
        for o in overflow
    )
    table = f"""
<table style="width:100%;border-collapse:collapse;font-size:0.9em">
  <thead>
    <tr style="background:#f5f5f5">
      <th style="padding:8px;border:1px solid #ddd;text-align:left">ID</th>
      <th style="padding:8px;border:1px solid #ddd;text-align:left">Verdict</th>
      <th style="padding:8px;border:1px solid #ddd;text-align:left">Location</th>
      <th style="padding:8px;border:1px solid #ddd;text-align:left">Claim</th>
      <th style="padding:8px;border:1px solid #ddd;text-align:left">Reason cut</th>
    </tr>
  </thead>
  <tbody>{rows}</tbody>
</table>
"""
    return f"""
<details style="margin-bottom:20px">
  <summary style="cursor:pointer;font-weight:600;font-size:1.1em;
    padding:8px 0">Overflow findings ({len(overflow)})</summary>
  <div style="margin-top:12px">{table}</div>
</details>
"""


def build_record_details(record: Dict[str, Any]) -> str:
    """Build collapsed <details> blocks for the council record."""
    parts: List[str] = []
    anon_map: Dict[str, str] = record.get("anonymization_mapping") or {}

    original_request = record.get("original_request", "")
    if original_request:
        parts.append(f"""
<details style="margin-bottom:16px">
  <summary style="cursor:pointer;font-weight:600">Original request</summary>
  <div style="margin-top:10px;padding:10px 14px;background:#fafafa;
    border:1px solid #eee;border-radius:4px">{md_to_html(original_request)}</div>
</details>
""")

    framed = record.get("framed_question", "")
    if framed:
        parts.append(f"""
<details style="margin-bottom:16px">
  <summary style="cursor:pointer;font-weight:600">Framed question</summary>
  <div style="margin-top:10px;padding:10px 14px;background:#fafafa;
    border:1px solid #eee;border-radius:4px">{md_to_html(framed)}</div>
</details>
""")

    advisors: List[Dict[str, Any]] = record.get("advisors") or []
    if advisors:
        advisor_blocks = ""
        for adv in advisors:
            letter = adv.get("letter", "?")
            name = adv.get("name", "?")
            real_name = anon_map.get(letter, name)
            advisor_blocks += f"""
<details style="margin-bottom:10px">
  <summary style="cursor:pointer">{e(letter)} ({e(real_name)})</summary>
  <div style="margin-top:8px;padding:10px 14px;background:#fafafa;
    border:1px solid #eee;border-radius:4px">{md_to_html(adv.get('response',''))}</div>
</details>
"""
        parts.append(f"""
<details style="margin-bottom:16px">
  <summary style="cursor:pointer;font-weight:600">Advisor responses</summary>
  <div style="margin-top:10px">{advisor_blocks}</div>
</details>
""")

    peer_reviews: List[Dict[str, Any]] = record.get("peer_reviews") or []
    if peer_reviews:
        pr_blocks = "".join(
            f"""
<details style="margin-bottom:10px">
  <summary style="cursor:pointer">{e(pr.get('probe',''))}</summary>
  <div style="margin-top:8px;padding:10px 14px;background:#fafafa;
    border:1px solid #eee;border-radius:4px">{md_to_html(pr.get('response',''))}</div>
</details>
"""
            for pr in peer_reviews
        )
        parts.append(f"""
<details style="margin-bottom:16px">
  <summary style="cursor:pointer;font-weight:600">Peer reviews</summary>
  <div style="margin-top:10px">{pr_blocks}</div>
</details>
""")

    synthesis = record.get("synthesis", "")

    ranked_list = record.get("ranked_list", "")
    if ranked_list:
        parts.append(f"""
<details style="margin-bottom:16px">
  <summary style="cursor:pointer;font-weight:600">Ranked list (before cap)</summary>
  <div style="margin-top:10px;padding:10px 14px;background:#fafafa;
    border:1px solid #eee;border-radius:4px">{md_to_html(ranked_list)}</div>
</details>
""")

    if synthesis:
        parts.append(f"""
<details style="margin-bottom:16px">
  <summary style="cursor:pointer;font-weight:600">Synthesis</summary>
  <div style="margin-top:10px;padding:10px 14px;background:#fafafa;
    border:1px solid #eee;border-radius:4px">{md_to_html(synthesis)}</div>
</details>
""")

    process_notes = record.get("process_notes", "")
    if process_notes:
        parts.append(f"""
<details style="margin-bottom:16px">
  <summary style="cursor:pointer;font-weight:600">Process notes</summary>
  <div style="margin-top:10px;padding:10px 14px;background:#fafafa;
    border:1px solid #eee;border-radius:4px">{md_to_html(process_notes)}</div>
</details>
""")

    if not parts:
        return ""

    inner = "\n".join(parts)
    return f"""
<section style="margin-bottom:28px">
  <h2 style="font-size:1.2em">Council record</h2>
  {inner}
</section>
"""


# ---------------------------------------------------------------------------
# Copy-to-clipboard JS (works on file:// via execCommand fallback)
# ---------------------------------------------------------------------------

COPY_SCRIPT = """
<script>
function copyComment(id) {
  var pre = document.getElementById('comment-' + id);
  var text = pre.getAttribute('data-comment');
  var ok = document.getElementById('copy-ok-' + id);

  function showOk() {
    ok.style.display = 'inline';
    setTimeout(function() { ok.style.display = 'none'; }, 1800);
  }

  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(showOk).catch(function() {
      fallbackCopy(text, showOk);
    });
  } else {
    fallbackCopy(text, showOk);
  }
}

function fallbackCopy(text, callback) {
  var ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.left = '-9999px';
  ta.style.top = '-9999px';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  try {
    document.execCommand('copy');
    callback();
  } catch(e) {
    console.error('copy failed', e);
  }
  document.body.removeChild(ta);
}
</script>
"""

CSS = """
<style>
  *, *::before, *::after { box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #fff;
    color: #222;
    line-height: 1.65;
    margin: 0;
    padding: 24px 16px 60px;
  }
  .container { max-width: 920px; margin: 0 auto; }
  h1, h2, h3 { color: #1a1a1a; }
  a { color: #2980b9; }
  code { background: #f0f0f0; padding: 1px 5px; border-radius: 3px;
         font-family: "SFMono-Regular", Consolas, monospace; font-size: 0.9em; }
  pre code { background: transparent; padding: 0; font-size: inherit; }
  pre { margin: 0; }
  details > summary { list-style: none; }
  details > summary::-webkit-details-marker { display: none; }
  details > summary::before { content: "+ "; font-weight: 700; }
  details[open] > summary::before { content: "- "; }
</style>
"""


# ---------------------------------------------------------------------------
# Full document assembly
# ---------------------------------------------------------------------------

def build_html(data: Dict[str, Any]) -> str:
    meta: Dict[str, Any] = data["meta"]
    verdict: Dict[str, Any] = data["verdict"]
    findings: List[Dict[str, Any]] = data.get("findings") or []
    overflow: List[Dict[str, Any]] = data.get("overflow") or []
    dropped: List[Dict[str, Any]] = data.get("dropped") or []
    corrections: List[Dict[str, Any]] = data.get("corrections") or []
    record: Optional[Dict[str, Any]] = data.get("record")

    # Collect malformed findings from all sections
    malformed: Dict[str, str] = {}
    malformed.update(validate_findings_and_collect_malformed(findings, "findings"))
    malformed.update(validate_findings_and_collect_malformed(overflow, "overflow"))
    malformed.update(validate_findings_and_collect_malformed(dropped, "dropped"))

    pipeline: Optional[Dict[str, Any]] = meta.get("pipeline")

    body_parts: List[str] = [
        build_header(meta),
        build_pipeline_chart(pipeline) if pipeline else "",
        build_verdict(verdict),
    ]

    if corrections:
        body_parts.append(build_corrections(corrections))

    body_parts.append(build_findings_table(findings, malformed))

    for finding in findings:
        body_parts.append(build_finding_detail(finding, malformed))

    if dropped:
        body_parts.append(build_dropped(dropped, malformed))

    if overflow:
        body_parts.append(build_overflow_details(overflow, malformed))

    if record:
        body_parts.append(build_record_details(record))

    body = "\n".join(body_parts)

    title = e(meta.get("source", "Code Review Report"))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Code Review: {title}</title>
  {CSS}
</head>
<body>
  <div class="container">
    {body}
  </div>
  {COPY_SCRIPT}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Self-validation
# ---------------------------------------------------------------------------

def validate_html(html_str: str) -> None:
    """Validate the generated HTML or raise ValueError with a message."""
    # Check balanced <details> tags.
    open_details = html_str.count("<details")
    close_details = html_str.count("</details>")
    if open_details != close_details:
        raise ValueError(
            f"Unbalanced <details>: {open_details} open, {close_details} close"
        )

    # Check balanced <div> tags.
    open_div = html_str.count("<div")
    close_div = html_str.count("</div>")
    if open_div != close_div:
        raise ValueError(
            f"Unbalanced <div>: {open_div} open, {close_div} close"
        )

    # No raw fenced-code fences should survive as rendered markdown.
    # Strip blocks that legitimately contain backtick content as plain text:
    #   <script>, <style>, <pre> (verbatim comment text), and data-comment="..." attrs.
    stripped = re.sub(r"<script[\s\S]*?</script>", "", html_str, flags=re.IGNORECASE)
    stripped = re.sub(r"<style[\s\S]*?</style>", "", stripped, flags=re.IGNORECASE)
    # Remove pre blocks (they hold the paste-ready comment verbatim).
    stripped = re.sub(r"<pre[\s\S]*?</pre>", "", stripped, flags=re.IGNORECASE)
    # Remove data-comment attribute values (HTML-escaped comment text).
    stripped = re.sub(r'data-comment="[^"]*"', "", stripped)
    if "```" in stripped:
        raise ValueError("Unrendered fenced-code fence (```) found in output body")

    # Non-trivial length.
    if len(html_str.encode("utf-8")) < 2000:
        raise ValueError(f"Output is suspiciously small: {len(html_str)} chars")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a code-review run directory to a self-contained HTML report."
    )
    parser.add_argument("--run-dir", required=True, help="Path to the run directory")
    parser.add_argument("--out", required=True, help="Output HTML file path")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    out_path = Path(args.out)

    if not run_dir.exists():
        print(f"Error: --run-dir does not exist: {run_dir}", file=sys.stderr)
        sys.exit(1)

    if not run_dir.is_dir():
        print(f"Error: --run-dir is not a directory: {run_dir}", file=sys.stderr)
        sys.exit(1)

    report_file = run_dir / "report.json"
    if not report_file.exists():
        print(f"Error: report.json not found in {run_dir}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(report_file, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        print(f"Error: report.json is not valid JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    for required in ("meta", "verdict", "findings"):
        if required not in data:
            print(f"Error: report.json is missing required key '{required}'", file=sys.stderr)
            sys.exit(1)

    # Validate findings and collect malformed before rendering
    malformed: Dict[str, str] = {}
    findings: List[Dict[str, Any]] = data.get("findings") or []
    overflow: List[Dict[str, Any]] = data.get("overflow") or []
    dropped: List[Dict[str, Any]] = data.get("dropped") or []
    malformed.update(validate_findings_and_collect_malformed(findings, "findings"))
    malformed.update(validate_findings_and_collect_malformed(overflow, "overflow"))
    malformed.update(validate_findings_and_collect_malformed(dropped, "dropped"))

    # Report malformed findings to stderr
    if malformed:
        print(f"Warning: {len(malformed)} malformed anchor(s) in report.json:", file=sys.stderr)
        for fid in sorted(malformed.keys()):
            print(f"  {fid}: {malformed[fid]}", file=sys.stderr)

    try:
        html_str = build_html(data)
    except Exception as exc:
        print(f"Error building HTML: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        validate_html(html_str)
    except ValueError as exc:
        print(f"Error: self-validation failed: {exc}", file=sys.stderr)
        sys.exit(1)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html_str)

    print(str(out_path.resolve()))


if __name__ == "__main__":
    main()

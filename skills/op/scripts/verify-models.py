#!/usr/bin/env python3
"""verify-models.py -- prove that op-routed subagents ran on their assigned model tiers.

Reads a Claude Code session transcript JSONL and reports whether each Agent/Task
dispatch landed on the requested model tier.

Usage:
  python3 verify-models.py [FILE]           # explicit transcript path
  python3 verify-models.py --session UUID   # locate by session id
  python3 verify-models.py                  # newest transcript for current project
  python3 verify-models.py --json           # JSON output
  python3 verify-models.py --all            # all transcripts for current project

Exit codes: 0 = ok, 1 = mismatch(es), 2 = no dispatches / transcript not found.
"""

import argparse
import glob
import json
import os
import sys


# ---------------------------------------------------------------------------
# Transcript location helpers
# ---------------------------------------------------------------------------

def _projects_root():
    config_dir = os.environ.get("CLAUDE_CONFIG_DIR", os.path.expanduser("~/.claude"))
    return os.path.join(config_dir, "projects")


def _cwd_slug():
    return os.getcwd().replace("/", "-")


def _find_transcript(args):
    """Return the path to the JSONL to analyse, or exit with code 2."""
    root = _projects_root()

    # 1) explicit positional file path
    if args.file:
        path = args.file
        if not os.path.isfile(path):
            print(f"error: file not found: {path}", file=sys.stderr)
            sys.exit(2)
        return path

    # 2) --session UUID
    if args.session:
        uuid = args.session
        slug = _cwd_slug()
        primary = os.path.join(root, slug, f"{uuid}.jsonl")
        if os.path.isfile(primary):
            return primary
        # fallback: search every project subdirectory
        for candidate in glob.glob(os.path.join(root, "*", f"{uuid}.jsonl")):
            return candidate
        print(f"error: session {uuid!r} not found under {root}/", file=sys.stderr)
        sys.exit(2)

    # 3) default: newest *.jsonl in <root>/<cwd-slug>/
    project_dir = os.path.join(root, _cwd_slug())
    if not os.path.isdir(project_dir):
        print(f"error: project transcript directory not found: {project_dir}", file=sys.stderr)
        sys.exit(2)
    candidates = glob.glob(os.path.join(project_dir, "*.jsonl"))
    if not candidates:
        print(f"error: no *.jsonl transcripts in {project_dir}", file=sys.stderr)
        sys.exit(2)
    return max(candidates, key=os.path.getmtime)


# ---------------------------------------------------------------------------
# JSONL parsing
# ---------------------------------------------------------------------------

def _total_tokens(usage):
    """Sum all four token fields, treating missing keys as 0."""
    if not isinstance(usage, dict):
        return 0
    return (
        usage.get("input_tokens", 0)
        + usage.get("output_tokens", 0)
        + usage.get("cache_creation_input_tokens", 0)
        + usage.get("cache_read_input_tokens", 0)
    )


def parse_transcript(path):
    """Parse a JSONL transcript and return four dicts.

    dispatches : {tool_use_id: {id, requested_model, description, subagent_type}}
    results    : {tool_use_id: {resolved_model, total_tokens, duration_ms}}
    orch_usage : {model_id: {tokens}}
    sub_usage  : {resolved_model: {tokens, duration_ms}}
    """
    dispatches = {}
    results = {}
    orch_usage = {}
    sub_usage = {}

    with open(path, "r", encoding="utf-8") as fh:
        for raw_line in fh:
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError:
                continue

            if not isinstance(record, dict):
                continue

            rec_type = record.get("type")
            message = record.get("message") or {}

            # --- assistant records: dispatches and orchestrator usage ---
            if rec_type == "assistant":
                model = message.get("model")
                usage = message.get("usage")
                if model and usage:
                    tokens = _total_tokens(usage)
                    if model not in orch_usage:
                        orch_usage[model] = {"tokens": 0}
                    orch_usage[model]["tokens"] += tokens

                content = message.get("content") or []
                if not isinstance(content, list):
                    continue
                for item in content:
                    if not isinstance(item, dict):
                        continue
                    if item.get("type") != "tool_use":
                        continue
                    if item.get("name") not in {"Agent", "Task"}:
                        continue
                    tool_id = item.get("id")
                    if not tool_id:
                        continue
                    inp = item.get("input") or {}
                    dispatches[tool_id] = {
                        "id": tool_id,
                        "requested_model": inp.get("model"),
                        "description": inp.get("description", ""),
                        "subagent_type": inp.get("subagent_type"),
                    }

            # --- user records: subagent results ---
            elif rec_type == "user":
                tool_use_result = record.get("toolUseResult")
                if not isinstance(tool_use_result, dict):
                    continue
                resolved = tool_use_result.get("resolvedModel")
                if not resolved:
                    continue

                # resolve the linked tool_use id from message.content first
                linked_id = None
                msg_content = message.get("content") or []
                if isinstance(msg_content, list):
                    for item in msg_content:
                        if isinstance(item, dict) and item.get("type") == "tool_result":
                            linked_id = item.get("tool_use_id")
                            break
                # fallback to toolUseID field
                if not linked_id:
                    linked_id = tool_use_result.get("toolUseID")
                if not linked_id:
                    continue

                total = tool_use_result.get("totalTokens") or 0
                if total == 0:
                    total = _total_tokens(tool_use_result.get("usage") or {})
                duration = tool_use_result.get("totalDurationMs") or 0

                results[linked_id] = {
                    "resolved_model": resolved,
                    "total_tokens": total,
                    "duration_ms": duration,
                }

                if resolved not in sub_usage:
                    sub_usage[resolved] = {"tokens": 0, "duration_ms": 0}
                sub_usage[resolved]["tokens"] += total
                sub_usage[resolved]["duration_ms"] += duration

    return dispatches, results, orch_usage, sub_usage


# ---------------------------------------------------------------------------
# Mismatch logic
# ---------------------------------------------------------------------------

_TIERS = {"haiku", "sonnet", "opus", "fable"}


def _tier_of(model_str):
    """Return the tier word from a model string, or None."""
    if not model_str:
        return None
    lower = model_str.lower()
    for tier in _TIERS:
        if tier in lower:
            return tier
    return None


def is_mismatch(requested_model, resolved_model):
    """True when a named tier was requested but is absent from resolvedModel."""
    if not requested_model:
        return False
    tier = _tier_of(requested_model)
    if not tier:
        return False
    return tier not in (resolved_model or "").lower()


# ---------------------------------------------------------------------------
# Row building
# ---------------------------------------------------------------------------

def build_rows(dispatches, results):
    """One row dict per dispatch."""
    rows = []
    for tool_id, d in dispatches.items():
        r = results.get(tool_id)
        requested = d["requested_model"] or "-"
        actual = r["resolved_model"] if r else None
        mismatch = is_mismatch(d["requested_model"], actual)
        rows.append({
            "requested": requested,
            "actual": actual or "(no result)",
            "task": d["description"] or d["subagent_type"] or tool_id,
            "mismatch": mismatch,
        })
    return rows


# ---------------------------------------------------------------------------
# Human report
# ---------------------------------------------------------------------------

def human_report(path, rows, orch_usage, sub_usage):
    lines = []
    dispatch_count = len(rows)
    mismatch_count = sum(1 for r in rows if r["mismatch"])

    # A) warning block
    if dispatch_count == 0:
        lines.append("WARNING: NO SUBAGENTS DISPATCHED")
        lines.append(f"Transcript: {path}")
        lines.append("")
    elif mismatch_count > 0:
        lines.append("WARNING: ROUTING PROBLEM")
        lines.append(
            f"  {mismatch_count} of {dispatch_count} dispatch(es) landed on the wrong model tier."
        )
        lines.append("")

    # B) routing table
    col_req = max(len("requested"), max((len(r["requested"]) for r in rows), default=0))
    col_act = max(len("actual"), max((len(r["actual"]) for r in rows), default=0))

    col_task = min(max((len(r["task"]) for r in rows), default=4), 60)
    lines.append(f"  {'requested':<{col_req}}  {'actual':<{col_act}}  task")
    lines.append("  " + "-" * (col_req + col_act + col_task + 6))
    for r in rows:
        suffix = "  MISMATCH" if r["mismatch"] else ""
        lines.append(f"  {r['requested']:<{col_req}}  {r['actual']:<{col_act}}  {r['task']}{suffix}")
    lines.append("")

    # C) model usage
    all_tokens = (
        sum(v["tokens"] for v in orch_usage.values())
        + sum(v["tokens"] for v in sub_usage.values())
    )
    lines.append("MODEL USAGE")
    for model, v in orch_usage.items():
        if v["tokens"] <= 0:
            continue  # skip empty buckets (e.g. <synthetic> placeholder turns)
        pct = int(round(v["tokens"] / all_tokens * 100)) if all_tokens else 0
        lines.append(f"  {model}  {v['tokens']} tokens  {pct}%  (orchestrator)")
    for model, v in sub_usage.items():
        lines.append(f"  {model}  {v['tokens']} tokens  (subagent)")
    lines.append("")

    # D) summary
    lines.append(f"Dispatches: {dispatch_count}  Mismatches: {mismatch_count}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON report
# ---------------------------------------------------------------------------

def json_report(rows, orch_usage, sub_usage):
    usage = []
    for model, v in orch_usage.items():
        if v["tokens"] <= 0:
            continue  # skip empty buckets (e.g. <synthetic> placeholder turns)
        usage.append({"model": model, "role": "orchestrator", "tokens": v["tokens"], "duration_ms": 0})
    for model, v in sub_usage.items():
        usage.append({"model": model, "role": "subagent", "tokens": v["tokens"], "duration_ms": v["duration_ms"]})
    mismatch_count = sum(1 for r in rows if r["mismatch"])
    return {
        "dispatches": [
            {"requested": r["requested"], "actual": r["actual"], "task": r["task"], "mismatch": r["mismatch"]}
            for r in rows
        ],
        "usage": usage,
        "summary": {"dispatch_count": len(rows), "mismatch_count": mismatch_count},
    }


# ---------------------------------------------------------------------------
# Exit code
# ---------------------------------------------------------------------------

def _exit_code(rows):
    if not rows:
        return 2
    if any(r["mismatch"] for r in rows):
        return 1
    return 0


# ---------------------------------------------------------------------------
# --all mode
# ---------------------------------------------------------------------------

def run_all(args):
    root = _projects_root()
    project_dir = os.path.join(root, _cwd_slug())
    if not os.path.isdir(project_dir):
        print(f"error: project transcript directory not found: {project_dir}", file=sys.stderr)
        sys.exit(2)
    candidates = sorted(glob.glob(os.path.join(project_dir, "*.jsonl")), key=os.path.getmtime)
    if not candidates:
        print(f"error: no *.jsonl transcripts in {project_dir}", file=sys.stderr)
        sys.exit(2)

    # A mismatch anywhere (exit 1) must win over a no-dispatch transcript
    # (exit 2). A plain numeric max would let 2 mask 1, hiding routing
    # failures the moment any transcript lacks dispatches.
    any_mismatch = False
    all_zero = True
    for path in candidates:
        dispatches, results, orch_usage, sub_usage = parse_transcript(path)
        rows = build_rows(dispatches, results)
        code = _exit_code(rows)
        if code == 1:
            any_mismatch = True
        if code != 2:
            all_zero = False
        if args.json:
            obj = json_report(rows, orch_usage, sub_usage)
            obj["file"] = path
            print(json.dumps(obj))
        else:
            print(f"=== {os.path.basename(path)} ===")
            print(human_report(path, rows, orch_usage, sub_usage))
    sys.exit(1 if any_mismatch else 2 if all_zero else 0)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Verify that op-routed subagents ran on their assigned model tiers."
    )
    parser.add_argument("file", nargs="?", help="Path to a .jsonl transcript file")
    parser.add_argument("--session", metavar="UUID", help="Session UUID to locate in the projects directory")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of human-readable text")
    parser.add_argument("--all", dest="all", action="store_true", help="Scan all transcripts for the current project")
    args = parser.parse_args()

    if args.all:
        run_all(args)
        return

    path = _find_transcript(args)
    dispatches, results, orch_usage, sub_usage = parse_transcript(path)
    rows = build_rows(dispatches, results)

    if args.json:
        print(json.dumps(json_report(rows, orch_usage, sub_usage)))
    else:
        print(human_report(path, rows, orch_usage, sub_usage))

    sys.exit(_exit_code(rows))


if __name__ == "__main__":
    main()

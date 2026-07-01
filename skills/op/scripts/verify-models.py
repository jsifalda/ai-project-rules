#!/usr/bin/env python3
"""verify-models.py -- prove that op-routed subagents ran on their assigned model tiers.

Reads a Claude Code session transcript JSONL and reports whether each Agent/Task
dispatch landed on the requested model tier.

Usage:
  python3 verify-models.py [FILE]   # explicit transcript path
  python3 verify-models.py          # newest transcript for current project

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

    # 2) default: newest *.jsonl in <root>/<cwd-slug>/
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
    """Parse a JSONL transcript and return two dicts.

    dispatches : {tool_use_id: {id, requested_model, description, subagent_type}}
    results    : {tool_use_id: {resolved_model, total_tokens}}
    """
    dispatches = {}
    results = {}

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

            # --- assistant records: dispatches ---
            if rec_type == "assistant":
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

                results[linked_id] = {
                    "resolved_model": resolved,
                    "total_tokens": total,
                }

    return dispatches, results


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

def human_report(path, rows, results):
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

    # C) per-model token tally (subagents only)
    tally = {}
    for r in results.values():
        model = r["resolved_model"]
        tally[model] = tally.get(model, 0) + r["total_tokens"]
    if tally:
        lines.append("MODEL USAGE")
        for model, tokens in tally.items():
            lines.append(f"  {model}  {tokens} tokens")
        lines.append("")

    # D) summary
    lines.append(f"Dispatches: {dispatch_count}  Mismatches: {mismatch_count}")
    return "\n".join(lines)


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
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Verify that op-routed subagents ran on their assigned model tiers."
    )
    parser.add_argument("file", nargs="?", help="Path to a .jsonl transcript file")
    args = parser.parse_args()

    path = _find_transcript(args)
    dispatches, results = parse_transcript(path)
    rows = build_rows(dispatches, results)

    print(human_report(path, rows, results))
    sys.exit(_exit_code(rows))


if __name__ == "__main__":
    main()

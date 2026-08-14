#!/usr/bin/env python3
"""Generate a machine-derived allowlist of legal diff anchors from a unified patch.

WHY this exists: reviewers were reading whole files with `git show <ref>:<path>` and
counting line numbers by eye. That produced anchors 2-3 lines off, so inline comments
landed on unrelated code (one recorded run: a finding about `setToolbarHidden` was anchored
to line 122, which is `barTintColor` inside the *else* branch). This script derives
every legal new-side and old-side line number directly from the diff headers and body,
making a correct anchor cheaper to look up than to guess.

Usage
-----
    python3 extract-anchors.py --diff path/to/diff.patch --out path/to/anchors.json
    python3 extract-anchors.py --diff path/to/diff.patch --out path/to/anchors.json --quiet

Exit 0 on success. Exit 1 if the diff is missing, unreadable, or empty.
"""

import argparse
import json
import re
import sys
from pathlib import Path


# Unified-diff headers that are never hunk body lines.
_HEADER_PREFIXES = (
    "diff --git",
    "index ",
    "new file mode",
    "deleted file mode",
    "old mode",
    "new mode",
    "similarity index",
    "rename from",
    "rename to",
    "Binary files",
)

# The @@ header: -old_start[,old_count] +new_start[,new_count] @@
_HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def _strip_b_prefix(path: str) -> str:
    """Remove the leading b/ that git adds to new-side paths."""
    return path[2:] if path.startswith("b/") else path


def _strip_a_prefix(path: str) -> str:
    return path[2:] if path.startswith("a/") else path


def parse_diff(text: str) -> dict:
    files: dict = {}
    current: dict | None = None
    in_hunk = False

    # Counters for the active hunk.
    old_line = 0
    new_line = 0
    hunk_new_start = 0
    hunk_new_count = 0
    new_side_advances = 0  # track advances so we can build the end of the hunk range

    def _finish_hunk() -> None:
        """Append the completed hunk range to current file, if it has new-side lines.

        Reset hunk_new_count immediately after appending so that the multiple header
        lines that follow a hunk body (---, +++, diff --git, etc.) each call this
        function without re-appending the same range to the next file's list.
        """
        nonlocal hunk_new_count
        if current is None or hunk_new_count == 0:
            return
        hunk_end = hunk_new_start + hunk_new_count - 1
        current["hunks"].append([hunk_new_start, hunk_end])
        hunk_new_count = 0

    for raw in text.splitlines():
        # ---- file-level header lines ----
        if raw.startswith("diff --git "):
            _finish_hunk()
            in_hunk = False
            # Derive new-side path from the `b/` half of `diff --git a/... b/...`.
            # Split on " b/" from the right to handle paths with spaces.
            parts = raw[len("diff --git "):].rsplit(" b/", 1)
            new_path = parts[1] if len(parts) == 2 else ""
            current = {
                "old_path": _strip_a_prefix(parts[0]) if parts else new_path,
                "new_file": False,
                "deleted": False,
                "renamed": False,
                "hunks": [],
                "added": [],
                "removed": [],
                "_new_path": new_path,
            }
            files[new_path] = current
            continue

        if any(raw.startswith(p) for p in _HEADER_PREFIXES):
            _finish_hunk()
            in_hunk = False
            if current is not None:
                if raw.startswith("new file mode"):
                    current["new_file"] = True
                elif raw.startswith("deleted file mode"):
                    current["deleted"] = True
                elif raw.startswith("rename from"):
                    current["renamed"] = True
                    current["old_path"] = raw[len("rename from "):].strip()
                elif raw.startswith("rename to"):
                    # rename to gives us the authoritative new path
                    new_path = raw[len("rename to "):].strip()
                    old_key = current["_new_path"]
                    current["_new_path"] = new_path
                    # Re-key in files dict.
                    if old_key in files:
                        files[new_path] = files.pop(old_key)
            continue

        # --- path headers (--- / +++) — authoritative path source, not body lines ---
        if raw.startswith("--- "):
            _finish_hunk()
            in_hunk = False
            if current is not None:
                path = raw[4:].strip()
                if path != "/dev/null":
                    current["old_path"] = _strip_a_prefix(path)
            continue

        if raw.startswith("+++ "):
            _finish_hunk()
            in_hunk = False
            if current is not None:
                path = raw[4:].strip()
                if path != "/dev/null":
                    new_path = _strip_b_prefix(path)
                    old_key = current["_new_path"]
                    current["_new_path"] = new_path
                    if old_key in files and old_key != new_path:
                        files[new_path] = files.pop(old_key)
                    # Deleted files keep old path as key; update current reference.
                    current = files.get(new_path) or files.get(old_key)
            continue

        # ---- hunk header ----
        m = _HUNK_RE.match(raw)
        if m:
            _finish_hunk()
            in_hunk = True
            old_line = int(m.group(1))
            old_count = int(m.group(2)) if m.group(2) is not None else 1
            new_line = int(m.group(3))
            hunk_new_count = int(m.group(4)) if m.group(4) is not None else 1
            hunk_new_start = new_line
            _ = old_count  # referenced only for clarity; we track by advancing
            continue

        if not in_hunk or current is None:
            continue

        # "\ No newline at end of file" — skip, advance neither counter.
        if raw.startswith("\\ "):
            continue

        # An empty line inside a hunk is a context line with its space stripped.
        if raw == "":
            old_line += 1
            new_line += 1
            continue

        prefix = raw[0]
        body = raw[1:]

        if prefix == " ":
            old_line += 1
            new_line += 1
        elif prefix == "+":
            current["added"].append({"line": new_line, "text": body})
            new_line += 1
        elif prefix == "-":
            current["removed"].append({"line": old_line, "text": body})
            old_line += 1

    # Finish the final hunk.
    _finish_hunk()

    # Build the output, keyed by clean new-side path (or old-side for deletions).
    result: dict = {}
    for entry in files.values():
        key = entry["_new_path"] if not entry["deleted"] else entry["old_path"]
        clean = {
            "old_path": entry["old_path"],
            "new_file": entry["new_file"],
            "deleted": entry["deleted"],
            "renamed": entry["renamed"],
            "hunks": entry["hunks"],
            "added": sorted(entry["added"], key=lambda x: x["line"]),
            "removed": sorted(entry["removed"], key=lambda x: x["line"]),
        }
        result[key] = clean

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract legal diff anchors from a unified patch file."
    )
    parser.add_argument("--diff", required=True, help="Path to the unified diff file.")
    parser.add_argument("--out", required=True, help="Path for the output JSON file.")
    parser.add_argument(
        "--quiet", action="store_true", help="Suppress the stderr summary."
    )
    args = parser.parse_args()

    diff_path = Path(args.diff)
    if not diff_path.exists():
        print(f"error: diff file not found: {args.diff}", file=sys.stderr)
        sys.exit(1)

    try:
        text = diff_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"error: cannot read diff: {exc}", file=sys.stderr)
        sys.exit(1)

    if not text.strip():
        print(f"error: diff file is empty: {args.diff}", file=sys.stderr)
        sys.exit(1)

    files = parse_diff(text)

    output = {"generated_from": args.diff, "files": files}

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if not args.quiet:
        total_added = sum(len(f["added"]) for f in files.values())
        total_removed = sum(len(f["removed"]) for f in files.values())
        print(
            f"extract-anchors: {len(files)} file(s), "
            f"{total_added} added lines, {total_removed} removed lines → {args.out}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()

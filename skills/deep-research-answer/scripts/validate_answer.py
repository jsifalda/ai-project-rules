#!/usr/bin/env python3
"""Validate a deep-research-answer chat answer. Stdlib only.

Usage: python3 validate_answer.py --answer answer.md
Exit 0 = PASS, 1 = FAIL.
"""
import argparse
import re
import sys

MIN_SOURCES = 5
LABELS = ["Quick answer", "Deep dive"]
FIELDS = ["Assumptions", "Conflicting evidence", "Added queries"]
ANSWER_RE = re.compile(r"^ANSWER:\s*(YES|NO|NOT A YES/NO QUESTION)(?=$|[\s.,:])")
FOOTNOTE_RE = re.compile(r"^\s*(?:[-*]\s+)?\[(\d+)\]:?\s+\S")
PRIMARY_RE = re.compile(r"Type:\s*primary\b(?!\s+or\b)", re.I)
LIST_RE = re.compile(r"^(\s*)(?:[-*]|\d+\.)\s+")
LABEL_LINE_RE = re.compile(r"^\s*(?:(?:[-*]|\d+\.)\s+)?[A-Z][\w ]{0,40}:(?:\s|$)")


def clean(line):
    return line.replace("`", "").replace("**", "")


def heading_text(line):
    return clean(line).strip("#*: \t").lower()


def field_filled(lines, label):
    """None = label missing. Text must sit after the colon, on the next line,
    or in a list below it. Under a list-item label it must be nested deeper."""
    pat = re.compile(r"^(\s*)(?:(?:[-*]|\d+\.)\s+)?" + re.escape(label)
                     + r":\s*(.*)$", re.I)
    for i, raw in enumerate(lines):
        m = pat.match(clean(raw))
        if not m:
            continue
        if m.group(2).strip():
            return True
        j = next((k for k in range(i + 1, len(lines)) if lines[k].strip()), None)
        if j is None or LABEL_LINE_RE.match(clean(lines[j])):
            return False
        nxt = clean(lines[j])
        if LIST_RE.match(clean(raw)):
            return indent(nxt) > len(m.group(1))
        return bool(LIST_RE.match(nxt)) or j == i + 1
    return None


def indent(line):
    return len(line) - len(line.lstrip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answer", required=True)
    args = ap.parse_args()
    try:
        with open(args.answer, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        ap.error(str(e))
    fails = []
    first = next((heading_text(ln).upper() for ln in lines if ln.strip()), "")
    if not ANSWER_RE.match(first):
        fails.append("First line must be the ANSWER line")
    pos = {}
    for i, ln in enumerate(lines):
        pos.setdefault(heading_text(ln), i)
    for label in LABELS:
        if label.lower() not in pos:
            fails.append(f"{label} label missing")
    if all(k.lower() in pos for k in LABELS) \
            and pos["deep dive"] < pos["quick answer"]:
        fails.append("Deep dive must come after Quick answer")
    if not field_filled(lines, "Question as researched"):
        fails.append("Question as researched missing or empty")
    notes = [clean(ln) for ln in lines if FOOTNOTE_RE.match(clean(ln))]
    nums = {FOOTNOTE_RE.match(ln).group(1) for ln in notes}
    primary = sum(1 for ln in notes if PRIMARY_RE.search(ln))
    if len(nums) < MIN_SOURCES:
        fails.append(f"Need at least {MIN_SOURCES} sources, found {len(nums)}")
    if not primary:
        fails.append("No primary source (Type: primary)")
    for field in FIELDS:
        v = field_filled(lines, field)
        if v is None:
            fails.append(f"{field} missing")
        elif not v:
            fails.append(f"{field} empty (write 'none' if none)")
    for f in fails:
        print("FAIL  " + f)
    print(f"{'FAIL' if fails else 'PASS'}  sources={len(nums)} primary={primary}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

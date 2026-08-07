#!/usr/bin/env python3
"""Rewrite a staged upstream skill so it makes sense in this repo.

Upstream is a plugin marketplace: a skill lives at <plugin>/skills/<name>/ and
freely points at plugin-level siblings (CONNECTORS.md, .mcp.json) and at
marketplace connector placeholders. Flattening into skills/<name>/
leaves those pointers dangling — the targets are simply not here.

This runs on the STAGED copy, before sync.sh copies it into place and hashes it.
That ordering matters: sync.sh records the hash of what it wrote, so transforming
first keeps the manifest baseline self-consistent and re-sync stays clean.

Usage:  contextualize.py <staged_skill_dir> <skill_name>
Prints one report line per change to stdout. Exit 0 always (never blocks a sync).
"""

import os
import re
import sys

# A link target we should leave alone: absolute URL, anchor, or mail link.
EXTERNAL = re.compile(r"^(https?://|mailto:|#)")

# Inline markdown link: [text](target)
MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")

# Upstream connector placeholder: "~~design tool". Matched only when the line has
# no closing "~~", so real strikethrough ("~~text~~") is never touched.
CONNECTOR = re.compile(r"~~([A-Za-z][A-Za-z0-9 _/-]*?)(?=\*\*|:|,|\.|$)")

NOT_WIRED = "(connector not wired in this repo)"


def is_dead_target(target, md_file, skill_dir):
    """True if a relative link target does not resolve inside the skill dir."""
    target = target.strip().split()[0] if target.strip() else ""
    if not target or EXTERNAL.match(target):
        return False
    path = target.split("#", 1)[0]
    if not path:
        return False
    resolved = os.path.normpath(os.path.join(os.path.dirname(md_file), path))
    skill_dir = os.path.normpath(skill_dir)
    escapes = not (resolved == skill_dir or resolved.startswith(skill_dir + os.sep))
    return escapes or not os.path.exists(resolved)


def blockquote_span(lines, i):
    """Extent of the contiguous blockquote containing line i, else just line i."""
    if not lines[i].lstrip().startswith(">"):
        return i, i
    start = i
    while start > 0 and lines[start - 1].lstrip().startswith(">"):
        start -= 1
    end = i
    while end + 1 < len(lines) and lines[end + 1].lstrip().startswith(">"):
        end += 1
    return start, end


def strip_dead_links(lines, md_file, skill_dir, rel, report):
    """Drop any line (or blockquote) carrying a link that resolves nowhere here."""
    drop = set()
    for i, line in enumerate(lines):
        if i in drop:
            continue
        for _text, target in MD_LINK.findall(line):
            if is_dead_target(target, md_file, skill_dir):
                start, end = blockquote_span(lines, i)
                drop.update(range(start, end + 1))
                report.append(
                    "%s:%d removed dead reference -> %s (no such file in this repo)"
                    % (rel, i + 1, target.strip())
                )
                for d in range(start, end + 1):
                    report.append("      - %s" % lines[d].rstrip())
                break
    return [l for i, l in enumerate(lines) if i not in drop], bool(drop)


def annotate_connectors(lines, rel, report):
    """Mark marketplace connector placeholders as not wired, and drop the ~~."""
    changed = False
    for i, line in enumerate(lines):
        if line.count("~~") % 2 == 0:  # paired -> real strikethrough, leave it
            continue
        new = CONNECTOR.sub(lambda m: "%s %s" % (m.group(1), NOT_WIRED), line)
        if new != line:
            lines[i] = new
            changed = True
            report.append("%s:%d connector placeholder marked not-wired" % (rel, i + 1))
            report.append("      - %s" % line.rstrip())
            report.append("      + %s" % new.rstrip())
    return lines, changed


def strip_argument_hint(lines, rel, report):
    """Remove the argument-hint frontmatter key (no native skill here uses it)."""
    if not lines or lines[0].strip() != "---":
        return lines, False
    try:
        close = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return lines, False
    out, changed, i = [], False, 0
    while i < len(lines):
        if 0 < i < close and lines[i].startswith("argument-hint:"):
            report.append("%s:%d removed argument-hint frontmatter" % (rel, i + 1))
            report.append("      - %s" % lines[i].rstrip())
            i += 1
            while i < close and lines[i][:1] in (" ", "\t"):  # block-scalar continuation
                i += 1
            changed = True
            continue
        out.append(lines[i])
        i += 1
    return out, changed


def collapse_blanks(lines):
    """Squeeze runs of 3+ blank lines left behind by removals down to one."""
    out = []
    for line in lines:
        if line.strip() == "" and out and out[-1].strip() == "":
            continue
        out.append(line)
    return out


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("usage: contextualize.py <staged_skill_dir> <skill_name>\n")
        return 2
    skill_dir, skill = sys.argv[1], sys.argv[2]
    report = []

    for root, _dirs, files in os.walk(skill_dir):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            rel = os.path.join(skill, os.path.relpath(path, skill_dir))
            with open(path, encoding="utf-8", errors="replace") as fh:
                original = fh.read()
            lines = original.split("\n")

            lines, a = strip_dead_links(lines, path, skill_dir, rel, report)
            lines, b = annotate_connectors(lines, rel, report)
            if fn == "SKILL.md":
                lines, c = strip_argument_hint(lines, rel, report)
            else:
                c = False

            if a or b or c:
                text = "\n".join(collapse_blanks(lines))
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(text)

    for line in report:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())

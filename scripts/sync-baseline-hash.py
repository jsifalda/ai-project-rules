"""Print the sha256 of a file. SKILL.md is hashed without its frontmatter metadata block, because repo convention adds one to every synced skill and that is not a local edit."""
import hashlib
import os
import sys

FENCE = b"---"
KEY = b"metadata:"


def strip_metadata(data):
    lines = data.splitlines(keepends=True)
    if not lines or lines[0].rstrip() != FENCE:
        return data
    close = next((i for i in range(1, len(lines)) if lines[i].rstrip() == FENCE), None)
    if close is None:
        return data
    kept, skipping = [lines[0]], False
    for line in lines[1:close]:
        if line.rstrip() == KEY and not line[:1].isspace():
            skipping = True
        elif skipping and (not line.strip() or line[:1] in b" \t"):
            pass
        else:
            skipping = False
            kept.append(line)
    return b"".join(kept + lines[close:])


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("usage: sync-baseline-hash.py <file>\n")
        return 2
    path = sys.argv[1]
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        sys.stderr.write("ERROR: cannot read %s: %s\n" % (path, e))
        return 1
    if os.path.basename(path) == "SKILL.md":
        data = strip_metadata(data)
    print(hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())

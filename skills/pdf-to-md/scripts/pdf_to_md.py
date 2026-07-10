#!/usr/bin/env python3
"""
pdf_to_md.py — general core for converting a text-based PDF into clean Markdown.

Does the mechanical, document-agnostic work:
  1. layout-aware text extraction (preserves word spacing that plain extraction drops)
  2. auto-detect and strip repeated page furniture (running headers / footers / page numbers)
  3. whitespace normalization (collapse justified-text padding)
  4. reflow visual line-wraps back into paragraphs, breaking at structural markers
  5. optional heading mapping via --heading REGEX::LEVEL

Document-specific structure (which markers, TOC, footnotes, tables) is decided by the
caller. Run --probe first to see page count, text-layer health, repeated furniture and
candidate markers, then pass the right flags. Requires: pypdf.
"""
import argparse
import re
import sys
from collections import Counter

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("pypdf is required. Ask before installing:  pip install pypdf")

# General structural-marker defaults (English + Czech legal/report conventions).
DEFAULT_BLOCK_STARTS = [
    r'^§\s*\d',
    r'^\(\d+\)',
    r'^\d+[.)]\s',
    r'^[A-Za-z][.)]\s',
    r'^[IVXLC]+\.\s',
    r'^(ČÁST|HLAVA|Díl|Oddíl|Článek|Čl\.|Kapitola|PART|CHAPTER|ARTICLE|SECTION|TITLE)\b',
]
# Lines that are almost always page furniture regardless of the document.
FURNITURE_PATTERNS = [
    r'^\d+\s*/\s*\d+$',                 # "3/117"
    r'^\d+$',                           # bare page number
    r'^-?\s*\d+\s*-?$',                 # "- 12 -"
    r'https?://',                       # source URL footers
    r'^\d{1,2}[./]\d{1,2}[./]\d{2,4},?\s*\d{1,2}:\d{2}',  # date-time stamps
]


def norm(line):
    return re.sub(r'[ \t]+', ' ', line).strip()


def extract_pages(path, mode):
    reader = PdfReader(path)
    out = []
    for page in reader.pages:
        if mode == 'layout':
            try:
                out.append(page.extract_text(extraction_mode="layout") or "")
                continue
            except Exception:
                pass
        out.append(page.extract_text() or "")
    return out


def detect_furniture(pages, threshold):
    """Return the set of normalized lines that repeat across >= threshold of pages."""
    n = max(len(pages), 1)
    firsts, lasts = Counter(), Counter()
    for pg in pages:
        ls = [norm(l) for l in pg.splitlines() if norm(l)]
        if ls:
            firsts[ls[0]] += 1
            lasts[ls[-1]] += 1
    repeated = set()
    for counter in (firsts, lasts):
        for line, count in counter.items():
            if count / n >= threshold:
                repeated.add(line)
    return repeated


def is_furniture(line, repeated, drop_res):
    if line in repeated:
        return True
    return any(r.search(line) for r in drop_res)


def clean_lines(pages, repeated, drop_res):
    out = []
    for pg in pages:
        for raw in pg.splitlines():
            c = norm(raw)
            if not c or is_furniture(c, repeated, drop_res):
                continue
            out.append(c)
    return out


def reflow(lines, block_res):
    """Join wrapped continuation lines; start a new block at any block-start marker."""
    blocks, buf = [], []
    for l in lines:
        if any(r.match(l) for r in block_res):
            if buf:
                blocks.append(" ".join(buf))
            buf = [l]
        else:
            buf.append(l)
    if buf:
        blocks.append(" ".join(buf))
    return blocks


def parse_heading_rules(specs):
    rules = []
    for spec in specs or []:
        if '::' not in spec:
            sys.exit(f"--heading needs REGEX::LEVEL, got: {spec}")
        pat, lvl = spec.rsplit('::', 1)
        rules.append((re.compile(pat), int(lvl)))
    return rules


def render(blocks, heading_rules, title):
    out = []
    if title:
        out.append(f"# {title}\n")
    for b in blocks:
        level = next((lvl for rx, lvl in heading_rules if rx.match(b)), 0)
        out.append(f"{'#' * level} {b}" if level else b)
    return "\n\n".join(out) + "\n"


def probe(path):
    pages = extract_pages(path, 'layout')
    n = len(pages)
    chars = [len("".join(norm(l) for l in pg.splitlines())) for pg in pages]
    avg = sum(chars) // max(n, 1)
    print(f"pages: {n}")
    print(f"avg chars/page (layout): {avg}   -> {'text layer OK' if avg > 200 else 'LIKELY SCANNED / image-only (needs OCR, unsupported)'}")
    rep = detect_furniture(pages, 0.5)
    print(f"\nrepeated page furniture (>=50% of pages), auto-stripped:")
    for r in sorted(rep):
        print(f"  {r[:90]!r}")
    full = "\n".join(pages)
    print("\ncandidate structural markers (line-start counts):")
    for name, pat in [
        ("§ sections", r'^\s*§\s*\d'),
        ("(N) subsections", r'^\s*\(\d+\)'),
        ("N. numbered", r'^\s*\d+\.\s'),
        ("a) lettered", r'^\s*[a-z]\)\s'),
        ("ČÁST/PART", r'^\s*(ČÁST|PART)\b'),
        ("HLAVA/CHAPTER", r'^\s*(HLAVA|CHAPTER|Kapitola)\b'),
        ("Článek/ARTICLE", r'^\s*(Článek|Čl\.|ARTICLE)\b'),
    ]:
        c = len(re.findall(pat, full, re.M))
        if c:
            print(f"  {name:22} {c}")


def main():
    ap = argparse.ArgumentParser(description="Convert a text-based PDF to clean Markdown.")
    ap.add_argument("pdf")
    ap.add_argument("-o", "--output", help="output .md path (default: stdout)")
    ap.add_argument("--mode", choices=["layout", "plain"], default="layout",
                    help="extraction mode; layout preserves spacing (default), plain is a fallback")
    ap.add_argument("--probe", action="store_true", help="report structure and exit (map before you convert)")
    ap.add_argument("--furniture-threshold", type=float, default=0.5,
                    help="drop lines repeating on >= this fraction of pages (default 0.5)")
    ap.add_argument("--drop", action="append", default=[], help="extra regex of lines to drop (repeatable)")
    ap.add_argument("--block-start", action="append", default=[],
                    help="extra regex that starts a new block (repeatable); adds to defaults")
    ap.add_argument("--no-default-blocks", action="store_true", help="use only --block-start patterns")
    ap.add_argument("--keep-lines", action="store_true", help="skip reflow, keep physical lines")
    ap.add_argument("--heading", action="append", default=[], help="REGEX::LEVEL heading map (repeatable)")
    ap.add_argument("--title", help="H1 title for the top of the document")
    args = ap.parse_args()

    if args.probe:
        probe(args.pdf)
        return

    pages = extract_pages(args.pdf, args.mode)
    repeated = detect_furniture(pages, args.furniture_threshold)
    drop_res = [re.compile(p) for p in FURNITURE_PATTERNS + args.drop]
    lines = clean_lines(pages, repeated, drop_res)

    block_pats = list(args.block_start)
    if not args.no_default_blocks:
        block_pats += DEFAULT_BLOCK_STARTS
    block_res = [re.compile(p) for p in block_pats]

    blocks = lines if args.keep_lines else reflow(lines, block_res)
    md = render(blocks, parse_heading_rules(args.heading), args.title)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"wrote {args.output} ({len(md)} chars, {len(blocks)} blocks)", file=sys.stderr)
    else:
        sys.stdout.write(md)


if __name__ == "__main__":
    main()

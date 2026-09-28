#!/usr/bin/env python3
"""Check that every cited URL came from a tool result this run, and that
'verified' claims rest on independent publishers. Stdlib only.

Usage: python3 verify_citations.py --report report.md --seen seen_urls.txt
seen_urls.txt: every URL that a search, fetch, or scrape tool returned this
run, one per line (extra text on a line is fine, URLs are extracted).
Exit 0 = PASS, 1 = FAIL.
"""
import argparse
import re
import sys

URL_RE = re.compile(r"https?://[^\s)>\]\"'<]+")
REF_RE = re.compile(r"\[(\d+)\]")
SLD = {"co", "go", "ac", "or", "ne", "com", "gov", "org", "net", "edu", "sc", "mil"}


def norm(u, keep_query=True):
    u = u.strip().rstrip(".,;:)")
    u = re.sub(r"^https?://", "", u, flags=re.I)
    u = re.sub(r"^www\.", "", u, flags=re.I)
    u = u.split("#")[0]
    if not keep_query:
        u = u.split("?")[0]
    return u.rstrip("/").lower()


def reg_domain(u):
    host = norm(u).split("/")[0].split(":")[0]
    parts = host.split(".")
    if len(parts) >= 3 and parts[-2] in SLD and len(parts[-1]) == 2:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def section(text, name):
    m = re.search(r"^##\s+%s\s*$(.*?)(?=^##\s|\Z)" % re.escape(name),
                  text, re.M | re.S)
    return m.group(1) if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--seen", required=True)
    a = ap.parse_args()
    try:
        text = open(a.report, encoding="utf-8").read()
    except OSError as e:
        ap.error("cannot read --report: %s" % e)
    try:
        seen_raw = open(a.seen, encoding="utf-8").read()
    except OSError as e:
        ap.error("cannot read --seen: %s" % e)
    seen_full = {norm(u) for u in URL_RE.findall(seen_raw)}
    seen_path = {norm(u, False) for u in URL_RE.findall(seen_raw)}
    fails, warns = [], []

    sources = {}
    for line in section(text, "Sources").splitlines():
        m = re.match(r"^\s*\[(\d+)\]\s+(.*)$", line)
        if m:
            u = URL_RE.search(m.group(2))
            sources[int(m.group(1))] = u.group(0) if u else None

    if not seen_full:
        fails.append("seen file has no URLs")
    for n, u in sorted(sources.items()):
        if not u:
            continue
        if norm(u) in seen_full:
            continue
        if norm(u, False) in seen_path:
            warns.append("Source [%d]: matched without query string: %s" % (n, u))
            continue
        fails.append("Source [%d]: URL not in any tool result, possibly "
                     "invented or mistyped: %s" % (n, u))

    by_url = {}
    for n, u in sources.items():
        if u:
            by_url.setdefault(norm(u), []).append(n)
    for u, ns in by_url.items():
        if len(ns) > 1:
            fails.append("Sources %s share one URL: %s" % (ns, u))

    for line in section(text, "Evidence").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[5].lower() != "verified":
            continue
        refs = {int(x) for x in REF_RE.findall(cells[3])}
        doms = {reg_domain(sources[r]) for r in refs if sources.get(r)}
        if len(doms) < 2:
            fails.append("Evidence %s: 'verified' but sources share one "
                         "publisher domain %s" % (cells[0], sorted(doms)))

    for w in warns:
        print("WARN  " + w)
    for f in fails:
        print("FAIL  " + f)
    print("%s  sources=%d seen_urls=%d"
          % ("PASS" if not fails else "FAIL", len(sources), len(seen_full)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

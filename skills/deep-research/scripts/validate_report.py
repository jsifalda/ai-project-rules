#!/usr/bin/env python3
"""Validate a deep-research chat report (v2). Stdlib only.

Usage: python3 validate_report.py --report report.md [--today YYYY-MM-DD]
Exit 0 = PASS (warnings allowed), 1 = FAIL.
"""
import argparse
import datetime as dt
import re
import sys

REQUIRED = ["Verdict", "Evidence", "Conflicts", "Action",
            "What changes the verdict", "Gaps and dead ends", "Sources"]
STATUSES = {"verified", "single-source", "conflict", "unverified"}
CAPS = {"quick": 300, "standard": 700, "deep": 1500}
FRESH = {"legal": 30, "price": 7, "ground-truth": 7, "health": 30,
         "technical": 90, "landscape": 90}
DATE_RE = re.compile(r"\b(20\d\d-\d\d-\d\d)\b")
REF_RE = re.compile(r"\[(\d+)\]")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF"
                      "\U0001F000-\U0001F2FF\U0001F900-\U0001F9FF]")
PLACEHOLDER_RE = re.compile(r"\b(TBD|TODO|FIXME)\b|\[citation needed\]|"
                            r"Content continues|YYYY-MM-DD|\[claim\]", re.I)
NUM_OK_RE = re.compile(r"\[\d+\]|\bC\d+\b|\(est\.\)|\(unverified\)|"
                       r"\(computed", re.I)
TEMPLATE_PH_RE = re.compile(
    r"\[(?:claim|value|query|result|what|who|settled facts|skipped urls|"
    r"1 to 2 sentences|test first|check under 10 min|condition that|"
    r"missing fact)\b[^\]\n]*\]", re.I)


def parse_date(s):
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        return None


def split_sections(text):
    preamble, sections, order, cur, buf = [], {}, [], None, []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if cur is not None:
                sections[cur] = "\n".join(buf)
            cur, buf = m.group(1).strip(), []
            order.append(cur)
        elif cur is None:
            preamble.append(line)
        else:
            buf.append(line)
    if cur is not None:
        sections[cur] = "\n".join(buf)
    return "\n".join(preamble), sections, order


def parse_sources(block):
    out = {}
    for line in block.splitlines():
        m = re.match(r"^\s*\[(\d+)\]\s+(.*)$", line)
        if not m:
            continue
        body = m.group(2)
        url = URL_RE.search(body)
        typ = re.search(r"Type:\s*(primary|secondary|lead)\b", body, re.I)
        chk = re.search(r"Checked\s+(20\d\d-\d\d-\d\d)", body)
        out[int(m.group(1))] = {
            "url": url.group(0) if url else None,
            "type": typ.group(1).lower() if typ else None,
            "checked": chk.group(1) if chk else None,
        }
    return out


def parse_table(block):
    rows = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells or set("".join(cells)) <= set("-: "):
            continue
        if cells[0] in ("#", "ID"):
            continue
        rows.append(cells)
    return rows


def strip_for_style(text):
    text = URL_RE.sub("", text)
    return re.sub(r"`[^`]*`", "", text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--today", default=dt.date.today().isoformat())
    a = ap.parse_args()
    today = parse_date(a.today)
    if today is None:
        ap.error("--today must be YYYY-MM-DD")
    try:
        text = open(a.report, encoding="utf-8").read()
    except OSError as e:
        ap.error("cannot read --report: %s" % e)
    fails, warns = [], []

    pre, sec, order = split_sections(text)

    mode_m = re.search(r"Mode:\**\s*(quick|standard|deep)\b", pre, re.I)
    class_m = re.search(r"Class:\**\s*([a-z-]+)", pre, re.I)
    mode = mode_m.group(1).lower() if mode_m else None
    klass = class_m.group(1).lower() if class_m else None
    if not mode:
        fails.append("Header: no 'Mode: quick|standard|deep'")
        mode = "standard"
    if not klass or klass not in FRESH:
        fails.append("Header: no valid 'Class:' (%s)" % ", ".join(FRESH))
        klass = "legal"

    # 1 structure
    missing = [s for s in REQUIRED if s not in sec]
    if missing:
        fails.append("Missing sections: " + ", ".join(missing))
    if order and order[0] != "Verdict":
        fails.append("First section must be 'Verdict', found '%s'" % order[0])
    if "Verdict" in sec and len(sec["Verdict"].split()) < 5:
        fails.append("Verdict is empty or too short")
    if "Conflicts" in sec and not sec["Conflicts"].strip():
        fails.append("Conflicts is empty (write 'none' if none)")
    if "Conflicts" in sec and "disconfirm" not in sec["Conflicts"].lower():
        fails.append("Conflicts: no 'Disconfirming query' line")

    # 2 sources
    sources = parse_sources(sec.get("Sources", ""))
    if not sources:
        fails.append("Sources: no entries in '[N] ...' format")
    for n, s in sorted(sources.items()):
        if not s["url"]:
            fails.append("Source [%d]: no URL" % n)
        if not s["type"]:
            fails.append("Source [%d]: no 'Type: primary|secondary|lead'" % n)
        if not s["checked"]:
            fails.append("Source [%d]: no 'Checked YYYY-MM-DD'" % n)

    body = "\n".join(v for k, v in sec.items() if k != "Sources")
    cited = {int(x) for x in REF_RE.findall(body)}
    for n in sorted(cited - set(sources)):
        fails.append("Citation [%d] has no Sources entry" % n)
    for n in sorted(set(sources) - cited):
        warns.append("Source [%d] is never cited" % n)

    # 3 evidence table
    rows = parse_table(sec.get("Evidence", ""))
    if not rows:
        fails.append("Evidence: no table rows")
    limit = FRESH[klass]
    for r in rows:
        rid = r[0] if r else "?"
        if len(r) < 6:
            fails.append("Evidence %s: needs 6 columns, has %d" % (rid, len(r)))
            continue
        src, checked, status = r[3], r[4], r[5].lower()
        refs = [int(x) for x in REF_RE.findall(src)]
        d = parse_date(checked)
        if status not in STATUSES:
            fails.append("Evidence %s: status '%s' not in %s"
                         % (rid, status, sorted(STATUSES)))
        if not d:
            fails.append("Evidence %s: Checked '%s' not YYYY-MM-DD" % (rid, checked))
        elif d > today:
            fails.append("Evidence %s: Checked date in the future" % rid)
        elif (today - d).days > limit:
            fails.append("Evidence %s: stale, %d days old, limit %d for class %s"
                         % (rid, (today - d).days, limit, klass))
        if status == "verified":
            if len(set(refs)) < 2:
                fails.append("Evidence %s: 'verified' needs 2 sources" % rid)
            elif not any(sources.get(x, {}).get("type") == "primary" for x in refs):
                fails.append("Evidence %s: 'verified' needs 1 primary source" % rid)
            if klass == "ground-truth":
                fails.append("Evidence %s: ground-truth claims cannot be "
                             "'verified' from web sources" % rid)
        if status == "single-source" and len(set(refs)) != 1:
            fails.append("Evidence %s: 'single-source' needs exactly 1 source" % rid)
        if status == "conflict" and len(set(refs)) < 2:
            fails.append("Evidence %s: 'conflict' needs 2+ sources" % rid)
        if status in ("verified", "single-source", "conflict") and not refs:
            fails.append("Evidence %s: no [N] in Src column" % rid)

    # 4 action
    act = sec.get("Action", "")
    items = [l for l in act.splitlines() if re.match(r"^\s*(\d+\.|-)\s+", l)]
    if not items:
        fails.append("Action: no list items")
    for l in items:
        if not (DATE_RE.search(l) or re.search(r"\btoday\b|\btest:", l, re.I)):
            warns.append("Action item has no date: " + l.strip()[:60])
    has_test = re.search(r"\btests?\b", act, re.I)
    if klass == "ground-truth" and not has_test:
        fails.append("Action: ground-truth class needs a Test line")
    any_primary = any(
        sources.get(int(x), {}).get("type") == "primary"
        for r in rows if len(r) >= 4 for x in REF_RE.findall(r[3]))
    if rows and not any_primary and klass != "landscape" \
            and not has_test:
        fails.append("Action: no primary source in Evidence, add a Test line "
                     "that checks the primary page")

    # 5 numbers in prose sections must be backed by [N], C#, (est.),
    # or a value already in the Evidence table
    table_nums = set()
    for r in rows:
        if len(r) >= 3:
            table_nums.update(re.findall(r"\d[\d,.]*", r[2]))
    for name in ("Verdict", "Action", "Conflicts", "What changes the verdict"):
        for l in sec.get(name, "").splitlines():
            stripped = re.sub(r"^\s*\d+\.\s+", "", l)
            for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", stripped):
                probe = re.sub(r'"[^"]*"', "", s)
                probe = DATE_RE.sub("", probe)
                for n in sorted(table_nums, key=len, reverse=True):
                    probe = re.sub(r"(?<![\d,.])%s(?![\d,.])" % re.escape(n), "", probe)
                probe = URL_RE.sub("", probe)
                probe = re.sub(r"\b(C\d+|\d{1,2}-minute|10 min|24/7)\b", "", probe)
                if re.search(r"\d", probe) and not NUM_OK_RE.search(s):
                    warns.append("%s: number without [N]/C#/(est.): %s"
                                 % (name, s.strip()[:70]))

    # 6 length
    words = len(re.findall(r"\S+", pre + "\n" + body))
    cap = CAPS[mode]
    if words > cap:
        fails.append("Length: %d words, cap %d for mode %s" % (words, cap, mode))

    # 7 style and placeholders
    style = strip_for_style(text)
    if "\u2014" in style:
        fails.append("Style: em dash found")
    if ";" in style:
        fails.append("Style: semicolon found (%d)" % style.count(";"))
    if EMOJI_RE.search(style):
        fails.append("Style: emoji found")
    ph = PLACEHOLDER_RE.search(style)
    if ph:
        fails.append("Placeholder text: '%s'" % ph.group(0))
    tph = TEMPLATE_PH_RE.search(style)
    if tph:
        fails.append("Placeholder text: '%s'" % tph.group(0))

    for w in warns:
        print("WARN  " + w)
    for f in fails:
        print("FAIL  " + f)
    print("%s  words=%d/%d mode=%s class=%s claims=%d sources=%d"
          % ("PASS" if not fails else "FAIL", words, cap, mode, klass,
             len(rows), len(sources)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Export Apple Mail conversation threads from a sender to one markdown file per thread.

Read-only against Mail: snapshots the Envelope Index DB to /tmp and queries the copy.
Never writes to the live Mail store. Maintains <out>/.manifest.json so re-runs only
write threads that are new or have new messages. Standard library only.

Usage:
    export_threads.py --sender <addr> --out <dir>
                      [--sender-only] [--limit N] [--conversation ID] [--dry-run]
"""
import argparse
import email
import email.policy
import html
import json
import re
import shutil
import sqlite3
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

MAIL_ROOT = Path.home() / "Library" / "Mail"
SLUG_MAXLEN = 60
REPLY_PREFIX_RE = re.compile(r"(?i)^\s*(re|fwd|fw|odp|odpoved|sv|aw)\s*:\s*")

# Lines that mark the start of quoted/forwarded history. Body is cut at the first match.
QUOTE_SEPARATORS = [
    re.compile(r"^\s*-{2,}\s*P[uů]vodn[ií]\b.*$", re.I),                  # ---- Původní e-mail ----
    re.compile(r"^\s*-{2,}\s*(Original Message|Forwarded message)\b.*$", re.I),
    re.compile(r"^\s*On\b.{0,200}\bwrote:\s*$", re.I),                    # On <date> <x> wrote:
    re.compile(r"^\s*Dne\b.{0,200}\bnapsal.{0,6}:\s*$", re.I),            # Dne <date> <x> napsal(a):
    re.compile(r"^\s*.{0,90}\bnapsal\(a\):\s*$", re.I),
    re.compile(r"^\s*Le\b.{0,200}[ée]crit\s*:\s*$", re.I),                # French clients
]
QUOTE_LINE = re.compile(r"^\s*>")


def trim_quotes(text):
    """Keep only the new text above the first quoted/forwarded block."""
    lines = text.split("\n")
    cut = len(lines)
    for i, ln in enumerate(lines):
        if QUOTE_LINE.match(ln) or any(p.match(ln) for p in QUOTE_SEPARATORS):
            cut = i
            break
    trimmed = "\n".join(lines[:cut]).rstrip()
    return trimmed if trimmed.strip() else text.strip()


def find_live_db():
    hits = sorted(MAIL_ROOT.glob("V*/MailData/Envelope Index"))
    if not hits:
        sys.exit("ERROR: no 'Envelope Index' under ~/Library/Mail/V*/MailData/ "
                 "(grant Full Disk Access to this terminal and relaunch).")
    return hits[-1]


def snapshot_db(live_db):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    snap = Path(f"/tmp/mail-snapshot-{ts}")
    snap.mkdir(parents=True, exist_ok=True)
    for suffix in ("", "-wal", "-shm"):
        src = Path(str(live_db) + suffix)
        if src.exists():
            shutil.copy2(src, snap / src.name)
    return snap


def open_db(snap):
    db = snap / "Envelope Index"
    con = sqlite3.connect(str(db))  # copy is writable; WAL frames apply correctly
    if con.execute("PRAGMA integrity_check;").fetchone()[0] != "ok":
        sys.exit(f"ERROR: snapshot integrity check failed for {db}")
    return con


def resolve_data_dir(v_dir, url):
    """Map a mailbox imap://<acct>/<encoded path> URL to its on-disk Data directory."""
    if not url or "://" not in url:
        return None
    _, rest = url.split("://", 1)
    acct, _, path = rest.partition("/")
    segments = [unquote(p) for p in path.split("/") if p]
    mbox = v_dir / acct
    for seg in segments:
        mbox = mbox / f"{seg}.mbox"
    for cand in list(mbox.glob("*/Data")) + [mbox / "Data"]:
        if cand.is_dir():
            return cand
    return None


def emlx_path(data_dir, rowid):
    if data_dir is None:
        return None
    rev = str(rowid // 1000)[::-1]
    msgs = data_dir.joinpath(*list(rev)) / "Messages"
    for name in (f"{rowid}.emlx", f"{rowid}.partial.emlx"):
        p = msgs / name
        if p.is_file():
            return p
    return None


def parse_emlx(path):
    raw = path.read_bytes()
    first, _, rest = raw.partition(b"\n")
    try:
        rest = rest[:int(first.strip())]  # drop trailing emlx plist via byte count
    except ValueError:
        pass
    return email.message_from_bytes(rest, policy=email.policy.default)


def html_to_text(s):
    s = re.sub(r"(?is)<(script|style).*?</\1>", "", s)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</p\s*>", "\n\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def body_text(msg):
    part = None
    try:
        part = msg.get_body(preferencelist=("plain", "html"))
    except Exception:
        pass
    if part is None:
        for p in msg.walk():
            if p.get_content_maintype() == "text":
                part = p
                break
    if part is None:
        return ""
    try:
        content = part.get_content()
    except Exception:
        payload = part.get_payload(decode=True) or b""
        content = payload.decode(part.get_content_charset() or "utf-8", "replace")
    if part.get_content_subtype() == "html":
        content = html_to_text(content)
    return content.strip()


def slugify(subject):
    s = subject or ""
    while True:
        stripped = REPLY_PREFIX_RE.sub("", s)
        if stripped == s:
            break
        s = stripped
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.encode("ascii", "ignore").decode("ascii").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return (s[:SLUG_MAXLEN].strip("-") or "thread")


def fetch_threads(con, sender, sender_only):
    sender_ids = [r[0] for r in con.execute(
        "SELECT ROWID FROM addresses WHERE address = ?", (sender,)).fetchall()]
    if not sender_ids:
        return {}, sender_ids
    qs = ",".join("?" * len(sender_ids))
    convs = [r[0] for r in con.execute(
        f"SELECT DISTINCT conversation_id FROM messages "
        f"WHERE sender IN ({qs}) AND deleted = 0", sender_ids).fetchall()]
    if not convs:
        return {}, sender_ids
    cqs = ",".join("?" * len(convs))
    sql = (f"SELECT m.ROWID, m.conversation_id, m.message_id, a.address, s.subject, "
           f"m.date_received, mb.url "
           f"FROM messages m "
           f"JOIN addresses a ON a.ROWID = m.sender "
           f"JOIN subjects s ON s.ROWID = m.subject "
           f"JOIN mailboxes mb ON mb.ROWID = m.mailbox "
           f"WHERE m.conversation_id IN ({cqs}) AND m.deleted = 0")
    params = list(convs)
    if sender_only:
        sql += f" AND m.sender IN ({qs})"
        params += sender_ids
    sql += " ORDER BY m.conversation_id, m.date_received"
    threads = {}
    for rowid, conv, msgid, addr, subj, recv, url in con.execute(sql, params):
        threads.setdefault(conv, []).append({
            "rowid": rowid, "message_id": msgid, "address": addr,
            "subject": subj or "", "received": recv, "url": url,
        })
    return threads, sender_ids


def dedupe(messages):
    """Drop duplicate copies (same Gmail message_id across All Mail / Sent)."""
    seen, out = {}, []
    for m in messages:
        key = ("mid", m["message_id"]) if m["message_id"] else ("row", m["rowid"])
        if key in seen:
            continue
        seen[key] = True
        out.append(m)
    return out


def render(conv, messages, v_dir, sender, trim):
    first = datetime.fromtimestamp(messages[0]["received"])
    last = datetime.fromtimestamp(messages[-1]["received"])
    subject = messages[0]["subject"].strip() or "(no subject)"
    today = datetime.now().strftime("%Y-%m-%d")
    participants = sorted({m["address"] for m in messages})
    lines = [
        "---",
        f"thread_id: {conv}",
        f"subject: {json.dumps(subject, ensure_ascii=False)}",
        f"sender_filter: {sender}",
        "participants: [" + ", ".join(participants) + "]",
        f"message_count: {len(messages)}",
        f"first: {first.strftime('%Y-%m-%d')}",
        f"last: {last.strftime('%Y-%m-%d')}",
        f"last_synced: {today}",
        "---",
        "",
        f"# {subject}",
        "",
    ]
    for i, m in enumerate(messages, 1):
        when = datetime.fromtimestamp(m["received"]).strftime("%Y-%m-%d %H:%M")
        data_dir = resolve_data_dir(v_dir, m["url"])
        path = emlx_path(data_dir, m["rowid"])
        frm, to, msubj, text = m["address"], "", m["subject"], None
        if path is not None:
            try:
                msg = parse_emlx(path)
                frm = msg.get("From") or frm
                to = msg.get("To") or ""
                msubj = msg.get("Subject") or msubj
                text = body_text(msg)
                if trim and text:
                    text = trim_quotes(text)
            except Exception as e:
                text = f"(could not parse message body: {e})"
        if not text:
            text = "(body not available locally)"
        lines.append(f"## {i}. {when} — {clean_header(frm)}")
        if to:
            lines.append(f"**To:** {clean_header(to)}  ")
        if msubj:
            lines.append(f"**Subject:** {clean_header(msubj)}")
        lines += ["", text, "", "---", ""]
    return "\n".join(lines).rstrip() + "\n", first, last, participants


def clean_header(v):
    return re.sub(r"\s+", " ", str(v)).strip()


def assign_filename(conv, slug, first, manifest, used):
    existing = manifest["threads"].get(str(conv))
    if existing and existing.get("file"):
        used.add(existing["file"])
        return existing["file"]
    for cand in (f"{slug}.md", f"{slug}-{first.strftime('%Y-%m')}.md", f"{slug}-{conv}.md"):
        if cand not in used:
            used.add(cand)
            return cand
    fallback = f"{slug}-{conv}.md"
    used.add(fallback)
    return fallback


def load_manifest(out):
    mf = out / ".manifest.json"
    if mf.is_file():
        return json.loads(mf.read_text())
    return {"threads": {}}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sender", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sender-only", action="store_true",
                    help="only messages sent by --sender (default: full thread, both sides)")
    ap.add_argument("--limit", type=int, default=0, help="process only N most-recent threads")
    ap.add_argument("--conversation", type=int, help="process only this conversation_id")
    ap.add_argument("--trim-quotes", dest="trim", action="store_const", const=True, default=None,
                    help="strip quoted/forwarded history, keep only each message's new text")
    ap.add_argument("--keep-quotes", dest="trim", action="store_const", const=False,
                    help="keep full bodies including quoted history (default)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    out = Path(args.out).expanduser()
    live_db = find_live_db()
    v_dir = live_db.parents[1]  # ~/Library/Mail/V10
    snap = snapshot_db(live_db)
    con = open_db(snap)

    threads, sender_ids = fetch_threads(con, args.sender, args.sender_only)
    con.close()
    if not sender_ids:
        print(f"No address row matches {args.sender!r}. Snapshot: {snap}")
        return
    for conv in threads:
        threads[conv] = dedupe(threads[conv])

    order = sorted(threads, key=lambda c: threads[c][-1]["received"], reverse=True)
    if args.conversation is not None:
        order = [c for c in order if c == args.conversation]
    if args.limit:
        order = order[:args.limit]

    manifest = load_manifest(out) if out.is_dir() else {"threads": {}}
    manifest.setdefault("threads", {})
    # trim choice: explicit flag wins, else inherit the archive's stored choice, else keep.
    trim = args.trim if args.trim is not None else manifest.get("trim_quotes", False)
    used = {v.get("file") for v in manifest["threads"].values() if v.get("file")}
    created = updated = unchanged = 0

    if not args.dry_run:
        out.mkdir(parents=True, exist_ok=True)

    for conv in order:
        messages = threads[conv]
        rowids = sorted(m["rowid"] for m in messages)
        prev = manifest["threads"].get(str(conv))
        if prev and sorted(prev.get("msg_rowids", [])) == rowids:
            unchanged += 1
            continue
        slug = slugify(messages[0]["subject"])
        first_dt = datetime.fromtimestamp(messages[0]["received"])
        fname = assign_filename(conv, slug, first_dt, manifest, used)
        body, first, last, participants = render(conv, messages, v_dir, args.sender, trim)
        action = "update" if prev else "create"
        if action == "create":
            created += 1
        else:
            updated += 1
        print(f"  [{action}] {fname}  ({len(messages)} msgs)")
        if not args.dry_run:
            (out / fname).write_text(body, encoding="utf-8")
            manifest["threads"][str(conv)] = {
                "file": fname,
                "subject": messages[0]["subject"].strip(),
                "count": len(messages),
                "msg_rowids": rowids,
                "first": first.strftime("%Y-%m-%d"),
                "last": last.strftime("%Y-%m-%d"),
                "last_synced": datetime.now().strftime("%Y-%m-%d"),
            }

    if not args.dry_run:
        manifest["sender"] = args.sender
        manifest["scope"] = "sender-only" if args.sender_only else "both-sides"
        manifest["trim_quotes"] = trim
        manifest["generated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M")
        (out / ".manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n{created} created, {updated} updated, {unchanged} unchanged "
          f"({len(order)} threads considered).")
    print(f"Snapshot at {snap}. Run `rm -rf {snap}` when done.")


if __name__ == "__main__":
    main()

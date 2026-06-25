---
name: apple-mail-thread-export
description: Export Apple Mail conversation threads from a given sender into one markdown file per thread, with an incremental manifest so re-runs only write new or changed threads. Use when the user wants to archive, download, or back up all emails from a sender to local .md files, group a sender's mail into thread files, or re-sync an existing mail archive to pick up new messages. Reads the local Mail.app SQLite index read-only through a /tmp snapshot and parses .emlx bodies. Do NOT use for sending or modifying mail, configuring Mail accounts or rules, Gmail API or IMAP fetch, non-Apple-Mail clients (Outlook, Thunderbird, Spark), or extracting attachments (text bodies only).
---

# Apple Mail Thread Export

Export every email involving a sender out of locally synced Apple Mail (macOS) into one
markdown file per conversation thread. Re-runnable: a state manifest in the output folder
records what was already written, so later runs only touch new or changed threads.

## Prerequisites

The terminal/IDE needs **Full Disk Access**. Probe first:

```bash
ls ~/Library/Mail/ 2>&1 | head -3
```

If the output contains `Operation not permitted`, stop and tell the user to grant Full Disk
Access in **System Settings → Privacy & Security → Full Disk Access** to the running
terminal/IDE, then fully quit and relaunch it.

## Run it

```bash
python3 scripts/export_threads.py --sender <address> --out <folder>
```

Common flags:

- `--sender-only` — only messages sent by `<address>`. Default includes the full thread
  (both sides of each conversation).
- `--limit N` — process only the N most recently active threads. Use `--limit 1` for a
  quick checkpoint before a full run.
- `--conversation <id>` — process only one `conversation_id`.
- `--trim-quotes` / `--keep-quotes` — strip quoted/forwarded history so each message shows
  only its new text, or keep full bodies. Default keeps full bodies. The choice is recorded
  in the manifest, so later re-syncs of the same folder reuse it unless overridden.
- `--dry-run` — print the create/update/skip plan without writing files.

The script is self-contained and uses only the Python standard library (no installs).

## What it does

1. **Snapshots** `~/Library/Mail/V*/MailData/Envelope Index` (plus `-wal`/`-shm`) to
   `/tmp/mail-snapshot-<ts>/` and runs `PRAGMA integrity_check`. It queries the copy only,
   never the live DB, and never writes to the Mail store.
2. **Groups by thread** using the native `messages.conversation_id` column (reliable — no
   subject guessing). It finds every conversation containing the sender, then pulls all
   messages in those conversations (both sides unless `--sender-only`).
3. **Extracts bodies** from the `.emlx`/`.partial.emlx` files (UTF-8 / quoted-printable
   decode via the stdlib `email` parser, HTML falls back to a tag-strip). Missing bodies get
   a `(body not available locally)` placeholder. Attachments are ignored.
4. **Names each file from the topic** — the earliest subject, with `Re:`/`Fwd:` stripped and
   diacritics transliterated to ASCII, kebab-cased. Collisions get a `-YYYY-MM` then
   `-<conversation_id>` suffix. The manifest pins each thread's filename so it stays stable.
5. **Writes** one markdown file per thread (messages chronological, YAML frontmatter with
   thread metadata) and updates `<out>/.manifest.json`.

## Incremental behavior

`<out>/.manifest.json` is the source of truth for "what was already downloaded". Per
conversation it stores the filename and the set of message ROWIDs. On each run:

- thread not in the manifest → **create** its file.
- thread present but with new message ROWIDs → **rewrite** its file (idempotent).
- thread unchanged → **skip** (file untouched).

So re-running after new mail arrives only writes the threads that changed. The manifest lives
with the data in the output folder, so each archive folder tracks its own state and one folder
should hold one sender's archive.

## Closing

After running, report the snapshot path and tell the user to clean it up — never auto-delete:

> Snapshot at `/tmp/mail-snapshot-<ts>`. Run `rm -rf /tmp/mail-snapshot-<ts>` when done.

## Notes

- **Date column is Unix epoch** on current macOS (V10). The script uses
  `datetime.fromtimestamp(date_received)` directly.
- **`.emlx` filename is `messages.ROWID`** (with `.partial.emlx` fallback); its directory is
  the digits of `floor(ROWID/1000)` reversed. The script resolves the per-mailbox `Data`
  directory from each mailbox URL, so it works across accounts and mailboxes.
- Gmail "All Mail" often stores large messages as `.partial.emlx` with attachment bytes not
  synced locally — another reason attachments are out of scope.
- Bodies keep quoted reply history (lossless); the same quoted text may recur across messages
  in a thread.

---
name: apple-mail-query
description: Query the local Apple Mail (Mail.app) database on macOS to list, search, count, or extract content from emails. Always snapshots the SQLite DB first, queries the copy read-only, and suggests cleanup when done. Use when the user asks to "read my apple mail", "find emails from X", "list mail from sender", "search my inbox", "extract from email bodies", or otherwise wants to analyze locally synced Mail.app messages. Do NOT use for sending mail, modifying messages, configuring Mail rules/accounts, Gmail API / IMAP fetch, or non-Apple-Mail clients (Outlook, Thunderbird, Spark).
---

# Apple Mail Query

Read-only investigation of locally synced Apple Mail data via the SQLite `Envelope Index` DB and `.emlx` body files.

## Prerequisites

The calling terminal/IDE needs **Full Disk Access**. Probe first:

```bash
ls ~/Library/Mail/ 2>&1 | head -3
```

If output contains `Operation not permitted`, stop and tell the user:

> Grant Full Disk Access in **System Settings → Privacy & Security → Full Disk Access** to the running terminal/IDE (Terminal, iTerm, Claude Code, etc.), then fully quit and relaunch it.

Do not proceed until access is confirmed.

## MANDATORY safety workflow (every run, in order)

1. **Locate the live DB:** `~/Library/Mail/V*/MailData/Envelope Index` (current macOS = `V10`).
2. **Snapshot to `/tmp/mail-snapshot-<ts>/`** — copy the DB **plus** `-wal` **plus** `-shm` siblings (WAL consistency requires all three):

    ```bash
    SNAP="/tmp/mail-snapshot-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$SNAP"
    cp ~/Library/Mail/V10/MailData/"Envelope Index"      "$SNAP/"
    cp ~/Library/Mail/V10/MailData/"Envelope Index-wal"  "$SNAP/"
    cp ~/Library/Mail/V10/MailData/"Envelope Index-shm"  "$SNAP/"
    echo "$SNAP"
    ```

3. **Verify integrity** — must return `ok`:

    ```bash
    sqlite3 -readonly "$SNAP/Envelope Index" "PRAGMA integrity_check;"
    ```

4. **Query with `sqlite3 -readonly` against the snapshot only.** Never open the live DB. Never write to either copy.
5. **Reading `.emlx` body files** from `~/Library/Mail/...` is allowed (it is non-destructive).
6. **At the end of the task,** state the snapshot path and tell the user to clean up. Do NOT auto-delete:

    > Snapshot at `/tmp/mail-snapshot-<ts>/`. Run `rm -rf /tmp/mail-snapshot-<ts>` when finished.

## Critical gotchas

- **Date format = Unix epoch on V10.** NOT Mac Absolute Time. Use `datetime(date_received, 'unixepoch', 'localtime')`. Adding `978307200` will put dates in 2057.
- **WAL mode is in use** — copying only the main DB without `-wal`/`-shm` yields a stale snapshot.
- **`addresses.address` is COLLATE NOCASE** — case-insensitive matching is automatic; no `LOWER()` needed.
- **emlx filename = `messages.ROWID`**, NOT `remote_id` or `message_id`. Fall back to `<ROWID>.partial.emlx` if `.emlx` is missing.

## Schema essentials

- `messages` — one row per message. FK columns: `sender → addresses.ROWID`, `subject → subjects.ROWID`, `mailbox → mailboxes.ROWID`. Filter `m.deleted = 0` to skip trashed. `m.read` is `0` (unread) / `1` (read).
- `addresses(address, comment)` — sender/recipient strings.
- `subjects(subject)` — deduped subject strings.
- `mailboxes(url, ...)` — e.g. `imap://<account-uuid>/%5BGmail%5D/All%20Mail`.

## Locating .emlx body files

- **Account dir:** `~/Library/Mail/V10/<account-uuid>/<mbox-path>.mbox/.../mbox/<inner-uuid>/Data/`
- **Filename:** `<messages.ROWID>.emlx` (or `<ROWID>.partial.emlx`).
- **Directory hierarchy:** digits of `floor(ROWID/1000)` **reversed**, each digit a level.
  - 258226 → `258` → reversed `852` → `Data/8/5/2/Messages/258226.emlx`
  - 5515 → `5` → `Data/5/Messages/5515.emlx`
  - 92800 → `92` → reversed `29` → `Data/2/9/Messages/92800.emlx`

Inline bash to compute the path component:

```bash
prefix=$(awk -v n="$rowid" 'BEGIN{n=int(n/1000); s=""; while(n>0){s=s (n%10); n=int(n/10)}; print s}')
dirpath=""
for ((i=0; i<${#prefix}; i++)); do dirpath+="/${prefix:$i:1}"; done
emlx="$DATA_DIR$dirpath/Messages/${rowid}.emlx"
[ ! -f "$emlx" ] && emlx="$DATA_DIR$dirpath/Messages/${rowid}.partial.emlx"
```

For body content extraction (HTML grep, regex), `grep -a` works directly on `.emlx` — text patterns survive the binary header/trailer.

## Example queries

Assume `SNAP="/tmp/mail-snapshot-..."` from the snapshot step.

### Q1 — List messages by sender

```bash
sqlite3 -readonly "$SNAP/Envelope Index" <<'SQL'
.mode list
.separator " | "
.headers on
SELECT
  datetime(m.date_received, 'unixepoch', 'localtime') AS received,
  CASE WHEN m.read=1 THEN 'R' ELSE 'U' END AS r,
  s.subject AS subject
FROM messages m
JOIN addresses a ON a.ROWID = m.sender
JOIN subjects s ON s.ROWID = m.subject
WHERE a.address = 'sender@example.com'
  AND m.deleted = 0
ORDER BY m.date_received DESC;
SQL
```

### Q2 — Filter by subject prefix and date range

```bash
SINCE=$(date -j -f "%Y-%m-%d" "2026-04-01" "+%s")
UNTIL=$(date -j -f "%Y-%m-%d" "2026-05-01" "+%s")

sqlite3 -readonly "$SNAP/Envelope Index" <<SQL
SELECT datetime(m.date_received, 'unixepoch', 'localtime'), s.subject
FROM messages m
JOIN addresses a ON a.ROWID = m.sender
JOIN subjects s ON s.ROWID = m.subject
WHERE a.address = 'sender@example.com'
  AND m.deleted = 0
  AND s.subject LIKE 'Subject prefix%'
  AND m.date_received BETWEEN $SINCE AND $UNTIL
ORDER BY m.date_received DESC;
SQL
```

### Q3 — Extract a regex pattern from each matching email body

Discover account UUIDs once:

```bash
find ~/Library/Mail/V10 -type d -name "All Mail.mbox" 2>&1 | head
```

Then iterate ROWIDs, decode the path, and grep:

```bash
DATA_DIR="/Users/$USER/Library/Mail/V10/<account-uuid>/[Gmail].mbox/All Mail.mbox/<inner-uuid>/Data"

sqlite3 -readonly "$SNAP/Envelope Index" "SELECT m.ROWID || '|' || s.subject FROM messages m JOIN addresses a ON a.ROWID=m.sender JOIN subjects s ON s.ROWID=m.subject WHERE a.address='sender@example.com' AND m.deleted=0 AND s.subject LIKE 'Subject prefix%' ORDER BY m.date_received DESC;" | while IFS='|' read -r rowid subject; do
  prefix=$(awk -v n="$rowid" 'BEGIN{n=int(n/1000); s=""; while(n>0){s=s (n%10); n=int(n/10)}; print s}')
  dirpath=""
  for ((i=0; i<${#prefix}; i++)); do dirpath+="/${prefix:$i:1}"; done
  emlx="$DATA_DIR$dirpath/Messages/${rowid}.emlx"
  [ ! -f "$emlx" ] && emlx="$DATA_DIR$dirpath/Messages/${rowid}.partial.emlx"
  if [ -f "$emlx" ]; then
    match=$(grep -aoE '[Qq]uality[^0-9<>]{0,15}[0-9]{1,3}\s*%' "$emlx" | head -1)
    [ -z "$match" ] && match="(not found)"
  else
    match="(emlx missing)"
  fi
  echo "$subject => $match"
done
```

## Closing rule

The final assistant message of every invocation must include the cleanup suggestion with the exact snapshot path, e.g.:

> Snapshot at `/tmp/mail-snapshot-20260502-203940`. Run `rm -rf /tmp/mail-snapshot-20260502-203940` when done.

Never auto-delete the snapshot. The user owns cleanup.

---
name: setup-notifications
description: Set up Claude Code push notifications via a webhook (e.g. n8n) so you get pinged when a session finishes a task or is waiting on your input. Use when the user says "notify me when the task is done", "send me a notification when Claude needs me", "set up notifications", or runs Claude Code in tmux / mobile SSH (Termius) where native notifications don't exist.
---

# Setup notifications

Install two Claude Code hooks that POST to a webhook so the user is notified when a
session **finishes a turn** (`Stop`) or **needs their input / a permission** (`Notification`).
Built for running Claude Code in tmux over mobile SSH, where no native notification exists.

The webhook receives a JSON body — wire it to anything (n8n → Telegram/email/push, ntfy,
Slack, etc.):

```json
{ "event": "Stop", "title": "✅ Claude: task done — myrepo",
  "message": "<last assistant message snippet>", "cwd": "/root",
  "host": "myhost", "session": "<id>", "timestamp": "2026-07-04T20:00:00+00:00" }
```

## Steps

1. **Gather the config** — ask the user (one `AskUserQuestion`, recommend a default for each):
   - **Webhook URL** — where notifications POST to (required).
   - **Auth** — send `Authorization: Bearer <token>`, or open webhook (no header)?
   - **Events** — both `Stop` + `Notification` (recommended), or just one.
   - **Throttle** — max one "task done" ping per N seconds per session (default 120; "needs input" always sends).
   - **Scope** — global `~/.claude/settings.json` (all sessions), or a project's `.claude/settings.json`.

2. **Install the hook script** — copy `assets/notify-webhook.sh` to `~/.claude/hooks/notify-webhook.sh`
   (`chmod 700`). Then create `~/.claude/hooks/notify.env` from `assets/notify.env.example`
   with the answers (`chmod 600` — it holds the URL/token, do not commit it). Leave
   `NOTIFY_AUTH_BEARER=""` for an open webhook.

3. **Register the hooks** — add to the target `settings.json` `hooks` object (preserve any
   existing hooks like `SessionStart`; only add the events the user chose):

   ```json
   "Stop":         [ { "hooks": [ { "type": "command", "command": "bash ~/.claude/hooks/notify-webhook.sh" } ] } ],
   "Notification": [ { "hooks": [ { "type": "command", "command": "bash ~/.claude/hooks/notify-webhook.sh" } ] } ]
   ```
   Use the absolute path (Claude Code does not expand `~` in every context); validate the
   file with `jq . settings.json`.

4. **Verify** end-to-end (the test actually fires the webhook — fine, it's the user's own):
   ```bash
   T="$(ls -t ~/.claude/projects/*/*.jsonl | head -1)"
   echo "{\"hook_event_name\":\"Stop\",\"session_id\":\"t1\",\"cwd\":\"$PWD\",\"transcript_path\":\"$T\"}" | bash ~/.claude/hooks/notify-webhook.sh
   echo '{"hook_event_name":"Notification","session_id":"t2","cwd":"'"$PWD"'","message":"Claude needs your permission"}' | bash ~/.claude/hooks/notify-webhook.sh
   sleep 3; cat ~/.claude/hooks/notify.log   # expect http=200; confirm the pushes arrive
   ```
   Re-running the Stop test within the throttle window should log `SKIP throttled`.

## Notes

- **Requirements:** `jq`, `curl`, `setsid` (standard on Linux). The script no-ops (exits 0)
  if `jq` or `NOTIFY_WEBHOOK_URL` is missing — it never breaks a session.
- **Non-blocking:** the HTTP call is detached (`setsid ... &`), so the session never waits
  on the network. No retry on timeout (the server may have processed it).
- **Notification event** also covers idle-waiting and permission prompts, so it doubles as
  an "I'm stuck, come back" ping.

## Rollback

Remove the `Stop` / `Notification` keys from `settings.json` and delete
`~/.claude/hooks/notify-webhook.sh` + `notify.env`.

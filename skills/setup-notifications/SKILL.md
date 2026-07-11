---
name: setup-notifications
description: Set up Claude Code push notifications via a webhook (e.g. n8n) so you get pinged when Claude needs your input or goes idle (optionally: also at the end of every turn). Use when the user says "notify me when the task is done", "send me a notification when Claude needs me", "set up notifications", or runs Claude Code in tmux / mobile SSH (Termius) where native notifications don't exist.
---

# Setup notifications

Install a Claude Code hook that POSTs to a webhook so the user is notified when Claude
**needs their input / a permission or goes idle** (`Notification`). Built for running Claude
Code in tmux over mobile SSH, where no native notification exists.

**Default: `Notification` only.** It already fires both when Claude needs a permission/input
and after ~60s of true idle — i.e. exactly the "come back, I need you" moments.

**Optional add-on: `Stop`.** Fires at the **end of _every_ assistant turn** (Claude Code has
no multi-turn "task" concept, so this is not a "task done" signal — it pings after each reply).
In a chatty back-and-forth session this is noisy even with throttling; only add it if the user
explicitly wants a ping after every turn.

The webhook receives a JSON body — wire it to anything (n8n → Telegram/email/push, ntfy,
Slack, etc.):

```json
{ "event": "Notification", "title": "🔔 Claude needs you — myrepo",
  "message": "Claude is waiting for your input", "cwd": "/root",
  "host": "myhost", "session": "<id>", "timestamp": "2026-07-04T20:00:00+00:00" }
```

## Steps

1. **Gather the config** — ask the user (one `AskUserQuestion`, recommend a default for each):
   - **Webhook URL** — where notifications POST to (required).
   - **Auth** — send `Authorization: Bearer <token>`, or open webhook (no header)?
   - **Events** — `Notification` only (recommended: pings when Claude needs input or goes
     idle). Optionally also add `Stop` for a ping at the end of every turn (noisy in
     back-and-forth sessions — only if the user asks for it).
   - **Throttle** — only relevant if `Stop` is added: max one per-turn ping per N seconds per
     session (default 120; `Notification` always sends).
   - **Scope** — global `~/.claude/settings.json` (all sessions), or a project's `.claude/settings.json`.

2. **Install the hook script** — copy `assets/notify-webhook.sh` to `~/.claude/hooks/notify-webhook.sh`
   (`chmod 700`). Then create `~/.claude/hooks/notify.env` from `assets/notify.env.example`
   with the answers (`chmod 600` — it holds the URL/token, do not commit it). Leave
   `NOTIFY_AUTH_BEARER=""` for an open webhook.

3. **Register the hook** — add to the target `settings.json` `hooks` object (preserve any
   existing hooks like `SessionStart`). Add `Notification` by default:

   ```json
   "Notification": [ { "hooks": [ { "type": "command", "command": "bash ~/.claude/hooks/notify-webhook.sh" } ] } ]
   ```
   Only if the user explicitly opted into per-turn pings, also add `Stop`:
   ```json
   "Stop":         [ { "hooks": [ { "type": "command", "command": "bash ~/.claude/hooks/notify-webhook.sh" } ] } ]
   ```
   Use the absolute path (Claude Code does not expand `~` in every context); validate the
   file with `jq . settings.json`.

4. **Verify** end-to-end (the test actually fires the webhook — fine, it's the user's own):
   ```bash
   echo '{"hook_event_name":"Notification","session_id":"t2","cwd":"'"$PWD"'","message":"Claude needs your permission"}' | bash ~/.claude/hooks/notify-webhook.sh
   sleep 3; cat ~/.claude/hooks/notify.log   # expect http=200; confirm the push arrives
   ```
   If `Stop` was also added, test it too and confirm re-running within the throttle window
   logs `SKIP throttled`:
   ```bash
   T="$(ls -t ~/.claude/projects/*/*.jsonl | head -1)"
   echo "{\"hook_event_name\":\"Stop\",\"session_id\":\"t1\",\"cwd\":\"$PWD\",\"transcript_path\":\"$T\"}" | bash ~/.claude/hooks/notify-webhook.sh
   ```

## Notes

- **Requirements:** `jq`, `curl`, `setsid` (standard on Linux). The script no-ops (exits 0)
  if `jq` or `NOTIFY_WEBHOOK_URL` is missing — it never breaks a session.
- **Non-blocking:** the HTTP call is detached (`setsid ... &`), so the session never waits
  on the network. No retry on timeout (the server may have processed it).
- **Notification event** covers both idle-waiting **and** permission prompts, so on its own it
  already delivers the "I'm stuck, come back" ping — which is why it's the recommended default
  and `Stop` is opt-in.
- **Why `Stop` is opt-in:** it fires at the end of every assistant turn, so an active
  back-and-forth session pings after each reply (throttled, but still noisy). It's a per-turn
  ping, not a "the whole task finished" signal.

## Rollback

Remove the `Notification` (and `Stop`, if added) keys from `settings.json` and delete
`~/.claude/hooks/notify-webhook.sh` + `notify.env`.

#!/usr/bin/env bash
# Claude Code Stop / Notification hook -> POST a notification to a webhook (e.g. n8n).
#
# Fires a push notification when a Claude Code session finishes a turn ("Stop") or is
# waiting on the user / a permission ("Notification"). Useful when running in tmux over
# mobile SSH where no native notifications exist.
#
# Config is read from `notify.env` next to this script (see notify.env.example):
#   NOTIFY_WEBHOOK_URL        target webhook (required; empty = no-op)
#   NOTIFY_AUTH_BEARER        bearer token, or empty for an open webhook
#   NOTIFY_STOP_THROTTLE_SECS min seconds between "task done" pings per session (default 120)
#   NOTIFY_SNIPPET_CHARS      max chars of the last assistant message to include (default 280)
#
# Never blocks the session (the HTTP call is detached) and ALWAYS exits 0.
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/notify.env"
LOG="$SCRIPT_DIR/notify.log"

# ---- config defaults (overridden by notify.env) ----
NOTIFY_WEBHOOK_URL=""
NOTIFY_AUTH_BEARER=""
NOTIFY_STOP_THROTTLE_SECS=120
NOTIFY_SNIPPET_CHARS=280
# shellcheck disable=SC1090
[ -f "$ENV_FILE" ] && . "$ENV_FILE"

# Nothing to do without a target or without jq.
[ -n "$NOTIFY_WEBHOOK_URL" ] || exit 0
command -v jq >/dev/null 2>&1 || { echo "$(date -Is) ERROR jq-missing" >>"$LOG"; exit 0; }

# ---- read hook payload from stdin ----
INPUT="$(cat)"
EVENT="$(printf '%s' "$INPUT"     | jq -r '.hook_event_name // empty')"
SESSION="$(printf '%s' "$INPUT"   | jq -r '.session_id // "unknown"')"
CWD="$(printf '%s' "$INPUT"       | jq -r '.cwd // empty')"
TRANSCRIPT="$(printf '%s' "$INPUT"| jq -r '.transcript_path // empty')"
NOTIF_MSG="$(printf '%s' "$INPUT" | jq -r '.message // empty')"

DIRNAME="$(basename "${CWD:-$PWD}")"
HOST="$(hostname)"
TS="$(date -Is)"

case "$EVENT" in
  Stop|SubagentStop)
    # Throttle "done" pings per session so active back-and-forth doesn't spam.
    STATE="${TMPDIR:-/tmp}/claude-notify-stop-${SESSION}"
    if [ -f "$STATE" ]; then
      last="$(stat -c %Y "$STATE" 2>/dev/null || echo 0)"
      now="$(date +%s)"
      if [ "$(( now - last ))" -lt "$NOTIFY_STOP_THROTTLE_SECS" ]; then
        echo "$TS SKIP throttled session=$SESSION" >>"$LOG"
        exit 0
      fi
    fi
    touch "$STATE" 2>/dev/null || true
    TITLE="✅ Claude: task done — $DIRNAME"
    MSG=""
    if [ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ]; then
      # Last assistant text block from the tail of the JSONL transcript.
      MSG="$(tail -n 80 "$TRANSCRIPT" | jq -rs \
        '[.[] | select(.type=="assistant") | .message.content[]? | select(.type=="text") | .text] | last // empty' \
        2>/dev/null | tr '\n' ' ' | sed 's/  */ /g')"
    fi
    MSG="$(printf '%s' "$MSG" | cut -c1-"$NOTIFY_SNIPPET_CHARS")"
    [ -n "$MSG" ] || MSG="(task finished)"
    ;;
  Notification)
    TITLE="🔔 Claude needs you — $DIRNAME"
    MSG="${NOTIF_MSG:-Claude is waiting for your input}"
    ;;
  *)
    echo "$TS SKIP unknown-event=${EVENT:-none}" >>"$LOG"
    exit 0
    ;;
esac

# ---- build JSON body safely (never string-concat user text into JSON) ----
PAYLOAD="$(jq -nc \
  --arg event "$EVENT" \
  --arg title "$TITLE" \
  --arg message "$MSG" \
  --arg cwd "${CWD:-$PWD}" \
  --arg host "$HOST" \
  --arg session "$SESSION" \
  --arg timestamp "$TS" \
  '{event:$event,title:$title,message:$message,cwd:$cwd,host:$host,session:$session,timestamp:$timestamp}')"

# ---- send detached so the session never waits on the network; no retry on timeout ----
export NOTIFY_WEBHOOK_URL NOTIFY_AUTH_BEARER PAYLOAD LOG EVENT SESSION TS
setsid bash -c '
  hdr=()
  [ -n "${NOTIFY_AUTH_BEARER:-}" ] && hdr=(-H "Authorization: Bearer ${NOTIFY_AUTH_BEARER}")
  code="$(curl -sS -o /dev/null -w "%{http_code}" -X POST "$NOTIFY_WEBHOOK_URL" \
    -H "Content-Type: application/json" "${hdr[@]}" \
    --data-binary "$PAYLOAD" --max-time 180 2>>"$LOG")"
  echo "$TS SENT event=$EVENT http=$code session=$SESSION" >>"$LOG"
' >/dev/null 2>&1 &

exit 0

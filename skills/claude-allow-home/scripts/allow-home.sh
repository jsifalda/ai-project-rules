#!/usr/bin/env bash
# Mark a folder as trusted in Claude Code without the interactive trust dialog.
#
# Claude Code stores per-directory trust in its global config (~/.claude.json) under a
# `projects` map keyed by absolute path. A trusted folder has
# `projects["<path>"].hasTrustDialogAccepted: true`. This script sets that flag (plus
# hasCompletedProjectOnboarding) programmatically, idempotently, and atomically.
#
# Usage:
#   bash allow-home.sh            # trusts "$HOME"
#   bash allow-home.sh /srv/app   # trusts an explicit path
#
# Config location override (rare):
#   CLAUDE_CONFIG_DIR=/some/dir bash allow-home.sh   # edits /some/dir/.claude.json
#
# Requires: jq

set -euo pipefail

TARGET="${1:-$HOME}"
CONFIG="${CLAUDE_CONFIG_DIR:-$HOME}/.claude.json"

# 1. Dependency check.
if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq is required but not installed." >&2
  echo "  Debian/Ubuntu: apt-get install -y jq   |   macOS: brew install jq" >&2
  exit 1
fi

# 2. Soft warning: Claude Code rewrites ~/.claude.json on exit and may clobber this change.
if pgrep -x claude >/dev/null 2>&1; then
  echo "warning: a 'claude' process is running — stop it first, or it may overwrite this change on exit." >&2
fi

# 3. Ensure the config exists.
[ -f "$CONFIG" ] || echo '{}' > "$CONFIG"

# 4. Backup before writing.
cp "$CONFIG" "$CONFIG.bak"

# 5. Merge the trust flags into the existing config (preserves all other keys).
tmp="$(mktemp)"
jq --arg p "$TARGET" '
  .projects = (.projects // {})
  | .projects[$p] = (.projects[$p] // {})
  | .projects[$p].hasTrustDialogAccepted = true
  | .projects[$p].hasCompletedProjectOnboarding = true
' "$CONFIG" > "$tmp" && mv "$tmp" "$CONFIG"

# 6. Verify and report.
result="$(jq -r --arg p "$TARGET" '.projects[$p].hasTrustDialogAccepted' "$CONFIG")"
echo "Trusted $TARGET: $result"
echo "Config: $CONFIG  (backup: $CONFIG.bak)"
[ "$result" = "true" ]

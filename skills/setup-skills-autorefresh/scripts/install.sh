#!/usr/bin/env bash
# install.sh — register the skills auto-sync hook for Claude Code.
#
# Wires sync-skills.js (its sibling in this dir) into Claude Code's
# ~/.claude/settings.json as a SessionStart hook, so every session start
# symlinks the skills under <skills-source-dir> into ~/.claude/skills/.
#
# Usage:
#   bash install.sh <skills-source-dir>
#   e.g. bash install.sh ~/instructions/skills
#
# Config location override (rare):
#   CLAUDE_CONFIG_DIR=/some/dir bash install.sh <dir>   # edits /some/dir/settings.json
#
# Idempotent: re-running replaces any existing sync-skills hook entry (so it
# also migrates an older ~/.claude/hooks/sync-skills.js registration) and
# re-points it at the source dir you pass. Requires: node.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
HOOK="$SCRIPT_DIR/sync-skills.js"
REPO_SKILLS_DEFAULT="$(cd "$SCRIPT_DIR/../.." && pwd -P)"   # this skill's own skills/ root

# 1. Require + validate the source-dir argument.
if [ "$#" -lt 1 ] || [ -z "${1:-}" ]; then
  echo "usage: bash install.sh <skills-source-dir>" >&2
  echo "  the folder that holds your skill subdirs (<skill>/SKILL.md)" >&2
  echo "  suggested: $REPO_SKILLS_DEFAULT" >&2
  exit 2
fi
SRC_ARG="$1"

# node is required (the hook is a node script).
if ! command -v node >/dev/null 2>&1; then
  echo "error: node is required but not installed." >&2
  exit 1
fi

# The hook script must be present next to this installer.
if [ ! -f "$HOOK" ]; then
  echo "error: hook script not found: $HOOK" >&2
  exit 1
fi

# Source must exist and be a directory — resolve to an absolute realpath.
if [ ! -d "$SRC_ARG" ]; then
  echo "error: not a directory: $SRC_ARG" >&2
  exit 1
fi
ABS_SOURCE="$(cd "$SRC_ARG" && pwd -P)"

# Source must hold at least one syncable skill (<subdir>/SKILL.md).
if ! ls -d "$ABS_SOURCE"/*/SKILL.md >/dev/null 2>&1; then
  echo "error: no skills found under $ABS_SOURCE (expected <skill>/SKILL.md)" >&2
  exit 1
fi

# 2. Locate settings.json; ensure it exists; back it up.
CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SETTINGS="$CONFIG_DIR/settings.json"
mkdir -p "$CONFIG_DIR"
[ -f "$SETTINGS" ] || echo '{}' > "$SETTINGS"
cp "$SETTINGS" "$SETTINGS.bak"

# 3. Soft warning: Claude Code rewrites settings.json on exit.
if pgrep -x claude >/dev/null 2>&1; then
  echo "warning: a 'claude' process is running — restart it after this so the change isn't overwritten." >&2
fi

# 4. Idempotent merge: drop any existing sync-skills entry, add the current one.
HOOK="$HOOK" ABS_SOURCE="$ABS_SOURCE" SETTINGS="$SETTINGS" node <<'NODE'
const fs = require('fs');
const { HOOK, ABS_SOURCE, SETTINGS } = process.env;

const raw = fs.readFileSync(SETTINGS, 'utf8').trim();
const cfg = raw ? JSON.parse(raw) : {};

cfg.hooks = cfg.hooks || {};
let sessionStart = Array.isArray(cfg.hooks.SessionStart) ? cfg.hooks.SessionStart : [];

// Drop any prior sync-skills.js entry across all groups (migrates old paths, dedupes).
for (const group of sessionStart) {
  if (group && Array.isArray(group.hooks)) {
    group.hooks = group.hooks.filter(
      (h) => !(h && typeof h.command === 'string' && h.command.includes('sync-skills.js'))
    );
  }
}

// Drop any group left empty so repeated re-installs don't accumulate orphan groups.
sessionStart = sessionStart.filter(
  (g) => !(g && Array.isArray(g.hooks) && g.hooks.length === 0)
);

// Ensure a group exists to hold the entry.
let group = sessionStart.find((g) => g && Array.isArray(g.hooks));
if (!group) { group = { hooks: [] }; sessionStart.push(group); }

group.hooks.push({
  type: 'command',
  command: `node "${HOOK}" "${ABS_SOURCE}"`,
  timeout: 15,
  statusMessage: 'Syncing skills...',
});

cfg.hooks.SessionStart = sessionStart;

const tmp = SETTINGS + '.tmp';
fs.writeFileSync(tmp, JSON.stringify(cfg, null, 2) + '\n');
try {
  fs.renameSync(tmp, SETTINGS);
} catch (e) {
  try { fs.unlinkSync(tmp); } catch {}
  throw e;
}
console.log('[install] registered SessionStart hook in ' + SETTINGS);
NODE

# 5. Run the hook once now so symlinks exist immediately.
node "$HOOK" "$ABS_SOURCE"

# 6. Remove the stale, pre-repo hook copy if present (registration no longer
#    points there; identical content lives in the repo, and settings.json.bak
#    rolls back the registration — so removal is safe and reversible).
LEGACY="$CONFIG_DIR/hooks/sync-skills.js"
if [ -f "$LEGACY" ] && [ "$LEGACY" != "$HOOK" ]; then
  rm -f "$LEGACY"
  echo "[install] removed stale hook copy: $LEGACY"
fi

# 7. Report.
echo
echo "Done."
echo "  hook script : $HOOK"
echo "  syncing from: $ABS_SOURCE"
echo "  settings    : $SETTINGS  (backup: $SETTINGS.bak)"
echo "  command     : node \"$HOOK\" \"$ABS_SOURCE\""
echo "Restart Claude Code so skill enumeration picks up the change."

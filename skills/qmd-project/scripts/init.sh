#!/usr/bin/env bash
# Bootstrap the given folder (default: $PWD) as a folder-local qmd "project".
# Idempotent: safe to re-run. Writes per-folder config, builds the index.
#
# Isolation model (folder-local + named index, shared models):
#   INDEX_PATH      -> <DIR>/.qmd/<NAME>.sqlite   (DB lives in the folder)
#   QMD_CONFIG_DIR  -> <DIR>/.qmd/config          (collections YAML in the folder)
#   --index <NAME>                                 (labeled handle + 2nd isolation layer)
#   XDG_CACHE_HOME  left unset                     (2.1GB models shared globally)
# A bare qmd call from elsewhere reads the global config+DB and cannot see this folder.
set -euo pipefail

command -v qmd >/dev/null 2>&1 || { echo "qmd not found on PATH" >&2; exit 1; }
command -v jq  >/dev/null 2>&1 || { echo "jq not found on PATH (needed to merge JSON config)" >&2; exit 1; }

DIR="${1:-$PWD}"
DIR="$(cd "$DIR" 2>/dev/null && pwd)" || { echo "No such directory: ${1:-$PWD}" >&2; exit 1; }
cd "$DIR"

# NAME = sanitized folder basename (lowercase, spaces->dash, keep [a-z0-9._-]).
NAME="$(basename "$DIR" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9._-')"
[ -n "$NAME" ] || NAME="qmd-project"

export INDEX_PATH="$DIR/.qmd/$NAME.sqlite"
export QMD_CONFIG_DIR="$DIR/.qmd/config"
mkdir -p "$QMD_CONFIG_DIR" "$DIR/.claude"

# --- .gitignore: keep .qmd/ (DB, wal/shm, config, log) out of git ---
if [ -f "$DIR/.gitignore" ]; then
  grep -qxF '/.qmd/' "$DIR/.gitignore" || printf '/.qmd/\n' >> "$DIR/.gitignore"
else
  printf '/.qmd/\n' > "$DIR/.gitignore"
fi

# --- .mcp.json: folder-scoped qmd MCP server (merge if file exists) ---
MCP="$DIR/.mcp.json"
[ -f "$MCP" ] || echo '{}' > "$MCP"
tmp="$(mktemp)"
jq --arg name "$NAME" --arg ip "$INDEX_PATH" --arg cd "$QMD_CONFIG_DIR" '
  .mcpServers = (.mcpServers // {})
  | .mcpServers["qmd"] = {
      command: "qmd",
      args: ["--index", $name, "mcp"],
      env: { INDEX_PATH: $ip, QMD_CONFIG_DIR: $cd }
    }
' "$MCP" > "$tmp" && mv "$tmp" "$MCP"

# --- .claude/settings.json: pre-approve MCP + auto-reindex on every session start ---
# $CLAUDE_PROJECT_DIR stays literal (expanded by CC at session start); $NAME is baked now.
HOOK_CMD=$(cat <<EOF
nohup sh -c 'export INDEX_PATH="\$CLAUDE_PROJECT_DIR/.qmd/${NAME}.sqlite" QMD_CONFIG_DIR="\$CLAUDE_PROJECT_DIR/.qmd/config"; qmd --index ${NAME} update && qmd --index ${NAME} embed' >>"\$CLAUDE_PROJECT_DIR/.qmd/reindex.log" 2>&1 &
EOF
)
SETTINGS="$DIR/.claude/settings.json"
[ -f "$SETTINGS" ] || echo '{}' > "$SETTINGS"
tmp="$(mktemp)"
jq --arg cmd "$HOOK_CMD" '
  .enabledMcpjsonServers = (((.enabledMcpjsonServers // []) + ["qmd"]) | unique)
  | .hooks = (.hooks // {})
  | .hooks.SessionStart = (((.hooks.SessionStart // [])
      | map(select(((.hooks // []) | map(.command // "") | join("\n")) | test("reindex\\.log") | not)))
      + [ { hooks: [ { type: "command", command: $cmd } ] } ])
' "$SETTINGS" > "$tmp" && mv "$tmp" "$SETTINGS"

# --- folder CLAUDE.md: tell CC to answer from the qmd index (append once) ---
CLAUDEMD="$DIR/CLAUDE.md"
MARKER="<!-- qmd-project -->"
if [ ! -f "$CLAUDEMD" ] || ! grep -qF "$MARKER" "$CLAUDEMD"; then
  cat >> "$CLAUDEMD" <<EOF

$MARKER
## qmd knowledge base (index: \`$NAME\`)

This folder's \`.md\` files are indexed by qmd as a local, on-device semantic index. The index DB (\`.qmd/$NAME.sqlite\`) and config (\`.qmd/config/\`) live inside this folder and are isolated from the global qmd index.

To answer any question about this folder's contents, query the index first instead of reading files one by one:
- Preferred: the \`qmd\` MCP \`query\` tool (active once Claude Code is restarted in this folder).
- CLI / same session: \`INDEX_PATH=.qmd/$NAME.sqlite QMD_CONFIG_DIR=.qmd/config qmd --index $NAME query "<question>"\`

The index auto-refreshes on session start. To force a refresh after editing files, run the same env prefix with \`qmd --index $NAME update && qmd --index $NAME embed\` (or \`scripts/reindex.sh\` from the qmd-project skill).
EOF
fi

# --- build the index (recursive, nested .md) ---
if ! qmd --index "$NAME" collection list 2>/dev/null | grep -qiF -- "$NAME"; then
  qmd --index "$NAME" collection add "$DIR" --name "$NAME" --mask "**/*.md"
fi
qmd --index "$NAME" update
qmd --index "$NAME" embed

echo
echo "qmd project '$NAME' ready in: $DIR"
qmd --index "$NAME" status 2>/dev/null || true

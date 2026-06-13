#!/usr/bin/env bash
# Scoped qmd wrapper for this project's local index (shipped by the qmd setup step).
# Resolves the project root (nearest ancestor holding .qmd/<NAME>.sqlite), sets the
# folder-local scope env, then execs qmd. Passthrough: run any qmd subcommand, e.g.
#   ask.sh query "how are refunds handled"
#   ask.sh get "qmd://__QMD_INDEX__/sub/file.md"
set -euo pipefail

NAME="__QMD_INDEX__"
command -v qmd >/dev/null 2>&1 || { echo "qmd not found on PATH" >&2; exit 1; }

dir="${CLAUDE_PROJECT_DIR:-$PWD}"
while [ "$dir" != "/" ] && [ ! -f "$dir/.qmd/$NAME.sqlite" ]; do dir="$(dirname "$dir")"; done
[ -f "$dir/.qmd/$NAME.sqlite" ] || { echo "qmd index '$NAME' not found (folder not indexed yet)." >&2; exit 1; }

export INDEX_PATH="$dir/.qmd/$NAME.sqlite" QMD_CONFIG_DIR="$dir/.qmd/config"
exec qmd --index "$NAME" "$@"

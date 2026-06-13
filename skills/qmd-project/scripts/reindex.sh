#!/usr/bin/env bash
# Incrementally refresh the folder-local qmd index (default folder: $PWD).
# qmd is incremental, so this is cheap when little changed.
set -euo pipefail

command -v qmd >/dev/null 2>&1 || { echo "qmd not found on PATH" >&2; exit 1; }

DIR="${1:-$PWD}"
DIR="$(cd "$DIR" 2>/dev/null && pwd)" || { echo "No such directory: ${1:-$PWD}" >&2; exit 1; }
cd "$DIR"

NAME="$(basename "$DIR" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9._-')"
[ -n "$NAME" ] || NAME="qmd-project"

if [ ! -f "$DIR/.qmd/$NAME.sqlite" ]; then
  echo "No qmd index at .qmd/$NAME.sqlite — run init.sh first." >&2
  exit 1
fi

export INDEX_PATH="$DIR/.qmd/$NAME.sqlite"
export QMD_CONFIG_DIR="$DIR/.qmd/config"

qmd --index "$NAME" update
qmd --index "$NAME" embed

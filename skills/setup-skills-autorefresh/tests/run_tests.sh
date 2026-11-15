#!/bin/sh
# Regression tests for scripts/sync-skills.js. Run from the skill root: sh tests/run_tests.sh
# Each case runs the hook on temp dirs, with a temp HOME and an absolute CLAUDE_CONFIG_DIR.
set -u
S="$(pwd)/scripts/sync-skills.js"; ok=0
D=$(mktemp -d) || exit 1
trap 'rm -rf "$D"' EXIT

SRC="$D/src"; CFG="$D/profile"
mkdir -p "$SRC/alpha" "$SRC/x" "$SRC-backup/x" "$CFG/commands" "$D/fakehome"
printf -- '---\nname: alpha\ndescription: test skill\n---\n' > "$SRC/alpha/SKILL.md"
ln -s "$SRC-backup/x" "$CFG/commands/backup-link"
ln -s "$SRC/x" "$CFG/commands/source-link"
ln -s "$SRC" "$CFG/commands/root-link"

HOME="$D/fakehome" CLAUDE_CONFIG_DIR="$CFG" node "$S" "$SRC" >/dev/null

[ -L "$CFG/commands/backup-link" ] || { echo "FAIL commands link into <source>-backup was removed"; ok=1; }
[ -L "$CFG/commands/source-link" ] && { echo "FAIL commands link into <source>/x was kept"; ok=1; }
[ -L "$CFG/commands/root-link" ] && { echo "FAIL commands link to <source> itself was kept"; ok=1; }
[ "$(readlink "$CFG/skills/alpha")" = "$SRC/alpha" ] || { echo "FAIL alpha not linked into CLAUDE_CONFIG_DIR/skills"; ok=1; }
[ -e "$D/fakehome/.claude/skills" ] && { echo "FAIL skills linked into HOME/.claude despite CLAUDE_CONFIG_DIR"; ok=1; }

[ $ok -eq 0 ] && echo "ALL TESTS PASS"
exit $ok

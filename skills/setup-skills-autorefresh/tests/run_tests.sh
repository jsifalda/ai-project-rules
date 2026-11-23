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

# Agents: <D>/agents is the sibling of $SRC
mkdir -p "$D/agents"
printf -- '---\nname: worker\n---\n' > "$D/agents/worker.md"
mkdir -p "$CFG/agents"
printf 'mine\n' > "$CFG/agents/mine.md"
printf 'mine\n' > "$D/agents/mine.md"
HOME="$D/fakehome" CLAUDE_CONFIG_DIR="$CFG" node "$S" "$SRC" 2>/dev/null >/dev/null
[ "$(readlink "$CFG/agents/worker.md")" = "$D/agents/worker.md" ] || { echo "FAIL worker.md not linked into CLAUDE_CONFIG_DIR/agents"; ok=1; }
[ -L "$CFG/agents/mine.md" ] && { echo "FAIL non-symlink agents/mine.md was replaced"; ok=1; }
[ "$(cat "$CFG/agents/mine.md")" = "mine" ] || { echo "FAIL non-symlink agents/mine.md was changed"; ok=1; }
ln -s "$D/fakehome" "$CFG/agents/foreign.md"
rm "$D/agents/worker.md"
HOME="$D/fakehome" CLAUDE_CONFIG_DIR="$CFG" node "$S" "$SRC" >/dev/null 2>&1
[ -L "$CFG/agents/worker.md" ] && { echo "FAIL stale agents/worker.md link was not pruned"; ok=1; }
[ -L "$CFG/agents/foreign.md" ] || { echo "FAIL unmanaged agents symlink was removed"; ok=1; }
[ -f "$CFG/agents/mine.md" ] || { echo "FAIL agents/mine.md removed on prune"; ok=1; }

CFG2="$D/profile2"; SRC2="$D/s2/src"
mkdir -p "$SRC2/beta"
printf -- '---\nname: beta\ndescription: t\n---\n' > "$SRC2/beta/SKILL.md"
HOME="$D/fakehome" CLAUDE_CONFIG_DIR="$CFG2" node "$S" "$SRC2" >/dev/null
[ -e "$CFG2/agents" ] && { echo "FAIL agents dir created without an agents sibling"; ok=1; }

# Agents: first source wins, and deleting a whole agents folder prunes its links
CFG3="$D/profile3"; A1="$D/c1/src"; A2="$D/c2/src"
mkdir -p "$A1" "$A2" "$D/c1/agents" "$D/c2/agents"
printf 'one\n' > "$D/c1/agents/dup.md"; printf 'two\n' > "$D/c2/agents/dup.md"; printf 'x\n' > "$D/c2/agents/only2.md"
HOME="$D/fakehome" CLAUDE_CONFIG_DIR="$CFG3" node "$S" "$A1" "$A2" >/dev/null 2>&1
[ "$(readlink "$CFG3/agents/dup.md")" = "$D/c1/agents/dup.md" ] || { echo "FAIL agent conflict did not keep the first source"; ok=1; }
rm -rf "$D/c2/agents"
HOME="$D/fakehome" CLAUDE_CONFIG_DIR="$CFG3" node "$S" "$A1" "$A2" >/dev/null 2>&1
[ -L "$CFG3/agents/only2.md" ] && { echo "FAIL link into a deleted agents folder was not pruned"; ok=1; }
[ -L "$CFG3/agents/dup.md" ] || { echo "FAIL first-source agent link was removed"; ok=1; }
ln -s "$D/fakehome" "$CFG3/agents/mine2.md"; printf 'x\n' > "$D/c1/agents/mine2.md"
HOME="$D/fakehome" CLAUDE_CONFIG_DIR="$CFG3" node "$S" "$A1" "$A2" >/dev/null 2>&1
[ "$(readlink "$CFG3/agents/mine2.md")" = "$D/fakehome" ] || { echo "FAIL unmanaged agent symlink was replaced by a source agent"; ok=1; }

[ $ok -eq 0 ] && echo "ALL TESTS PASS"
exit $ok

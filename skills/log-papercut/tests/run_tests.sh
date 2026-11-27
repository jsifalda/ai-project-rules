#!/usr/bin/env bash
# Run from anywhere: bash tests/run_tests.sh
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$HERE/../scripts/file.sh"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
bad=0
check() { if [ "$2" = "$3" ]; then echo "ok   $1"; else echo "FAIL $1 (want '$3', got '$2')"; bad=1; fi; }

mkdir -p "$T/bin"
cat > "$T/bin/gh" <<'STUB'
#!/usr/bin/env bash
echo "$*" >> "$GH_LOG"
[ "${GH_FAIL:-}" = 1 ] && exit 1
if [ "$1 $2" = "issue list" ]; then echo "${GH_LIST:-[]}"; exit 0; fi
echo "https://example.invalid/issues/1"
STUB
chmod +x "$T/bin/gh"
export GH_LOG="$T/gh.log"
BASEPATH="$PATH"
GHPATH="$T/bin:$BASEPATH"
ARGS=(--skill demo --title "flag rejected" --tried "ran it" --expected "ok" --got "error" --fix "fix the help")
run() { env -u PAPERCUT_REPO PAPERCUT_FILE="$T/out.jsonl" PATH="${RUNPATH:-$BASEPATH}" "$@" bash "$SCRIPT" "${ARGS[@]}" >"$T/stdout" 2>"$T/stderr"; echo $?; }

bash "$SCRIPT" --skill demo >/dev/null 2>&1; check "missing arg exits 2" "$?" 2

k="gh"; k="${k}p_"; fake="${k}aaaaaaaaaaaaaaaaaaaa"
rm -f "$T/out.jsonl"
PAPERCUT_FILE="$T/out.jsonl" bash "$SCRIPT" --skill demo --title t --tried "$fake" --expected e --got g --fix f >/dev/null 2>&1
check "secret exits 3" "$?" 3
check "secret writes nothing" "$([ -e "$T/out.jsonl" ] && echo written || echo none)" none

rm -f "$T/out.jsonl"; : > "$GH_LOG"
check "no env exits 0" "$(RUNPATH="$GHPATH" run)" 0
python3 -c 'import json,sys;d=json.loads(open(sys.argv[1]).read().splitlines()[-1]);assert d["skill"]=="demo" and d["title"]=="flag rejected" and "ts" in d' "$T/out.jsonl"
check "no env writes valid JSON" "$?" 0
check "no env skips gh" "$(wc -c < "$GH_LOG" | tr -d ' ')" 0

: > "$GH_LOG"
check "no match exits 0" "$(RUNPATH="$GHPATH" run env PAPERCUT_REPO=o/r)" 0
grep -q 'issue create.*--label papercut' "$GH_LOG"; check "no match calls issue create with label" "$?" 0
grep -q 'issue comment' "$GH_LOG"; check "no match skips comment" "$?" 1

: > "$GH_LOG"
check "match exits 0" "$(RUNPATH="$GHPATH" run env PAPERCUT_REPO=o/r GH_LIST='[{"number":7,"title":"papercut(demo): flag rejected"}]')" 0
grep -q 'issue comment 7' "$GH_LOG"; check "match calls issue comment" "$?" 0
grep -q 'issue create' "$GH_LOG"; check "match skips create" "$?" 1

rm -f "$T/out.jsonl"; : > "$GH_LOG"
check "gh failing exits 0" "$(RUNPATH="$GHPATH" run env PAPERCUT_REPO=o/r GH_FAIL=1)" 0
check "gh failing falls back to JSONL" "$(wc -l < "$T/out.jsonl" | tr -d ' ')" 1

a="sk"; a="${a}-"; sk="${a}bbbbbbbbbbbbbbbbbbbbbbbb"
rm -f "$T/out.jsonl"
PAPERCUT_FILE="$T/out.jsonl" bash "$SCRIPT" --skill demo --title t --tried x --expected e --got "$sk" --fix f >/dev/null 2>&1
check "sk- token in --got exits 3" "$?" 3
ak="AK"; ak="${ak}IA"; ak="${ak}ABCDEFGHIJKLMNOP"
PAPERCUT_FILE="$T/out.jsonl" bash "$SCRIPT" --skill demo --title t --tried x --expected e --got g --fix "$ak" >/dev/null 2>&1
check "AKIA key in --fix exits 3" "$?" 3
gl="glp"; gl="${gl}at-"; gl="${gl}cccccccccccccccccccc"
PAPERCUT_FILE="$T/out.jsonl" bash "$SCRIPT" --skill demo --title "$gl" --tried x --expected e --got g --fix f >/dev/null 2>&1
check "glpat- in --title exits 3" "$?" 3
check "refused secrets write nothing" "$([ -e "$T/out.jsonl" ] && echo written || echo none)" none
PAPERCUT_FILE="$T/out.jsonl" bash "$SCRIPT" --skill demo --title t --tried "saw task-notification tag" --expected e --got g --fix f >/dev/null 2>&1
check "task-notification is not refused" "$?" 0

: > "$GH_LOG"
check "non-matching title exits 0" "$(RUNPATH="$GHPATH" run env PAPERCUT_REPO=o/r GH_LIST='[{"number":9,"title":"papercut(demo): other symptom"}]')" 0
grep -q 'issue create' "$GH_LOG"; check "non-matching title creates issue" "$?" 0
grep -q 'issue comment' "$GH_LOG"; check "non-matching title skips comment" "$?" 1

mkdir -p "$T/nonode"
for c in bash env grep mkdir dirname python3; do ln -sf "$(command -v $c)" "$T/nonode/$c"; done
ln -sf "$T/bin/gh" "$T/nonode/gh"
rm -f "$T/out.jsonl"
check "no node exits 0" "$(RUNPATH="$T/nonode" run)" 0
python3 -c 'import json,sys;d=json.loads(open(sys.argv[1]).read().splitlines()[-1]);assert d["skill"]=="demo" and "ts" in d' "$T/out.jsonl"
check "no node writes valid JSON" "$?" 0

[ $bad -eq 0 ] && echo "ALL TESTS PASS"
exit $bad

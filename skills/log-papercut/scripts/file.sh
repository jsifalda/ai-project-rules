#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: file.sh --skill <name> --title <short symptom> --tried <text> --expected <text> --got <text> --fix <text>" >&2
  exit 2
}

skill=""; title=""; tried=""; expected=""; got=""; fix=""
while [ $# -gt 0 ]; do
  [ $# -ge 2 ] || usage
  case "$1" in
    --skill) skill="$2" ;;
    --title) title="$2" ;;
    --tried) tried="$2" ;;
    --expected) expected="$2" ;;
    --got) got="$2" ;;
    --fix) fix="$2" ;;
    *) usage ;;
  esac
  shift 2
done
for v in "$skill" "$title" "$tried" "$expected" "$got" "$fix"; do
  [ -n "$v" ] || usage
done

all="$skill
$title
$tried
$expected
$got
$fix"
if printf '%s' "$all" | grep -Eq 'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|(^|[^A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|xox[bp]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|-----BEGIN .*PRIVATE KEY|glpat-[A-Za-z0-9_-]{20,}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}|Bearer [A-Za-z0-9._-]{20,}'; then
  echo "refused: a field looks like it holds a secret. Remove it and run again." >&2
  exit 3
fi
if printf '%s' "$all" | grep -Eiq '(password|passwd|secret|token|api[_-]?key)[=:][^ ]{6,}'; then
  echo "refused: a field looks like it holds a secret. Remove it and run again." >&2
  exit 3
fi

log_local() {
  local path="${PAPERCUT_FILE:-${XDG_STATE_HOME:-$HOME/.local/state}/papercuts.jsonl}"
  mkdir -p "$(dirname "$path")"
  if command -v node >/dev/null 2>&1; then
    P_SKILL="$skill" P_TITLE="$title" P_TRIED="$tried" P_EXPECTED="$expected" P_GOT="$got" P_FIX="$fix" \
      node -e 'const e=process.env;console.log(JSON.stringify({ts:new Date().toISOString(),skill:e.P_SKILL,title:e.P_TITLE,tried:e.P_TRIED,expected:e.P_EXPECTED,got:e.P_GOT,fix:e.P_FIX}))' >> "$path"
  else
    P_SKILL="$skill" P_TITLE="$title" P_TRIED="$tried" P_EXPECTED="$expected" P_GOT="$got" P_FIX="$fix" \
      python3 -c 'import json,os,datetime;e=os.environ;print(json.dumps({"ts":datetime.datetime.now(datetime.timezone.utc).isoformat(),"skill":e["P_SKILL"],"title":e["P_TITLE"],"tried":e["P_TRIED"],"expected":e["P_EXPECTED"],"got":e["P_GOT"],"fix":e["P_FIX"]}))' >> "$path"
  fi
  echo "logged to $path"
}

file_issue() {
  local issue_title="papercut($skill): $title" body number
  body="$(printf '**Skill:** %s\n\n**Tried:** %s\n\n**Expected:** %s\n\n**Got:** %s\n\n**Fix:** %s\n\nFiled by: log-papercut\n' "$skill" "$tried" "$expected" "$got" "$fix")"
  # Plain list, not --search: the search index lags, so a fresh duplicate is missed.
  number="$(T="$issue_title" gh issue list -R "$PAPERCUT_REPO" --label papercut --state open --limit 500 \
    --json number,title --jq 'first(.[]|select(.title==env.T)|.number)')" || return 1
  if [ -n "$number" ]; then
    gh issue comment "$number" -R "$PAPERCUT_REPO" --body "$body" >/dev/null || return 1
    echo "commented #$number"
  else
    gh label create papercut -R "$PAPERCUT_REPO" >/dev/null 2>&1 || true
    gh issue create -R "$PAPERCUT_REPO" --label papercut --title "$issue_title" --body "$body" || return 1
  fi
}

if [ -n "${PAPERCUT_REPO:-}" ] && command -v gh >/dev/null 2>&1; then
  if file_issue; then exit 0; fi
fi
log_local

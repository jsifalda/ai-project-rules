#!/usr/bin/env bash
# Scans for content that violates the universality policy in rules/universality.md.
# Usage:
#   scripts/check-universality.sh                    # scan tracked files in the repo
#   scripts/check-universality.sh path1 path2 ...    # scan specific files and/or directories (used by pre-commit)
# Exit code:
#   0 = clean
#   1 = violations found

set -u

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DENYLIST="${REPO_ROOT}/scripts/universality-denylist.txt"

# Files & paths that are allowed to contain forbidden patterns (policy, scanner, denylist itself).
SKIP_REL=(
  "rules/universality.md"
  "scripts/check-universality.sh"
  "scripts/universality-denylist.txt"
  "scripts/universality-denylist.txt.example"
  ".githooks/pre-commit"
)

is_skipped() {
  local rel="$1"
  # Always skip .git internals and node_modules.
  case "$rel" in
    .git/*|*/.git/*|node_modules/*|*/node_modules/*) return 0 ;;
  esac
  local s
  for s in "${SKIP_REL[@]}"; do
    [[ "$rel" == "$s" ]] && return 0
  done
  return 1
}

# Patterns as three parallel arrays so regex alternation `|` doesn't collide with a field
# separator. Using POSIX ERE for grep -E. Patterns are intentionally permissive — false
# positives are easier to silence (skip-list / denylist edit) than false negatives are to debug.
PATTERN_NAMES=(
  "personal-path-unix"
  "personal-path-windows"
  "secret-aws-key"
  "secret-github-pat"
  "secret-slack-token"
  "secret-generic"
  "internal-host"
)
PATTERN_REGEXES=(
  '/(Users|home)/[a-zA-Z0-9_.-]+/'
  'C:\\Users\\[a-zA-Z0-9_.-]+\\'
  'AKIA[0-9A-Z]{16}'
  'ghp_[A-Za-z0-9]{20,}'
  'xox[baprs]-[A-Za-z0-9-]{10,}'
  '(api[_-]?key|secret|password|token)[[:space:]]*[:=][[:space:]]*["'\''][A-Za-z0-9_+/=-]{16,}["'\'']'
  '[a-zA-Z0-9.-]+\.(internal|corp)([/'\''":[:space:]]|$)'
)
PATTERN_HINTS=(
  "Use ~, \${HOME}, or repo-relative paths instead of absolute personal paths."
  "Use %USERPROFILE% or a portable path instead of Windows personal paths."
  "Looks like an AWS access key. Move to an env var; never commit live secrets."
  "Looks like a GitHub PAT. Rotate it now if real, and use an env var."
  "Looks like a Slack token. Rotate if real and use an env var."
  "Looks like a hardcoded secret. Reference an env var instead."
  "Internal hostname leaked. Replace with a public URL or instruct the reader to configure their own."
)

violations=0
report() {
  local cat="$1" file="$2" line="$3" hint="$4" match="$5"
  printf '  [%s] %s:%s\n    %s\n    hint: %s\n' "$cat" "$file" "$line" "$match" "$hint"
  violations=$((violations + 1))
}

scan_file() {
  local file="$1"
  local rel="${file#${REPO_ROOT}/}"
  is_skipped "$rel" && return 0
  [[ -f "$file" ]] || return 0
  # Skip binary files.
  if LC_ALL=C grep -Iq . "$file" 2>/dev/null; then : ; else return 0 ; fi

  local i name regex hint
  for i in "${!PATTERN_NAMES[@]}"; do
    name="${PATTERN_NAMES[$i]}"
    regex="${PATTERN_REGEXES[$i]}"
    hint="${PATTERN_HINTS[$i]}"
    while IFS=: read -r lineno match; do
      [[ -z "$lineno" ]] && continue
      report "$name" "$rel" "$lineno" "$hint" "$match"
    done < <(grep -nE "$regex" "$file" 2>/dev/null || true)
  done

  # Denylist (fixed strings, case-insensitive). Optional file.
  if [[ -f "$DENYLIST" ]]; then
    # Strip blanks and comments.
    local tmp
    tmp="$(grep -vE '^[[:space:]]*(#|$)' "$DENYLIST" || true)"
    if [[ -n "$tmp" ]]; then
      while IFS=: read -r lineno match; do
        [[ -z "$lineno" ]] && continue
        report "denylist" "$rel" "$lineno" "Matched a name in scripts/universality-denylist.txt. Replace with a placeholder." "$match"
      done < <(printf '%s\n' "$tmp" | grep -niFf /dev/stdin "$file" 2>/dev/null || true)
    fi
  fi
}

# Build file list.
files=()
if [[ $# -gt 0 ]]; then
  for f in "$@"; do
    if [[ -d "$f" ]]; then
      while IFS= read -r sub; do
        files+=("$sub")
      done < <(find "$f" -type f -not -path '*/.git/*' -not -path '*/node_modules/*')
    elif [[ -f "$f" ]]; then
      files+=("$f")
    fi
  done
else
  # Scan tracked files in the repo (so we don't trip over untracked junk).
  if command -v git >/dev/null && git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    while IFS= read -r f; do
      files+=("${REPO_ROOT}/${f}")
    done < <(git -C "$REPO_ROOT" ls-files)
  else
    while IFS= read -r f; do
      files+=("$f")
    done < <(find "$REPO_ROOT" -type f -not -path '*/.git/*' -not -path '*/node_modules/*')
  fi
fi

if [[ ${#files[@]} -gt 0 ]]; then
  for f in "${files[@]}"; do
    scan_file "$f"
  done
fi

if [[ $violations -gt 0 ]]; then
  printf '\nuniversality check: %d violation(s) found.\n' "$violations" >&2
  printf 'see rules/universality.md for the policy.\n' >&2
  exit 1
fi

printf 'universality check: clean (%d files scanned).\n' "${#files[@]}"
exit 0

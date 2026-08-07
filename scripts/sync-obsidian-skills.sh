#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================

REPO_OWNER="kepano"
REPO_NAME="obsidian-skills"
BRANCH="main"

# Skills to sync — add or remove entries here
SKILLS=(
  "defuddle"
  "json-canvas"
  "obsidian-bases"
  "obsidian-cli"
  "obsidian-markdown"
)

# =============================================================================
# Args
# =============================================================================

for arg in "$@"; do
  case "$arg" in
    --help|-h)
      cat <<'EOF'
Sync the five Obsidian skills from kepano/obsidian-skills into this repo's
skills/ folder.

Usage:
  sync-obsidian-skills.sh [--help]

This script takes no skill names. It always syncs a fixed set, the same
five skills every run:
  - defuddle
  - json-canvas
  - obsidian-bases
  - obsidian-cli
  - obsidian-markdown

Destination:
  This repo's own skills/ folder.

OVERWRITE HAZARD (read this before running):
  This script has no safety net at all. Unlike the sibling sync scripts,
  there is no sha256 baseline, no manifest, and no --force gate. Every run
  deletes local files that are not present upstream and overwrites every
  remaining file unconditionally. Any local edit you made to one of the
  five skills above is lost, with no warning and no prompt.
  Commit or stash local changes to those skills before running this.

Changing the skill set:
  Edit the SKILLS array near the top of this script.

Rate limits:
  Set GITHUB_TOKEN in the environment for higher GitHub API rate limits.

New skills:
  Each NEW skill this script creates needs a row added to the '## Skills'
  table in README.md.
EOF
      exit 0
      ;;
    -*)
      echo "ERROR: unknown flag: $arg" >&2
      exit 2
      ;;
    *)
      echo "ERROR: this script takes no skill names. It syncs a fixed set. See --help." >&2
      exit 2
      ;;
  esac
done

# Local skills directory (resolved relative to this script's location).
# Default target is this repo's own skills/ folder.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCAL_SKILLS_DIR="$(cd "$SCRIPT_DIR/../skills" && pwd)" || {
  echo "ERROR: cannot resolve the repo's skills/ folder" >&2
  exit 1
}

# Capture which skills are new (no local dir yet) before anything downloads,
# so the closing report can tell you which ones need a README row.
new_skills=()
for skill in "${SKILLS[@]}"; do
  [ -d "$LOCAL_SKILLS_DIR/$skill" ] || new_skills+=("$skill")
done

echo "WARNING: this sync overwrites the five Obsidian skills unconditionally." >&2
echo "         There is no baseline and no --force gate. Local edits to them are lost." >&2
echo "         Commit or stash changes to those skills first if you want to keep them." >&2

# =============================================================================
# Setup
# =============================================================================

TMPFILE=$(mktemp)
HEADER_FILE=$(mktemp)
trap 'rm -f "$TMPFILE" "$HEADER_FILE"' EXIT

# Optional GitHub token for higher rate limits.
# CURL_OPTS is for file downloads, where -f is right: a 404 must fail rather than
# write an error page into a skill file.
CURL_OPTS=(-fsSL)
# API_OPTS is for the tree request, which inspects the HTTP status itself and so
# must NOT use -f. With -f curl exits non-zero, the "|| echo 000" fallback appends
# to the captured code, and a 403 arrives as "403000". That never matches the
# rate-limit branch below, so the GITHUB_TOKEN hint would never print.
API_OPTS=(-sSL)
if [ -n "${GITHUB_TOKEN:-}" ]; then
  CURL_OPTS+=(-H "Authorization: token $GITHUB_TOKEN")
  API_OPTS+=(-H "Authorization: token $GITHUB_TOKEN")
fi

downloaded=0
removed=0
errors=0

# =============================================================================
# Step 1: Fetch full file tree from GitHub API (single call)
# =============================================================================

echo "Fetching file tree from $REPO_OWNER/$REPO_NAME@$BRANCH..."

TREE_URL="https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/git/trees/$BRANCH?recursive=1"

HTTP_CODE=$(curl -sS -D "$HEADER_FILE" -o "$TMPFILE" -w "%{http_code}" \
  "${API_OPTS[@]}" "$TREE_URL" 2>/dev/null || echo "000")

if [ "$HTTP_CODE" != "200" ]; then
  echo "ERROR: GitHub API returned HTTP $HTTP_CODE"
  if [ "$HTTP_CODE" = "000" ]; then
    echo "Network error — check your internet connection"
  elif [ "$HTTP_CODE" = "403" ]; then
    echo "Rate limited — set GITHUB_TOKEN env variable for higher limits"
  fi
  cat "$TMPFILE" 2>/dev/null
  exit 1
fi

# Check rate limit
RATE_REMAINING=$(grep -i 'x-ratelimit-remaining' "$HEADER_FILE" 2>/dev/null | tr -d '\r' | awk '{print $2}' || echo "")
if [ -n "$RATE_REMAINING" ] && [ "$RATE_REMAINING" -lt 10 ] 2>/dev/null; then
  echo "WARNING: GitHub API rate limit low ($RATE_REMAINING remaining). Set GITHUB_TOKEN for higher limits."
fi

# =============================================================================
# Step 2: Parse tree to find files for target skills
# =============================================================================

command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 is required"; exit 1; }

REMOTE_FILES=$(python3 -c "
import sys, json

with open(sys.argv[1]) as f:
    tree = json.load(f)

skills = set(sys.argv[2:])
for item in tree.get('tree', []):
    if item['type'] != 'blob':
        continue
    parts = item['path'].split('/')
    if len(parts) >= 3 and parts[0] == 'skills' and parts[1] in skills:
        print(item['path'])
" "$TMPFILE" "${SKILLS[@]}")

if [ -z "$REMOTE_FILES" ]; then
  echo "ERROR: No matching files found in remote tree. Check skill names and repo structure."
  exit 1
fi

echo "Found $(echo "$REMOTE_FILES" | wc -l | tr -d ' ') files across ${#SKILLS[@]} skills"
echo ""

# =============================================================================
# Step 3: Clean local files not present in remote
# =============================================================================

for skill in "${SKILLS[@]}"; do
  local_skill_dir="$LOCAL_SKILLS_DIR/$skill"
  if [ -d "$local_skill_dir" ]; then
    while IFS= read -r local_file; do
      rel_path="${local_file#"$LOCAL_SKILLS_DIR"/}"
      remote_path="skills/$rel_path"
      if ! echo "$REMOTE_FILES" | grep -qxF "$remote_path"; then
        rm "$local_file"
        echo "[removed] $rel_path"
        removed=$((removed + 1))
      fi
    done < <(find "$local_skill_dir" -type f 2>/dev/null)
    # Clean empty directories
    find "$local_skill_dir" -type d -empty -delete 2>/dev/null || true
  fi
done

# =============================================================================
# Step 4: Download files
# =============================================================================

RAW_BASE="https://raw.githubusercontent.com/$REPO_OWNER/$REPO_NAME/$BRANCH"

while IFS= read -r remote_path; do
  # remote_path is like "skills/defuddle/SKILL.md"
  # local_rel is like "defuddle/SKILL.md"
  local_rel="${remote_path#skills/}"
  local_path="$LOCAL_SKILLS_DIR/$local_rel"
  local_dir="$(dirname "$local_path")"

  mkdir -p "$local_dir"

  if curl "${CURL_OPTS[@]}" -o "$local_path" "$RAW_BASE/$remote_path" 2>/dev/null; then
    echo "[synced]  $local_rel"
    downloaded=$((downloaded + 1))
  else
    echo "[ERROR]   Failed to download: $remote_path"
    errors=$((errors + 1))
  fi
done <<< "$REMOTE_FILES"

# =============================================================================
# Step 5: Summary
# =============================================================================

echo ""
echo "=== Sync Complete ==="
echo "Skills:     ${#SKILLS[@]} ($(IFS=', '; echo "${SKILLS[*]}"))"
echo "Downloaded: $downloaded files"
echo "Removed:    $removed files"
echo "Errors:     $errors"

if [ "${#new_skills[@]}" -gt 0 ]; then
  echo ""
  echo "=== NEW SKILLS — REGISTER THESE in the '## Skills' table in README.md ==="
  echo "(Hand-maintained catalog, rows alphabetical. Add one row per skill:"
  echo "   [\`<name>\`](skills/<name>/SKILL.md) | What it does | Depends on | Origin"
  echo " Origin = https://github.com/kepano/obsidian-skills"
  echo " Curate the one-liner from each description below — don't paste it whole.)"
  python3 -c "
import sys, re, os
base = sys.argv[1]
for skill in sys.argv[2:]:
    p = os.path.join(base, skill, 'SKILL.md')
    desc = ''
    if os.path.isfile(p):
        text = open(p, encoding='utf-8', errors='replace').read()
        m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
        if m:
            dm = re.search(r'^description:\s*(.*?)(?=^\S|\Z)', m.group(1) + '\n', re.DOTALL | re.MULTILINE)
            if dm:
                desc = re.sub(r'\s+', ' ', dm.group(1).lstrip('>|-').strip())
    print('  - %s: %s' % (skill, (desc[:300] + '...') if len(desc) > 300 else desc))
" "$LOCAL_SKILLS_DIR" "${new_skills[@]}"
fi

if [ "$errors" -gt 0 ]; then
  exit 1
fi

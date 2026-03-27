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

# Local skills directory (resolved relative to this script's location)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCAL_SKILLS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# =============================================================================
# Setup
# =============================================================================

TMPFILE=$(mktemp)
HEADER_FILE=$(mktemp)
trap 'rm -f "$TMPFILE" "$HEADER_FILE"' EXIT

# Optional GitHub token for higher rate limits
CURL_OPTS=(-fsSL)
if [ -n "${GITHUB_TOKEN:-}" ]; then
  CURL_OPTS+=(-H "Authorization: token $GITHUB_TOKEN")
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
  "${CURL_OPTS[@]}" "$TREE_URL" 2>/dev/null || echo "000")

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

if [ "$errors" -gt 0 ]; then
  exit 1
fi

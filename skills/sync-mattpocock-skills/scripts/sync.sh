#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================

REPO_OWNER="mattpocock"
REPO_NAME="skills"
BRANCH="main"

# Upstream layout is nested: skills/<category>/<name>/...
# Local layout is flat:       skills/<name>/...   (the sync flattens on download)

# =============================================================================
# Args & paths
# =============================================================================

FORCE="${FORCE:-0}"
REQUESTED=()
for arg in "$@"; do
  case "$arg" in
    --force|-f) FORCE=1 ;;
    -*) echo "ERROR: unknown flag: $arg"; exit 2 ;;
    *) REQUESTED+=("$arg") ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCAL_SKILLS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"   # the repo's skills/ folder
STATE_DIR="$SCRIPT_DIR/../state"
STATE_FILE="$STATE_DIR/synced.txt"
MANIFEST="$STATE_DIR/manifest.txt"
mkdir -p "$STATE_DIR"
[ -f "$STATE_FILE" ] || : > "$STATE_FILE"
[ -f "$MANIFEST" ] || : > "$MANIFEST"

command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 is required"; exit 1; }
SHASUM=(shasum -a 256)
command -v shasum >/dev/null 2>&1 || SHASUM=(sha256sum)
command -v "${SHASUM[0]}" >/dev/null 2>&1 || { echo "ERROR: shasum/sha256sum is required"; exit 1; }

# If no skills were named, fall back to the previously-synced set (state file).
if [ "${#REQUESTED[@]}" -eq 0 ]; then
  while IFS= read -r line; do
    line="$(echo "$line" | tr -d '[:space:]')"
    [ -n "$line" ] && REQUESTED+=("$line")
  done < "$STATE_FILE"
  if [ "${#REQUESTED[@]}" -eq 0 ]; then
    echo "ERROR: no skills named and state/synced.txt is empty."
    echo "Pass one or more skill names, e.g.:  bash scripts/sync.sh to-prd handoff"
    exit 1
  fi
  echo "No skills named — using previously-synced set: ${REQUESTED[*]}"
  echo ""
fi

# =============================================================================
# Setup
# =============================================================================

TMPFILE=$(mktemp)
HEADER_FILE=$(mktemp)
STAGE_DIR=$(mktemp -d)
trap 'rm -rf "$TMPFILE" "$HEADER_FILE" "$STAGE_DIR"' EXIT

CURL_OPTS=(-fsSL)
if [ -n "${GITHUB_TOKEN:-}" ]; then
  CURL_OPTS+=(-H "Authorization: token $GITHUB_TOKEN")
fi

downloaded=0
removed=0
skipped=0
errors=0
applied_skills=()

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

RATE_REMAINING=$(grep -i 'x-ratelimit-remaining' "$HEADER_FILE" 2>/dev/null | tr -d '\r' | awk '{print $2}' || echo "")
if [ -n "$RATE_REMAINING" ] && [ "$RATE_REMAINING" -lt 10 ] 2>/dev/null; then
  echo "WARNING: GitHub API rate limit low ($RATE_REMAINING remaining). Set GITHUB_TOKEN for higher limits."
fi

# =============================================================================
# Step 2: Resolve each requested skill to its category and remote files
# =============================================================================
# Output lines, one per remote blob to sync:  <name>\t<remote_path>
# where remote_path = skills/<category>/<name>/<rest>
#
# Resolution rules (python):
#   - bare "tdd"            → find skills/<cat>/tdd/... across all categories
#   - qualified "eng/tdd"   → require that exact category
#   - 0 matches            → error, list available
#   - >1 category for bare → error, ask to qualify
#   - deprecated/in-progress → allowed, but a warning is printed to stderr

RESOLVED=$(python3 -c "
import sys, json

with open(sys.argv[1]) as f:
    tree = json.load(f)
requested = sys.argv[2:]

# Map: (category, name) -> list of full blob paths; and name -> set(categories)
from collections import defaultdict
by_skill = defaultdict(list)
cats_for = defaultdict(set)
for item in tree.get('tree', []):
    if item['type'] != 'blob':
        continue
    parts = item['path'].split('/')
    if len(parts) >= 4 and parts[0] == 'skills':
        cat, name = parts[1], parts[2]
        by_skill[(cat, name)].append(item['path'])
        cats_for[name].add(cat)

def available():
    return '\n'.join('  %s/%s' % (c, n) for (c, n) in sorted(by_skill.keys()))

errors = []
for req in requested:
    if '/' in req:
        cat, name = req.split('/', 1)
        key = (cat, name)
        if key not in by_skill:
            errors.append('No upstream skill \"%s\". Available:\n%s' % (req, available()))
            continue
        chosen = [key]
    else:
        name = req
        cats = sorted(cats_for.get(name, []))
        if not cats:
            errors.append('No upstream skill named \"%s\". Available:\n%s' % (name, available()))
            continue
        if len(cats) > 1:
            errors.append('Skill \"%s\" exists in multiple categories: %s. Re-run qualified, e.g. %s/%s'
                          % (name, ', '.join(cats), cats[0], name))
            continue
        chosen = [(cats[0], name)]
    for (cat, name) in chosen:
        if cat in ('deprecated', 'in-progress'):
            sys.stderr.write('WARNING: %s/%s is from an unstable category (%s)\n' % (cat, name, cat))
        for path in sorted(by_skill[(cat, name)]):
            print('%s\t%s' % (name, path))

if errors:
    sys.stderr.write('\n'.join(errors) + '\n')
    sys.exit(3)
" "$TMPFILE" "${REQUESTED[@]}") || { echo ""; echo "ERROR: skill resolution failed (see above)"; exit 1; }

if [ -z "$RESOLVED" ]; then
  echo "ERROR: nothing resolved to sync."
  exit 1
fi

# Unique list of skill names actually resolved (preserves request intent)
TARGET_NAMES=$(echo "$RESOLVED" | awk -F'\t' '{print $1}' | sort -u)
echo "Resolved $(echo "$TARGET_NAMES" | wc -l | tr -d ' ') skill(s): $(echo "$TARGET_NAMES" | paste -sd' ' -)"
echo ""

RAW_BASE="https://raw.githubusercontent.com/$REPO_OWNER/$REPO_NAME/$BRANCH"

# =============================================================================
# Step 3: For each skill — stage upstream, check for local edits, then apply
# =============================================================================

# Helper: hash recorded in manifest for a local rel path ("<name>/<rest>")
manifest_hash() {
  awk -v p="$1" '$2==p {print $1; exit}' "$MANIFEST"
}
# Helper: current sha256 of a file
file_hash() {
  "${SHASUM[@]}" "$1" | awk '{print $1}'
}

for skill in $TARGET_NAMES; do
  # Remote blob paths for this skill
  skill_remote=$(echo "$RESOLVED" | awk -F'\t' -v s="$skill" '$1==s {print $2}')

  # --- Stage all upstream files for this skill into STAGE_DIR/<name>/<rest> ---
  stage_ok=1
  while IFS= read -r remote_path; do
    # remote_path = skills/<cat>/<name>/<rest>  ->  local_rel = <name>/<rest>
    rest="${remote_path#skills/*/}"          # strips "skills/<cat>/" -> "<name>/<rest>"
    stage_path="$STAGE_DIR/$rest"
    mkdir -p "$(dirname "$stage_path")"
    if ! curl "${CURL_OPTS[@]}" -o "$stage_path" "$RAW_BASE/$remote_path" 2>/dev/null; then
      echo "[ERROR]   Failed to download: $remote_path"
      errors=$((errors + 1))
      stage_ok=0
    fi
  done <<< "$skill_remote"
  [ "$stage_ok" -eq 1 ] || { echo "[skipped: download error] $skill"; continue; }

  local_skill_dir="$LOCAL_SKILLS_DIR/$skill"

  # --- Detect local edits against the manifest baseline ---
  modified_files=()
  if [ -d "$local_skill_dir" ] && [ "$FORCE" -ne 1 ]; then
    while IFS= read -r lf; do
      rel="${lf#"$LOCAL_SKILLS_DIR"/}"        # <name>/<rest>
      recorded="$(manifest_hash "$rel")"
      current="$(file_hash "$lf")"
      if [ -z "$recorded" ] || [ "$recorded" != "$current" ]; then
        modified_files+=("$rel")
      fi
    done < <(find "$local_skill_dir" -type f 2>/dev/null)
  fi

  if [ "${#modified_files[@]}" -gt 0 ]; then
    echo "[skipped: locally modified] $skill"
    for mf in "${modified_files[@]}"; do echo "    ~ $mf"; done
    echo "    re-run with --force to overwrite"
    skipped=$((skipped + 1))
    continue
  fi

  # --- Apply: clean removed files, then copy staged files into place ---
  staged_rel=$(cd "$STAGE_DIR/$skill" 2>/dev/null && find . -type f | sed 's|^\./||' || true)

  if [ -d "$local_skill_dir" ]; then
    while IFS= read -r lf; do
      rel="${lf#"$local_skill_dir"/}"
      if ! echo "$staged_rel" | grep -qxF "$rel"; then
        rm "$lf"
        echo "[removed] $skill/$rel"
        removed=$((removed + 1))
      fi
    done < <(find "$local_skill_dir" -type f 2>/dev/null)
  fi

  while IFS= read -r rel; do
    [ -z "$rel" ] && continue
    dest="$local_skill_dir/$rel"
    mkdir -p "$(dirname "$dest")"
    cp "$STAGE_DIR/$skill/$rel" "$dest"
    echo "[synced]  $skill/$rel"
    downloaded=$((downloaded + 1))
  done <<< "$staged_rel"

  find "$local_skill_dir" -type d -empty -delete 2>/dev/null || true
  applied_skills+=("$skill")
done

# =============================================================================
# Step 4: Persist state (synced names) and manifest (per-file hashes)
# =============================================================================

if [ "${#applied_skills[@]}" -gt 0 ]; then
  # synced.txt = union of prior set + newly applied, sorted unique
  {
    cat "$STATE_FILE"
    printf '%s\n' "${applied_skills[@]}"
  } | sed '/^[[:space:]]*$/d' | sort -u > "$STATE_FILE.tmp"
  mv "$STATE_FILE.tmp" "$STATE_FILE"

  # manifest.txt = drop old entries for applied skills, re-add fresh hashes
  applied_re=$(printf '%s\n' "${applied_skills[@]}" | paste -sd'|' -)
  awk -v re="^($applied_re)/" '$2 !~ re' "$MANIFEST" > "$MANIFEST.tmp" || : > "$MANIFEST.tmp"
  for skill in "${applied_skills[@]}"; do
    while IFS= read -r lf; do
      rel="${lf#"$LOCAL_SKILLS_DIR"/}"
      printf '%s  %s\n' "$(file_hash "$lf")" "$rel" >> "$MANIFEST.tmp"
    done < <(find "$LOCAL_SKILLS_DIR/$skill" -type f 2>/dev/null)
  done
  sort -k2 "$MANIFEST.tmp" -o "$MANIFEST.tmp"
  mv "$MANIFEST.tmp" "$MANIFEST"
fi

# =============================================================================
# Step 5: Summary
# =============================================================================

echo ""
echo "=== Sync Complete ==="
echo "Requested:  ${REQUESTED[*]}"
echo "Applied:    ${#applied_skills[@]} ($(IFS=', '; echo "${applied_skills[*]:-none}"))"
echo "Files:      $downloaded written, $removed removed"
echo "Skipped:    $skipped (locally modified — use --force)"
echo "Errors:     $errors"

if [ "$errors" -gt 0 ]; then
  exit 1
fi

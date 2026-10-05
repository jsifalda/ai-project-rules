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

LIST=0
HELP=0
DEST=""
REQUESTED=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --list|-l)  LIST=1 ;;
    --help|-h)  HELP=1 ;;
    --dest)     shift; [ "$#" -gt 0 ] && [ -n "$1" ] || { echo "ERROR: --dest needs a directory"; exit 2; }; DEST="$1" ;;
    --dest=*)   DEST="${1#--dest=}"; [ -n "$DEST" ] || { echo "ERROR: --dest needs a directory"; exit 2; } ;;
    -*)         echo "ERROR: unknown flag: $1"; exit 2 ;;
    *)          REQUESTED+=("$1") ;;
  esac
  shift
done

# =============================================================================
# --help: answer before any dependency check, network call, or state write
# =============================================================================
# Kept first on purpose. It must work on a machine with no python3, and it must
# never create a state directory as a side effect of asking for the usage text.

if [ "$HELP" -eq 1 ]; then
  cat <<'HELPTEXT'
sync-mattpocock-skills.sh

Pulls skills from github.com/mattpocock/skills into a flat skills folder.
Upstream nests every skill under a category dir (engineering, productivity, misc,
deprecated, in-progress). This script flattens that down to skills/<name>/.

USAGE
  sync-mattpocock-skills.sh [<name> ...] [--list] [--dest <dir>]

FLAGS
  --list, -l      Print the upstream catalog grouped by category, then exit.
  --dest <dir>    Sync into <dir> instead of the repo's skills/ folder.
  --dest=<dir>    Same flag, joined form. A missing dir is created.
  --help, -h      Print this text and exit.

NAMES
  Pass one or more skill names. A name that lives in more than one category is
  ambiguous, so qualify it as <category>/<name>, for example productivity/handoff.
  Run with no names at all and the script re-syncs the set recorded in the state
  file. That errors out when the state file is empty, which is the case on a
  fresh clone.

CARRIED SKILLS
  This repo carries these upstream skills.
    prototype        synced by this script, engineering category
    handoff          synced by this script, productivity category
    grill-me         hand-port of productivity/grilling, see REFUSED NAMES
    grill-with-docs  hand-port with local edits
    domain-modeling  hand-port with local edits
    retro            hand-port with local edits
  No baseline is committed for them, so a re-sync of any of them is refused (see
  OVERWRITE SAFETY). Port an upstream change by hand.

PATHS
  Default destination   the repo's skills/ folder
  State                 scripts/.sync-state/mattpocock/
  State for a --dest    scripts/.sync-state/mattpocock/dests/<hash>/

OVERWRITE SAFETY
  Every written file is recorded in a sha256 baseline. The first sync to the default
  destination writes the baseline to scripts/sync-baselines/mattpocock.txt. Commit
  that file, so the gate holds on every clone and worktree. SKILL.md is hashed
  without its frontmatter metadata block. A skill whose directory does not exist is
  new and syncs normally. A skill is refused and never overwritten when:
    - a local file differs from its baseline hash
    - a local file has no baseline entry
    - a baseline file is missing on disk
    - the skill directory contains a symlink
    - the skill directory exists but has no baseline entries
  There is no override flag. To take an upstream update for a refused skill, port it
  by hand, or delete the skill directory and re-run.
  Exit code: 1 if any download error happened, else 2 if anything was refused,
  else 0.

REFUSED NAMES
  grilling and grill-me are both refused outright. This repo carries the upstream
  grilling body as skills/grill-me/, a deliberate fork. Syncing grilling would add
  a duplicate directory rather than refresh it, and upstream's own grill-me is a
  stub that would overwrite the fork with a skill that does nothing here. Pull an
  upstream change by hand instead.

AFTER A SYNC
  Every newly synced skill needs its own row in the '## Skills' table in README.md.
  The script prints the new names with their descriptions so you can write the rows.

ENVIRONMENT
  GITHUB_TOKEN    Optional. Raises the GitHub API rate limit.

EXAMPLES
  bash scripts/sync-mattpocock-skills.sh --list
  bash scripts/sync-mattpocock-skills.sh <name>
  bash scripts/sync-mattpocock-skills.sh <category>/<name>
  bash scripts/sync-mattpocock-skills.sh prototype --dest ~/other-repo/skills
HELPTEXT
  exit 0
fi

# =============================================================================
# Hard refusal: the "grilling" and "grill-me" names
# =============================================================================
# skills/grill-me/ is a deliberate local fork of the upstream productivity/grilling
# body. Upstream now publishes both names, and neither one is safe to sync here:
#
#   grilling  -> this script derives the local directory from the upstream name and
#                has no rename map, so it would write a second, competing directory
#                next to skills/grill-me/ rather than refresh the fork.
#   grill-me  -> upstream's own grill-me is a stub that delegates to a /grilling
#                command that does not exist here, so syncing it by name would
#                replace our full-body fork with something that does nothing.
#
# Called twice below: once on the command line arguments (before any network call),
# and again after the state file has been read, so a poisoned state file is caught too.

refuse_grill_names() {
  local req name
  [ "${#REQUESTED[@]}" -gt 0 ] || return 0
  for req in "${REQUESTED[@]}"; do
    name="${req##*/}"
    case "$name" in
      grilling|grill-me) ;;
      *) continue ;;
    esac

    echo "ERROR: refusing to sync \"$req\"." >&2
    echo "" >&2
    echo "This repo carries the upstream grilling body as skills/grill-me/. That" >&2
    echo "directory is a deliberate fork. The body is upstream verbatim, the frontmatter" >&2
    echo "is not, and the name grill-me is the part other skills point at." >&2
    echo "" >&2

    if [ "$name" = "grilling" ]; then
      echo "Syncing grilling would create a second directory, skills/grilling/, sitting" >&2
      echo "next to skills/grill-me/ with a near-identical description competing for the" >&2
      echo "same triggers. It would not refresh the fork." >&2
    else
      echo "Upstream publishes its own grill-me, but it is a stub whose whole body is a" >&2
      echo "pointer to a /grilling session. That command does not exist here, so syncing" >&2
      echo "it would overwrite a working skill with one that does nothing." >&2
    fi

    echo "" >&2
    echo "The better-plan and prd-creator skills both declare a dependency on the name" >&2
    echo "grill-me, so either outcome breaks them." >&2
    echo "" >&2
    echo "To pull an upstream update, copy the new upstream body into" >&2
    echo "skills/grill-me/SKILL.md by hand and leave the existing frontmatter untouched." >&2
    exit 2
  done
}

refuse_grill_names

command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 is required"; exit 1; }
SHASUM=(shasum -a 256)
command -v shasum >/dev/null 2>&1 || SHASUM=(sha256sum)
command -v "${SHASUM[0]}" >/dev/null 2>&1 || { echo "ERROR: shasum/sha256sum is required"; exit 1; }

# Resolve physically (-P) so the default target is always the repo's own
# skills/ folder, regardless of how this script was invoked.
SCRIPT_DIR="$(cd -P "$(dirname "$0")" && pwd -P)"
DEFAULT_DEST="$(cd -P "$SCRIPT_DIR/../skills" && pwd -P)" || {
  echo "ERROR: cannot resolve the repo's skills/ folder"
  exit 1
}

# --dest points the sync at any other skills folder; missing dirs are created.
if [ -n "$DEST" ]; then
  if [ ! -d "$DEST" ]; then
    mkdir -p "$DEST" || { echo "ERROR: cannot create --dest: $DEST"; exit 2; }
    echo "[created] $DEST"
  fi
  LOCAL_SKILLS_DIR="$(cd -P "$DEST" && pwd -P)"
else
  LOCAL_SKILLS_DIR="$DEFAULT_DEST"
fi
[ -w "$LOCAL_SKILLS_DIR" ] || { echo "ERROR: destination is not writable: $LOCAL_SKILLS_DIR"; exit 2; }

# The synced-set is per-destination and gitignored. The default dest keeps it
# directly under STATE_BASE, any other dest under STATE_BASE/dests/<slug>/, so two
# targets never share a synced-set. The slug is a hash, not the path, so no local
# directory name is ever written into the repo.
# The overwrite baseline (MANIFEST) for the default dest is tracked in git, so the
# gate holds on a fresh clone and in every worktree. A --dest run keeps its
# baseline next to its synced-set, untracked.
# A missing MANIFEST reads as empty. It is created at the first manifest write,
# never at setup, so --list and refused-only runs leave no stray file behind.
STATE_BASE="$SCRIPT_DIR/.sync-state/mattpocock"
BASELINE_DIR="$SCRIPT_DIR/sync-baselines"
if [ "$LOCAL_SKILLS_DIR" = "$DEFAULT_DEST" ]; then
  STATE_DIR="$STATE_BASE"
  MANIFEST="$BASELINE_DIR/mattpocock.txt"
else
  DEST_SLUG="$(printf '%s' "$LOCAL_SKILLS_DIR" | "${SHASUM[@]}" | cut -c1-8)"
  STATE_DIR="$STATE_BASE/dests/$DEST_SLUG"
  MANIFEST="$STATE_DIR/manifest.txt"
fi
STATE_FILE="$STATE_DIR/synced.txt"
mkdir -p "$STATE_DIR"
[ -f "$STATE_FILE" ] || : > "$STATE_FILE"

echo "Destination: $LOCAL_SKILLS_DIR"

# =============================================================================
# Setup
# =============================================================================

TMPFILE=$(mktemp)
HEADER_FILE=$(mktemp)
STAGE_DIR=$(mktemp -d)
trap 'rm -rf "$TMPFILE" "$HEADER_FILE" "$STAGE_DIR"' EXIT

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
refused=0
errors=0
applied_skills=()
new_skills=()

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

RATE_REMAINING=$(grep -i 'x-ratelimit-remaining' "$HEADER_FILE" 2>/dev/null | tr -d '\r' | awk '{print $2}' || echo "")
if [ -n "$RATE_REMAINING" ] && [ "$RATE_REMAINING" -lt 10 ] 2>/dev/null; then
  echo "WARNING: GitHub API rate limit low ($RATE_REMAINING remaining). Set GITHUB_TOKEN for higher limits."
fi

# =============================================================================
# --list mode: print the full catalog grouped by category, then exit
# =============================================================================
# Needs the tree, so it sits after the fetch. It sits before the state-file
# fallback below so that --list still works on a fresh clone with empty state.
# The parsing rules match the resolver's exactly, so the catalog can never
# disagree with what a real sync resolves.

if [ "$LIST" -eq 1 ]; then
  python3 -c "
import sys, json
from collections import defaultdict
tree = json.load(open(sys.argv[1]))

by_cat = defaultdict(set)      # category -> set(name)
for item in tree.get('tree', []):
    if item['type'] != 'blob':
        continue
    parts = item['path'].split('/')
    if len(parts) >= 4 and parts[0] == 'skills':
        by_cat[parts[1]].add(parts[2])

cats_for = {}                  # name -> [categories]
for cat, names in by_cat.items():
    for n in names:
        cats_for.setdefault(n, []).append(cat)
dupes = {n for n, cats in cats_for.items() if len(cats) > 1}

UNSTABLE = ('deprecated', 'in-progress')
total = sum(len(s) for s in by_cat.values())
print('Available skills in %s/%s (%d across %d categories):'
      % (sys.argv[2], sys.argv[3], total, len(by_cat)))
print()
for cat in sorted(by_cat):
    flag = '   (unstable category, syncing from it prints a warning)' if cat in UNSTABLE else ''
    print('  %s/%s' % (cat, flag))
    for n in sorted(by_cat[cat]):
        tag = '   <- name also in another category, qualify as %s/%s' % (cat, n) if n in dupes else ''
        print('    %s%s' % (n, tag))
    print()
if dupes:
    print('Ambiguous names (exist in >1 category): %s' % ', '.join(sorted(dupes)))
    print('Sync these qualified as <category>/<name>.')
" "$TMPFILE" "$REPO_OWNER" "$REPO_NAME"
  exit 0
fi

# =============================================================================
# No skills named and not listing: fall back to the previously-synced set
# =============================================================================

if [ "${#REQUESTED[@]}" -eq 0 ]; then
  while IFS= read -r line; do
    line="$(echo "$line" | tr -d '[:space:]')"
    [ -n "$line" ] && REQUESTED+=("$line")
  done < "$STATE_FILE"
  if [ "${#REQUESTED[@]}" -eq 0 ]; then
    echo "ERROR: no skills named and scripts/.sync-state/mattpocock/synced.txt is empty."
    echo "Run with --list to see what upstream offers, then pass one or more names:"
    echo "  bash scripts/sync-mattpocock-skills.sh <name>"
    exit 1
  fi
  echo "No skills named — using previously-synced set: ${REQUESTED[*]}"
  echo ""
  # Re-check: a state file could carry either name from an older or hand-edited run.
  refuse_grill_names
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

# A manifest line is "<sha256>  <rel path>". The path is everything after the first
# two-space separator, so a path may hold spaces. A missing MANIFEST reads as empty.
# Helper: hash recorded in manifest for a local rel path ("<name>/<rest>")
manifest_hash() {
  [ -f "$MANIFEST" ] || return 0
  P="$1" awk '{ path = substr($0, index($0, "  ") + 2) } path == ENVIRON["P"] { print $1; exit }' "$MANIFEST"
}
# Helper: every rel path recorded in manifest for one skill
manifest_paths() {
  [ -f "$MANIFEST" ] || return 0
  S="$1" awk '{ path = substr($0, index($0, "  ") + 2) } index(path, ENVIRON["S"] "/") == 1 { print path }' "$MANIFEST"
}
# Helper: baseline hash of a file (SKILL.md is hashed without its metadata block)
file_hash() {
  python3 "$SCRIPT_DIR/sync-baseline-hash.py" "$1"
}
# Helper: replace one skill's manifest entries with the hashes of its files on disk.
# Runs per skill right after that skill is applied, so a later abort never leaves an
# applied skill without a baseline. The dir and file are created here, on first write.
write_manifest() {
  local skill="$1" lf rel
  mkdir -p "$(dirname "$MANIFEST")"
  if [ -f "$MANIFEST" ]; then
    S="$skill" awk '{ path = substr($0, index($0, "  ") + 2) } index(path, ENVIRON["S"] "/") != 1' "$MANIFEST" > "$MANIFEST.tmp"
  else
    : > "$MANIFEST.tmp"
  fi
  while IFS= read -r lf; do
    rel="${lf#"$LOCAL_SKILLS_DIR"/}"
    printf '%s  %s\n' "$(file_hash "$lf")" "$rel" >> "$MANIFEST.tmp"
  done < <(find "$LOCAL_SKILLS_DIR/$skill" -type f 2>/dev/null)
  LC_ALL=C sort -t' ' -k3 "$MANIFEST.tmp" -o "$MANIFEST.tmp"
  mv "$MANIFEST.tmp" "$MANIFEST"
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
  # Capture newness BEFORE the copy step creates the directory.
  was_new=1; [ -d "$local_skill_dir" ] && was_new=0

  # --- Detect local edits against the manifest baseline (no bypass) ---
  modified_files=()
  baseline_paths="$(manifest_paths "$skill")"
  if [ -d "$local_skill_dir" ]; then
    while IFS= read -r lf; do
      rel="${lf#"$LOCAL_SKILLS_DIR"/}"        # <name>/<rest>
      recorded="$(manifest_hash "$rel")"
      current="$(file_hash "$lf")"
      if [ -z "$recorded" ] || [ "$recorded" != "$current" ]; then
        modified_files+=("~ $rel")
      fi
    done < <(find "$local_skill_dir" -type f 2>/dev/null)
    while IFS= read -r rel; do
      [ -n "$rel" ] || continue
      [ -f "$LOCAL_SKILLS_DIR/$rel" ] || modified_files+=("- $rel")
    done <<< "$baseline_paths"
    while IFS= read -r ll; do
      modified_files+=("~ ${ll#"$LOCAL_SKILLS_DIR"/} (symlink)")
    done < <(find "$local_skill_dir" -type l 2>/dev/null)
  fi

  if [ "${#modified_files[@]}" -gt 0 ]; then
    echo "[refused: locally modified] $skill"
    for mf in "${modified_files[@]}"; do echo "    $mf"; done
    if [ -z "$baseline_paths" ]; then echo "    (no baseline recorded for this skill)"; fi
    echo "    revert $local_skill_dir/ to the baseline or delete it, then re-run."
    refused=$((refused + 1))
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
  write_manifest "$skill"
  applied_skills+=("$skill")
  # Full if-block, not a bare "[ ] && ...": as the last statement of the loop body
  # that would return non-zero whenever was_new is 0, and set -e would abort here.
  if [ "$was_new" -eq 1 ]; then
    new_skills+=("$skill")
  fi
done

# =============================================================================
# Step 4: Persist state (synced names). The manifest is written per skill, in the loop.
# =============================================================================

if [ "${#applied_skills[@]}" -gt 0 ]; then
  # synced.txt = union of prior set + newly applied, sorted unique
  {
    cat "$STATE_FILE"
    printf '%s\n' "${applied_skills[@]}"
  } | sed '/^[[:space:]]*$/d' | sort -u > "$STATE_FILE.tmp"
  mv "$STATE_FILE.tmp" "$STATE_FILE"
fi

# =============================================================================
# Step 5: Summary
# =============================================================================

echo ""
echo "=== Sync Complete ==="
echo "Destination: $LOCAL_SKILLS_DIR"
echo "Requested:  ${REQUESTED[*]}"
echo "Applied:    ${#applied_skills[@]} ($(IFS=', '; echo "${applied_skills[*]:-none}"))"
echo "Files:      $downloaded written, $removed removed"
echo "Refused:    $refused (locally modified, see above)"
echo "Errors:     $errors"

if [ "${#new_skills[@]}" -gt 0 ]; then
  echo ""
  echo "=== NEW SKILLS — REGISTER THESE in the '## Skills' table in README.md ==="
  echo "(Hand-maintained catalog, rows alphabetical. Add one row per skill:"
  echo "   [\`<name>\`](skills/<name>/SKILL.md) | What it does | Depends on | Origin"
  echo " Origin = https://github.com/mattpocock/skills"
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
elif [ "$refused" -gt 0 ]; then
  exit 2
fi

#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================

REPO_OWNER="anthropics"
REPO_NAME="knowledge-work-plugins"
BRANCH="main"

# Upstream is a PLUGIN MARKETPLACE, nested two ways:
#   <plugin>/skills/<name>/...                     (marketing, engineering, ...)
#   partner-built/<vendor>/skills/<name>/...        (apollo, brand-voice, ...)
# Local layout is flat: skills/<name>/...          (the sync flattens on download)
# The "plugin label" used to qualify a name is the dir that directly holds skills/:
#   marketing/skills/x        -> label "marketing"
#   partner-built/apollo/...  -> label "apollo"

# =============================================================================
# Args & paths
# =============================================================================

LIST=0
DEST=""
HELP=0
REQUESTED=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --list|-l)  LIST=1 ;;
    --dest)     shift; [ "$#" -gt 0 ] && [ -n "$1" ] || { echo "ERROR: --dest needs a directory"; exit 2; }; DEST="$1" ;;
    --dest=*)   DEST="${1#--dest=}"; [ -n "$DEST" ] || { echo "ERROR: --dest needs a directory"; exit 2; } ;;
    --help|-h)  HELP=1 ;;
    -*)         echo "ERROR: unknown flag: $1"; exit 2 ;;
    *)          REQUESTED+=("$1") ;;
  esac
  shift
done

if [ "$HELP" -eq 1 ]; then
  cat <<'EOF'
Sync skills from anthropics/knowledge-work-plugins into a flat skills folder.

Upstream is a plugin marketplace: each skill lives nested under a plugin dir
(marketing, engineering, ...) or under partner-built/<vendor>/. This script
flattens that nesting into a plain skills/<name>/ layout locally.

Usage:
  sync-anthropic-skills.sh [<name> ...] [--list] [--dest <dir>]

Flags:
  <name> ...       One or more skill names to sync.
  --list, -l       Print the full upstream catalog, grouped by plugin, and exit.
  --dest <dir>     Sync into <dir> instead of the default destination.
                    Also accepts --dest=<dir>.
  --help, -h       Show this help and exit.

No names given:
  Re-syncs the previously-synced set recorded in the state file. Errors if
  that set is empty (nothing has been synced here yet).

Ambiguous names:
  A name that exists in more than one plugin must be qualified as
  <plugin>/<name>, e.g. marketing/standup.

Default destination:
  This repo's skills/ folder.

State file location:
  scripts/.sync-state/anthropic/ (default destination)
  scripts/.sync-state/anthropic/dests/<hash>/ (for a --dest run)

Rate limits:
  Set GITHUB_TOKEN in the environment for higher GitHub API rate limits.

Overwrite safety:
  Every written file is recorded in a sha256 baseline. The first sync to the
  default destination writes the baseline to
  scripts/sync-baselines/anthropic.txt. Commit that file, so the gate holds on
  every clone and worktree. SKILL.md is hashed without its frontmatter metadata
  block. A skill whose directory does not exist is new and syncs normally. A
  skill is refused and never overwritten when:
    - a local file differs from its baseline hash
    - a local file has no baseline entry
    - a baseline file is missing on disk
    - the skill directory contains a symlink
    - the skill directory exists but has no baseline entries
  There is no override flag. To take an upstream update for a refused skill,
  port it by hand, or delete the skill directory and re-run.
  Exit code: 1 if any download error happened, else 2 if anything was refused,
  else 0.

New skills:
  Each NEW skill synced into this repo needs a row added to the '## Skills'
  table in README.md.

Examples:
  sync-anthropic-skills.sh --list
  sync-anthropic-skills.sh standup incident-response
  sync-anthropic-skills.sh marketing/standup
  sync-anthropic-skills.sh --dest ../other-project/skills incident-response
EOF
  exit 0
fi

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
    echo "[created] $DEST" >&2
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
STATE_BASE="$SCRIPT_DIR/.sync-state/anthropic"
BASELINE_DIR="$SCRIPT_DIR/sync-baselines"
if [ "$LOCAL_SKILLS_DIR" = "$DEFAULT_DEST" ]; then
  STATE_DIR="$STATE_BASE"
  MANIFEST="$BASELINE_DIR/anthropic.txt"
else
  DEST_SLUG="$(printf '%s' "$LOCAL_SKILLS_DIR" | "${SHASUM[@]}" | cut -c1-8)"
  STATE_DIR="$STATE_BASE/dests/$DEST_SLUG"
  MANIFEST="$STATE_DIR/manifest.txt"
fi
STATE_FILE="$STATE_DIR/synced.txt"
mkdir -p "$STATE_DIR"
[ -f "$STATE_FILE" ] || : > "$STATE_FILE"

echo "Destination: $LOCAL_SKILLS_DIR" >&2

# =============================================================================
# Setup — fetch the upstream file tree once
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

echo "Fetching file tree from $REPO_OWNER/$REPO_NAME@$BRANCH..." >&2
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
  echo "WARNING: GitHub API rate limit low ($RATE_REMAINING remaining). Set GITHUB_TOKEN for higher limits." >&2
fi

# =============================================================================
# --list mode — print the full catalog grouped by plugin, then exit
# =============================================================================

if [ "$LIST" -eq 1 ]; then
  python3 -c "
import sys, json
from collections import defaultdict
tree = json.load(open(sys.argv[1]))
by_plugin = defaultdict(set)   # label -> set(name)
for item in tree.get('tree', []):
    if item['type'] != 'blob':
        continue
    parts = item['path'].split('/')
    if parts[0] == 'partner-built' and len(parts) >= 5 and parts[2] == 'skills':
        by_plugin[parts[1]].add(parts[3])
    elif len(parts) >= 4 and parts[1] == 'skills':
        by_plugin[parts[0]].add(parts[2])
names = set()
for s in by_plugin.values():
    names |= s
dupes = set()
seen = {}
for label, s in by_plugin.items():
    for n in s:
        seen.setdefault(n, []).append(label)
dupes = {n for n, labs in seen.items() if len(labs) > 1}
total = sum(len(s) for s in by_plugin.values())
print('Available skills in %s/%s (%d across %d plugins):' % (sys.argv[2], sys.argv[3], total, len(by_plugin)))
print()
for label in sorted(by_plugin):
    print('  %s/' % label)
    for n in sorted(by_plugin[label]):
        tag = '   <- name also in another plugin, qualify as %s/%s' % (label, n) if n in dupes else ''
        print('    %s%s' % (n, tag))
    print()
if dupes:
    print('Ambiguous names (exist in >1 plugin): %s' % ', '.join(sorted(dupes)))
    print('Sync these qualified as <plugin>/<name>.')
" "$TMPFILE" "$REPO_OWNER" "$REPO_NAME"
  exit 0
fi

# =============================================================================
# No skills named and not listing — fall back to previously-synced set
# =============================================================================

if [ "${#REQUESTED[@]}" -eq 0 ]; then
  while IFS= read -r line; do
    line="$(echo "$line" | tr -d '[:space:]')"
    [ -n "$line" ] && REQUESTED+=("$line")
  done < "$STATE_FILE"
  if [ "${#REQUESTED[@]}" -eq 0 ]; then
    echo "ERROR: no skills named and scripts/.sync-state/anthropic/synced.txt is empty."
    echo "Run with --list to see what's available, then pass one or more names:"
    echo "  bash scripts/sync-anthropic-skills.sh standup incident-response"
    exit 1
  fi
  echo "No skills named — re-syncing previously-synced set: ${REQUESTED[*]}" >&2
  echo "" >&2
fi

# =============================================================================
# Resolve each requested skill to its plugin label and remote blob paths
# =============================================================================
# Output lines, one per remote blob:  <name>\t<remote_path>

RESOLVED=$(python3 -c "
import sys, json
from collections import defaultdict
tree = json.load(open(sys.argv[1]))
requested = sys.argv[2:]

by_skill = defaultdict(list)   # (label, name) -> [full paths]
labels_for = defaultdict(set)  # name -> set(label)
for item in tree.get('tree', []):
    if item['type'] != 'blob':
        continue
    parts = item['path'].split('/')
    if parts[0] == 'partner-built' and len(parts) >= 5 and parts[2] == 'skills':
        label, name = parts[1], parts[3]
    elif len(parts) >= 4 and parts[1] == 'skills':
        label, name = parts[0], parts[2]
    else:
        continue
    by_skill[(label, name)].append(item['path'])
    labels_for[name].add(label)

def available():
    return '\n'.join('  %s/%s' % (l, n) for (l, n) in sorted(by_skill.keys()))

errors = []
for req in requested:
    if '/' in req:
        label, name = req.rsplit('/', 1)
        key = (label, name)
        if key not in by_skill:
            errors.append('No upstream skill \"%s\". Run --list to see all. Nearest matches:\n%s'
                          % (req, '\n'.join('  %s/%s' % (l, n) for (l, n) in sorted(by_skill) if n == name) or '  (none)'))
            continue
        chosen = [key]
    else:
        name = req
        labs = sorted(labels_for.get(name, []))
        if not labs:
            errors.append('No upstream skill named \"%s\". Run --list to see all.' % name)
            continue
        if len(labs) > 1:
            errors.append('Skill \"%s\" exists in multiple plugins: %s. Re-run qualified, e.g. %s/%s'
                          % (name, ', '.join(labs), labs[0], name))
            continue
        chosen = [(labs[0], name)]
    for (label, name) in chosen:
        for path in sorted(by_skill[(label, name)]):
            print('%s\t%s' % (name, path))

if errors:
    sys.stderr.write('\n'.join(errors) + '\n')
    sys.exit(3)
" "$TMPFILE" "${REQUESTED[@]}") || { echo ""; echo "ERROR: skill resolution failed (see above)"; exit 1; }

if [ -z "$RESOLVED" ]; then
  echo "ERROR: nothing resolved to sync."
  exit 1
fi

TARGET_NAMES=$(echo "$RESOLVED" | awk -F'\t' '{print $1}' | sort -u)
echo "Resolved $(echo "$TARGET_NAMES" | wc -l | tr -d ' ') skill(s): $(echo "$TARGET_NAMES" | paste -sd' ' -)" >&2
echo "" >&2

RAW_BASE="https://raw.githubusercontent.com/$REPO_OWNER/$REPO_NAME/$BRANCH"

# =============================================================================
# For each skill — stage upstream, check for local edits, then apply
# =============================================================================

# A manifest line is "<sha256>  <rel path>". The path is everything after the first
# two-space separator, so a path may hold spaces. A missing MANIFEST reads as empty.
manifest_hash() {
  [ -f "$MANIFEST" ] || return 0
  P="$1" awk '{ path = substr($0, index($0, "  ") + 2) } path == ENVIRON["P"] { print $1; exit }' "$MANIFEST"
}
manifest_paths() {
  [ -f "$MANIFEST" ] || return 0
  S="$1" awk '{ path = substr($0, index($0, "  ") + 2) } index(path, ENVIRON["S"] "/") == 1 { print path }' "$MANIFEST"
}
file_hash() { python3 "$SCRIPT_DIR/sync-baseline-hash.py" "$1"; }
# Replace one skill's manifest entries with the hashes of its files on disk.
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

downloaded=0; removed=0; refused=0; errors=0
applied_skills=(); new_skills=(); ctx_reports=()

for skill in $TARGET_NAMES; do
  skill_remote=$(echo "$RESOLVED" | awk -F'\t' -v s="$skill" '$1==s {print $2}')

  # --- Stage all upstream files: <...>/skills/<name>/<rest> -> STAGE_DIR/<name>/<rest> ---
  stage_ok=1
  while IFS= read -r remote_path; do
    rest="${remote_path##*/skills/}"          # strip "<...>/skills/" -> "<name>/<rest>"
    stage_path="$STAGE_DIR/$rest"
    mkdir -p "$(dirname "$stage_path")"
    if ! curl "${CURL_OPTS[@]}" -o "$stage_path" "$RAW_BASE/$remote_path" 2>/dev/null; then
      echo "[ERROR]   Failed to download: $remote_path"
      errors=$((errors + 1)); stage_ok=0
    fi
  done <<< "$skill_remote"
  [ "$stage_ok" -eq 1 ] || { echo "[skipped: download error] $skill"; continue; }

  # --- Adapt the staged copy to this repo (drop pointers to things absent here) ---
  # Must run BEFORE the modified-check and copy below: the manifest records the hash
  # of what we WRITE, so transforming first keeps the baseline self-consistent and
  # re-sync idempotent. See the overwrite-safety notes under --help.
  ctx_out=$(python3 "$SCRIPT_DIR/sync-anthropic-contextualize.py" "$STAGE_DIR/$skill" "$skill" 2>/dev/null || true)

  local_skill_dir="$LOCAL_SKILLS_DIR/$skill"
  was_new=1; [ -d "$local_skill_dir" ] && was_new=0

  # --- Detect local edits against the manifest baseline (no bypass) ---
  modified_files=()
  baseline_paths="$(manifest_paths "$skill")"
  if [ -d "$local_skill_dir" ]; then
    while IFS= read -r lf; do
      rel="${lf#"$LOCAL_SKILLS_DIR"/}"
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
    echo "    (locally edited, or a native skill of the same name)"
    echo "    revert $local_skill_dir/ to the baseline or delete it, then re-run."
    refused=$((refused + 1)); continue
  fi

  # --- Apply: clean removed files, then copy staged files into place ---
  staged_rel=$(cd "$STAGE_DIR/$skill" 2>/dev/null && find . -type f | sed 's|^\./||' || true)

  if [ -d "$local_skill_dir" ]; then
    while IFS= read -r lf; do
      rel="${lf#"$local_skill_dir"/}"
      if ! echo "$staged_rel" | grep -qxF "$rel"; then
        rm "$lf"; echo "[removed] $skill/$rel"; removed=$((removed + 1))
      fi
    done < <(find "$local_skill_dir" -type f 2>/dev/null)
  fi

  while IFS= read -r rel; do
    [ -z "$rel" ] && continue
    dest="$local_skill_dir/$rel"
    mkdir -p "$(dirname "$dest")"
    cp "$STAGE_DIR/$skill/$rel" "$dest"
    echo "[synced]  $skill/$rel"; downloaded=$((downloaded + 1))
  done <<< "$staged_rel"

  find "$local_skill_dir" -type d -empty -delete 2>/dev/null || true
  write_manifest "$skill"
  applied_skills+=("$skill")
  [ "$was_new" -eq 1 ] && new_skills+=("$skill")
  if [ -n "$ctx_out" ]; then ctx_reports+=("$ctx_out"); fi
done

# =============================================================================
# Persist state (synced names). The manifest is written per skill, in the loop.
# =============================================================================

if [ "${#applied_skills[@]}" -gt 0 ]; then
  { cat "$STATE_FILE"; printf '%s\n' "${applied_skills[@]}"; } \
    | sed '/^[[:space:]]*$/d' | sort -u > "$STATE_FILE.tmp"
  mv "$STATE_FILE.tmp" "$STATE_FILE"
fi

# =============================================================================
# Lint synced descriptions (warn only — never mutate upstream content)
# =============================================================================
# Copilot CLI rejects ": " (colon+space) in a SKILL.md description (YAML plain-scalar
# terminator), and descriptions should stay <=1024 chars. Warn so the agent can fix.

if [ "${#applied_skills[@]}" -gt 0 ]; then
  python3 -c "
import sys, re, os
base = sys.argv[1]
issues = []
for skill in sys.argv[2:]:
    p = os.path.join(base, skill, 'SKILL.md')
    if not os.path.isfile(p):
        continue
    text = open(p, encoding='utf-8', errors='replace').read()
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if not m:
        issues.append('%s: no YAML frontmatter found' % skill); continue
    fm = m.group(1)
    dm = re.search(r'^description:\s*(.*?)(?=^\S|\Z)', fm + '\n', re.DOTALL | re.MULTILINE)
    desc = dm.group(1).strip() if dm else ''
    if not desc:
        issues.append('%s: empty/missing description' % skill); continue
    is_block = desc[:1] in ('>', '|')
    if ': ' in desc and not is_block:
        issues.append('%s: description contains \": \" (breaks Copilot CLI) — rewrite with \" — \" or a >- block scalar' % skill)
    plain = re.sub(r'\s+', ' ', desc.lstrip('>|-').strip())
    if len(plain) > 1024:
        issues.append('%s: description is %d chars (>1024) — trim it' % (skill, len(plain)))
if issues:
    sys.stderr.write('\nDESCRIPTION LINT WARNINGS:\n')
    for i in issues:
        sys.stderr.write('  ! ' + i + '\n')
" "$LOCAL_SKILLS_DIR" "${applied_skills[@]}"
fi

# =============================================================================
# Summary
# =============================================================================

if [ "${#ctx_reports[@]}" -gt 0 ]; then
  echo ""
  echo "=== CONTEXT FIXES APPLIED (staged copy adapted to this repo) ==="
  echo "(Upstream is a plugin marketplace; flattening leaves its pointers dangling.)"
  printf '%s\n' "${ctx_reports[@]}"
fi

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
  echo " Origin = https://github.com/anthropics/knowledge-work-plugins"
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

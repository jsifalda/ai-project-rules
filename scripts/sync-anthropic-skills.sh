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

FORCE="${FORCE:-0}"
LIST=0
DEST=""
HELP=0
REQUESTED=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --force|-f) FORCE=1 ;;
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
  sync-anthropic-skills.sh [<name> ...] [--list] [--force] [--dest <dir>]

Flags:
  <name> ...       One or more skill names to sync.
  --list, -l       Print the full upstream catalog, grouped by plugin, and exit.
  --force, -f      Overwrite local edits instead of skipping them.
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
  Local edits are detected against a sha256 baseline recorded at sync time,
  and are skipped with a warning until you pass --force. On a fresh clone
  there is no baseline yet, so every existing skill reports as locally
  modified. That is expected. --force is the correct response.

New skills:
  Each NEW skill synced into this repo needs a row added to the '## Skills'
  table in README.md.

Examples:
  sync-anthropic-skills.sh --list
  sync-anthropic-skills.sh standup incident-response
  sync-anthropic-skills.sh marketing/standup --force
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

# State is per-destination, gitignored. The default dest keeps its baseline
# directly under STATE_BASE; any other dest gets its own baseline under
# STATE_BASE/dests/<slug>/, so two targets never share a synced-set or an
# overwrite baseline. The slug is a hash, not the path, so no local directory
# name is ever written into the repo.
STATE_BASE="$SCRIPT_DIR/.sync-state/anthropic"
if [ "$LOCAL_SKILLS_DIR" = "$DEFAULT_DEST" ]; then
  STATE_DIR="$STATE_BASE"
else
  DEST_SLUG="$(printf '%s' "$LOCAL_SKILLS_DIR" | "${SHASUM[@]}" | cut -c1-8)"
  STATE_DIR="$STATE_BASE/dests/$DEST_SLUG"
fi
STATE_FILE="$STATE_DIR/synced.txt"
MANIFEST="$STATE_DIR/manifest.txt"
mkdir -p "$STATE_DIR"
[ -f "$STATE_FILE" ] || : > "$STATE_FILE"
[ -f "$MANIFEST" ] || : > "$MANIFEST"

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

manifest_hash() { awk -v p="$1" '$2==p {print $1; exit}' "$MANIFEST"; }
file_hash() { "${SHASUM[@]}" "$1" | awk '{print $1}'; }

downloaded=0; removed=0; skipped=0; errors=0
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
  [ -n "$ctx_out" ] && ctx_reports+=("$ctx_out")

  local_skill_dir="$LOCAL_SKILLS_DIR/$skill"
  was_new=1; [ -d "$local_skill_dir" ] && was_new=0

  # --- Detect local edits against the manifest baseline ---
  modified_files=()
  if [ -d "$local_skill_dir" ] && [ "$FORCE" -ne 1 ]; then
    while IFS= read -r lf; do
      rel="${lf#"$LOCAL_SKILLS_DIR"/}"
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
    echo "    (locally edited, or a native skill of the same name — re-run with --force to overwrite)"
    skipped=$((skipped + 1)); continue
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
  applied_skills+=("$skill")
  [ "$was_new" -eq 1 ] && new_skills+=("$skill")
done

# =============================================================================
# Persist state (synced names) and manifest (per-file hashes)
# =============================================================================

if [ "${#applied_skills[@]}" -gt 0 ]; then
  { cat "$STATE_FILE"; printf '%s\n' "${applied_skills[@]}"; } \
    | sed '/^[[:space:]]*$/d' | sort -u > "$STATE_FILE.tmp"
  mv "$STATE_FILE.tmp" "$STATE_FILE"

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
echo "Skipped:    $skipped (locally modified — use --force)"
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
fi

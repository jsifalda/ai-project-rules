---
name: ship-pr
description: RESTRICTED-INVOCATION skill — do NOT auto-trigger. The only entry points are the user typing the literal slash command `/ship-pr`, or the ship step of a skill declaring `ship-pr` as a dependency (such as the final stage of a `/better-plan` run). Phrasing like "ship this", "create a PR", "send this for review", or any paraphrase are ANTI-TRIGGERS — they MUST NOT load this skill; use ordinary commit + push tools instead and, if helpful, offer `/ship-pr`. When invoked through either entry point — runs an end-to-end git ship workflow from a dirty working tree to an open PR (GitHub) or MR (GitLab), self-assigned to you. Auto-detects provider via `git remote` and derives branch name, commit message, and PR title/body from the change and repo conventions, no per-step prompts. Do NOT use for committing without opening a PR, reviewing or editing existing PRs, force-pushing or rewriting history, cutting releases, or anything touching tags or changelogs.
---

# Ship PR

## Invocation (check this first)

These are the only entry points allowed:

1. The user types the literal slash command `/ship-pr`.
2. A skill that declares `ship-pr` as a dependency reaches its ship step — currently
   `better-plan` (Stage 4) and `loop-todos` (its per-entry PR step).

Anything else is an anti-trigger. None of these load this skill — "ship this", "ship these
changes", "create a PR", "open a PR", "open an MR", "push and create PR", "send this for
review", "push this up", or any other paraphrase. Commit and push with ordinary git tools
instead, and offer `/ship-pr` if it seems useful. This skill opens a real PR against a real
remote with no per-step confirmation, so a wrong trigger is outward-facing and awkward to
walk back.

This rule is prompt-enforced, not harness-enforced. This skill deliberately carries no
`disable-model-invocation` flag, because that flag is a binary block with no per-caller
allowlist — it removes the skill from the Skill tool entirely, so a dependent skill's ship
step fails with `cannot be used with Skill tool`. Do not re-add it to "tighten" invocation
without first removing every dependent skill's ship step.

Go from a dirty working tree to an open PR/MR in one pass. Auto-derive everything from the change and the repo's own conventions. No per-step confirmations.

The skill runs the four phases in strict order. The hot path costs **three tool calls**: one for Phase 1, one for Phase 3a, one for Phase 3b. Phase 2 is reasoning, and Phase 4 is text. Keep each phase in one bash block. Do not split a block into per-command calls — each extra call is a full model round-trip, and the round-trips, not the commands, are what make this skill slow.

Abort on the first failure with a one-line reason — do not retry with `--no-verify`, `--force`, or any other bypass flag. (Sole exception: on GitHub, a push denied for lack of write access triggers the fork fallback in Phase 3b — an alternate destination, not a bypass.)

## Phase 1 — Preflight, provider, and conventions

Run this one block. It aborts with a single reason, or it prints one `key=value` header plus labelled sections. Read the output; do not re-run any part of it as a separate call.

```bash
# test the printed value, not the exit status — a bare repo exits 0 and prints "false"
[ "$(git rev-parse --is-inside-work-tree 2>/dev/null)" = "true" ] || { echo "ABORT: not a git repository"; exit 1; }

BRANCH=$(git rev-parse --abbrev-ref HEAD)
[ "$BRANCH" != "HEAD" ] || { echo "ABORT: detached HEAD — checkout a branch first"; exit 1; }

# resolve state files via git-path — inside a linked worktree .git is a file, not a dir.
# Test the rebase-merge / rebase-apply DIRECTORIES, not REBASE_HEAD. A rebase paused at
# a `break` or `edit` step has no REBASE_HEAD (no commit is being applied), so a
# REBASE_HEAD-only check reports "clean" mid-rebase. Edit a file during that pause and
# the run would branch, commit and push on top of an unfinished rebase.
for PAIR in rebase-merge:rebase rebase-apply:rebase MERGE_HEAD:merge \
            CHERRY_PICK_HEAD:cherry-pick REVERT_HEAD:revert sequencer:sequencer; do
  if [ -e "$(git rev-parse --git-path "${PAIR%%:*}")" ]; then
    echo "ABORT: ${PAIR##*:} in progress — finish or abort it first"; exit 1
  fi
done

# -uall expands an untracked directory into its individual files. Without it a new
# directory collapses to a single `?? dir/` line — the secret filter never sees the
# files inside, and staging that one path would add the whole tree recursively.
# core.quotePath=false stops git C-escaping non-ASCII names (café.md, not "caf\303\251.md").
# A name containing a space or a quote is STILL wrapped in double quotes — see Phase 3a.
PORCELAIN=$(git -c core.quotePath=false status --porcelain -uall) \
  || { echo "ABORT: git status failed"; exit 1; }
[ -n "$PORCELAIN" ] || { echo "ABORT: no changes to commit"; exit 1; }

ORIGIN_URL=$(git remote get-url origin 2>/dev/null) || { echo "ABORT: no origin remote configured"; exit 1; }

# Reduce a remote URL to host + path, so the two transports for one repo compare equal:
#   https://github.com/acme/widget.git  ->  github.com/acme/widget
#   git@github.com:acme/widget.git      ->  github.com/acme/widget
norm_remote() {
  printf '%s' "$1" | sed -E 's#^[a-zA-Z0-9+.-]+://##; s#^[^/@]*@##; s#:#/#; s#/+$##; s#\.git$##'
}

# `get-url` returns the FETCH url. If a repo really pushes to a DIFFERENT repo, the branch
# lands on one and the PR opens on the other. Compare host+path, not the raw strings —
# "fetch over HTTPS, push over SSH, same repo" is a normal setup and must not abort.
PUSH_URL=$(git remote get-url --push origin 2>/dev/null) || PUSH_URL="$ORIGIN_URL"
if [ "$(norm_remote "$PUSH_URL")" != "$(norm_remote "$ORIGIN_URL")" ]; then
  echo "ABORT: origin fetch and push point at different repos — push goes to $PUSH_URL"; exit 1
fi
HOST=$(printf '%s' "$ORIGIN_URL" | sed -E 's#^[a-zA-Z0-9+.-]+://##; s#^[^/@]*@##; s#[:/].*$##')
case "$HOST" in
  github.com|*.github.*) PROVIDER=gh ;;
  gitlab.com|*gitlab*)   PROVIDER=glab ;;
  *) echo "ABORT: unsupported remote host: $HOST"; exit 1 ;;
esac

# presence only — a shell builtin, ~0ms, no network
command -v "$PROVIDER" >/dev/null 2>&1 || { echo "ABORT: $PROVIDER not installed"; exit 1; }

DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null | sed 's|^origin/||')
if [ -z "$DEFAULT_BRANCH" ]; then   # network fallback only when the local ref is unset
  if [ "$PROVIDER" = gh ]; then
    DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null)
  else
    DEFAULT_BRANCH=$(glab repo view -F json 2>/dev/null | jq -r '.default_branch // empty')
  fi
fi

echo "branch=$BRANCH"
echo "provider=$PROVIDER"
echo "host=$HOST"
echo "default_branch=$DEFAULT_BRANCH"
echo "user_name=$(git config user.name)"

echo "--- status ---";   printf '%s\n' "$PORCELAIN"
echo "--- log ---";      git log --pretty=%s -20
echo "--- branches ---"; git branch -a --sort=-committerdate | head -12

# one grep pass over every convention file — never one read per file.
# Deduplicate by content first: AGENTS.md is usually a symlink to CLAUDE.md,
# and a grep over both prints every rule twice.
echo "--- conventions ---"
set --
SEEN=""
for F in AGENTS.md CLAUDE.md .claude/CLAUDE.md CONTRIBUTING.md \
         .github/PULL_REQUEST_TEMPLATE.md .github/pull_request_template.md \
         .gitlab/merge_request_templates/*; do
  [ -f "$F" ] || continue
  K=$(cksum < "$F" | tr ' ' '-')   # keep the CRC/size separator — "12 345" must not equal "123 45"
  case " $SEEN " in *" $K "*) continue ;; esac
  SEEN="$SEEN $K"
  set -- "$@" "$F"
done
[ "$#" -gt 0 ] && grep -HinE 'branch|commit|conventional|pull request|merge request|ticket|prefix|sign-?off' "$@" 2>/dev/null | head -40   # -H keeps the filename even for a single file

echo "--- pr template ---"
for T in .github/PULL_REQUEST_TEMPLATE.md .github/pull_request_template.md .gitlab/merge_request_templates/*; do
  if [ -f "$T" ]; then
    echo "== $T"; head -c 4000 "$T"; echo
    [ "$(wc -c < "$T")" -gt 4000 ] && echo "== (truncated at 4000 bytes)"
    break
  fi
done

exit 0   # every real abort above exited 1 already — never leak a stray status
```

Read the result like this:

- Any `ABORT:` line ends the run. Print that reason and stop.
- `default_branch=` empty — ask the user once for the default branch, then continue.
- `default_branch=` is read from the local `refs/remotes/origin/HEAD`, which is set at clone time and never refreshed here. A refresh is a network call on every run, which is the cost this skill exists to avoid. If the remote renamed its default branch, that local ref goes stale and the PR targets the wrong base. The symptom is loud — `gh pr create` rejects a base that no longer exists — and `git remote set-head origin -a` repairs it. Run that once if you see it.
- `--- status ---` is the file inventory for Phase 2 and Phase 3a. Do not fetch it again.
- `--- conventions ---` and `--- pr template ---` carry the repo's own rules. These files often
  state explicit branch, commit, and PR rules. Honor them when present — they beat every default below.
- If a PR/MR template printed, the template **is** the body. Fill it in instead of the default `## Summary`.

Infer style from the log and branch sections. Look for these patterns:

- Conventional commits: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, `test:`, `perf:`, with optional `(scope)`
- Branch prefixes: `feature/`, `fix/`, `feat/`, `chore/`, `<username>/`, or `<TICKET-ID>-`
- Ticket-ID embedding: `[ABC-123]`, `(ABC-123)`, or `ABC-123` in the subject

If signals conflict or are absent, fall back to:

- Commit: conventional commits (`type: subject` or `type(scope): subject`)
- Branch: `<type>/<kebab-slug>`

Do **not** look up the upstream repo slug here. The fork fallback in Phase 3b is the only consumer, that path is almost never taken, and the lookup is a network call. Phase 3b gets it lazily.

## Phase 2 — Derive branch name, commit message, PR title and body

First answer one question:

```
Who authored the working-tree changes?
  I did, in this session   -> write the message from what you did.
                              NO diff read at all. The Phase 1 porcelain
                              output is the file inventory.

  Subagents I dispatched   -> git diff HEAD --stat
                              Reconcile it against the task summaries you
                              hold. Read the full git diff HEAD ONLY for a
                              file the summaries did not lead you to expect.

  Someone else / earlier   -> git diff HEAD --stat
  session                     then git diff HEAD if the stat leaves the
                              commit type ambiguous
```

The reason: in most `/ship-pr` runs you just made the changes. You know the type, the scope, and the why better than any diff reader. To re-read the diff is to re-derive what is already in context, and it costs a large block of tokens.

The middle branch exists because a delegating run is different. When work was routed to subagents, you hold their task summaries, not their diffs. A subagent can touch a file its summary never mentions. `--stat` is one line per file and it costs almost nothing, so read it and check the file list against what you expect. Write the message from your own knowledge; use the stat to catch what the summaries left out.

This does not weaken the secret scan in Phase 3a. That scan tests path globs and file size only. It never reads diff content.

Decide:

- **Type** — feat / fix / refactor / docs / chore / test / perf, based on what the change actually does (new behavior vs. corrected behavior vs. internal cleanup vs. docs-only)
- **Scope** — optional, only if the change is clearly scoped to one module/area visible in the changed paths
- **Subject** — imperative, ≤72 chars, no trailing period
- **Branch name** — matches detected convention; topic portion ≤50 chars, kebab-case. Example: `feat/parse-multipart-upload`, `jsmith/fix-login-redirect`
- **Commit body** — optional, why/impact-focused: add only when the reason isn't obvious from subject + diff; 1-2 short bullets max, no file-by-file inventory. Omit for single-file one-liners. On a single-commit MR/PR the body becomes the description verbatim — keep it clean.
- **PR title** — same as the commit subject for single-commit PRs.
- **PR body** — a `## Summary` section only:

  ```markdown
  ## Summary
  - <1–3 bullets covering what and why>
  ```

  Add a `## Test plan` section ONLY if the user explicitly asks for one. Not by default.
- **Assignee** — the new PR/MR is self-assigned to the authenticated CLI user (you). On both providers this is a dedicated post-create step; the result is read back and reported, never fired blind. Best-effort, never blocks the ship — see Phase 3b.

### Attribution policy (hard rule)

NEVER include any of the following in commit messages, PR titles, PR bodies, or branch names:

- `Co-Authored-By: Claude` (any model, any email)
- `🤖 Generated with [Claude Code]` or any variant
- "Generated by Claude" / "Powered by Anthropic" / "AI-generated" footers
- Any trailer or badge referencing Claude, Anthropic, Sonnet, Opus, Haiku, or AI assistance

The commit message ends after the descriptive body. The PR body ends after the `## Summary` section. No trailing block.

## Phase 3 — Execute

Two bash blocks: 3a branches, stages, commits and pushes; 3b opens the PR/MR and reads the assignee back. Stop on the first failure — do NOT retry with `--no-verify`, `--no-gpg-sign`, `--force`, or `--amend`. The sole exception is a push denied for lack of write access on GitHub, which triggers the fork fallback in 3b (an alternate destination, not a bypass).

### 3a. Branch, stage, commit, push — one block

Before you write the block, filter the Phase 1 porcelain list yourself. That list comes from `git status --porcelain -uall`, which expands an untracked directory into its individual files. One exception: a submodule whose pointer moved appears as a bare directory (` M vendor/lib`). `-uall` does not expand submodules, and it does not need to — `git add` stages one gitlink for it, not a tree. Drop every path that matches a secret pattern:

- `.env*` except `.env.example` and `.env.sample`
- `*.pem`, `*.key`, `*.p12`, `*.pfx`
- `id_rsa*`, `id_ed25519*`, `id_ecdsa*`
- `credentials*`, `*credentials.json`, `*service-account*.json`
- Files larger than 10 MB

If a suspicious file is the only change, abort and ask the user explicitly.

Then put the surviving paths, one per line, into the `PATHS` heredoc below. Carry the literal list for two reasons. It keeps staging explicit-path, so the never-`git add -A` rule holds inside a single call. And it avoids parsing `--porcelain -z` in shell, which is fragile for renames (`R  old -> new` is two paths in one record).

Write each path as the **bare path**, not the porcelain line. Three rules:

1. **Drop the first 3 characters.** A porcelain line is 2 status characters plus a space, then the path. `git add -- " M src/app.ts"` fails; `git add -- "src/app.ts"` works.
2. **Unwrap a quoted path.** Phase 1 sets `core.quotePath=false`, so a non-ASCII name arrives bare. A name holding a space, a quote, or a control character is still wrapped in double quotes with backslash escapes — `"two words.md"`. Strip the quotes and unescape before writing the line. Verified: `git add -- '"two words.md"'` fails with `pathspec … did not match any files`, and under `set -e` that kills the block after the checkout.
3. **A rename is two paths.** `R  old -> new` needs both `old` and `new` on their own lines.

```bash
set -e

DEFAULT_BRANCH="<default-branch>"
WANTED="<derived-branch>"

# Both must be non-empty. An empty DEFAULT_BRANCH makes the test below always false,
# so the run would stay on the default branch and push a commit straight to it.
[ -n "$DEFAULT_BRANCH" ] || { echo "ABORT: default branch unknown — ask the user, then re-run"; exit 1; }
[ -n "$WANTED" ] || { echo "ABORT: no branch name derived"; exit 1; }

CURRENT=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT" = "$DEFAULT_BRANCH" ]; then
  CAND="$WANTED"; N=2
  while git show-ref --verify --quiet "refs/heads/$CAND" \
     || git ls-remote --exit-code --heads origin "$CAND" >/dev/null 2>&1; do
    CAND="$WANTED-$N"; N=$((N+1))
  done
  git checkout -b "$CAND"
else
  CAND="$CURRENT"   # already on a feature branch — append to it
fi
echo "branch=$CAND"   # echo BEFORE anything that can fail — see the note below

# Never commit to the default branch. The test above is the only thing standing between
# this run and that hard rule, so assert the result rather than trusting it.
[ "$CAND" != "$DEFAULT_BRANCH" ] || { echo "ABORT: refusing to commit to the default branch"; exit 1; }

# Start from a clean index. An earlier aborted run can leave paths staged, and the commit
# below would sweep them in — including a path the secret filter dropped on this pass.
git reset -q

while IFS= read -r P; do
  [ -n "$P" ] || continue
  # An added-then-deleted path (porcelain `AD`) is gone after the reset above and there is
  # nothing left to commit for it. Skip it rather than letting `git add` fail the block.
  if [ ! -e "$P" ] && ! git cat-file -e "HEAD:$P" 2>/dev/null; then
    echo "skip=$P (added then deleted — nothing to commit)"; continue
  fi
  # An UNtracked directory would stage its whole tree recursively and skip both guards
  # below. A TRACKED directory is a submodule gitlink — `git add` stages one pointer, not
  # a tree, so it is safe and must be allowed or no submodule repo could ever ship.
  # -L first: a symlink TO a directory is safe too; `git add` stages the link.
  case "$P" in */) echo "ABORT: untracked directory, not a file: $P"; exit 1 ;; esac
  if [ -d "$P" ] && [ ! -L "$P" ] && ! git ls-files --error-unmatch -- "$P" >/dev/null 2>&1; then
    echo "ABORT: untracked directory, not a file: $P"; exit 1
  fi
  if [ -f "$P" ] && [ -n "$(find "$P" -size +10M)" ]; then
    echo "ABORT: file larger than 10 MB: $P"; exit 1
  fi
  git add -- "$P"
done <<'PATHS'
<one path per line, secret-filtered>
PATHS

git commit -m "$(cat <<'MSG'
<subject>

<optional body bullets>
MSG
)"
echo "commit=$(git rev-parse --short HEAD)"   # echo BEFORE the push, for the same reason

git push -u origin "$CAND"
```

Rules for this block:

- `set -e` is what makes it safe to bundle. A failed hook stops the block before the push.
- Never redirect stderr in this block. A pre-commit hook's error must reach the user verbatim.
- No `--no-verify`. If a pre-commit hook fails, fix the underlying issue (or surface it to the user) — do not bypass.
- If the commit fails, do not run `--amend` to "retry". Create a NEW commit after fixing.
- Never `--force` or `--force-with-lease` on the push.
- Echo `branch=` and `commit=` **before** the step that can fail, never after. `set -e` stops the block on a failed push, and a push denied for lack of write access is exactly what starts the fork fallback. That fallback needs the real branch name — which may carry a `-2` / `-3` suffix — so the name must already be on stdout when the push dies.
- Never hand an **untracked** directory to the staging loop. `git add -- "dir/"` stages the whole tree recursively, and neither the secret filter nor the size guard can see the files inside. Phase 1 uses `git status --porcelain -uall`, so untracked files are listed individually and this case should not arise; the guard in the loop is the backstop. A **tracked** directory is a different thing — it is a submodule gitlink, `git add` stages a single pointer for it, and the guard lets it through.
- A branch created but left commitless leaves nothing on the remote — it was never pushed. It is not inert locally, though. An abort partway through the staging loop leaves the new branch checked out and the already-added paths sitting in the index. That is why the block runs `git reset -q` before it stages: on a re-run `CURRENT` is no longer the default branch, so the `else` path is taken, and without the reset the commit would sweep in leftovers from the previous attempt — including a path the secret filter dropped this time.

### 3b. Open the PR/MR and read the assignee back — one block

Run the block for the detected provider. Each one echoes the values Phase 4 reports, so Phase 4 makes no further calls.

**GitHub:**

```bash
set -e
DEFAULT_BRANCH="<default-branch>"

# Do NOT pass --assignee to the create. Assignment is best-effort, and a rejected
# assignee fails the whole create — which would lose the PR over a non-critical step.
if ! PR_URL=$(gh pr create \
  --base "$DEFAULT_BRANCH" \
  --title "<title>" \
  --body "$(cat <<'BODY'
## Summary
- ...
BODY
)"); then
  # An OPEN PR for this branch may already exist — return that URL instead of an error.
  # Filter on state. `gh pr view` also resolves a CLOSED or MERGED PR for this branch,
  # and returning one of those would report a stale URL as if the ship had succeeded.
  PR_URL=$(gh pr view --json url,state -q 'select(.state=="OPEN") | .url' 2>/dev/null || true)
  [ -n "$PR_URL" ] || { echo "ABORT: branch pushed; PR not created — run: gh pr create --base \"$DEFAULT_BRANCH\""; exit 1; }
fi

# dedicated post-create assign step — never blocks the ship
gh pr edit --add-assignee "@me" >/dev/null 2>&1 || true

PR_ASSIGNEES=$(gh pr view --json assignees -q '[.assignees[].login] | join(",")' 2>/dev/null || true)
echo "pr=$PR_URL"
echo "assignee=$PR_ASSIGNEES"
```

`--add-assignee "@me"` self-assigns the PR to you (resolved server-side). It runs after the create, so a repo that lets you push but not assign still gets its PR. The read-back on the next line is what the report prints, so a failed assign shows as `NOT set`, never as a silent success.

**GitLab:** create the MR first, then self-assign in a **separate** step. Do NOT pass `--assignee` to `glab mr create` — it is a known silent no-op (glab injects a `/assignee` quick-action into the description instead of setting the assignee field, and when that doesn't process you get `ok created` with an empty assignee and no warning — glab issues #974/#878/#358). `glab mr update --assignee` writes the assignee field directly via the PUT update endpoint, so it actually sticks.

`glab mr update` and `glab mr view` with no IID target the MR for the current branch. You are still on the feature branch here, so they resolve correctly.

```bash
set -e
DEFAULT_BRANCH="<default-branch>"

glab mr create \
  --target-branch "$DEFAULT_BRANCH" \
  --title "<title>" \
  --description "$(cat <<'BODY'
## Summary
- ...
BODY
)" \
  --fill=false || true   # an MR may already exist — the read-back below settles it

# self-assign target (best-effort). `.username // empty` yields "" on any lookup failure
# (error response, 401, missing field), so a failed lookup just skips the assign.
GLAB_USER=$(glab api user 2>/dev/null | jq -r '.username // empty') || GLAB_USER=""
if [ -n "$GLAB_USER" ]; then
  glab mr update --assignee "$GLAB_USER" >/dev/null 2>&1 || true   # dedicated assign step — never blocks the ship
fi

MR_JSON=$(glab mr view -F json 2>/dev/null || true)
# Guarded for the same reason as the assignee read-back below. jq exits 5 on non-JSON
# input, which under set -e would kill the block AFTER the MR was created, with no
# ABORT line and no recovery command.
MR_URL=$(printf '%s' "$MR_JSON" | jq -r '.web_url // empty' 2>/dev/null || true)
[ -n "$MR_URL" ] || { echo "ABORT: branch pushed; MR not created — run: glab mr create --target-branch \"$DEFAULT_BRANCH\" --fill=false"; exit 1; }
# `.assignees[]?` — the `?` matters. On an MR with no assignees the field is null, and a
# bare `.assignees[]` exits 5 ("Cannot iterate over null"), which under `set -e` would kill
# this block AFTER the MR was already created. Assignment must never block the ship.
GLAB_ASSIGNEES=$(printf '%s' "$MR_JSON" | jq -r '[.assignees[]?.username] | join(",")' 2>/dev/null || true)

echo "pr=$MR_URL"
echo "assignee=$GLAB_ASSIGNEES"
```

The read-back makes a silent assign failure visible in the Phase 4 report, instead of a manual surprise later. It never blocks the ship.

#### GitHub-only fork fallback (push denied in 3a)

If the 3a push fails **specifically because you lack write access** — stderr matches `Permission to .* denied`, `Write access to repository not granted`, or `The requested URL returned error: 403` — do NOT abort and do NOT retry with any bypass flag. This is not a bypass; it routes the branch to a legitimate alternate destination. Fork the upstream, push there, and open the PR against the upstream repo. All of it in one block:

```bash
set -e
DEFAULT_BRANCH="<default-branch>"
BRANCH="<branch-from-3a>"   # 3a echoed `branch=` before the push, so this value is known

# Look the upstream slug up HERE, not in Phase 1 — this path is almost never taken.
# Capture it BEFORE `gh repo fork` to be safe. `--remote-name fork` keeps origin on
# upstream (it suppresses the default origin -> upstream rename), so the lookup is
# correct before and after the fork — but before removes all doubt.
ORIGIN_SLUG=$(gh repo view --json nameWithOwner -q .nameWithOwner) \
  || { echo "ABORT: cannot resolve the upstream repo — run: gh repo view --json nameWithOwner"; exit 1; }

# Capture the login once and reuse it. Inside an `echo` argument a failure is invisible
# even under set -e — `echo "fork=$(false)/repo"` prints `fork=/repo` and exits 0.
LOGIN=$(gh api user -q .login) \
  || { echo "ABORT: cannot resolve your GitHub login — run: gh api user -q .login"; exit 1; }

# Create the fork in your account, add it as a separate remote "fork".
gh repo fork --remote --remote-name fork --clone=false
git push -u fork "$BRANCH"

# Target the upstream repo explicitly and set the head to your fork. Without
# --repo/--head, `gh pr create` prompts interactively and breaks the one-shot flow.
# Do NOT pass --assignee here — you typically lack assign rights on a repo you
# cannot push to, and it would fail the create.
if ! PR_URL=$(gh pr create \
  --repo "$ORIGIN_SLUG" \
  --base "$DEFAULT_BRANCH" \
  --head "$LOGIN:$BRANCH" \
  --title "<title>" \
  --body "$(cat <<'BODY'
## Summary
- ...
BODY
)"); then
  # `gh pr view --repo <slug>` REQUIRES a PR argument and always fails without one
  # ("argument required when using the --repo flag"), so look the open PR up with
  # `gh pr list`, which filters cross-repo by head.
  PR_URL=$(gh pr list --repo "$ORIGIN_SLUG" --head "$LOGIN:$BRANCH" --state open \
             --json url -q '.[0].url' 2>/dev/null || true)
  [ -n "$PR_URL" ] || { echo "ABORT: branch pushed to fork; PR not created — run: gh pr create --repo \"$ORIGIN_SLUG\" --base \"$DEFAULT_BRANCH\" --head \"$LOGIN:$BRANCH\""; exit 1; }
fi

# best-effort self-assign — silently ignored if you lack assign rights on the upstream repo
gh pr edit "$PR_URL" --add-assignee "@me" >/dev/null 2>&1 || true

# Address the PR by URL. The URL carries the repo, so --repo is neither needed nor allowed.
PR_ASSIGNEES=$(gh pr view "$PR_URL" --json assignees -q '[.assignees[]?.login] | join(",")' 2>/dev/null || true)
echo "pr=$PR_URL"
echo "assignee=$PR_ASSIGNEES"
echo "fork=$LOGIN/${ORIGIN_SLUG#*/}"
```

`gh repo fork` is idempotent — if the fork already exists it just (re)adds the remote and exits 0.

Rules for this fallback:

- **GitHub only.** On GitLab, a push-denied error aborts (`no write access — fork fallback is GitHub-only`); the fork+MR model differs and is out of scope.
- A push failure that is NOT an access/permission error (non-fast-forward, network, pre-push hook) still aborts per the normal rule.
- Record that the fork path was taken, so Phase 4 adds the `fork:` line.

## Phase 4 — Report

Print these lines to chat:

```
branch:    <branch-name>
commit:    <short-sha>  <subject>
pr:        <url>
assignee:  <you>            # or:  NOT set — assign manually
```

Fill every value from the variables Phase 3a and Phase 3b already echoed — `branch=`, `commit=`, `pr=`, `assignee=`, and `fork=` on the fork path. The subject beside the short SHA is the one you wrote in Phase 2; you already have it. Make no fresh call.

The `assignee:` line is mandatory and must reflect the read-back, not the intent — so a silent assign failure is visible here, not discovered later. If your login (GitHub) or `$GLAB_USER` (GitLab) is in the `assignee=` value, print it. Otherwise print `assignee: NOT set — assign manually`.

If the GitHub fork fallback was used, add its `fork=` value as a line, so the user sees where the branch lives:

```
fork:      <your-login>/<repo>
```

Nothing else. No trailing summary, no narrative paragraph.

## Hard rules (never violate)

- Never `--no-verify` / `--no-gpg-sign` — pre-commit hooks must run.
- Never `--amend` — always a new commit, even after a hook failure.
- Never `--force` / `--force-with-lease`.
- Never `git add -A` / `git add .` — stage by explicit path.
- Never auto-install `gh`, `glab`, or anything else — ask the user first.
- Never push to the default branch.
- Never push to a remote other than `origin` — the only exception is the GitHub fork fallback (remote `fork`) after an access-denied push. Even then, never `--force`.
- Never include Claude / Anthropic / AI-generated attribution anywhere.
- Never swallow stderr in Phase 3a. Hook and push errors must reach the user verbatim.
- Self-assignment is best-effort — never let it abort the ship. Opening the PR/MR is the critical step; a failed or empty assignee lookup is a no-op, not a failure. But it must be a dedicated post-create step whose result is read back and reported (Phase 4) — never silently skipped. Never pass an assignee to the create itself: on GitHub `gh pr create --assignee` fails the whole create when the assignee is rejected, and on GitLab `glab mr create --assignee` is a silent no-op. Assign with `gh pr edit --add-assignee` or `glab mr update --assignee` after the create.

## Failure modes (abort with a one-line reason)

| Condition | Message |
|---|---|
| Not in a git work tree | `not a git repository` |
| Detached HEAD | `detached HEAD — checkout a branch first` |
| Active rebase/merge/cherry-pick | `<operation> in progress — finish or abort it first` |
| Working tree clean | `no changes to commit` |
| No `origin` remote | `no origin remote configured` |
| Unsupported provider host | `unsupported remote host: <host>` |
| `origin` fetch and push URLs differ | `origin fetch and push URLs differ — push goes to <url>` |
| Revert or sequencer operation in progress | `<operation> in progress — finish or abort it first` |
| Provider CLI not installed | `<gh\|glab> not installed` |
| Default branch detection failed | ask the user once |
| Suspicious-only diff (secrets) | `staged file looks like a secret: <path> — confirm to proceed` |
| A path to stage is over 10 MB | `file larger than 10 MB: <path>` |
| A path to stage is a directory | `directory path, not a file: <path>` |
| Pre-commit hook failure | surface the hook's error verbatim and stop |
| Push denied — no write access (GitHub) | fork upstream, push to `fork`, open cross-repo PR (not an error) |
| Push denied — no write access (GitLab) | `no write access — fork fallback is GitHub-only` |
| Push fails for any other reason | surface the git error and stop |
| Existing **open** PR/MR for branch | return existing URL (not an error) |
| `git status` failed | `git status failed` |
| No branch name derived | `no branch name derived` |
| Default branch unknown at Phase 3a | `default branch unknown — ask the user, then re-run` |
| Derived branch equals the default branch | `refusing to commit to the default branch` |
| PR creation failed after push | `branch pushed; PR not created — run: gh pr create --base <default>` (GitLab: `glab mr create --target-branch <default> --fill=false`) |
| PR creation failed after a fork push | `branch pushed to fork; PR not created — run: gh pr create --repo <slug> --base <default> --head <login>:<branch>` |
| Upstream slug lookup failed on the fork path | `cannot resolve the upstream repo — run: gh repo view --json nameWithOwner` |
| GitHub login lookup failed on the fork path | `cannot resolve your GitHub login — run: gh api user -q .login` |

The two `PR creation failed after …` rows matter because the commit and the push already landed. A second `/ship-pr` run cannot repair either one — the tree is clean, so the run aborts with `no changes to commit`. Always give the user the recovery command. An expired or missing CLI login is the common cause; `gh auth login` or `glab auth login` fixes it, then the recovery command opens the PR.

The `Upstream slug lookup failed` row is different: it fires on the fork path before the fork push, so nothing has reached any remote yet. Do not tell the user a branch was pushed.

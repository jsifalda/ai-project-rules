---
name: ship-pr
disable-model-invocation: true
description: MANUAL-INVOCATION-ONLY skill — do NOT auto-trigger. Only invoke when the user explicitly types the literal slash command `/ship-pr`. Natural-language phrasing such as "ship this", "ship these changes", "create a PR", "open a PR", "open an MR", "push and create PR", "send this for review", or any paraphrase are ANTI-TRIGGERS — they MUST NOT cause this skill to load; handle those with standard commit + push tools instead and, if helpful, ask whether to run `/ship-pr`. When (and only when) explicitly invoked — runs an end-to-end git ship workflow from a dirty working tree to an open PR (GitHub) or MR (GitLab), self-assigned to you, in one shot. Auto-detects provider via `git remote`, auto-derives branch name, commit message, and PR title/body from the diff and existing repo conventions, no per-step prompts. Do NOT use for committing without opening a PR, reviewing or editing existing PRs, force-pushing or rewriting history, cutting releases, or anything touching tags or changelogs.
---

# Ship PR

Go from a dirty working tree to an open PR/MR in one pass. Auto-derive everything from the diff and the repo's own conventions. No per-step confirmations.

The skill runs six phases in strict order. Abort on the first failure with a one-line reason — do not retry with `--no-verify`, `--force`, or any other bypass flag. (Sole exception: on GitHub, a push denied for lack of write access triggers the fork fallback in Phase 5d — an alternate destination, not a bypass.)

## Phase 1 — Preflight

Run each check; abort immediately on failure.

```bash
git rev-parse --is-inside-work-tree   # must print "true"
git rev-parse --abbrev-ref HEAD       # must not be "HEAD" (detached)
test ! -e .git/REBASE_HEAD && test ! -e .git/MERGE_HEAD && test ! -e .git/CHERRY_PICK_HEAD
git status --porcelain                 # must produce at least one line
git remote get-url origin              # must succeed
```

If the working tree is clean, abort with: `no changes to commit`.

If a rebase/merge/cherry-pick is in progress, abort and tell the user to finish or abort it first.

## Phase 2 — Detect provider and default branch

Parse `git remote get-url origin`:

- Host matches `github.com` or `*.github.*` → provider = `gh`
- Host matches `gitlab.com` or contains `gitlab` → provider = `glab`
- Neither → abort: `unsupported remote host: <host>`

Verify the CLI is installed and authenticated:

```bash
gh auth status      # for GitHub
glab auth status    # for GitLab
```

If the CLI is missing or unauthenticated, abort and tell the user. Do NOT auto-install — installing global tools requires explicit user approval.

Detect the default branch:

```bash
git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null | sed 's|^origin/||'
# Fallback if origin/HEAD is not set:
gh repo view --json defaultBranchRef -q .defaultBranchRef.name   # GitHub
glab repo view -F json | jq -r .default_branch                    # GitLab
```

Store as `$DEFAULT_BRANCH`. If detection fails, ask the user once.

For GitHub only, also capture the canonical upstream slug now — **before** any fork, while `origin` still resolves to upstream. The fork fallback in Phase 5 uses it to target the PR at the upstream repo:

```bash
ORIGIN_SLUG=$(gh repo view --json nameWithOwner -q .nameWithOwner)   # e.g. owner/repo — GitHub only
```

Store as `$ORIGIN_SLUG`.

## Phase 3 — Detect project conventions

Read whichever of these exist; do not fail if missing:

- `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, `CONTRIBUTING.md`
- `.github/PULL_REQUEST_TEMPLATE.md`, `.github/pull_request_template.md`
- `.gitlab/merge_request_templates/Default.md` (or any file in that dir)

These often state explicit branch/commit/PR rules. Honor them when present.

Then infer style from history:

```bash
git log --pretty=%s -30                        # commit subject style
git branch -a --sort=-committerdate | head -20 # branch-name pattern
git config user.name                           # for username-prefixed branches
```

Look for these patterns:

- Conventional commits: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, `test:`, `perf:`, with optional `(scope)`
- Branch prefixes: `feature/`, `fix/`, `feat/`, `chore/`, `<username>/`, or `<TICKET-ID>-`
- Ticket-ID embedding: `[ABC-123]`, `(ABC-123)`, or `ABC-123` in subject

If signals conflict or are absent, fall back to:

- Commit: conventional commits (`type: subject` or `type(scope): subject`)
- Branch: `<type>/<kebab-slug>`

## Phase 4 — Derive branch name, commit message, PR title and body

Read the full diff:

```bash
git diff HEAD            # all changes (staged + unstaged)
git status --porcelain   # for file inventory
```

Decide:

- **Type** — feat / fix / refactor / docs / chore / test / perf, based on what the diff actually does (new behavior vs. corrected behavior vs. internal cleanup vs. docs-only)
- **Scope** — optional, only if the change is clearly scoped to one module/area visible in the diff paths
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
- **Assignee** — the new PR/MR is self-assigned to the authenticated CLI user (you). Best-effort, never blocks the ship — see Phase 5e.

### Attribution policy (hard rule)

NEVER include any of the following in commit messages, PR titles, PR bodies, or branch names:

- `Co-Authored-By: Claude` (any model, any email)
- `🤖 Generated with [Claude Code]` or any variant
- "Generated by Claude" / "Powered by Anthropic" / "AI-generated" footers
- Any trailer or badge referencing Claude, Anthropic, Sonnet, Opus, Haiku, or AI assistance

The commit message ends after the descriptive body. The PR body ends after the `## Summary` section. No trailing block.

## Phase 5 — Execute

Run in order. Stop on the first failure — do NOT retry with `--no-verify`, `--no-gpg-sign`, `--force`, or `--amend`. The sole exception is a push denied for lack of write access on GitHub, which triggers the fork fallback in 5d (an alternate destination, not a bypass).

### 5a. Create or stay on a feature branch

```bash
CURRENT=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT" = "$DEFAULT_BRANCH" ]; then
  git checkout -b "<derived-branch>"
fi
# else: stay on the current feature branch (treat as appending)
```

If the derived branch name already exists locally or on the remote, append a short numeric suffix (`-2`, `-3`, …).

### 5b. Stage files by name

Iterate the porcelain output and add each path explicitly. Never run `git add -A` or `git add .` — they sweep in secrets and large binaries.

Skip / abort on these patterns (likely secrets):

- `.env*` except `.env.example` and `.env.sample`
- `*.pem`, `*.key`, `*.p12`, `*.pfx`
- `id_rsa*`, `id_ed25519*`, `id_ecdsa*`
- `credentials*`, `*credentials.json`, `*service-account*.json`
- Files larger than 10 MB

If a suspicious file is the only change, abort and ask the user explicitly.

### 5c. Commit

Use a HEREDOC so multi-line messages preserve formatting and quotes:

```bash
git commit -m "$(cat <<'EOF'
<subject>

<optional body bullets>
EOF
)"
```

No `--no-verify`. If a pre-commit hook fails, fix the underlying issue (or surface it to the user) — do not bypass.

If the commit fails, do not run `--amend` to "retry". Create a NEW commit after fixing.

### 5d. Push

```bash
git push -u origin "<branch>"
```

If the upstream is already set, plain `git push` is fine. Never `--force` or `--force-with-lease`.

#### GitHub-only fork fallback (push denied)

If the push fails **specifically because you lack write access** — stderr matches `Permission to .* denied`, `Write access to repository not granted`, or `The requested URL returned error: 403` — do NOT abort and do NOT retry with any bypass flag. This is not a bypass; it routes the branch to a legitimate alternate destination. Fork the upstream and push there:

```bash
# Create the fork in your account, add it as a separate remote "fork".
# --remote-name fork keeps origin pointing at upstream (suppresses the default origin→upstream rename).
gh repo fork --remote --remote-name fork --clone=false

# Push the branch to the fork.
git push -u fork "<branch>"
```

`gh repo fork` is idempotent — if the fork already exists it just (re)adds the remote and exits 0.

Rules for this fallback:

- **GitHub only.** On GitLab, a push-denied error aborts (`no write access — fork fallback is GitHub-only`); the fork+MR model differs and is out of scope.
- A push failure that is NOT an access/permission error (non-fast-forward, network, pre-push hook) still aborts per the normal rule.
- Record that the fork path was taken and set the PR head to `<your-login>:<branch>` for Phase 5e.

### 5e. Open the PR/MR

GitHub:

```bash
gh pr create \
  --base "$DEFAULT_BRANCH" \
  --assignee "@me" \
  --title "<title>" \
  --body "$(cat <<'EOF'
## Summary
- ...
EOF
)"
```

`--assignee "@me"` self-assigns the PR to you (resolved server-side). In the normal write-access path this always succeeds.

GitHub — fork fallback (only when Phase 5d forked): target the upstream repo explicitly and set the head to your fork. Without `--repo`/`--head`, `gh pr create` prompts interactively, which breaks the one-shot flow. Do NOT pass `--assignee` here — you typically lack assign rights on a repo you can't push to, and it would fail the create. Self-assign best-effort after creation instead.

```bash
gh pr create \
  --repo "$ORIGIN_SLUG" \
  --base "$DEFAULT_BRANCH" \
  --head "$(gh api user -q .login):<branch>" \
  --title "<title>" \
  --body "$(cat <<'EOF'
## Summary
- ...
EOF
)"

# best-effort self-assign — silently ignored if you lack assign rights on the upstream repo
gh pr edit --repo "$ORIGIN_SLUG" --add-assignee "@me" 2>/dev/null || true
```

GitLab: resolve your username first and self-assign. `.username // empty` yields an empty string on any lookup failure (error/401 response, missing field), so `$GLAB_USER` is never the literal `null`; the `${GLAB_USER:+…}` guard then drops the flag and the MR is created without an assignee. A failed lookup can't block the MR.

```bash
GLAB_USER=$(glab api user 2>/dev/null | jq -r '.username // empty') || GLAB_USER=""   # self-assign target (best-effort)

glab mr create \
  --target-branch "$DEFAULT_BRANCH" \
  ${GLAB_USER:+--assignee "$GLAB_USER"} \
  --title "<title>" \
  --description "$(cat <<'EOF'
## Summary
- ...
EOF
)" \
  --fill=false
```

If creation fails because a PR/MR already exists for this branch, retrieve and return the existing URL instead of creating a new one:

```bash
gh pr view --json url -q .url            # GitHub
glab mr view -F json | jq -r .web_url    # GitLab
```

## Phase 6 — Report

Print exactly three lines to chat:

```
branch:  <branch-name>
commit:  <short-sha>  <subject>
pr:      <url>
```

If the GitHub fork fallback (Phase 5d) was used, add a fourth line so the user sees where the branch lives:

```
fork:    <your-login>/<repo>
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
- Self-assignment is best-effort — never let it abort the ship. Opening the PR/MR is the critical step; a failed or empty assignee lookup is a no-op, not a failure.

## Failure modes (abort with a one-line reason)

| Condition | Message |
|---|---|
| Not in a git work tree | `not a git repository` |
| Detached HEAD | `detached HEAD — checkout a branch first` |
| Active rebase/merge/cherry-pick | `<operation> in progress — finish or abort it first` |
| Working tree clean | `no changes to commit` |
| No `origin` remote | `no origin remote configured` |
| Unsupported provider host | `unsupported remote host: <host>` |
| Provider CLI missing or unauthenticated | `<gh\|glab> not installed or not authenticated` |
| Default branch detection failed | ask the user once |
| Suspicious-only diff (secrets) | `staged file looks like a secret: <path> — confirm to proceed` |
| Pre-commit hook failure | surface the hook's error verbatim and stop |
| Push denied — no write access (GitHub) | fork upstream, push to `fork`, open cross-repo PR (not an error) |
| Push denied — no write access (GitLab) | `no write access — fork fallback is GitHub-only` |
| Push fails for any other reason | surface the git error and stop |
| Existing PR/MR for branch | return existing URL (not an error) |

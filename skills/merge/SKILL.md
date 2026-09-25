---
name: merge
description: >-
  Bring the current branch up to date with the remote default branch and push the result to
  the branch's own PR or MR. Fetches, merges (never rebases), resolves conflicts, runs the
  project's own verification gates, then pushes only the current branch to its own upstream.
  Works in a linked git worktree and in a plain checkout, GitHub and GitLab alike, no provider
  CLI needed. Use when the user types /merge, or says merge main into this branch, sync this
  branch with main, update this branch from main, pull main into here, or asks to resolve
  conflicts with main and push. Optional argument, a base branch name, overrides the detected
  default branch. Do NOT use to open a PR (ship-pr), to merge a PR into main, to rebase, to
  squash, to force-push, or to switch branches.
metadata:
  version: "1.0"
---

# Merge

Bring the current branch up to date with the remote default branch, then push the result to the
branch's own pull request or merge request. The skill fetches, merges, resolves the conflicts,
runs the project's own gates, and pushes. It changes no branch other than the one you are on.

The skill exists because the obvious commands are wrong here. In a linked worktree the default
branch is usually checked out somewhere else, so `git checkout main` fails. The stash stack is
shared across every worktree of the repository, so a stash can carry away another session's
work. The branch is already on a PR, so a rebase rewrites published history and breaks the
review.

Two remotes take part, and they can differ. The **base remote** holds the default branch. It is
`upstream` when that remote exists, the fork convention, and `origin` otherwise. The **push
remote** is where this branch's own upstream lives, and `origin` when no upstream is set.

## Phase 1 — Preflight

Run this one block. It is read-only, except for `git remote set-head`, which writes a local ref
only. It aborts with a single `ABORT:` line, or it prints the resolved values.

```bash
set -e

[ "$(git rev-parse --is-inside-work-tree 2>/dev/null)" = "true" ] || { echo "ABORT: not a git repository"; exit 1; }

CURRENT=$(git branch --show-current)
[ -n "$CURRENT" ] || { echo "ABORT: detached HEAD, checkout a branch first"; exit 1; }

if [ -e "$(git rev-parse --git-path MERGE_HEAD)" ]; then MERGE_IN_PROGRESS=1; else MERGE_IN_PROGRESS=0; fi

for STATE in rebase-merge rebase-apply CHERRY_PICK_HEAD REVERT_HEAD sequencer; do
  if [ -e "$(git rev-parse --git-path "$STATE")" ]; then
    echo "ABORT: $STATE in progress, finish or abort it first"; exit 1
  fi
done

if [ "$MERGE_IN_PROGRESS" = 0 ] && [ -n "$(git status --porcelain)" ]; then
  echo "ABORT: working tree is dirty, commit or discard your changes first"; exit 1
fi

PUSH_REMOTE=$(git config --get "branch.$CURRENT.remote" || true)
PUSH_BRANCH=$(git config --get "branch.$CURRENT.merge" || true)
PUSH_BRANCH=${PUSH_BRANCH#refs/heads/}
if [ -n "$PUSH_REMOTE" ] && [ "$PUSH_REMOTE" != "." ] && [ -n "$PUSH_BRANCH" ]; then
  SET_UPSTREAM=0
else
  PUSH_REMOTE=origin
  PUSH_BRANCH=$CURRENT
  SET_UPSTREAM=1
fi
git remote get-url "$PUSH_REMOTE" >/dev/null 2>&1 || { echo "ABORT: remote $PUSH_REMOTE is not configured"; exit 1; }

if git remote get-url upstream >/dev/null 2>&1; then BASE_REMOTE=upstream; else BASE_REMOTE=origin; fi
git remote get-url "$BASE_REMOTE" >/dev/null 2>&1 || { echo "ABORT: remote $BASE_REMOTE is not configured"; exit 1; }

DEFAULT_BRANCH="$ARGUMENTS"
if [ -z "$DEFAULT_BRANCH" ]; then
  DEFAULT_BRANCH=$(git symbolic-ref "refs/remotes/$BASE_REMOTE/HEAD" --short 2>/dev/null | sed "s|^$BASE_REMOTE/||")
fi
if [ -z "$DEFAULT_BRANCH" ]; then
  git remote set-head "$BASE_REMOTE" -a >/dev/null 2>&1 || true
  DEFAULT_BRANCH=$(git symbolic-ref "refs/remotes/$BASE_REMOTE/HEAD" --short 2>/dev/null | sed "s|^$BASE_REMOTE/||")
fi
[ -n "$DEFAULT_BRANCH" ] || { echo "ABORT: cannot detect the default branch, run: git remote set-head $BASE_REMOTE -a"; exit 1; }

if [ "$CURRENT" = "$DEFAULT_BRANCH" ] || [ "$PUSH_BRANCH" = "$DEFAULT_BRANCH" ]; then
  echo "ABORT: refusing to push the default branch"; exit 1
fi

if [ "$MERGE_IN_PROGRESS" = 1 ] && ! git merge-base --is-ancestor MERGE_HEAD "$BASE_REMOTE/$DEFAULT_BRANCH" 2>/dev/null; then
  echo "ABORT: a different merge is in progress (MERGE_HEAD is not on $BASE_REMOTE/$DEFAULT_BRANCH), finish or abort it first"; exit 1
fi

echo "current: $CURRENT"
echo "base_remote: $BASE_REMOTE"
echo "default_branch: $DEFAULT_BRANCH"
echo "push_remote: $PUSH_REMOTE"
echo "push_branch: $PUSH_BRANCH"
echo "set_upstream: $SET_UPSTREAM"
echo "merge_in_progress: $MERGE_IN_PROGRESS"
```

Read the output like this.

- Any `ABORT:` line ends the run. Print that reason and stop.
- `$ARGUMENTS` holds the optional base branch name. When the user gives one, it wins over the
  detected default branch. When it is empty, the block reads `refs/remotes/<base-remote>/HEAD`.
- The block tests `MERGE_HEAD` before it tests the working tree, because a merge in progress
  makes the tree dirty by definition. A `/merge` run that stopped on a conflict re-enters here,
  and the dirty-tree abort must not fire on it. The ancestor test then proves that the merge in
  progress is a merge of the default branch and not some other merge the user started by hand.
  `merge_in_progress: 1` means the merge already exists. Skip Phase 2 and resume at Phase 3.
- The working tree must be clean otherwise. The skill never stashes, because every worktree of
  the repository shares one stash stack, and a pop can take another session's work. Tell the
  user to commit or discard the changes first.
- **Every later block runs as its own command, so the shell variables do not survive.** Copy
  the printed values into the `<...>` placeholders of Phase 2 and Phase 5 by hand. Never reuse
  a variable name from an earlier command.

## Phase 2 — Fetch and merge

Fill the placeholders from the Phase 1 output, then run the block.

```bash
set -e
BASE_REMOTE="<base-remote>"
DEFAULT_BRANCH="<default-branch>"
git fetch "$BASE_REMOTE" "$DEFAULT_BRANCH"
git merge --no-edit "$BASE_REMOTE/$DEFAULT_BRANCH"
```

Keep Git's own merge message. Do not pass `--no-ff`. A fast-forward is a good result. The
outcome is one of three.

- Output `Already up to date` means there is nothing to integrate. Go to Phase 5 and report
  `merge: nothing to do`.
- Exit status 0 with a fast-forward or a clean merge means the merge is already committed. Skip
  Phase 3 and go to Phase 4.
- Exit status 1 with conflict lines means Phase 3.

## Phase 3 — Resolve conflicts

This phase is your work, not a script. Take the files one at a time.

1. List them with `git diff --name-only --diff-filter=U`.
2. Read all three versions of each file before you change it. `git show :1:<path>` is the merge
   base, `git show :2:<path>` is your branch, `git show :3:<path>` is the default branch. Keep
   the intent of both sides. Never take `--ours` or `--theirs` wholesale on a source file.
3. A lockfile conflict is different. It is generated output, so regenerate it instead of
   merging it. The lockfiles are `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`,
   `bun.lock`, `bun.lockb`, `Cargo.lock`, `poetry.lock`, `uv.lock`, `Gemfile.lock`, `go.sum`,
   and `composer.lock`. Run `git checkout --theirs -- <file>`, then regenerate with the
   lockfile-only command of the manager the repository already uses, for example
   `pnpm install --lockfile-only`, `npm install --package-lock-only`, `cargo generate-lockfile`,
   `uv lock`, or `go mod tidy`. Look the flag up for any other manager. Such a command
   updates the lockfile and adds no package. Use the manager the repository's lockfile names.
   Never a different one.
4. A generated file whose source of truth is in the repository follows the same rule. Test
   snapshots and built assets committed on purpose belong here. Take the default-branch side,
   then regenerate the file from its source.
5. A conflict that needs a product or design decision is a STOP. Both sides change the same
   behaviour on purpose, the default branch deleted a file this branch edits, or two migrations
   collide. Leave the merge in progress. Report the file, the intent of each side, and one
   recommendation. Do not guess. When the user answers, `/merge` resumes through the Phase 1
   `MERGE_HEAD` path.
6. Stage each file with `git add -- <file>` as you finish it.

Before the commit, both of these must print nothing. They catch a conflict marker left in the
staged content.

```bash
git diff --cached --check
git diff --cached | grep -nE '^\+(<{7} |={7}$|>{7} )'
```

Close the merge with `git commit --no-edit`. Never `--no-verify`. Report a pre-commit hook
failure verbatim and fix its cause. After the fix, stage it with `git add` and run
`git commit --no-edit` again. Never `--amend`, because the merge commit does not exist yet.

## Phase 4 — Verify

Run the gates the project defines for itself. Read the project's own agent instructions first,
`CLAUDE.md` or `AGENTS.md`, for a verification protocol. Then use the package scripts, `build`,
`test`, `lint`, and `typecheck`, or the language equivalent such as `cargo test`,
`go test ./...`, or `pytest`.

- A conflict resolution is authored code. Give it whatever review path the project's own
  protocol defines for authored changes. A clean merge that authored no line is integration
  only, and the project's protocol decides whether review runs on it.
- A gate that fails because of the merge gets a follow-up commit. Never `--amend`. Then run the
  gates again.
- A gate can fail for a reason that predates the merge. Treat it as pre-existing only when the
  failing test or file was not touched by this branch, and either the default branch's own CI
  is red or the failure is in code that only the default branch changed. Report it as
  `FAIL (pre-existing)` and continue to the push. It is not this merge's defect. Do not stash
  anything to prove this.
- No gates in the project means `gates: none found`. Do not invent one.

## Phase 5 — Push

Fill the placeholders from the Phase 1 output, then run the block. It pushes only when the
remote is reachable and the local branch is ahead of it.

```bash
set -e
PUSH_REMOTE="<push-remote>"
PUSH_BRANCH="<push-branch>"
CURRENT="<current>"
SET_UPSTREAM="<set-upstream>"

set +e
git ls-remote --exit-code --heads "$PUSH_REMOTE" "$PUSH_BRANCH" >/dev/null
RC=$?
set -e
case "$RC" in
  0) git fetch "$PUSH_REMOTE" "$PUSH_BRANCH" || { echo "ABORT: cannot reach remote $PUSH_REMOTE"; exit 1; }
     AHEAD=$(git rev-list --count "$PUSH_REMOTE/$PUSH_BRANCH..HEAD") ;;
  2) AHEAD=1 ;;
  *) echo "ABORT: cannot reach remote $PUSH_REMOTE"; exit 1 ;;
esac

if [ "$AHEAD" = 0 ]; then
  echo "push: nothing to push"
elif [ "$SET_UPSTREAM" = 1 ]; then
  git push -u "$PUSH_REMOTE" "$CURRENT"
else
  git push "$PUSH_REMOTE" "HEAD:refs/heads/$PUSH_BRANCH"
fi
```

`git ls-remote --exit-code` exits 2 when the branch does not exist on the remote yet, which is
the first push of a new branch. Any other non-zero code is a network or auth failure, and the
block aborts instead of guessing.

Never `--force`. Never `--force-with-lease`. Never `--no-verify`. Never a remote other than the
push remote. Report a pre-push hook failure verbatim.

A push rejected as non-fast-forward means somebody pushed to the PR branch while you worked. Do
not force. Report `push: BLOCKED non-fast-forward` and stop. The user integrates the remote
branch themselves, for example with `git pull --ff-only <push-remote> <push-branch>` when it
fast-forwards, and then runs `/merge` again. The skill never runs that command.

## Phase 6 — Report

Print this block. Nothing follows it.

```
base:       <base-remote>/<default-branch> @ <short-sha>
branch:     <current-branch>
merge:      <short-sha>  <subject>        # or: nothing to do
conflicts:  <n> files resolved: <list>    # or: none / STOPPED on <file>
gates:      <name> pass, <name> pass      # or: none found / <name> FAIL (pre-existing)
push:       <push-remote>/<push-branch> @ <short-sha>   # or: nothing to push / BLOCKED <reason>
```

## Hard rules (never violate)

- Merge, never rebase. The branch is on a PR, and a history rewrite breaks the review.
- Never push the default branch. Never push a branch other than the current one.
- Never `--force`, `--force-with-lease`, `--no-verify`, `--amend`, `git stash`,
  `git checkout <other-branch>`, or `git pull`. A command the skill hands to the user to run is
  not the skill running it.
- Never resolve a conflict by taking one side wholesale on a source file.
- Stop on a conflict that needs a decision. Do not guess.
- Operate in the current worktree only. Never touch another worktree or the main checkout.

## Abort conditions

| Condition | Message |
|---|---|
| Not in a git work tree | `not a git repository` |
| Detached HEAD | `detached HEAD, checkout a branch first` |
| Rebase, cherry-pick, revert, or sequencer in progress | `<state> in progress, finish or abort it first` |
| Working tree dirty, no merge in progress | `working tree is dirty, commit or discard your changes first` |
| Push remote or base remote missing | `remote <remote> is not configured` |
| Default branch undetected | `cannot detect the default branch, run: git remote set-head <base-remote> -a` |
| Current branch or push branch equals the default branch | `refusing to push the default branch` |
| Merge in progress is not a merge of the default branch | `a different merge is in progress (MERGE_HEAD is not on <base-remote>/<default-branch>), finish or abort it first` |
| Conflict needs a product or design decision | `STOPPED on <file>`, merge left in progress, report both intents and one recommendation |
| Push remote unreachable | `cannot reach remote <push-remote>` |
| Push rejected as non-fast-forward | `BLOCKED non-fast-forward`, integrate the remote branch and run `/merge` again |

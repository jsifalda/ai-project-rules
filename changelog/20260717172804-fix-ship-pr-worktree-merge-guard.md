# Fix ship-pr merge guard failing open in git worktrees

- `/ship-pr` Phase 1 preflight now resolves `REBASE_HEAD` / `MERGE_HEAD` / `CHERRY_PICK_HEAD` via `git rev-parse --git-path` instead of hardcoded `.git/…` paths.
- Inside a linked worktree `.git` is a file, not a directory, so the hardcoded paths could never exist there — the in-progress-operation guard always passed, letting a ship commit and push over an unresolved merge/rebase/cherry-pick. Fail-open bug on the path the user actually works from.

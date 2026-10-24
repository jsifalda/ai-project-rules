# Fix CodeRabbit findings on the git-ship ranges rule

- Updated the `rules/git-ship.md` line in `README.md` to match the widened trigger in `rules/general.md`: any PR or MR work and a git worktree.
- Why: CodeRabbit flagged the README load conditions as out of date on PR #217.
- Added a `## Ranges` line to `rules/git-ship.md`: resolve the default branch from the remote, fetch `origin/<default>` with an explicit refspec when it is missing, ask when there is no `origin`.
- Why: a single-branch clone has no `origin/<default>` ref, and a bare-name fetch does not create it.

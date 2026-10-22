# Remove a worktree from outside it

- Added a rule to the Worktrees section of `rules/git-ship.md`: `cd` to the main checkout, then run `/usr/bin/git -C <worktree> worktree remove <worktree>`.
- Why: when the shell cwd is inside the worktree, `git worktree remove` exits 1 with a getcwd error after the removal succeeds. `git -C` changes the git directory, not the shell cwd.

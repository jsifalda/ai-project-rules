# Add proportionality, git and dotfile rules

- `rules/general.md`: match effort to the request size, never close an open design question as out of scope, skip Phase 3 review for a mechanical git task, and run one git command per Bash call.
- `rules/general.md`: shell config and home dotfiles are now edited directly, with a secret-safe line lookup. Global env and credential files stay banned.
- `rules/git-ship.md`: include every file the user names for a PR, and derive the repo name in a worktree from the git common dir or the remote URL. The worktree-only chaining rule moved to `general.md`.
- Why: user-requested rules for proportional effort, literal instruction following and environment facts.

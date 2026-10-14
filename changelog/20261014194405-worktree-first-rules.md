# Prefer Claude Code worktrees, gate plans on one

- `rules/general.md` gets a `# WORKTREES (Claude Code)` rule: prefer a Claude Code worktree for a git-repo change, and suggest one once when the session is not in one.
- Shortened the prior-art and no-install-path rules to partly offset the new always-loaded lines.
- `setup-aiengineering` injects a Worktree Gate (Step 7c, baseline v20, skill 1.3): in a git repo, every plan checks for a Claude Code worktree, else its first step switches into a new one and runs the bootstrap script.
- Fixed the baseline checklist's maintainer loop, which named the wrong step for some delivery types.
- Why: a worktree isolates each change, so parallel sessions do not collide in one checkout.

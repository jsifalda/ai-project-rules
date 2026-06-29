# Add .worktreeinclude handling to setup-aiengineering worktree module

- Step 7 now detects gitignored, non-regenerable config (`.env` and friends) and proposes a root `.worktreeinclude`, so Claude-created worktrees carry over secrets/config the SessionStart hook cannot rebuild.
- Guards against a configured `WorktreeCreate` hook (which disables `.worktreeinclude`), uses probe-then-ask + merge-not-clobber, and reports the outcome in Step 8.
- Why: the existing hook only restores derivable deps. A fresh worktree still started without its env files, so it was not actually runnable until now.
- Synced the README skill row and frontmatter description.

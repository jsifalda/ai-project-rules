# Remove claude-version-check skill

- Deleted the `claude-version-check` skill (`skills/claude-version-check/`) and its README row.
- Why: low-value utility (checks Claude Code CLI version vs latest). Its description loaded into the available-skills list every session, so removing it trims per-session token load.
- Sync hook auto-prunes the `~/.claude` symlink and `~/.copilot` copy on next SessionStart. No cross-references existed.

# Skills sync follows CLAUDE_CONFIG_DIR

- `setup-skills-autorefresh` hook now links skills into `${CLAUDE_CONFIG_DIR:-~/.claude}/skills` (absolute values only, a relative one warns and falls back to `~/.claude`).
- Legacy command migration matches a source only with a path separator, so a `<source>-backup` link is no longer removed.
- Why: a second Claude Code profile (another `CLAUDE_CONFIG_DIR`) needs its own skills dir, because each profile's `skills/synced/` holds that account's claude.ai skills.
- Docs and skill text updated, version 1.1.

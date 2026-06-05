# Move skills sync hook into the repo + add setup-skills-autorefresh skill

- Relocated the Claude Code skills auto-sync hook from the untracked
  `~/.claude/hooks/sync-skills.js` into the repo at
  `skills/setup-skills-autorefresh/scripts/sync-skills.js`, so it's committed
  and reproducible on other machines.
- The synced source folder is now a **parameter** (passed on the hook command
  line) instead of a hardcoded path — the hook can sync any skills folder you
  point it at.
- Added the `setup-skills-autorefresh` skill with a bundled `install.sh` that
  asks for / validates the source folder, registers the `SessionStart` hook in
  `~/.claude/settings.json` (idempotent, backs up to `.bak`, migrates the old
  hook path), runs it once, and removes the stale copy.
- Why: make the skills auto-load setup portable, versioned, and one-command to
  install or re-point on any machine.
- Refreshed `CLAUDE.md`, `README.md`, and the autoload reference memory to the
  new path and the source-as-argument behavior.

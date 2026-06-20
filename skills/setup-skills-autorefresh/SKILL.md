---
name: setup-skills-autorefresh
disable-model-invocation: true
description: Set up auto-refresh syncing of agent skills into Claude Code on this machine. Registers a SessionStart hook in ~/.claude/settings.json that, at every session start, symlinks each skill folder (any subfolder holding a SKILL.md) from a source folder you choose into ~/.claude/skills/ so they auto-load, and prunes ones you removed. Takes the source folder as a parameter, and if you don't give one it asks and recommends this repo's own skills/ dir, then verifies the path exists and holds at least one skill first. Idempotent — re-running re-points the source and migrates any older hook registration. Use when the user says "set up skills auto-refresh", "install the skills sync hook", "auto-sync my skills into Claude Code", "make my skills folder auto-load every session", or runs /setup-skills-autorefresh. Do NOT use for unrelated settings.json changes (permissions, env, model, other hooks) or one-off manual skill copying.
---

## What this does

Registers a `SessionStart` hook in Claude Code's `~/.claude/settings.json` that runs
`sync-skills.js` (bundled in this skill's `scripts/`) at the start of every session.
The hook symlinks each skill folder (`<name>/SKILL.md`) found under a **source folder
you choose** into `~/.claude/skills/`, and prunes symlinks for skills that no longer
exist. Result — drop a skill into that folder and it auto-loads next session, on any
machine where you've run this once.

The source folder is a parameter baked into the hook command, so the same script syncs
whatever folder you point it at.

## Prerequisite

- `node` (the hook is a Node script — already required by Claude Code's other hooks).
- The folder you want to sync, holding `<skill>/SKILL.md` subdirectories.

## Steps

1. **Determine the source folder.**
   - If the user named a folder, use it.
   - If not, ask which folder to sync from. Recommend this repo's own `skills/`
     directory as the default (resolve it from this skill's own location — it is
     `<this-skill>/../..`). Accept any absolute path the user gives instead.

2. **Install** — run the bundled installer with the chosen folder (from this skill's
   directory):

   ```bash
   bash scripts/install.sh <skills-source-dir>
   # example:
   bash scripts/install.sh ~/instructions/skills
   ```

   The installer **validates** the path — it must exist, be a directory, and contain at
   least one `<skill>/SKILL.md` — and **refuses invalid paths**. If it errors, ask the
   user for a corrected path and retry. On success it backs up `settings.json` to
   `.bak`, registers the hook idempotently, runs it once so symlinks exist immediately,
   and removes any stale pre-repo hook copy at `~/.claude/hooks/sync-skills.js`.

3. **Verify:**

   ```bash
   grep sync-skills ~/.claude/settings.json   # shows the registered command + your folder
   ls -la ~/.claude/skills/                   # skill symlinks now present
   ```

   Then restart Claude Code — the "Syncing skills..." status fires at session start and
   the skills under your folder load automatically.

## Notes

- **Idempotent / re-point** — re-running with a different folder updates the source;
  re-running with the same folder changes nothing. It never creates duplicate hook
  entries (it strips any prior `sync-skills.js` entry before adding the current one,
  which also migrates an older `~/.claude/hooks/sync-skills.js` registration).
- **Filtering** — to skip or restrict specific skills, edit the `WHITELIST` /
  `BLACKLIST` arrays at the top of `scripts/sync-skills.js`.
- **Timing** — Claude Code enumerates skills at session start, so a brand-new skill
  first appears in the *next* session. The installer's one-time run creates the symlink
  immediately, but enumeration still happens at startup.
- **Custom config dir** — set `CLAUDE_CONFIG_DIR` to edit `<dir>/settings.json` instead
  of `~/.claude/settings.json`.
- **Scope** — installs the Claude Code hook only. A separate Copilot CLI variant
  (copy-based) is not handled here.
- **Rollback** — restore `~/.claude/settings.json.bak`, or delete the `sync-skills.js`
  entry from `hooks.SessionStart`.

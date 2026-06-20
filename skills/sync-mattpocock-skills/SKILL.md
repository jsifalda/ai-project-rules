---
name: sync-mattpocock-skills
description: Sync a curated subset of skills from the mattpocock/skills GitHub repo into this repo's flat skills/ folder, ready to use. Upstream nests each skill under a category dir (engineering, productivity), so the sync flattens it into a top-level skills directory named after the skill. Use when the user wants to sync, update, or pull mattpocock skills. Given skill names, syncs exactly those; given none, it offers the previously-synced set from state/synced.txt for confirmation. Re-sync refreshes unchanged copies silently but warns and skips any locally-modified skill, or a name that collides with a native skill, until run with --force.
---

# Sync Matt Pocock Skills

Pulls named skills from [mattpocock/skills](https://github.com/mattpocock/skills) into this repo's `skills/` folder. The upstream repo nests skills under category dirs (`engineering/`, `productivity/`, `misc/`, …); this sync **flattens** them so `skills/engineering/tdd/` lands locally as `skills/tdd/` — ready for the `setup-skills-autorefresh` hook to symlink into `~/.claude/skills/`.

## When to Use

- User asks to sync, update, or pull Matt Pocock skills
- User names one or more upstream skills to bring in
- User wants to refresh already-synced skills to the latest upstream version

## Skills Synced (default set)

Used when the user names nothing (the seed in `state/synced.txt`):

| Skill | Upstream | Description |
|-------|----------|-------------|
| prototype | engineering/prototype | Build a throwaway prototype to flesh out a design |
| handoff | productivity/handoff | Compact the conversation into a handoff doc for another agent |

Any other upstream skill can be synced ad-hoc by name (e.g. `tdd`, `diagnosing-bugs`, `domain-modeling`, `to-prd`, `to-issues`). Bare names are searched across all categories; if a name exists in more than one, qualify it as `category/name`.

## Instructions

1. **User named skills** → run them directly. From this skill's directory:
   ```bash
   bash scripts/sync.sh <name> [<name> ...]
   ```
   Or from anywhere:
   ```bash
   bash "$(dirname "$(realpath SKILL.md)")/scripts/sync.sh" <name> [<name> ...]
   ```

2. **User gave no list** → do NOT run blind. First show the previously-synced set and confirm:
   ```bash
   cat state/synced.txt
   ```
   Show that set to the user and ask whether to sync exactly it. On yes, run `bash scripts/sync.sh` (no args — it reads `state/synced.txt`). On no, ask which skills they want and pass those as args.

3. **Handle skip warnings.** A `[skipped: locally modified]` line means the local copy was edited since last sync, or the name collides with a native skill (e.g. `grill-me`) that this sync never created. Surface the named files to the user and only re-run with `--force` after they confirm they want to overwrite:
   ```bash
   bash scripts/sync.sh <name> --force
   ```

4. **After a sync that created new skills** (this repo commits synced skills): for each new `skills/<name>/` dir, add a row to the `## Skills` table in `README.md`, then commit per the repo changelog convention.

## How re-sync decides (overwrite safety)

The script keeps a per-file sha256 baseline in `state/manifest.txt`:

- local copy unchanged since last sync → refreshed silently to latest upstream
- local copy edited (hash differs) or no baseline (native skill) → skipped with a warning, needs `--force`
- this means a legit upstream update still applies without `--force`, but your local edits are never clobbered silently

## Configuration

- `state/synced.txt` — the default set offered when no skills are named. Edit to change it.
- `scripts/sync.sh` — `REPO_OWNER`, `REPO_NAME`, `BRANCH` to change the upstream source.
- Set `GITHUB_TOKEN` for higher API rate limits.
- `--force` (or `FORCE=1`) overwrites locally-modified skills.

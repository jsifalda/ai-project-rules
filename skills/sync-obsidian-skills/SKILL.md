---
name: sync-obsidian-skills
description: Sync Obsidian-related skills (defuddle, json-canvas, obsidian-bases, obsidian-cli, obsidian-markdown) from the kepano/obsidian-skills GitHub repo. Use when the user wants to update, sync, or pull the latest Obsidian skill definitions from the upstream repository.
---

# Sync Obsidian Skills

Pulls the latest versions of Obsidian-related skills from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) and replaces local copies. Creates skills that don't exist locally.

## When to Use

- User asks to sync, update, or refresh Obsidian skills
- User wants to pull latest skill definitions from GitHub
- User mentions updating skills from kepano/obsidian-skills

## Skills Synced

| Skill | Description |
|-------|-------------|
| defuddle | Extract clean content from web pages |
| json-canvas | Create/edit JSON Canvas (.canvas) files |
| obsidian-bases | Create/edit Obsidian Bases (.base) files |
| obsidian-cli | CLI interaction with running Obsidian instances |
| obsidian-markdown | Create/edit Obsidian Flavored Markdown |

## Instructions

1. Run the sync script:
   ```bash
   bash "$(dirname "SKILL_PATH")/scripts/sync.sh"
   ```
   Replace `SKILL_PATH` with the resolved path to this SKILL.md, e.g.:
   ```bash
   bash /Users/jsifalda/instructions/skills/sync-obsidian-skills/scripts/sync.sh
   ```
2. Check exit code and output for errors
3. Report which skills were synced and any issues

## Configuration

Edit `scripts/sync.sh` to change:
- `SKILLS` array: add/remove skills to sync
- `REPO_OWNER`, `REPO_NAME`, `BRANCH`: change upstream source
- Set `GITHUB_TOKEN` env var for higher API rate limits

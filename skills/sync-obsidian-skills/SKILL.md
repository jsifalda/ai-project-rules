---
name: sync-obsidian-skills
disable-model-invocation: true
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

## Local divergences (do NOT blindly overwrite)

Some local copies have been deliberately edited away from upstream. A plain sync replaces
files wholesale, so it would silently revert these. Before syncing any skill listed here,
diff it against upstream, re-apply the local change on top, and tell the user what was
carried over.

| Skill | Local divergence | Why |
|-------|------------------|-----|
| obsidian-markdown | `## Diagrams` uses ASCII / Unicode box-drawing, not Mermaid. The Mermaid-only `class NodeName internal-link;` line is removed. | Repo-wide decision to drop Mermaid in favour of inline ASCII / Unicode diagrams. |

Note on `obsidian-markdown`: dropping `class NodeName internal-link;` removes a real
Obsidian capability, linking a diagram node to a note. It has no ASCII equivalent and is
intentionally gone, not reformatted. Do not "restore" it while re-applying the divergence.

## Instructions

`scripts/sync.sh` overwrites each local file unconditionally (`curl -o`) — no diff, no
backup, no dry-run. Steps 1 and 4 below are what actually protect the divergences above;
skipping them silently reverts them.

1. **Before syncing**, confirm the working tree is clean (`git status --short`). A dirty
   tree makes step 4 unable to tell an upstream change from your own uncommitted edit —
   commit or stash first.
2. Run the sync script. From inside this skill's directory:
   ```bash
   bash scripts/sync.sh
   ```
   Or from anywhere, using a portable path derived at runtime:
   ```bash
   bash "$(dirname "$(realpath SKILL.md)")/scripts/sync.sh"
   ```
3. Check exit code and output for errors
4. **Re-apply local divergences.** For every skill in the table above, run
   `git diff -- skills/<name>/` and look for the divergence being reverted. Where upstream
   overwrote it, re-apply the local edit on top of the incoming version — keep genuine
   upstream improvements, restore the local change. Never resolve this by discarding the
   whole sync (`git checkout`), which throws away real updates too.
5. Report which skills were synced, which divergences were re-applied, and any issues
4. If this sync created a skill not yet listed in README.md's `## Skills` table, add a row for it — link its `Origin` cell to `https://github.com/kepano/obsidian-skills` (the upstream repo root) — then commit per the repo changelog convention. For already-listed skills, confirm their `Origin` cell already links there.

## Configuration

Edit `scripts/sync.sh` to change:
- `SKILLS` array: add/remove skills to sync
- `REPO_OWNER`, `REPO_NAME`, `BRANCH`: change upstream source
- Set `GITHUB_TOKEN` env var for higher API rate limits

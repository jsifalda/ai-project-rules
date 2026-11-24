# Re-sync the Obsidian skills from upstream

- Fixed `scripts/sync-obsidian-skills.sh` for the new upstream layout (`plugins/obsidian/skills/`). The old path matched nothing, so the sync failed.
- Added a guard that stops the sync before any delete when a listed skill has no upstream files.
- Re-synced `defuddle`, `json-canvas`, `obsidian-bases`, `obsidian-cli` and `obsidian-markdown` to upstream, and bumped each to version 1.1.
- Added the new upstream `obsidian-headless` skill, because the `ob` CLI it documents runs vault sync on our server. Skipped `knap`, which has no use here.
- Kept the local `defuddle` description, because it routes web page reads to defuddle instead of WebFetch. The README and the script help now say to re-apply it after each sync.

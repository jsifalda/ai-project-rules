# Track skill sync provenance, disable create-implementation-plan auto-trigger

- Added `disable-model-invocation: true` to `create-implementation-plan`, matching the slash-only convention already used by `handoff`/`prototype`.
- Confirmed it isn't synced from anywhere (checked `sync-mattpocock-skills`/`sync-obsidian-skills` state files) — it's native to this repo.
- Added a 4th "Origin" column to README's Skills table, backfilled for the 8 skills actually synced from upstream (`grill-me`, `handoff`, `prototype` from `mattpocock/skills`; `defuddle`, `json-canvas`, `obsidian-bases`, `obsidian-cli`, `obsidian-markdown` from `kepano/obsidian-skills`), linking each to its upstream repo root. Dropped the now-redundant inline provenance notes from 3 descriptions.
- Updated `CLAUDE.md` and both sync skills' instructions so future syncs keep filling this column instead of leaving provenance undocumented.
- Why: provenance was previously scattered and inconsistent (some synced skills noted it inline, five weren't noted at all) — a dedicated column makes it a mandatory, checkable convention.

# Import grill-with-docs and domain-modeling from upstream

- Imported `grill-with-docs` and `domain-modeling` from `mattpocock/skills`, using `scripts/sync-mattpocock-skills.sh`.
- `grill-with-docs` is pure delegation. Its whole body invokes two other skills, so `domain-modeling` had to come along too. The chain stops there — `domain-modeling` invokes no skill.
- Edit 1: `/grilling` became `/grill-me` in `skills/grill-with-docs/SKILL.md`. Upstream names that skill `grilling`; this repo already carries the same body as `grill-me`, and the sync script hard-refuses both names. Without the edit the skill points at nothing.
- Edit 2: ADR filenames in `skills/domain-modeling/ADR-FORMAT.md` and `skills/domain-modeling/SKILL.md` changed from sequential (`0001-slug.md`) to date-plus-slug (`YYYY-MM-DD-slug.md`). The `## Numbering` heading became `## Naming`. `CLAUDE.md`'s `## Identifiers` bans counter-based ids, and `skills/setup-adrs/` already uses the date form.
- Both edits make `domain-modeling` a hand-maintained fork. Future sync runs report it as locally modified and skip it unless `--force`. That is the wanted protection — the same one `grill-me` relies on.
- `grill-with-docs` stays byte-identical to upstream, so it still re-syncs cleanly.
- README `## Skills` table gained one row per new skill.
- Deliberately not done: `wayfinder` was considered and dropped, which also dropped its dependencies `setup-matt-pocock-skills` and `research`.
- Deliberately not done: a review flagged an `ADR's` / `ADRs` typo in the `grill-with-docs` description, plus two suggestions about ADR paths and same-day filename collisions. All three were rejected on purpose, to keep the file byte-identical to upstream and to avoid contradicting `CLAUDE.md`.

# Add sync-mattpocock-skills skill

- New `sync-mattpocock-skills` skill: pulls a curated subset of skills from the public `mattpocock/skills` repo into the flat `skills/` folder.
- Upstream nests skills under category dirs (`engineering/`, `productivity/`); the sync flattens them to top-level `skills/<name>/` so the autorefresh hook picks them up.
- Seed set materialized and committed: `handoff`, `prototype`. Any other upstream skill (e.g. `tdd`, `to-prd`, `to-issues`) can be synced ad-hoc by name.
- Re-sync is edit-safe: a per-file sha256 baseline (`state/manifest.txt`) lets it refresh unchanged copies silently but skip locally-modified skills (and native-name collisions) unless `--force`.
- Relaxed the shared skill validator to allow the `disable-model-invocation` and `argument-hint` frontmatter keys, so third-party skills sync verbatim and keep their manual-only behavior.
- README `## Skills` table updated with the new rows.

## Why

Reuse Matt Pocock's engineering/productivity skills without hand-copying, mirroring the existing `sync-obsidian-skills` workflow but adapted to a different upstream layout.

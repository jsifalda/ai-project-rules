# setup-adrs: switch ADR identity from sequential integers to date-prefixed slugs

- Changed the ADR filename scheme from `NNNN-slug.md` (zero-padded autoincrement) to
  `YYYY-MM-DD-slug.md`. ADRs now reference and supersede each other by the full dated stem
  instead of a globally-allocated number.
- Removed the "re-check the default branch / renumber the loser / fix inbound links" ritual.
  Parallel branches pick different slugs, so they never collide on merge.
- Added a "date prefix is permanent once landed" rule so the filename↔reference mapping never
  breaks (supersede, never re-date).
- Added Step 3b: detect an existing integer scheme and offer conversion — rename each ADR using
  its `Date:` field (git-first-commit fallback) and rewrite all inbound `ADR-NNNN` references.
- Renamed seed asset `0001-record-architecture-decisions.md` → `seed-record-architecture-decisions.md`
  and dropped the `ADR-NNNN`/`ADR-0001` number from templates and the seed.
- Why: a single integer conflated stable identity with ordering and needed a shared counter,
  which raced under parallel authoring and forced painful renumber-on-merge conflicts.
- Touched: `setup-adrs` SKILL, policy template, adr/architecture/seed assets, README skills row.

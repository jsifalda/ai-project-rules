# Add an abort gate to better-plan

- Added Stage 1b to `better-plan`. It runs once Stage 1 has settled what the request really
  needs, and before the grill. When what Stage 1 found needs no code change — a stale cache, a
  restart, a setting, a user action, or a bug that does not reproduce — the flow stops and
  reports the remedy.
- Why: the skill produced a full plan for problems that needed no work at all. The gate is the
  `# CHEAPEST REMEDY FIRST` rule in `rules/general.md`, applied at the point where the flow
  commits to a deliverable.
- Every later stage keeps its behaviour when the flow reaches it, and the stage numbering is
  unchanged. The gate is the one new way the flow can end before Stage 2.

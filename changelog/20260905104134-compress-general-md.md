# Compress `rules/general.md` to rules-only bullets

- Rewrote every section of `rules/general.md` as one-line bullets. Word count went from 4257 to about 3100. Every heading, rule, condition, qualifier, threshold, command, path, and example stays. Every `**Why:**` line and every inline rationale clause is gone.
- Why: the file loads on every session in every agent, so its size is a per-session token cost. Rationale lived in the file to stop a rule from being argued away; the user chose to pay that risk for the smaller surface.
- One normative addition under `# RESTRICTIONS`: never push to a remote without explicit user instruction. The section said "extends the push rule above" but held no push rule, and `CLAUDE.md` already pointed at RESTRICTIONS for it.
- The installer list under `## Dependency Management` collapsed to a pointer at RESTRICTIONS, which holds the superset.
- Both review lenses ran twice. The harness lens caught qualifier drift ("prefer", "avoid", "usually", "whenever possible") and a dropped ban that the compression had turned into a description. All restored. CodeRabbit's findings were all proposals to change pre-existing rules and were rejected as out of scope.

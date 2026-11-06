# Load coding rules on demand

- Moved `# CODING STANDARDS` (with `## Comments`), `## TypeScript` and `# DEPENDENCY MANAGEMENT` from `rules/general.md` to the new `rules/coding.md`. The text stays the same. Only the cross-references to `general.md` `# RESTRICTIONS` and the line wrapping changed.
- Added a Tier 2 trigger row in `rules/general.md`: code, script or config changes, and dependency choices, load `rules/coding.md`.
- Updated the rule-file descriptions in `README.md` and `CLAUDE.md`.
- Why: most sessions write no code, so these rules used about 3.4 KB of the always-loaded layer for no use. The install gate stays always-on in `# RESTRICTIONS`.

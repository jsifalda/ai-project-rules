# Make the stale-line rule global

- Moved the delete-or-fix-stale-lines rule from `rules/docs-diagrams.md` and `rules/authoring.md` into `rules/general.md` core principles.
- Why: the rule matters for every written store (docs, vault notes, memory, plans, rules), but it loaded only during docs or instruction work.
- Dropped the example sentence from the "Match effort" line to offset the always-loaded cost.
- Fixed factual defects the prompt audit found in `rules/general.md`: em dashes in the Phase headings, wrapped rule lines, a double space, a missing full stop, and the `## Worktree entry (Claude Code)` heading reference.

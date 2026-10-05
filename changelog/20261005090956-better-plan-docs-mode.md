# Add docs mode to better-plan

- `better-plan` adds a Stage 1c docs mode check. For an ADR, a PRD, or a domain-model change, Stage 2 grills via `grill-with-docs` instead of `grill-me`. The grill can also switch docs mode on.
- Glossary and ADR drafts stay in the plan file until approval, and a first plan task writes them. Plan mode stays read-only.
- `grill-with-docs` drops `disable-model-invocation` so another skill can invoke it, and gains trigger text so a plain grill still goes to `grill-me`.
- The sync script skips this locally modified skill. A `--force` re-sync reverts both edits.
- Why: bigger features get domain docs from the same grill, with no separate run.

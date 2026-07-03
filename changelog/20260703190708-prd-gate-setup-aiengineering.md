# Add opt-in PRD gate module to setup-aiengineering

- Added a new `references/prd-gate.md` inject block and wired it into `setup-aiengineering` (Modules table, Step 4 menu, Step 5 inject list, Step 8 report, References, Rules, description).
- When opted in, it injects a `## PRD Gate` policy into a repo's AGENTS.md/CLAUDE.md: substantial features need a PRD via `/prd-creator` first, the plan is drafted from that PRD, and every implementation plan reads `docs/prds/*.md` for business context.
- Opt-in / default-off (diverges from the module convention on purpose), gated to substantial features only, hard-references `/prd-creator` with an install check.
- Why: keep new-feature work grounded in the business problem, not just code.

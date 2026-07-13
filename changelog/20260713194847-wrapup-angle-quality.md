# indie-hacker-wrapup: session traceability + angle-quality fixes

- Ledger rows now carry `profile:` (`.claude` vs `.claude-pro`), `theme:`, `src:`, and an evidence anchor, so a logged angle links back to the session and profile that produced it. Pinned the ledger to the literal `~/.claude/` path so both agent profiles share one file instead of forking.
- Added a fourth scoring check (originality) with a banned-cliché list, an archetype-diversity rule, theme-level dedup, and a stronger inside-baseball guard — to stop the skill emitting specific-but-formulaic, already-said angles.
- Rewrote `references/angle-examples.md` to teach diverse post archetypes and the novelty gate instead of a single reversal template.
- Why: angles read generic and had no traceability back to their session.

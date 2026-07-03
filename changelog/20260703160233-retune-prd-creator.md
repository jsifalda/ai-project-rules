# Retune prd-creator to PRD best practices

- Realigned the PRD template to the best-practice "golden" structure: Summary, Problem & context (with evidence), Users & use cases, merged Goals & success metrics (baseline + target + guardrails), Scope in/out, Solution outline with explicit functional requirements, Risks/assumptions/dependencies, Rollout & measurement, plus Open Questions.
- Added a 1-2 page length target, behavior-not-pixels and outcome-first quality rules, and a living-document rule (keep the PRD as the single source of truth).
- Changed output: PRDs now save to `docs/prds/` (tracked, not gitignored) and each PRD is linked from the project `README.md` under a `## PRDs` section (README created if missing, idempotent).
- Kept the junior-developer implementable framing per user preference — outcome-first sections wrap the existing detailed requirements rather than replacing them.
- Why: make PRD creation a standard, helpful-but-minimal step in the AI engineering flow for every big feature.

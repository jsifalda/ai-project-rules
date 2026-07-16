# ADR read-before-plan rule + numbering collision guard

- Added a "Read the ADRs before you plan" rule to the ADR policy `setup-adrs` injects — read
  `ARCHITECTURE.md`, scan `docs/adr/` slugs, open what touches the area, and treat a plan that
  contradicts an accepted ADR as a bug.
- Why: the policy only gated writing ADRs. Nothing told an agent to read them, so a planning agent
  opened one by luck and re-proposed already-discarded alternatives.
- Added a numbering-collision guard: re-check the number against the default branch when landing.
- Why: two ADRs both landed as 0012 downstream, which left references-by-number unresolvable.
- Registered the read rule in `setup-aiengineering`'s baseline checklist (v2 → v3), so re-runs on
  older repos detect the gap and offer the rule.

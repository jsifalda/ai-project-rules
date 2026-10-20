# Review tiers

## Classify first

- Classify the change before the first review or verification gate. Judge the diff, not the request.
- Print one line, then continue without waiting: `Review tier: N because <reason>; reply with a tier number to override`.
- Run Phase 4 of `rules/general.md` at every tier.

## Tiers

| Tier | Change | Run |
|---|---|---|
| 0 | Git sync, a merge that meets the repo's integration-only exemption with its evidence, a typo, a doc edit outside rules, skills and `CLAUDE.md`, a README index row, a single config value | The validator and local gates. No review lenses. |
| 1 | Logic in a single skill, a text edit to rules, skills or `CLAUDE.md`, or a small code change | Every review lens that fires, once. After fixes, re-run the local gates only. |
| 2 | A multi-file feature, a cross-repo port, security- or XSS-relevant HTML, tracking or network egress | Every review lens that fires, and the re-review round. |

## CodeRabbit errors

- Never re-run a CodeRabbit run that returned an error. Label it `skipped (CodeRabbit unavailable — <reason>)` and tell the user it happened.
- Run CodeRabbit again in a later re-review round when the tier calls for one.

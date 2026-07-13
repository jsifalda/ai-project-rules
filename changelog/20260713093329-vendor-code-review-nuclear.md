# Vendor code-review-nuclear skill

- Added `skills/code-review-nuclear/` (SKILL.md + references/code-smells.md), vendored from intercom/2x-skills (MIT). Named `code-review-nuclear` locally; upstream calls it `thermo-nuclear-code-review`.
- Generalized so it carries no upstream-only assumptions: every framework/linter/layer named is an explicit example to adapt, and the output-format sample path is stack-neutral. Kept the upstream `metadata:` frontmatter block and added `license: MIT` plus a one-line attribution.
- Why: gives this repo a strict single-axis structural/architectural review lens ("code judo") distinct from the correctness-focused reviewers already here.
- Added the README Skills-table row (`Depends on: —`).

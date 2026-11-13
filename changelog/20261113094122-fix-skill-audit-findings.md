# Fix prompt-audit findings in 12 skills

- Fixed high-confidence prompt-audit findings against Opus 5.5 in `council`, `council-v2`, `summarise-text`, `summarise-url`, `seo-keyword-generator`, `setup-aiengineering`, `hallmark`, `persona-luca`, `distill-notes-v2`, `highlight-key-takeaways`, `setup-notifications` and `frontend-design`.
- `council` and `council-v2`: removed dead memory-file references.
- `summarise-text`, `summarise-url` and `seo-keyword-generator`: replaced asks for reasoning in the output, which can trigger a reasoning-extraction refusal.
- `setup-aiengineering`: symlink direction is now `CLAUDE.md` real, `AGENTS.md` the link.
- `hallmark`: removed dead links from `SKILL.md`, and the version stamp from the preview template and its examples.
- `persona-luca`: removed the WWLD trigger that clashed with `persona-levelsio`.
- `distill-notes-v2`: moved the self-test before the output step.
- `highlight-key-takeaways`: aligned the Tier 2 cap with the per-note caps.
- `setup-notifications`: fixed the hook path clash, absolute path now a `<HOME>` placeholder.
- `frontend-design`: replaced the vague "avoid generic AI look" line with named defaults to avoid.
- Minor version bump in each skill.
- Why: instructions written for older models cause over-triggering and dead references on current ones.

# Drop dead design.md, route frontend design via the skill

- Deleted `rules/design.md`: it was a near-verbatim duplicate of `skills/frontend-design/SKILL.md`, and nothing loaded it (no `CLAUDE.md` names it, Gemini/Copilot only load `general.md`).
- Widened the `frontend-design` skill `description` so it fires on incidental side-project UI, not only explicit design asks, with a guard to defer to an existing repo's own conventions.
- Fixed `README.md` and `CLAUDE.md`: they claimed three `rules/` files always-apply via frontmatter. Corrected to two files, loaded only because `CLAUDE.md`'s First Action names them; frontend aesthetics now point to the skill.
- Why: the always-apply frontmatter was never honored by any loader here, so the docs were misleading and `design.md` was dead weight. The skill's own description is the real router, so widening it beats adding a global rule that would fight `general.md` simplicity-first.

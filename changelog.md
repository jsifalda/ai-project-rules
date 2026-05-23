> **Frozen archive** — do not edit. New entries go in `changelog/` as individual files.

---

20260523T0850 — Refresh docs to match current repo state

• Why: README still described the repo as the original "AI Dev Tasks" fork, ignoring 35 skills, `rules/`, `gemini-cli/`, and the sync hook. `CLAUDE.md` was a 22-line stub.
• What: rewrote `README.md` as a personal monorepo overview (repo layout, skills sync, rules, skills, gemini-cli commands, legacy PRD workflow); expanded `CLAUDE.md` with repository layout, skills-sync architecture, and conventions sections.
• How: structural rewrite of `README.md`; section additions to `CLAUDE.md` (`AGENTS.md` inherits via symlink).

---

20260420T0825 — Add `highlight-key-takeaways` skill

• Why: mark AI-authored highlights in Obsidian notes so they are distinguishable from the user's own.
• What: new skill under `skills/highlight-key-takeaways/` that wraps key takeaways in `==...==` and appends an italic AI-authored marker on edited notes.
• How: single SKILL.md file; no bundled resources; triggers on "highlight key takeaways" / "highlight key learnings" / "mark the important parts".

---

20260414T1842 — Add TDD (mandatory) to rules/general.md

• Why: enforce test-first discipline and improve test quality; prefer E2E for user flows.
• What: added "### TDD (mandatory)" under "## Testing" with Red → Green → Refactor → Commit and Kent Beck's test‑quality desiderata.
• How: inserted new subsection only; no dependencies added.

---

# Add archive folder for retired skills

- Added `archive/skills/` for retired skills. The sync hook reads only `skills/`, so archived skills stay in the repo but no longer load.
- Archived `retro` and `create-implementation-plan`.
- Added the archive steps to `CLAUDE.md` and an `## Archive` table to `README.md`.
- Removed pointers to the archived skills from `distill-insight`, `scripts/synced-skills.txt`, `scripts/sync-mattpocock-skills.sh` and the `CLAUDE.md` identifiers carve-out.
- Exempted `archive/` from the Identifiers rule, and allowed a universality or policy fix inside an archived skill.
- Pointed `distill-insight` Step 9 at its `## Rule text` section, so the skill gives one rule form.
- Why: keep unused instructions for reference without loading them into every session.

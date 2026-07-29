# Merge the universality policy into CLAUDE.md

- Folded `rules/universality.md` into a condensed `## Universality requirement` section in `CLAUDE.md` and **deleted the rule file**.
- Why: nothing in the repo ever loaded `rules/`. The policy reached agents only through a 7-line pointer stub, so the table, scanner usage, and clone setup sat in a file nobody opened. `CLAUDE.md` is already read every session, and `AGENTS.md` symlinks to it.
- Rewrote the one worked example that would have tripped the scanner once the content left the `SKIP_REL` allowlist, so `CLAUDE.md` stays fully scanned. Added a rule against allowlisting files to silence hits.
- Repointed all referrers: `README.md`, `skills/create-skill/SKILL.md`, and the scanner's own header comment and failure message.
- Fixed a contradiction that predates this change: `CLAUDE.md` and `README.md` each described `changelog.md` as a live log in one place and a frozen archive in another. Both now say frozen archive, and both list the `changelog/` directory.
- Documented `scripts/` and `.githooks/` in the repository-layout sections, since the merged policy issues commands from both.

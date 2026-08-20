# Vendor the hallmark design skill

- Copied the `hallmark` skill from `Nutlope/hallmark` into `skills/hallmark/`, pinned at
  commit `13ac0ec7e148655948100b6396439e481361d690`. Upstream licence is MIT.
- Every file matches upstream byte-for-byte. The one exception is `SKILL.md`, which drops
  the `version: 1.1.0` frontmatter line — this repo's skill validator refuses any key
  outside its allowed set, and widening that gate for one skill was not worth it.
- Left the upstream `site/` and `docs/` directories behind. They hold a demo web page and
  its images, which no agent here reads. A known effect is that links from the skill into
  those directories do not resolve. The theme palettes and the diversification axes are
  written inside the copied files, so the skill still works.
- Added the `README.md` skills-table row, and corrected two lines that named
  `frontend-design` as the only design skill. Both now name `frontend-design` for general
  UI work and `hallmark` for anti-generic-AI-look builds, audits, redesigns, and design
  extraction.

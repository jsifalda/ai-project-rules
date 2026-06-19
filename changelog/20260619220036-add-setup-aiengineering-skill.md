# Add setup-aiengineering skill + new-skill incorporation convention

- Landed the `setup-aiengineering` skill (bootstraps a repo's AI-engineering baseline: inject policy blocks, delegate to sibling setup skills, scaffold a worktree hook).
- Added its missing row to the `README.md` skills table to satisfy the README-sync convention.
- Added a `CLAUDE.md` convention: every new skill under `skills/` now triggers a one-question prompt about whether it belongs as a `setup-aiengineering` module, with a short how-to for wiring it in.
- Why: keep the bootstrapper's module menu from silently drifting out of date as new setup/standards skills get added.

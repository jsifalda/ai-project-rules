# Expose repo skills as project-level skills

- Added relative symlink `.claude/skills → ../skills`.
- Makes every skill in `skills/` available as a project-level skill whenever Claude Code runs in this repo, with no per-machine setup.
- Self-maintaining: future skills appear automatically; portable to any clone.

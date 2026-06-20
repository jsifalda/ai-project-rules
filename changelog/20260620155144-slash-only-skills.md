# Make manual-only skills slash-invocation only

- Added `disable-model-invocation: true` to 9 skills so Claude no longer auto-triggers them from a description match. They stay invocable via their `/command`: `ship-pr` (already self-declared manual-only), and the side-effectful ops `setup-aiengineering`, `setup-adrs`, `setup-changelog`, `user-scenarios-setup`, `setup-skills-autorefresh`, `claude-allow-home`, `qmd-project`, `sync-obsidian-skills`.
- Allowed the new field in `skills/create-skill/scripts/quick_validate.py` (the pre-commit validator previously rejected any unknown frontmatter key).
- Documented in `create-skill` when to set the flag (destructive/outward-facing actions and heavy setup/bootstrap ops) and that the default is to leave it unset.
- Why: auto-firing a bootstrap or git-ship skill on a loose natural-language match scaffolds files or mutates config; the cost of not auto-firing is one typed slash command. The asymmetry favors slash-only for these.

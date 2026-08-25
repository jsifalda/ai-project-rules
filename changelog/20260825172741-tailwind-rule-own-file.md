# Move the Tailwind v4 cursor trap into its own rule file

- `rules/tailwind.md` now holds the trap and its `@layer base` fix. `rules/builder.md` names it
  under `## Related rules` and no longer carries the section itself.
- Why: the trap is a stack gotcha, not stack-selection guidance. Keeping it inline made every
  stack-choice load carry it.
- The new file has no trigger of its own. `applyTo` and `paths` are inert for Claude Code, which
  reads a rule file only when a `CLAUDE.md` names it, so the file is reached through `builder.md`.
  `README.md` and `CLAUDE.md` say so plainly rather than promising a wider trigger.
- Known gap, recorded in `builder.md` itself: an existing repo already on Tailwind v4 never loads
  `builder.md`, so it never reaches the rule. Closing that needs a trigger the consuming project
  owns.

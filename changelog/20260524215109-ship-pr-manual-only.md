# Restrict `ship-pr` skill to explicit slash-command invocation

- Rewrote the `description:` frontmatter in `skills/ship-pr/SKILL.md` so the skill no longer auto-triggers on natural-language phrases like "ship this", "open a PR", "create an MR".
- Old "Use when ..." trigger list converted into an explicit ANTI-TRIGGER list, gated by a hard "MANUAL-INVOCATION-ONLY — do NOT auto-trigger" opener.
- Skill body (Phases 1-6, hard rules, failure modes) untouched — only the invocation contract changed.
- Why: the skill was loading itself from incidental chat phrasing; user wants it to fire only on the literal `/ship-pr` slash command.

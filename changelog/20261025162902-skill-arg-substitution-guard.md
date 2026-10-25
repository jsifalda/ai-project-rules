# Guard skills against Claude Code argument substitution

- Braced `$1` in the ship-pr URL helpers. Claude Code replaced it with a skill argument, so a run with two or more arguments aborted with "cannot read host/owner/repo".
- Braced `$0` in a create-skill pitfall and added a pitfall bullet for bare `$<digit>`.
- `quick_validate.py` now rejects a bare `$<digit>` in a SKILL.md body, with regression tests in `skills/create-skill/tests/`, so the bug cannot return.
- Fixed two create-skill statements the prompt audit found wrong: where the universality scanner lives, and what validation checks.

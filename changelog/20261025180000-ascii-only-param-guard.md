# Make the skill argument guard ASCII-only

- Compiled the bare positional parameter check in the `create-skill` validator with `re.ASCII`.
- Why: Claude Code's substitution regex is ASCII-only. Before this fix, the validator passed `$1é` (which Claude Code substitutes) and rejected `$١` (which Claude Code leaves alone).
- Added two regression fixtures for these cases.

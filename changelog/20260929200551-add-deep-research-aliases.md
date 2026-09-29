# Add /dr and /dpa aliases for the deep-research skills

- Added the slash-only skills `dr` and `dpa`. They hand off to `deep-research` and `deep-research-answer` with the arguments unchanged.
- Added their rows to the README skills table.
- Why: short triggers are faster to type on a phone. Claude Code has no alias field for skills, so a thin wrapper skill does the job and the original skills stay unchanged.

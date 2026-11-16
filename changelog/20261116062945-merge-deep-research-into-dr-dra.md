# Merge deep-research skills into dr and dra

- Moved `deep-research` into `dr` and `deep-research-answer` into `dra`, replacing the slash-only wrapper skills.
- Removed the long names. Both skills are now model-invocable, at version 3.0.
- Updated cross-references, `skill_file` paths, script docstrings and README rows.
- Fixed routing between the two: single facts go to `dra`, and `dra` runs both research passes through `dr`, with no built-in research tool needed.
- Why: one name per skill, no wrapper hop, and the model can call the short names on its own.

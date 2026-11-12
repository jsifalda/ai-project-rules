# Add disable-model-invocation column to README skill tables

- Added a last `disable-model-invocation` column to the README `## Skills` and `## Archive` tables: `true` when the skill's frontmatter sets the flag, `—` otherwise.
- Added the missing `setup-notifications` row, so the table lists every skill.
- Synced the column list in the README prose, the CLAUDE.md Conventions bullets, and the row-template hint in the 3 upstream sync scripts.
- Why: a reader can now see at a glance which skills are slash-only by flag, and which are restricted only in their prompt text.

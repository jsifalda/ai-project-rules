# Make agents delete stale lines before adding

- The authoring and docs standards now say to delete or fix wrong, stale or contradicted lines on a topic before adding to it.
- Why: wrong context poisons agents.
- Fixed a wrong `MEMORY.md` reference in `rules/authoring.md` and added the 1024-character hard cap for a skill description.
- Docs rule: a wrong dated record, such as an ADR or changelog entry, is superseded by a new one, never deleted.
- Replaced the worked commit example in `rules/git-ship.md`, which broke the authoring rules, with a rule line for the task-ID position.

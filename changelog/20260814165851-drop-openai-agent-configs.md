# Drop the OpenAI agent configs from the two imported skills

- Deleted `skills/grill-with-docs/agents/openai.yaml` and
  `skills/domain-modeling/agents/openai.yaml`. Upstream ships them for OpenAI agents. This
  repo targets Claude Code, Copilot CLI, Gemini CLI, and Cursor, so nothing here reads them.
- Nothing referenced the two files. Both skills still pass the validator and the universality
  scanner.
- Correction to `changelog/20260814145436-import-grill-with-docs.md`: that entry says
  `grill-with-docs` stays byte-identical to upstream and re-syncs cleanly. That is wrong. The
  `/grilling` to `/grill-me` edit changed its `SKILL.md`, so it is a hand-maintained fork too.
  Both imported skills are forks.
- A future `sync-mattpocock-skills.sh` run skips both skills, because every remaining file
  differs from the sha256 baseline. The deletions hold.
- A run with `--force` restores both deleted files. The script copies every upstream file
  under a skill directory, and its modified-file check reads only files that still exist
  locally, so a deleted file raises no warning. Delete them again after any forced re-sync.

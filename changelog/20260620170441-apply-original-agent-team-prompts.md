# Apply author's original agent-team prompts to the team-* skills

- Replaced the reconstructed prompt bodies with the author's verbatim originals from the X article
  config (writer, reviewer, tester, and the ship lead command).
- Renamed `team-writer` → `team-code-writer` so the role reads clearly as a code writer.
- Made all four skills auto-invocable (removed `disable-model-invocation`).
- Dropped the `handoff.md` scratchpad and `src/`/`tests/` territories — those were narrative-only in
  the article and are not part of the actual shipped prompts.
- Adapted agent/command frontmatter to valid skill keys: `tools:` → `allowed-tools:` (reviewer stays
  read-only), removed the unsupported `model:` key.
- Why: the user supplied the verbatim originals and asked to apply them over the earlier
  reconstruction.
- Also updated the `README.md` skills table to match.

# Move the counts rule to global reach

- The counts rule now lives in `rules/general.md` under `# COUNTS IN INSTRUCTIONS`. It bans a
  statement of how many items a set holds.
- The rule reached only this repo before. It sat in `CLAUDE.md`, which loads only when an agent works
  inside this repo. `rules/general.md` loads in every session in every repo, so the rule now applies
  to all work.
- The rule is not specific to this repo. Any instruction file in any project becomes inconsistent the
  same way when it states a count.
- `CLAUDE.md` keeps a `## Counts` section, but the section is now a pointer. It sends the reader to
  `rules/general.md` and restates no rule. A second full copy would drift from the first, which is
  the failure the rule forbids.
- The version in `rules/general.md` drops the example about this repo. That file loads everywhere, so
  a story about one skill here does not belong in it. The example stays in
  `changelog/20260810085949-drop-brittle-counts.md`.
- This change mirrors the split used for the writing-style rule. `rules/general.md` owns the rule and
  `CLAUDE.md` points at it. The counts rule and the writing-style rule now share that structure.

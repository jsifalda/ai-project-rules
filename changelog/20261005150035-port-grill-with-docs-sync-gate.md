# Port grill-with-docs from upstream and hard-block sync of edited skills

- Hand-ported the upstream grill-with-docs change: it now calls grill-me and domain-modeling through the Skill tool. The local frontmatter stays.
- Took the upstream rename of CONTEXT.md to GLOSSARY.md in domain-modeling, grill-with-docs, better-plan and the README. The local date-slug ADR policy stays.
- Removed `--force` from the mattpocock and anthropic sync scripts. A locally edited skill is now refused and never overwritten.
- Moved the default overwrite baseline to a git-tracked file, `scripts/sync-baselines/<source>.txt`. SKILL.md is hashed without its `metadata` block.
- Why: the old baseline was gitignored and absent on every clone. Every skill then read as modified, and the documented answer was `--force`, which erased deliberate local edits.

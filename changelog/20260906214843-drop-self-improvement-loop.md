# Drop the self-improvement loop from the rule set

- Removed `# SELF IMPROVEMENT LOOP` from `rules/general.md` and its summary bullet from
  `CLAUDE.md`'s Key Rules.
- Why: the section described how one person's agent maintains one private memory store. That is a
  personal workflow, not a universal rule, and this repo is public and universal-by-charter. An
  earlier attempt to rewrite the section in place was reverted after review found it encoded a
  machine-specific constraint as a universal one.
- The content now lives in the author's private agent config, merged with the memory rules it
  already duplicated.
- Accepted tradeoff: consumers that read `general.md` without that private config (Copilot CLI,
  Gemini CLI) no longer get the "persist a lesson after a correction" instruction.

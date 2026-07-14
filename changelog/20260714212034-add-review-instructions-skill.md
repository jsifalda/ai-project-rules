# Add the review-instructions skill

- New slash-only skill that rewrites a project's agent instruction file (`CLAUDE.md`/`AGENTS.md`) as the operating manual a less capable model would need to work at the level of the model doing the rewrite.
- Why: instruction files get written by a strong model for a strong model. They record decisions but not the traps, not the bar, and not what to do when the file runs out of answers. Hand one to a weaker model and it fails in ways the file never anticipated.
- Demands four sections in the output — conventions with a proving anchor, named failure modes each carrying the one rule that prevents it, a quality bar per deliverable as checkable criteria with adjectives banned, and escalation rules as `if <observable trigger> → <closed-set action>`.
- Ships a coverage ledger so a rewrite cannot silently drop a live rule, which is the worst outcome the skill could produce.
- Gated to the project root and prompted onto Fable, since the model doing the writing is the thing being distilled.
- Drafts to `<TARGET>.review.md` and replaces the original only on explicit approval.
- Closes a real gap: several skills here write policy *into* instruction files, none read one back.

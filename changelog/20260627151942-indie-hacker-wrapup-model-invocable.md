# Allow model invocation of the `indie-hacker-wrapup` skill

- Removed `disable-model-invocation: true` from the `indie-hacker-wrapup` skill frontmatter.
- The flag marked the skill user-invoke-only, so the Skill tool refused to launch it — it only ran when typed as `/indie-hacker-wrapup`. Now the model can invoke it directly.
- The slash-command path still works; only the model-invocation restriction is lifted.
- Mirrors the earlier `op` change. The global CLAUDE.md "offer only, never auto-run" wrap-up rule is deliberately left as-is, so end-of-session behavior is unchanged.

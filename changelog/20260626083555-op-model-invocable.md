# Allow model invocation of the `op` skill

- Removed `disable-model-invocation: true` from the `op` skill frontmatter.
- The flag marked the skill user-invoke-only, so the Skill tool refused to launch it — it only ran when typed as `/op`. Now the model can invoke it directly (e.g. right after plan mode, to route a plan across models).
- The slash-command path still works; only the model-invocation restriction is lifted.
- Same change applied to the sibling `opusplan` skill, which lives outside this repo (in `~/.agents`).

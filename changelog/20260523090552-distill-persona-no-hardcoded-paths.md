# distill-persona: drop preset skill paths, always ask user

- Removed the three hard-coded preset paths from Step 6 (`~/instructions/skills/`, `~/mofa/ai-prompts/.agents/skills/`, `~/mofa/gemini/skills/`). The skill now asks the user for an absolute path in plain chat instead.
- Made the closing "auto-sync will pick it up" line conditional — only mention it when the chosen path actually is an auto-sync source.
- Reason: aligns the skill with the new repo-wide universality requirement (no personal directory layouts checked in).

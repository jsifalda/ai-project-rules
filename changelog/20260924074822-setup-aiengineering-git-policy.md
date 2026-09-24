# setup-aiengineering: local-commit git policy, drop the writing-style module

- The injected Git Policy now lets the agent commit locally when a task passes verification, without asking. Push only on a user instruction. Never force-push, even when asked.
- Removed the Git Policy exception bullet for the Commit gate, because the base policy now grants the local commit.
- Removed the writing-style (ASD-STE100) module and deleted `skills/setup-aiengineering/references/writing-style.md`. Existing target repos keep their injected section.
- Why: the user wants agents to commit finished work locally and leave every push to the user. The global rules already define the writing style, so the module was a duplicate.
- Skill version stays v15. The Git Policy change is forward-only: an existing repo gets it only on a manual re-run.
- Review fixes: the Claude Code tool name in the review lenses is now `Agent`, and the verification block no longer claims "no exceptions" next to its own exemptions.

# setup-aiengineering: offer `/install-github-app` as a final step

- Added a final Step 9 to the `setup-aiengineering` skill: when the skill runs inside Claude Code
  on a GitHub-hosted repo that isn't already wired, it suggests the user run `/install-github-app`
  to set up the Claude GitHub App (`@claude` on issues/PRs + automatic PR review).
- Gated on the `CLAUDECODE=1` env var plus a GitHub-remote and not-already-installed check, so it
  stays silent on other agents (Copilot CLI, Gemini CLI, Cursor) and non-GitHub repos.
- Why: the local baseline setup ended without helping the user wire up CI-side Claude automation,
  which only Claude Code's built-in command can do — this closes that gap without the skill
  performing an action it can't (a user slash command).

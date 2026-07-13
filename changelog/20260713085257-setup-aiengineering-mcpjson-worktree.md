# setup-aiengineering: carry `.mcp.json` into new worktrees

- Step 7 `.worktreeinclude` probe now detects a gitignored `.mcp.json` and always carries it over.
- Added Step 7b: when a repo has no `.mcp.json`, inject a one-line reminder into the agent
  instructions (gitignore it + add to `.worktreeinclude` when one is introduced).
- Synced the Rules bullet and Step 8 report line to mention `.mcp.json`.
- Why: project `.mcp.json` (local MCP servers, e.g. Playwright MCP) is gitignored, so Claude-created
  worktrees silently lost it — Playwright MCP disappeared in every new worktree. Surfaced in
  signalseek-v2, whose own `.worktreeinclude` + `.gitignore` were fixed in the same session.

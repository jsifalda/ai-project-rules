# Add agent-team workflow skills (team-writer/reviewer/tester/ship)

- Added four slash-only skills under `skills/` that reconstruct the 4-role Claude Code "agent team"
  config from @zodchiii's X article: `team-writer` (builds in `src/`), `team-reviewer` (read-only,
  no fixing), `team-tester` (spec-first, in `tests/`), and `team-ship` (lead orchestrator).
- `team-ship` writes a shared brief, assigns non-overlapping territories, spawns the three roles as
  subagents through a `handoff.md` scratchpad, and gates the merge on human approval.
- Why: a single agent can't catch its own mistakes — separating writer, reviewer, and tester into
  narrow roles with tight tools removes the self-review blind spot. Packaged as repo skills so the
  workflow is reusable in any project.
- The X article's verbatim code was login/anti-scrape locked, so the prompts are faithful
  reconstructions from the post's narrative, not character-for-character copies.
- Also updated the `README.md` skills table with the four new rows.

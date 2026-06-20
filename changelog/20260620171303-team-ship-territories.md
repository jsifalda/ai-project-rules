# team-ship scaffolds agent territories into the project's rules

- Added a first step to the `team-ship` skill: before dispatching the roles, ensure the project's
  agent-rules file (AGENTS.md → CLAUDE.md → .claude/CLAUDE.md, creating CLAUDE.md if none) carries
  an `## Agent territories` section, appended only if not already present.
- Why: the roles run in parallel, so the project needs a written territory contract (writer owns
  `src/`, tester owns `tests/`, reviewer read-only, cross-area work via `handoff.md`) for the
  subagents to stay in their lanes. The rule was in the source article's narrative but not in the
  prompts.
- Also updated the `README.md` team-ship row.

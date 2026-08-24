# Rename qa-user-scenarios to verify-user-scenarios, and close its review findings

- Renamed the skill to `verify-user-scenarios` — directory, frontmatter name, slash trigger,
  heading, and the README row. `qa-` named a job title, not what the skill does. Nothing had
  shipped under the old name, so the rename was free now and expensive later.
- Closed every CodeRabbit finding on PR #146. Four were internal contradictions where the skill
  told an agent two different things in two places — the Phase 4 step contract, the database
  allowlist, the evidence-filename rule, and the report's part list against the report template.
- Tightened two safety rules. The database reset now needs an explicit yes every time, because a
  warning is not consent and the wipe is the only irreversible thing the skill does. The privacy
  check now masks the matched value instead of printing the surrounding text, which was copying
  real names and addresses into chat and into the persisted receipt file.
- Gave the report template the fields the skill already mandated — preflight result, database
  target, reset and seed status, Playwright MCP status, and a status line per phase.
- Left the database guard on a plain host allowlist. The SSH-tunnel hardening idea is wider than
  this change, and the owner chose to leave it.

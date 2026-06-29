# Add better-plan chained planning skill

- Added `skills/better-plan/SKILL.md`, a slash-only skill that runs one planning pass in four stages: build a plan with plan-mode rigor, stress-test it by delegating to `grill-me`, cost-route the tasks by delegating to `op`, then present the routed plan and execute on approval.
- Added the matching row to the `## Skills` table in `README.md`.
- Why: running plan → grill → route by hand is friction and easy to skip. One command makes every plan come out grilled and cost-routed by default.

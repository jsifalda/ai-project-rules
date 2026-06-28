# Add goal-breakdown skill

- Added `skills/goal-breakdown/` — decomposes a big finite goal into a sharp end state, ordered milestones (riskiest first), and one-day tasks with a single next action; supports a Continue mode to re-plan as milestones complete.
- Genericized the description's cross-reference to another skill (was naming `summarise-url`) to avoid rename coupling and keep the skill portable.
- Updated the README skills table with the new row.
- Why: gives a reusable, opinionated breakdown method for turning stuck-feeling goals into a startable plan.

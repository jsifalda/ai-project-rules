# setup-analytics: Title Case project name and a confirm gate

- Derive the project name from the origin repo name, with a main-checkout fallback, and convert it to Title Case (`kasese-risk-map` → `Kasese Risk Map`).
- Always ask the user to confirm the project name before the plan table and before any console form is submitted.
- Why: the skill copied the slug with spaces into Clarity and GA, and a linked worktree gave the worktree name instead of the project name.

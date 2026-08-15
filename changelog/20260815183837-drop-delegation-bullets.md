# Drop the delegation bullets from the four setup-* skills

- Removed the `## When to use` bullet that named the caller from `setup-adrs`, `setup-changelog`,
  `setup-user-scenarios`, and `setup-todo-backlog`. All four now list user intent only.
- Why — a `## When to use` list tells the agent when to reach for the skill. A caller does not
  reach for it that way. `setup-aiengineering` Step 6 already names each skill it delegates to, and
  so does `domain-modeling` through `ADR-FORMAT.md`. The bullet repeated the caller's own wiring
  inside the callee, where it could drift without anything catching it.
- This supersedes the line in `changelog/20260815182342-relax-setup-skill-invocation.md` that says
  each skill gained a bullet for its delegation route. That entry stays as written.
- `setup-todo-backlog` lost a bullet that predates this branch — "A setup or bootstrap flow
  delegates backlog provisioning to this skill". It was the same kind of statement, so it went with
  the other three. All four `## When to use` lists now have the same shape.
- No change to any `description`, and none to the delegation itself. `setup-aiengineering` Step 6
  still reaches all four, because none of them carries `disable-model-invocation`.

# Take the `op` routing stage out of `/better-plan`

- Deleted `better-plan`'s Stage 3, which handed the plan to the `op` skill to assign each task a
  model tier, and rewrote the old Stage 4 so the approved plan executes inline in the session
  instead of being dispatched to subagents.
- The workflow is now four stages — build, grill, execute, ship — after the enhance preface, with
  the ship stage still conditional. Renumbered every stage and every cross-reference, including the
  one in `skills/ship-pr/SKILL.md` that named `better-plan` Stage 5 as its dependent entry point.
- Dropped `op` from the skill's `description` and from its `Depends on` cell in the README.
- Why: the routing stage made the flow pay a decomposition and dispatch step on every run, and the
  user wants the plan executed directly.
- `skills/op/` is untouched. `/op` still works on its own and keeps its README row.

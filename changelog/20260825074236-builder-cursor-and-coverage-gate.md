# Tailwind v4 cursor rule, and one merged tests-and-coverage gate

- `rules/builder.md`: record the Tailwind v4 preflight change that dropped `cursor: pointer` from
  buttons, with the single `@layer base` fix. Per-component `cursor-pointer` utilities hide the bug
  in each new component instead of fixing it once.
- `setup-aiengineering`: merge the separate Tests and Test coverage gates into one **Tests and
  coverage** gate. The coverage command already runs the same tests, so a second bare test run
  costs time and checks nothing new.
- The merge needs the subsumption to be true, so the coverage command must now derive from the
  configured test script. A hand-built command can bypass config, projects, or filters the script
  carries.
- A repo can have a test framework and no coverage tool. That state now has an owner: a Step 5
  branch that offers to wire one, and a written degraded form of the gate to inject when the user
  declines.

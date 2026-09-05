# Add a prompt-audit lens to the verification gate

- `## Verification Protocol` gains another Step 2 lens — the `claude-api` skill's `prompt-audit`
  subcommand. It fires only when the diff touches an agent-facing prompt, and it reads each
  touched file whole.
- Ported the same audit into `create-skill`, so a newly authored skill is checked before it is
  reported done.
- **Why:** CodeRabbit and the `code-review` agent both look for code defects. Neither knows what
  prompt decay looks like — a pinned model id, a deprecated parameter shape, an instruction a
  current model no longer needs. In this repo the prompts are the product, so that class of
  defect shipped silently and stayed.
- Its findings run through the existing Step 4 triage, so the normative carve-out still holds: a
  finding that would rewrite what a rule requires is drafted and shown, never auto-applied.
- Reworded the Step 2 to Step 5 lens counts to set language, per `# COUNTS IN INSTRUCTIONS`.
  Adding a lens made every "both lenses" wrong.
- Not applied retroactively — the lens was not run against the existing skills in this change.

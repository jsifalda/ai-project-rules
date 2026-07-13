# Add 5c nuclear review + skill provenance note to setup-aiengineering

- Added step 5c (nuclear structural review) to the verification-protocol template: a subagent
  running the `code-review-nuclear` skill, guarded as optional/skip-if-unavailable, alongside 5a and
  5b. Merge now waits for all three before deduping.
- `setup-aiengineering` now stamps a visible italic provenance note above the policy sections it
  injects, so readers know those blocks were skill-generated and are re-run-managed.
- Why: add a structural/maintainability review lens beyond correctness, and make generated policy
  blocks traceable to their source skill.

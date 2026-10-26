# Add generate-user-scenarios skill

- New `generate-user-scenarios` skill derives BDD Given/When/Then scenarios from a PRD, or any problem-and-solution source, and writes them into the PRD as a `## User Scenarios` section.
- `setup-user-scenarios` offers to seed existing PRDs that have no scenarios yet, and its injected policy copies the scenarios a change implements into the inventory.
- `setup-aiengineering` PRD gate runs the generator before planning (baseline v21). Its Rules section now keeps only rules stated nowhere else, and new Step 6a restores the ADR scope rows after `setup-adrs` creates their files.
- Why: scenarios were written by hand after code shipped. Now they come from the PRD before the plan, so they define what gets built.

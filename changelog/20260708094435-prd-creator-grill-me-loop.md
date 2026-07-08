# prd-creator offers an optional grill-me pressure-test

- Added Core Workflow step 6: after a PRD is saved, offer to stress-test it with the grill-me skill, let the user iterate, then fold the resolved decisions back into the saved PRD (confirmed before writing).
- Guarded the reference: if grill-me is not available, the step is skipped silently, so the skill stays portable for public-repo readers.
- Marked grill-me as an optional dependency in the README skills table.
- Why: catch weak assumptions and unresolved decisions before any code gets written.

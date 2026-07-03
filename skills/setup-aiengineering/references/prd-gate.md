# PRD Gate Template

Inject the section below into the project's agent instructions file. Copy it verbatim. It has no
`{{...}}` placeholders — PRDs live at `docs/prds/`, the path the `/prd-creator` skill writes to.

---

## PRD Gate

Substantial new features start from a Product Requirements Document (PRD). This keeps implementation
grounded in the business problem and its users, not just the code.

**What counts as substantial** — a new user-facing capability, a new subsystem or integration, or a
multi-file effort that changes what the product does. Bug fixes, refactors, small enhancements, copy
tweaks, config, and chores are exempt. Do not gate them.

**Before building a substantial feature:**

1. **Require a PRD first.** If the feature has no PRD under `docs/prds/`, do not start implementing.
   Prompt the user to create one with the `/prd-creator` skill. If `/prd-creator` is not installed in
   this environment, tell the user and ask them to add it before proceeding — do not hand-roll a
   substitute.
2. **Draft the plan from the PRD.** Once the PRD exists, use it as the source for the implementation
   plan. Scope, functional requirements, and success signals come from the PRD, not a fresh guess.

**Before starting ANY implementation plan**, read every PRD under `docs/prds/*.md` for business
context, so the work reflects the product's goals, constraints, and prior decisions — not just the
immediate request.

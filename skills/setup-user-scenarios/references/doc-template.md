# {{PROJECT_NAME}} User Scenarios

> Canonical inventory of every user-facing scenario this app supports. Every
> new feature MUST add a scenario here. See the project's agent instructions
> file (`AGENTS.md` or `CLAUDE.md`) → User Scenarios for the rule.

## Conventions

- **Stable IDs**: `<DOMAIN>-<NN>` (e.g. `AUTH-01`, `BILLING-04`). IDs are
  immutable. When a scenario is removed, retire the ID — never reuse.
- **One scenario per ID** — don't bundle multiple Given/When/Then bodies.
  Edge cases and error paths get their own IDs.
- **`Verified by:`** — every scenario carries a pointer to the test that
  proves it. Use `TODO` when no test exists yet; those surface in the
  Coverage Matrix as gaps and become follow-up tasks.
- **Domain prefixes (frozen)**: {{DOMAIN_LIST}}. To add a new domain, update
  the list above AND the matching list in the project's agent instructions.
- **Source paths** are informational only; `Verified by:` paths must resolve
  to a real test file in the repo.

### Scenario voice

The Given/When/Then body describes what a *user perceives*, not what the code
does. Apply these rules to every scenario body:

1. **No code symbols in the body.** No function names, error class names, JSON
   field names, HTTP status codes, SQL identifiers, table or column or index
   names, env var names. If a reader has to grep the codebase to follow the
   scenario, it's wrong.
2. **No HTTP verbs or route paths.** "When they POST /api/foo with {x}" →
   "When they submit the form" or "When they click X." The HTTP layer is an
   implementation detail.
3. **Outcomes are what the user sees.** "They see a message explaining…",
   "They land on the dashboard.", "The campaign is paused and won't fetch new
   content." Not "status flips to PAUSED" or "the API returns 409."
4. **`Source:` and `Verified by:` stay technical.** Code paths belong on those
   lines, not in Given/When/Then.

Example — same behaviour, two voices:

- ❌ **Then** `assertCanCreateCampaign` throws `AccessError` with code
  `CAMPAIGN_LIMIT_REACHED`
- ✅ **Then** they see a message that they've reached their plan's limit, with
  a link to upgrade

When a status, tier, or enum name contains an underscore (e.g. `PAST_DUE`,
`CAMPAIGN_LIMIT_REACHED`), rewrite it as prose the user would read on screen
("past due", "their plan's campaign limit"). Single-word status names like
ACTIVE or tier names like STARTER are allowed.

---

{{SEEDED_SCENARIOS}}

---

## Coverage Matrix

| ID            | Verified by                                                                       |
| ------------- | --------------------------------------------------------------------------------- |
{{COVERAGE_MATRIX_ROWS}}

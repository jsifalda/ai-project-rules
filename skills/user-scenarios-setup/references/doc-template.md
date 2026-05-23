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

---

{{SEEDED_SCENARIOS}}

---

## Coverage Matrix

| ID            | Verified by                                                                       |
| ------------- | --------------------------------------------------------------------------------- |
{{COVERAGE_MATRIX_ROWS}}

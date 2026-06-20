## User Scenarios

`docs/user-scenarios.md` is the canonical BDD-formatted inventory of every user-facing scenario this app supports. It **MUST be kept in sync** whenever user-visible behavior changes — new page, new API endpoint, new UI flow, new business rule, new tier gate, new email, new error path.

### Rules

- **Stable IDs**: `<DOMAIN>-<NN>` (e.g. `AUTH-01`). IDs are immutable. When a scenario is removed, retire the ID — **never reuse retired IDs**.
- **One scenario per ID** — edge cases and error paths get their own IDs, not extra Given/When/Then bodies under one ID.
- **Every scenario has Given / When / Then steps** plus a `Verified by:` line pointing to a real test file (or `TODO` when no test exists yet). `TODO` entries are gaps that become follow-up tasks.
- **User-facing voice in bodies** — Given/When/Then describes what the user perceives, not the code. No function names, error class names, HTTP verbs, route paths, status codes, or DB identifiers in the body. Full rules: `docs/user-scenarios.md` → Conventions → Scenario voice.
- **Coverage Matrix sync**: every scenario must appear in the `## Coverage Matrix` table at the bottom of the doc with the same ID. No orphan rows in the matrix; no scenarios missing from it.
- **Frozen domain prefixes**: {{DOMAIN_LIST}}. To add a new domain, update both `docs/user-scenarios.md`'s Conventions section AND this list.

### When adding or modifying user-facing behavior

1. Add or update a scenario in `docs/user-scenarios.md` with a stable `<DOMAIN>-<NN>` ID and Given/When/Then steps **written in user-facing voice** (see Conventions → Scenario voice).
2. Add a `Verified by:` line pointing to a real test file under the project's source tree, or `TODO` if no test exists yet (then create a follow-up task).
3. Append (or update) the matching row in the Coverage Matrix.

Changes solely to `docs/user-scenarios.md` are documentation-only and skip code verification protocols.

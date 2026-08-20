# ADR Policy Template

Inject the section below into the project's agent instructions file (AGENTS.md or CLAUDE.md).
Copy it verbatim. If the project uses an ADR directory other than `docs/adr/`, substitute the
chosen path everywhere before injecting.

---

## ADRs (Architecture Decision Records)

Record meaningful technical decisions as ADRs in `docs/adr/`. ADRs inject judgment by example —
future agents read them, stay true to past choices, and supersede what's stale.

### Read the ADRs before you plan

- Read `ARCHITECTURE.md` first — the current-state recap, so you don't have to read every ADR
  (tiered on purpose: ADR count grows without a cap).
- Scan `docs/adr/` filenames — the slugs are the index. Open ADRs touching the area you're
  changing, plus any `ARCHITECTURE.md` links from the sections you're touching.
- Open the ADR itself for the *why* — discarded alternatives and their grounds — not just the
  recap; that's what stops you proposing one of them again.
- A plan that contradicts an accepted ADR without superseding it is a bug. Supersede a genuinely
  stale ADR (see *How to create one*); never silently work around it.

### When to create an ADR

- A decision made **with alternatives** — one path chosen, others discarded for reasons not
  obvious from the code.
- A **new pattern, abstraction, dependency, or direction** the codebase lacked.
- It **reverses or replaces** an earlier decision → write a new ADR and supersede the old one.
- A future reader (human or AI) would otherwise have to reconstruct the reasoning and might get
  it wrong.

### When NOT to create an ADR

- Reusing a **proven pattern** already well understood — no novelty, no real choice.
- Mechanical or no-decision changes (e.g. adding an obvious menu action).
- Worthiness is independent of work size — judge the novelty of the decision, not the size of
  the ticket. When in doubt, skip the noise.

### How to create one

1. Copy `docs/adr/0000-template.md` → `docs/adr/YYYY-MM-DD-short-slug.md` (today's date, 2–5
   word kebab-case slug) — the `YYYY-MM-DD-slug` stem is the ADR's permanent identity, referenced
   and superseded by other ADRs. Parallel branches pick different slugs so they never collide on
   merge; a merged ADR is never re-dated (inbound references would break).
2. Fill in Context, Decision, Options considered (incl. discarded + why), Consequences,
   Supersedes/Superseded-by.
3. Set Status (Proposed → Accepted). If it replaces an older ADR, mark that one
   `Superseded by YYYY-MM-DD-slug` (the new ADR's stem).

**Budget: 250 words for the whole file — a cap, not a target.** Add 20 words per option past
three. Context 50 · Decision 70 · Options 20 each · Consequences 40 · Supersedes 15. Over the
cap, cut words, never a discarded option. **Why** over how. Never delete an old ADR; supersede
it.

### Recap doc (ARCHITECTURE.md)

- `ARCHITECTURE.md` is the 10,000ft view **derived from the ADRs** — keep it current so agents
  grasp the system without reading every ADR.
- After an ADR introduces or supersedes a cross-cutting decision, update the matching section of
  `ARCHITECTURE.md` and link the ADR.
- ADRs hold the *why* and the discarded options; `ARCHITECTURE.md` holds only the
  **current state**.

---

**Note for skill user**: If the project does not want the recap doc, drop the
`### Recap doc (ARCHITECTURE.md)` subsection and step 1 of `### Read the ADRs before you plan`
(scanning `docs/adr/` stands alone). If the ADR directory is not `docs/adr/`, substitute the
chosen path in every reference above.

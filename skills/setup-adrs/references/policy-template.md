# ADR Policy Template

Inject the section below into the project's agent instructions file (AGENTS.md or CLAUDE.md).
Copy it verbatim. If the project uses an ADR directory other than `docs/adr/`, substitute the
chosen path everywhere before injecting.

---

## ADRs (Architecture Decision Records)

Record meaningful technical decisions as ADRs in `docs/adr/`. ADRs inject judgment by example:
future agents read them, stay true to past choices, and supersede what's stale — instead of
re-deriving the same reasoning each time.

### When to create an ADR

Create one when the decision is worth remembering the next time a similar problem comes up —
anything genuinely new in how the system is built:

- A meaningful decision made **with alternatives** — one path chosen, others discarded for
  reasons not obvious from the code.
- It introduces a **new pattern, abstraction, dependency, or direction** the codebase lacked.
- It **reverses or replaces** an earlier decision → write a new ADR and supersede the old one.
- A future reader (human or AI) would otherwise have to reconstruct the reasoning and might
  get it wrong.

### When NOT to create an ADR

- Reusing a **proven pattern** already well understood — no novelty, no real choice.
- Mechanical or no-decision changes (e.g. adding an obvious menu action).

Decision-worthiness is **independent of the size of the work**: a large task can carry zero new
direction (skip); a small one can introduce an interesting pattern (record it). Judge the
novelty of the decision, not the size of the ticket. When in doubt, skip the noise.

### How to create one

1. Copy `docs/adr/0000-template.md` → `docs/adr/NNNN-short-slug.md`, where `NNNN` is the next
   zero-padded sequential number and the slug is a 2–5 word kebab-case summary.
2. Fill in Context (why), Decision (what), Options considered (incl. discarded + why),
   Consequences, and Supersedes/Superseded-by.
3. Set Status (Proposed → Accepted). If it replaces an older ADR, mark that one
   `Superseded by ADR-NNNN`.

Keep it concise — **why** over how. Never delete an old ADR; supersede it.

### Recap doc (ARCHITECTURE.md)

`ARCHITECTURE.md` is the 10,000ft view **derived from the ADRs** — keep it current so agents
grasp the system without reading every ADR. After an ADR introduces or supersedes a
cross-cutting decision, update the matching section of `ARCHITECTURE.md` and link the ADR.
Individual ADRs hold the *why* and the discarded options; `ARCHITECTURE.md` holds only the
**current state**.

---

**Note for skill user**: If the project does not want the recap doc, drop the
`### Recap doc (ARCHITECTURE.md)` subsection. If the ADR directory is not `docs/adr/`,
substitute the chosen path in every reference above.

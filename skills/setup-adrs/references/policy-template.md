# ADR Policy Template

Inject the section below into the project's agent instructions file (AGENTS.md or CLAUDE.md).
Copy it verbatim. If the project uses an ADR directory other than `docs/adr/`, substitute the
chosen path everywhere before injecting.

---

## ADRs (Architecture Decision Records)

Record meaningful technical decisions as ADRs in `docs/adr/`. ADRs inject judgment by example:
future agents read them, stay true to past choices, and supersede what's stale — instead of
re-deriving the same reasoning each time.

### Read the ADRs before you plan

ADRs only pay off if they get read. **Before starting any implementation plan:**

1. Read `ARCHITECTURE.md`. It is the current-state recap of every cross-cutting decision.
2. Scan the filenames in `docs/adr/`. The slugs are the index. Open the ADRs that touch the
   area you are about to change, plus any ADR that `ARCHITECTURE.md` links from the sections
   you are touching.

Open the ADR itself, not just the recap, when you need the *why*. The recap tells you what the
current state is. The ADR tells you which alternatives were discarded and on what grounds,
which is what stops you proposing one of them again.

A plan that contradicts an accepted ADR without superseding it is a bug. If the ADR is
genuinely stale, say so and supersede it (see *How to create one*). Never silently work
around it.

Tiered on purpose, not "read every ADR": ADR count grows without a cap, and `ARCHITECTURE.md`
was built to spare exactly that read.

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

1. Copy `docs/adr/0000-template.md` → `docs/adr/YYYY-MM-DD-short-slug.md`, where `YYYY-MM-DD` is
   today's date and the slug is a 2–5 word kebab-case summary. The `YYYY-MM-DD-slug` stem is the
   ADR's permanent identity — other ADRs reference and supersede it by that stem.
   Parallel branches pick different slugs, so they never collide on merge. Never re-date a merged
   ADR — inbound references point at the full stem and would break.
2. Fill in Context (why), Decision (what), Options considered (incl. discarded + why),
   Consequences, and Supersedes/Superseded-by.
3. Set Status (Proposed → Accepted). If it replaces an older ADR, mark that one
   `Superseded by YYYY-MM-DD-slug` (the new ADR's stem).

Keep it concise — **why** over how. Never delete an old ADR; supersede it.

### Recap doc (ARCHITECTURE.md)

`ARCHITECTURE.md` is the 10,000ft view **derived from the ADRs** — keep it current so agents
grasp the system without reading every ADR. After an ADR introduces or supersedes a
cross-cutting decision, update the matching section of `ARCHITECTURE.md` and link the ADR.
Individual ADRs hold the *why* and the discarded options; `ARCHITECTURE.md` holds only the
**current state**.

---

**Note for skill user**: If the project does not want the recap doc, drop the
`### Recap doc (ARCHITECTURE.md)` subsection and step 1 of `### Read the ADRs before you plan`
(scanning `docs/adr/` stands alone). If the ADR directory is not `docs/adr/`, substitute the
chosen path in every reference above.

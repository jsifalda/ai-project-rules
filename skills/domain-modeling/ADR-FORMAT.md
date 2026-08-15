# ADR Format

## Which format to use

The repo can already have its own ADR system. Use it when it does. Check in this order and stop
at the first match.

1. **An ADR template exists.** Look in `docs/adr/`, `doc/adr/`, `adr/`, and
   `docs/architecture/decisions/` for a `0000-template.md`. Copy it for the new ADR, and write
   into that same directory. Obey the repo's `## ADRs` policy, and update `ARCHITECTURE.md` if
   the policy names one.
2. **An `## ADRs` section exists in `AGENTS.md`, `CLAUDE.md`, or `.claude/CLAUDE.md`.** Obey it.
   It gives the directory, the filename form, and the body format.
3. **Neither exists, and the `setup-adrs` skill is available.** Tell the user the repo has no ADR
   system, and ask before you install one. `setup-adrs` writes several files and adds a policy
   section to the agent-instructions file, so it must not run as a silent side effect of one ADR.
   Use the template it writes.
4. **Neither exists, and `setup-adrs` is not available.** Use the minimal format below.

Search every listed path before you go to step 3. A repo that keeps ADRs somewhere other than
`docs/adr/` still has an ADR system, and telling the user it has none is wrong.

A missing `setup-adrs` never blocks the ADR. Step 4 always works.

The `## Minimal format`, `## Template`, `## Optional sections`, and `## Naming` sections below
apply to step 4 only. `## When to offer an ADR` applies to all four steps — whether a decision
deserves an ADR is independent of which format writes it.

## Minimal format

ADRs live in `docs/adr/` and use date-plus-slug filenames: `YYYY-MM-DD-slug.md`.

Create the `docs/adr/` directory lazily — only when the first ADR is needed.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why* — not in filling out sections.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by YYYY-MM-DD-slug`) — useful when decisions are revisited
- **Considered Options** — only when the rejected alternatives are worth remembering
- **Consequences** — only when non-obvious downstream effects need to be called out

## Naming

Filenames are `YYYY-MM-DD-slug.md`, where the date is the day you write the ADR. The date-plus-slug
pair is the identity — chosen from local information only, so parallel authors never collide. No
counter, no scanning for the highest number, no renumbering. The name is permanent once the ADR
lands; supersede a stale ADR instead of re-dating it.

## When to offer an ADR

All three of these must be true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If a decision is easy to reverse, skip it — you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."

### What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library — just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was deliberate.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it — otherwise someone will suggest GraphQL again in six months.

# Agent-Instructions Scope Template

Inject the block below at the **very top** of the project's agent instructions file, above the
provenance note and above every `##` section. Copy it verbatim, except for the substitutions named
under `## Substitutions` at the bottom.

This block is **always injected** — it is not a deselectable module. It governs the file this skill
creates, so a target repo never gets one without it.

**Idempotent.** If a block containing the line `This file is agent instructions only.` is already at
the top of the file, update it in place instead of adding a second copy.

---

**This file is agent instructions only.** Every line in it must be something an agent has to know in
*every* session to act correctly — a command, a gate, a convention, a trap warning. Everything else
lives in its own document, and this file points at it.

| Content | Home |
|---|---|
| What the product is, how to run it, dev commands, usage | `README.md` |
| How the system is built, its structure, its current state | `ARCHITECTURE.md` |
| Why a decision was made, the discarded options, the full context of a trap | `docs/adr/` |
| A rule, a gate, a convention, or a read-first pointer | **here** |

**The test is not "does it instruct?" — an unbounded list of project facts can be written as
imperatives and still not belong.** The test is: *would a new agent have to act differently in every
session without this line?* A rule passes. A body of knowledge does not, however imperative its
wording.

**Point, do not copy.** A pointer is itself a rule, so it belongs here — but write it as a directive
that names its trigger, never as a bare link:

```markdown
## Architecture

Read `ARCHITECTURE.md` before planning any change. A plan that contradicts an accepted ADR
without superseding it is a bug.

## Gotchas

Read the ADRs in `docs/adr/` before editing <the areas that bite in this repo>.
The ADR slugs are the index.
```

Never restate here what another document already owns. A second copy is a hand-maintained sync that
loses, and the reader who finds the stale copy trusts it.

---

## Substitutions

- **`ARCHITECTURE.md`** — keep it only when the ADR module ran and that file exists. If it does not,
  drop its row and merge its content home into `README.md`. Never point a rule at a file the repo
  does not have.
- **`docs/adr/`** — use the ADR directory the ADR module actually chose. If no ADR system was set
  up, drop that row too, and route trap context to `ARCHITECTURE.md`, else `README.md`.
- **`<the areas that bite in this repo>`** — name real areas, from what the repo evidences. With
  nothing to name yet, omit the whole `## Gotchas` example; a pointer to an empty ADR directory
  teaches an agent to ignore pointers.

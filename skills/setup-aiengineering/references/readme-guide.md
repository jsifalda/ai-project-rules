# README Guide — the root README, its goal statement, and its docs index

Use this when scaffolding or updating the target repo's root `README.md`. The README does two jobs
and only two: it states **what the project is for**, and it **indexes the docs** the other modules
created. Everything else (tech stack, dev commands, project structure) belongs in `AGENTS.md` — do
not duplicate it here.

This runs after the doc-system delegation, so the index reflects what actually landed, not what was
selected.

## Goal capture

The README never ships an unconfirmed guess. **Every hit except hit 2 ends in user confirmation** —
hit 2 reuses prose the user already wrote and writes nothing back, so there is nothing to confirm.

Walk the cascade and **stop at the first hit**:

1. **`AGENTS.md` `Project Overview`** — any overview counts, whether Step 3 backfilled it this run or
   it predates the run. A fresh backfill is grounded in the implementation; an older one may itself be
   stale, which is exactly what the contradiction check on the merge path is for. Reuse it rather than
   re-deriving.
2. **Existing root README** — its H1 **and** the first paragraph above the first `##`. Both are
   required: a bare H1 is a name, not a statement of purpose, so a README whose first `##` follows
   straight after the title misses this hit and the cascade continues.
3. **Manifest `description`** — `package.json`, `pyproject.toml`, `Cargo.toml`.
4. **Entry points + directory tree** — read a few, then propose a draft under the grounding rules in
   `references/backfill-guide.md` (only claim what the repo evidences, never invent).
5. **No evidence** (greenfield) → ask outright: *"What is this project for, in one sentence?"*

Then present the goal statement plus 2–4 sentences of context and ask the user to confirm or correct
it before writing.

- **Hit 2 needs no confirmation.** When the goal came from the existing README's own prose, the user
  already wrote it and the merge path forbids overwriting it — so there is nothing to confirm and
  nothing to write. Skip the ask and leave the prose alone. Every *other* hit ends in confirmation.
- **Hit 5 is a blocking ask.** On a true greenfield the goal exists only in the user's head. Ask, and
  wait for the answer — there is no omission branch for the goal statement.
- **The context sentences are scaffold-only.** They fill the new-README template. The merge path
  never adds context prose to a README that already has its own. On hit 5 there is nothing to draft
  them from — omit the paragraph entirely unless the user volunteers more than the one sentence.
- **The `(inferred)` marker never ships into README prose.** `backfill-guide.md` says to mark
  inferences `(inferred)`; that marker belongs on what you **show the user when proposing**, not in
  the file. README prose is public-facing. Confirmation is what keeps the guess out, so the rule's
  intent survives even though its mechanism differs here.
- **Prefer omission over a guess** — governs the *context* sentences, not the goal statement: a
  README with a thin but true goal beats one with an invented mission.

## Scaffolding a new README

When the repo has no root `README.md`, write this. Project name comes from the manifest `name`, else
the `AGENTS.md` H1 (strip a trailing `— Agent Instructions`), else the directory name — a checkout
directory is often renamed or temporary, so prefer any name the repo states about itself.

```markdown
# Project name

Goal statement — one sentence: what this project is for.

Two to four sentences of context: who it is for, what problem it solves, where it stands.

## Documentation

- [Agent instructions](AGENTS.md) — engineering standards and workflow rules for agents.
- [Architecture](ARCHITECTURE.md) — system overview and component map.
- [Architecture decisions](docs/adr/) — ADRs: why things are the way they are.
- [Changelog](changelog/) — what changed, one entry per change.
- [User scenarios](docs/user-scenarios.md) — BDD scenarios for the main user flows.
```

Include a bullet **only** for a candidate that resolved (see below). A repo where the user declined
ADRs gets no ADR line.

## The Documentation index

Resolve candidates by **probing the path on disk** — never link a path you have not verified. Every
candidate is conditional on that probe, including the ones another module scaffolded this run. Fixed
blurbs and a fixed canonical order are what make re-runs idempotent — though that applies only to
bullets **we** author. An existing hand-written blurb always stays as it is, so a merged README that
mixes our wording with the author's is the expected outcome, not a defect to normalize.

| Candidate | Path | Note |
|-----------|------|------|
| Agent instructions | `AGENTS.md` | Step 1 normally guarantees it — probe anyway |
| Architecture | `ARCHITECTURE.md` | only if it exists — the user can decline it in `setup-adrs` |
| Architecture decisions | first existing of `docs/adr`, `doc/adr`, `adr`, `docs/architecture/decisions` | use the dir the delegate actually chose |
| Changelog | `changelog/` | only if it exists — the directory, **not** a frozen root `changelog.md` |
| User scenarios | `docs/user-scenarios.md` | only if it exists |

- **Link style** — bare relative paths, no `./` prefix (`docs/adr/`, not `./docs/adr/`). This matches
  the entries `prd-creator` writes. Directory targets take a trailing slash (`docs/adr/`,
  `changelog/`); file targets do not (`AGENTS.md`).
- **Canonical order** — the table's order. New bullets slot into it relative to what is already there.

## Merging into an existing README

Never clobber unasked. The user's own words outrank the template every time — only an explicit answer
from the user can change prose they already wrote.

1. **Resolve candidates.** Probe each path. Drop any that does not exist on disk.
2. **No root `README.md`** → write the full scaffold, with a bullet for each resolved candidate.
   Done. **Guard:** nothing resolved → write the title and goal but no `## Documentation` heading;
   never leave an empty section.
3. **`README.md` exists** → parse its `##` headings, ignoring any `##` line inside a fenced code block
   (a phantom `## Documentation` would route you to merge-only and silently write nothing).

   Then apply the **already-linked filter**, which governs both branches below: for each resolved
   candidate, check whether its path already appears as a link target **anywhere in the README**, not
   just inside `## Documentation`. Normalize before comparing — strip a leading `./` and a trailing
   `/`. Already linked → drop it from the list. A README with no `## Documentation` can still link
   `ARCHITECTURE.md` from its own prose, which is why the filter runs before the branch, not inside it.

   - **No `## Documentation`** → insert the section, containing exactly the filtered list.
     **Placement:** immediately before `## PRDs` or `## Codebase Guide` if either exists — we may not
     move those, and appending past them buries the index at the bottom — otherwise at end of file.
     **Guard:** if that list is empty, write nothing — never create an empty section.
   - **`## Documentation` exists** → merge only. Append each bullet from the filtered list in
     canonical order relative to the bullets already present. Never duplicate, relocate, or reword an
     already-linked entry — a hand-written blurb beats ours. Never remove, reorder, or reword any
     existing bullet, whether or not it points at a candidate.
4. **Goal statement** — the prose above the first `##` is the existing goal. **Never overwrite it
   unasked**, and never rewrite it just to match our phrasing.
   - **No prose above the first `##`** → insert the confirmed goal statement there. This is the only
     way a goal reaches a merged README; without it, the confirmation you just ran is dead work.
   - **Prose contradicts the goal captured this run** → show both and **ask which is current**. This
     is the same decision as the goal-capture confirmation, so fold the two into one ask — never ask
     twice.
     - Confirmed the new one → replace the goal prose with the agreed **goal sentence** only. Context
       sentences stay out of a merged README, per the scaffold-only rule above.
     - Declined, or unsure → keep the existing text verbatim.
   - **Prose agrees, or merely differs in wording** → leave it alone. Do not ask.

   The contradiction branch fires on one path only: hit 1 won, meaning an `AGENTS.md`
   `Project Overview` outranked a README whose prose says something different. Hit 2 *is* that prose,
   so it has nothing to compare against.
5. **Nothing to add** → no write. Report *"README documentation index already current."*

The whole-file link check in step 3 is load-bearing — do **not** narrow it to the `## Documentation`
section. A README that already links `ARCHITECTURE.md` under its own `## Architecture` heading would
then get that same link duplicated into ours.

## Section ownership

This module owns exactly one section: `## Documentation`. Two other sections in the same file belong
to other skills — leave them exactly as they are.

- **`## PRDs`** — owned by `prd-creator`. Never create, edit, or remove it.
- **`## Codebase Guide`** — owned by `create-codebase-docs`. Never create, edit, or remove it.

Never mirror their links into `## Documentation` either. Duplicated links drift apart; a sibling
section that its own skill keeps current is the better outcome.

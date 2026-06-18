---
name: setup-adrs
description: Bootstrap an Architecture Decision Record (ADR) system in any project — creates an ADR directory with a template and a seed ADR-0001, scaffolds an ARCHITECTURE.md recap doc, and injects a when-to-create-an-ADR policy into AGENTS.md or CLAUDE.md. Use when setting up ADRs, adding architecture decision records, scaffolding ADR tracking, initializing decision logging, or the user mentions "setup adrs". Do NOT use to write or fill in a single ADR for one specific decision (just copy the template), to set up changelogs or PRDs, or to record non-architectural product decisions.
---

# Setup ADRs

Set up an Architecture Decision Record system in any project. Each meaningful technical
decision gets a numbered, version-controlled record in `docs/adr/`, and an `ARCHITECTURE.md`
recap doc keeps the current-state overview. ADRs inject judgment by example — future agent
sessions read them, stay true to past choices, and supersede what's stale.

## When to use

- User asks to "set up ADRs", "add architecture decision records", or "scaffold ADR tracking"
- User wants the ADR pattern (record + recap doc + policy) replicated in a new repo
- User mentions "setup adrs" or "initialize decision records"

## Workflow

### Step 1: Assess current state

Check the project for:
1. An existing ADR directory — look for `docs/adr`, `doc/adr`, `adr`, `docs/architecture/decisions`. Reuse it if found; otherwise default to `docs/adr/`.
2. The highest existing ADR number in that directory (to avoid clobbering `0001`).
3. An existing `ARCHITECTURE.md` at root.
4. An existing agent-instructions file — `AGENTS.md`, `.claude/CLAUDE.md`, or `CLAUDE.md`.

### Step 2: Create the ADR directory + template

```bash
mkdir -p docs/adr
```

Copy `assets/adr-template.md` → `docs/adr/0000-template.md`. This `0000-template.md` is the
file every future ADR is copied from. If the directory already has a `0000-template.md`, skip.

### Step 3: Seed ADR-0001

Copy `assets/0001-record-architecture-decisions.md` → `docs/adr/0001-record-architecture-decisions.md`
and replace the `YYYY-MM-DD` Date placeholder with today's date. This is the classic first
ADR recording the decision to use ADRs, so the directory isn't empty.

**Skip this step if any numbered ADR (`0001` or higher) already exists** — the project is
already using ADRs.

### Step 4: Scaffold the recap doc

1. **If `ARCHITECTURE.md` already exists, do NOT overwrite it.** Show the user the recap-doc
   subsection of the policy and let them decide how to reconcile. Stop here.
2. **Detect greenfield vs working repo.** A working repo has real source — e.g. `src/`, `lib/`,
   `app/`, `packages/`, or a populated manifest (`package.json`, `pyproject.toml`, `go.mod`,
   `Cargo.toml`) alongside actual source files. Greenfield = empty or docs/config only.
3. **Greenfield → copy the blank template** (`assets/architecture-template.md` → `ARCHITECTURE.md`).
4. **Working repo → ask first**: "This repo already has code. Want me to draft `ARCHITECTURE.md`
   from the current implementation instead of a blank template?"
   - **No** → copy the blank template.
   - **Yes** → survey the codebase (read-only) and write a **populated** `ARCHITECTURE.md` using
     the template's sections, each grounded in real files:
     - **Overview** ← README, manifest description, top-level layout.
     - **Key components** ← main source dirs / modules / services / entry points.
     - **Cross-cutting decisions** ← language/runtime, framework, data store, auth, error
       handling, build/deploy config — tag each `(no ADR yet)` so it can be backfilled later.
     - **Conventions** ← test setup, lint/format config, observable naming/structure patterns.

   **Grounding rules**: only claim what the repo evidences; mark guesses `(inferred)`; never
   invent components or decisions; keep it a concise recap, not exhaustive docs. Survey via
   README, manifests, the directory tree, and a few key entry points / codebase search — read
   only, change nothing but `ARCHITECTURE.md`.

### Step 5: Inject the ADR policy

Read the full policy from [references/policy-template.md](references/policy-template.md).

**Pick the target file** (where `## ADRs` goes) — first match wins; root files come first so a
project that uses `CLAUDE.md` is honored:
1. `AGENTS.md` at project root
2. `CLAUDE.md` at project root
3. `.claude/CLAUDE.md`

If a target exists, append the `## ADRs` section to it. If **none** exist, create `AGENTS.md` at
root with the policy (`AGENTS.md` is the cross-tool canonical file).

**Keep `AGENTS.md` and `CLAUDE.md` resolving to one file.** After choosing/creating the target,
**if `AGENTS.md` is the real policy file at root AND no `CLAUDE.md` exists at root**, create a
relative symlink at the project root so Claude Code (which reads `CLAUDE.md`) sees the same file:

```bash
ln -s AGENTS.md CLAUDE.md   # run at project root
```

This one condition covers both cases that need it: none-existed (you just created `AGENTS.md`)
and `AGENTS.md`-only. Guards:
- Only when **no `CLAUDE.md` exists** — never overwrite a real `CLAUDE.md`, or any existing file, with a symlink.
- If a real `CLAUDE.md` exists **separately** from `AGENTS.md`, inject into `AGENTS.md`, leave both as-is, and tell the user `CLAUDE.md` is a separate file they may want to reconcile.
- If the project uses `CLAUDE.md` or `.claude/CLAUDE.md` and has **no `AGENTS.md`**, just inject there — do NOT introduce `AGENTS.md` or a symlink.
- If `CLAUDE.md` is already a symlink to `AGENTS.md`, they are the same file — inject once into `AGENTS.md`.
- Symlinks need `core.symlinks=true` on Windows checkouts; macOS/Linux work out of the box.

**Before injecting**: if a `## ADRs` section already exists in the target, ask the user
whether to replace or skip.

**If the ADR directory is not `docs/adr/`**, substitute the chosen path everywhere in the
policy before injecting. **If the user declined the recap doc**, drop the
`### Recap doc (ARCHITECTURE.md)` subsection.

### Step 6: Verify

Confirm to the user:
- ADR directory created at `docs/adr/` (or the reused path) with `0000-template.md`
- Seed `0001-record-architecture-decisions.md` created (or skipped — already in use)
- `ARCHITECTURE.md` — drafted from the codebase, blank template, or left untouched (already existed)
- Policy injected into `[target file]`; `CLAUDE.md → AGENTS.md` symlink created (if applicable)

## ADR format (quick reference)

**When to create one**: only for a meaningful technical decision worth remembering — one made
with discarded alternatives, a new pattern/abstraction/dependency/direction, or a reversal of
a past decision. Skip reused proven patterns and mechanical no-decision changes. Worthiness is
independent of work size. Full criteria live in the policy template.

**Filename**: `docs/adr/NNNN-short-slug.md`
- `NNNN`: next zero-padded sequential number (ADRs cross-reference and supersede each other, so
  numbering is sequential, not timestamped)
- Slug: 2–5 word kebab-case (e.g. `0007-use-postgres-for-events`)

**Status lifecycle**: Proposed → Accepted → Superseded by ADR-NNNN / Deprecated

**Content**: copy `0000-template.md` — Context (why), Decision (what), Options considered
(incl. discarded + why), Consequences, Supersedes/Superseded-by.

## Rules

- Sequential numbering, never timestamps — ADRs reference each other by number.
- Never delete or rewrite an accepted ADR — supersede it with a new one and mark the old one.
- Keep ADRs concise. Focus on **why** over how.
- `ARCHITECTURE.md` holds only current state, derived from the ADRs — update it after an ADR
  changes a cross-cutting decision.
- In a repo with existing code, ask before scaffolding the recap doc, and on yes populate
  `ARCHITECTURE.md` from the implementation rather than dropping a blank template — ground every
  section in real files and never invent.
- Do not overwrite an existing `ARCHITECTURE.md` or an existing `## ADRs` policy section
  without asking.
- Inject into the project's existing agent file — `AGENTS.md`, root `CLAUDE.md`, or
  `.claude/CLAUDE.md` (first match). If none exists, create `AGENTS.md` and symlink
  `CLAUDE.md → AGENTS.md`; also add that symlink when only `AGENTS.md` exists. Never overwrite a
  real `CLAUDE.md` with a symlink.

## References

- [policy-template.md](references/policy-template.md) — full `## ADRs` policy to inject into AGENTS.md/CLAUDE.md

## Assets

- `assets/adr-template.md` — copied into the project as `docs/adr/0000-template.md`
- `assets/architecture-template.md` — copied into the project as `ARCHITECTURE.md`
- `assets/0001-record-architecture-decisions.md` — copied as the seed first ADR (fill the Date)

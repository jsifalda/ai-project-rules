---
name: user-scenarios-setup
description: Bootstrap a BDD-formatted user-scenarios inventory in any project. Creates `docs/user-scenarios.md` with a Conventions section, frozen domain prefixes, seeded example scenarios, and a Coverage Matrix, then injects a doc-sync policy into `AGENTS.md` or `CLAUDE.md` so future agents must keep the doc in sync with user-visible changes. Use when the user asks to "set up user scenarios", "bootstrap a user-scenarios doc", "add a scenarios inventory", "scenarios setup", or wants to replicate the pattern in a new repo. Do NOT use for one-off scenario edits in an existing doc, for generating end-to-end tests, for changelog setup (see `setup-changelog`), or for PRD breakdown into stories (see `prd-breakdown`).
---

# User Scenarios Setup

Bootstrap a canonical user-scenarios inventory in any project. The output is a `docs/user-scenarios.md` file in BDD (Given/When/Then) format, keyed by stable IDs (`<DOMAIN>-<NN>`), plus a policy block in the project's agent instructions that requires every user-visible change to add or update a scenario.

## When to use

- User asks to "set up user scenarios" or "add a scenarios doc" to a project
- User wants to replicate the user-scenarios pattern in a new repo
- User mentions "user-scenarios setup" or "bootstrap user scenarios"

## Workflow

### Step 1: Assess current state

Check the project root for:

1. Existing `docs/user-scenarios.md`
2. Existing agent instructions file in this priority order:
   1. `AGENTS.md` at project root
   2. `.claude/CLAUDE.md`
   3. `CLAUDE.md` at project root

Decide the target instructions file using the first match. If none exist, you will create `AGENTS.md` in Step 4.

### Step 2: Gather inputs

Ask the user **one question per turn**:

1. **Project name** — used for the doc title (`# <ProjectName> User Scenarios`). Example: `Acme`, `SignalSeek`.
2. **Frozen domain prefixes** — comma-separated, all-caps letters only (e.g. `AUTH, BILLING, ADMIN`). These become the stable namespace for scenario IDs. Validate the input: each entry must match `^[A-Z]+$`. If a value fails, re-ask with the offending entry called out.

Hold both values for the next steps.

### Step 3: Create `docs/user-scenarios.md`

Read [references/doc-template.md](references/doc-template.md) and write it to `docs/user-scenarios.md` in the target project after applying these substitutions:

- Replace every occurrence of `{{PROJECT_NAME}}` with the project name from Step 2.
- Replace `{{DOMAIN_LIST}}` with the comma-separated domain prefixes in backticks: `` `AUTH`, `BILLING`, `ADMIN` ``.
- Replace the `{{SEEDED_SCENARIOS}}` block with one seeded scenario per domain — for each domain `D`, emit a `### D-01: User performs a <D> action` block with placeholder Given/When/Then steps and `Verified by: TODO`. Use the literal domain name in the title; never invent product-specific copy. The user replaces these titles with real user-visible behaviors after setup.
- Replace `{{COVERAGE_MATRIX_ROWS}}` with one table row per seeded scenario: `| D-01        | TODO |` (pad the ID column to match the header).

If `docs/user-scenarios.md` already exists, **ask the user** before overwriting. Options to offer: (a) back up the existing file to `docs/user-scenarios.md.bak` and replace, (b) skip Step 3 entirely (still run Step 4), or (c) abort.

If the `docs/` directory does not exist, create it.

### Step 4: Inject the doc-sync policy

Read [references/policy-template.md](references/policy-template.md). Replace `{{DOMAIN_LIST}}` with the same backticked domain list from Step 3.

Append the substituted block to the target instructions file from Step 1. If none of `AGENTS.md`, `.claude/CLAUDE.md`, `CLAUDE.md` exist, create `AGENTS.md` at project root containing only the policy block (with a top-level title heading).

**Before appending**: scan the target file for an existing `## User Scenarios` heading. If found, ask the user whether to (a) replace the existing section, (b) skip Step 4, or (c) abort. Do not silently duplicate.

### Step 5: Verify and report

Confirm to the user, in a single short message:

- `docs/user-scenarios.md` created (or skipped if user chose to)
- Policy injected into `<target file path>` (or replaced / skipped)
- Frozen domains seeded: `<comma-separated domain list from Step 2>`
- Next step the user should take: add real `Verified by:` test paths to the seeded scenarios as tests land, and replace the placeholder titles with real user-visible behaviors.

Optionally mention that a follow-up the user can request separately is a doc-shape lint test (Jest / Vitest / `node:test`) that enforces unique IDs, frozen-domain membership, Given/When/Then presence, `Verified by:` presence, and Coverage Matrix sync. This skill deliberately does not bundle one — adding it is a one-line ask in a later session.

## Rules

- Never invent product- or domain-specific scenario copy. Stick to generic placeholders in seeded scenarios. The user fills in real behaviors after setup.
- Never modify scenarios in an existing `docs/user-scenarios.md` — only overwrite the whole file (with backup) or skip.
- Domain prefixes are all-caps letters only. Reject `Auth`, `BILLING-CORE`, numeric prefixes.
- Retired scenario IDs must never be reused — this is stated in the doc template and the policy. The skill itself does not need to enforce it at setup time, only document it.
- Policy block uses `## User Scenarios` as its heading — fixed, so future runs can detect duplicates.

## References

- [Doc template](references/doc-template.md) — skeleton for `docs/user-scenarios.md` with `{{PROJECT_NAME}}`, `{{DOMAIN_LIST}}`, `{{SEEDED_SCENARIOS}}`, `{{COVERAGE_MATRIX_ROWS}}` placeholders.
- [Policy template](references/policy-template.md) — block injected into `AGENTS.md`/`CLAUDE.md` with `{{DOMAIN_LIST}}` placeholder.

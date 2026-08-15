---
name: setup-user-scenarios
description: RESTRICTED-INVOCATION — do NOT auto-trigger. Only the literal `/setup-user-scenarios` command or `setup-aiengineering` Step 6 may load this. Paraphrases are ANTI-TRIGGERS. When invoked — bootstrap a BDD-formatted user-scenarios inventory in any project. Creates `docs/user-scenarios.md` with a Conventions section, frozen domain prefixes, seeded example scenarios, and a Coverage Matrix, then injects a doc-sync policy into `AGENTS.md` or `CLAUDE.md` so future agents must keep the doc in sync with user-visible changes. Do NOT use for one-off scenario edits in an existing doc, for generating end-to-end tests, for changelog setup (see `setup-changelog`), or for PRD breakdown into stories (see `prd-breakdown`).
---

# User Scenarios Setup

## Invocation (check this first)

These are the only entry points allowed:

1. The user types the literal slash command `/setup-user-scenarios`.
2. `setup-aiengineering` reaches Step 6 and delegates the User scenarios module.

Everything else is an anti-trigger. None of these load this skill — "add user scenarios", "write
some Given/When/Then", "document the user flows", or any other paraphrase. This skill creates
`docs/user-scenarios.md` and appends a blocking verification gate to the project's
agent-instructions file, so a wrong trigger changes files the user did not ask about. Editing one
scenario in an existing doc is not this skill.

This rule is prompt-enforced, not harness-enforced. This skill deliberately carries no
`disable-model-invocation` flag, because that flag is a binary block with no per-caller
allowlist — it removes the skill from the Skill tool entirely, so a dependent skill's delegation
step fails with `cannot be used with Skill tool`. Do not re-add it to "tighten" invocation
without first removing every dependent skill's delegation step.

Bootstrap a canonical user-scenarios inventory in any project. The output is a `docs/user-scenarios.md` file in BDD (Given/When/Then) format, keyed by stable IDs (`<DOMAIN>-YYYY-MM-DD-slug`), plus a policy block in the project's agent instructions that requires every user-visible change to add or update a scenario.

## When to use

See `## Invocation` above. Those two entry points are the only ones. A user who describes
wanting a scenarios doc is not one of them — offer `/setup-user-scenarios` and wait for them to
run it.

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
- Replace the `{{SEEDED_SCENARIOS}}` block with one seeded scenario per domain — for each domain `D`, emit a `### D-YYYY-MM-DD-example-scenario: User performs a <D> action` block, using today's date, with placeholder Given/When/Then steps and `Verified by: TODO`. Use the literal domain name in the title; never invent product-specific copy. The user replaces these titles with real user-visible behaviors after setup.
- Replace `{{COVERAGE_MATRIX_ROWS}}` with one table row per seeded scenario, using the same dated ID as its heading: `| D-YYYY-MM-DD-example-scenario | TODO |` (pad the ID column to match the header, widening both if a real ID runs longer).

If `docs/user-scenarios.md` already exists, **ask the user** before overwriting. Options to offer: (a) back up the existing file to `docs/user-scenarios.md.bak` and replace, (b) skip Step 3 entirely (still run Step 4), or (c) abort.

If the `docs/` directory does not exist, create it.

### Step 4: Inject the doc-sync policy

Read [references/policy-template.md](references/policy-template.md). Replace `{{DOMAIN_LIST}}` with the same backticked domain list from Step 3.

**If Step 3 was skipped because an existing `docs/user-scenarios.md` was kept as-is**, check the ID scheme that existing doc actually uses. If it is not the dated `<DOMAIN>-YYYY-MM-DD-slug` scheme this skill produces, do not inject a policy that claims dated ids. Substitute the scheme the existing doc actually uses into the policy's id wording instead, and state which scheme was used in the Step 5 report, so nobody later assumes the ids are dated when they are not.

Append the substituted block to the target instructions file from Step 1. If none of `AGENTS.md`, `.claude/CLAUDE.md`, `CLAUDE.md` exist, create `AGENTS.md` at project root containing only the policy block (with a top-level title heading).

**Before appending**: scan the target file for an existing `## User Scenarios` heading. If found, ask the user whether to (a) replace the existing section, (b) skip Step 4, or (c) abort. Do not silently duplicate.

### Step 5: Verify and report

Confirm to the user, in a single short message:

- `docs/user-scenarios.md` created (or skipped if user chose to)
- Policy injected into `<target file path>` (or replaced / skipped)
- If `docs/user-scenarios.md` already existed and was kept as-is, which ID scheme the injected policy documents — so nobody later assumes dated ids when the repo doesn't use them
- Frozen domains seeded: `<comma-separated domain list from Step 2>`
- Next step the user should take: add real `Verified by:` test paths to the seeded scenarios as tests land, and replace the placeholder titles with real user-visible behaviors.

Optionally mention that a follow-up the user can request separately is a doc-shape lint test (Jest / Vitest / `node:test`) that enforces unique IDs, frozen-domain membership, Given/When/Then presence, `Verified by:` presence, and Coverage Matrix sync. This skill deliberately does not bundle one — adding it is a one-line ask in a later session.

## Rules

- Never invent product- or domain-specific scenario copy. Stick to generic placeholders in seeded scenarios. The user fills in real behaviors after setup.
- Never modify scenarios in an existing `docs/user-scenarios.md` — only overwrite the whole file (with backup) or skip.
- Domain prefixes are all-caps letters only. Reject `Auth`, `BILLING-CORE`, numeric prefixes.
- IDs are date-based and immutable: `<DOMAIN>-YYYY-MM-DD-slug`. A counter-based numeric tail forces scanning the whole doc for the highest number already in use, so two agents on two branches can land on the same next number and the collision only surfaces at merge. A date plus a slug is chosen from local information only, so parallel authors never collide.
- Retired scenario IDs must never be reused — this is stated in the doc template and the policy. The skill itself does not need to enforce it at setup time, only document it.
- Policy block uses `## User Scenarios` as its heading — fixed, so future runs can detect duplicates.

## References

- [Doc template](references/doc-template.md) — skeleton for `docs/user-scenarios.md` with `{{PROJECT_NAME}}`, `{{DOMAIN_LIST}}`, `{{SEEDED_SCENARIOS}}`, `{{COVERAGE_MATRIX_ROWS}}` placeholders.
- [Policy template](references/policy-template.md) — block injected into `AGENTS.md`/`CLAUDE.md` with `{{DOMAIN_LIST}}` placeholder.

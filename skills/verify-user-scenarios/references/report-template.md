# Run report template

> The literal shape of a run report. Fill every `{{PLACEHOLDER}}`. Write the filled report to
> the chat, and the same text to a receipt file in the evidence directory.

---

## {{PROJECT}} — QA run

- Date: {{DATE}}
- Scope: {{SCOPE}}
- Commit: {{COMMIT}}
- Dev server: {{DEV_SERVER_URL}}

## Run preparation

- Environment preflight: {{ENV_PREFLIGHT}}
- Database target: {{DATABASE_TARGET}}
- Reset: {{RESET_STATUS}}
- Seed: {{SEED_STATUS}}
- Playwright MCP: {{PLAYWRIGHT_MCP_STATUS}}
- Test plan: {{TEST_PLAN}}
- Phase 1 Discover: {{PHASE_1_STATUS}}
- Phase 2 Select: {{PHASE_2_STATUS}}
- Phase 3 Plan: {{PHASE_3_STATUS}}
- Phase 4 Prepare: {{PHASE_4_STATUS}}
- Phase 5 Execute: {{PHASE_5_STATUS}}
- Phase 6 Judge: {{PHASE_6_STATUS}}
- Phase 7 Self-audit: {{PHASE_7_STATUS}}
- Phase 8 Report: {{PHASE_8_STATUS}}
- Phase 9 Decide: {{PHASE_9_STATUS}}

`{{ENV_PREFLIGHT}}` is the preflight's own report, the names of any missing required
variables, or `no preflight in this project`.

`{{DATABASE_TARGET}}` is the resolved host the run was allowed to write to.

`{{RESET_STATUS}}` is `ran`, `declined — ran against whatever data was present`, or
`failed (<what broke>)`.

`{{SEED_STATUS}}` is `ran`, `did not run`, or `failed (<what broke>)`.

`{{PLAYWRIGHT_MCP_STATUS}}` is `available`, or `skipped (<reason>)`.

`{{TEST_PLAN}}` is the Phase 3 test plan reproduced in full — five fields per selected
scenario: scenario ID, route to load, preconditions, interaction to drive, the single
observable that decides the verdict — or the literal `not written`. `not written` is
itself a finding: a run that opened the browser without a plan improvised and then
rationalised whatever it saw.

Each `{{PHASE_N_STATUS}}` is `passed`, `failed (<what broke>)`, or `skipped (<reason>)`.

## Coverage

{{COVERAGE_LINE}}

{{OUT_OF_SCOPE_REASONS}}

`{{COVERAGE_LINE}}` is a per-domain breakdown, not one sentence: one line per domain in
`{{DOMAIN}}: {{N_SELECTED}} of {{N_DOMAIN_TOTAL}} selected` shape, then the inventory
total in the original shape (`{{N_RUN}} run, {{N_SKIPPED}} out of scope, {{N_TOTAL}} in
the inventory.`), then every domain with nothing selected named explicitly
(`{{ZERO_SELECTED_DOMAINS}} had nothing selected.`).

`{{OUT_OF_SCOPE_REASONS}}` is one bullet per skipped scenario ID, not per group:
`- {{SCENARIO_ID}}: {{REASON}}`. `not selected` is not a reason.

## Verdict summary

{{N_PASS}} pass · {{N_FAIL}} fail · {{N_GAP}} gap · {{N_DRIFT}} drift · {{N_BLOCKED}} blocked

## Verdict table

`{{VERDICT_ROWS}}` replaces the example rows below, one row per scenario, in the same shape.
Three example rows, covering three different verdicts, for the shape only:

| ID | Domain | Verdict | Note | Evidence |
| --- | --- | --- | --- | --- |
| SEARCH-2026-01-01-filter-by-price | SEARCH | pass | Range filter matched the Then step. | evidence/search-filter-by-price.png |
| CATALOG-2026-01-01-report-listing | CATALOG | gap | No report control on the listing page. | none |
| PAYMENTS-2026-01-01-refund-request | PAYMENTS | blocked | Prerequisite scenario failed. | evidence/payments-refund-request.png |

Evidence is the screenshot path, or the literal `none`. A verdict whose evidence is
`none` is a verdict with nothing behind it — it shows as an empty cell, not as a row
that quietly disappears.

## Findings detail

{{FINDING_BLOCKS}}

One block per non-pass scenario, in exactly this field order:

### {{SCENARIO_ID}}

- **Scenario:** {{SCENARIO_TITLE}}
- **Expected:** {{THEN_STEP_QUOTE}}
- **Observed:** {{WHAT_THE_BROWSER_SHOWED}}
- **Evidence:** {{SCREENSHOT_PATH}}
- **Severity:** {{SEVERITY}}
- **Nearest cause:** {{NEAREST_CAUSE}}

`Nearest cause` is optional. Fill it only when the run itself saw a likely cause. Leave it
blank rather than guess. A guess dressed as a diagnosis is worse than no line.

## Workarounds and surfaces not observed

{{WORKAROUND_BLOCKS}}

`{{WORKAROUND_BLOCKS}}` is one block per workaround, or the literal `none`. Each block,
in exactly this field order:

- **Bypassed:** {{WHAT_THE_PRODUCT_COULD_NOT_DO}}
- **Done instead:** {{STEP_TAKEN_OUTSIDE_THE_INTERFACE}}
- **Surface left unobserved:** {{WHAT_THEREFORE_HAS_NO_EVIDENCE}}
- **Interface branches closed:** {{CONTROLS_NO_LONGER_RENDERABLE}}
- **Scenarios blocked by this:** {{SCENARIO_IDS}}

The fourth field is the one runs forget: a workaround that alters account or fixture
state can make a control structurally unrenderable for the rest of the run, so that
control is not weakly covered — it is absent.

## Links the application emitted

{{EMITTED_LINK_ROWS}}

`{{EMITTED_LINK_ROWS}}` replaces the example row below, one row per link, in the same
shape, or the literal `none`.

| URL | Where it came from | What rendered |
| --- | --- | --- |
| https://example.test/reset?token=abc123 | Callback harvested from a password-reset mail fixture | The reset form, pre-filled with the token. |
| https://example.test/profile | Callback carried inside the account-confirmation link | **The not-found page.** The account page is served at another address. |

The second row is the shape that matters. A callback the product generates is asserted by
nothing, so it is found here or not at all.

`Where it came from` is e.g. a navigation control on a named page, a redirect after a
form submission, or a callback carried inside a link harvested from server output.
These links belong to no scenario, so they are reported here rather than forced into
the verdict table.

## Hard-rule self-audit

{{SELF_AUDIT_ROWS}}

`{{SELF_AUDIT_ROWS}}` replaces the example row below, one row per hard rule, in the
same shape.

| Rule | Honoured / violated / n.a. | Proof |
| --- | --- | --- |
| Never award a `pass` from a control's presence | honoured | 14 controls operated against 14 scenarios whose Then step describes an action. |
| Never leave a workaround unrecorded | n.a. | No step was taken outside the interface. |
| Never inherit a slice | violated | The 20 IDs came from a plan file and were never ranked. |

One row per rule in the skill's `Hard rules` list, and no row for a rule that list does not
carry. The rows are the checklist in
[self-audit.md](self-audit.md), in the same order.

A violated rule is reported, never quietly corrected.

## Decisions

One entry per finding. The user picks one option per finding.

- **{{SCENARIO_ID}}** — {{ONE_LINE_FINDING}}
  - [ ] Fix now
  - [ ] Record it
  - [ ] Amend the scenario
  - [ ] Drop it
  - Answer: {{ANSWER}}

---

The report ends here. No narrative summary follows it. No recommendation is added beyond
what was asked for.

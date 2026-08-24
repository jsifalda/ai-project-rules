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
- Phase 1 Discover: {{PHASE_1_STATUS}}
- Phase 2 Select: {{PHASE_2_STATUS}}
- Phase 3 Plan: {{PHASE_3_STATUS}}
- Phase 4 Prepare: {{PHASE_4_STATUS}}
- Phase 5 Execute: {{PHASE_5_STATUS}}
- Phase 6 Judge: {{PHASE_6_STATUS}}
- Phase 7 Report: {{PHASE_7_STATUS}}
- Phase 8 Decide: {{PHASE_8_STATUS}}

`{{ENV_PREFLIGHT}}` is the preflight's own report, the names of any missing required
variables, or `no preflight in this project`.

`{{DATABASE_TARGET}}` is the resolved host the run was allowed to write to.

`{{RESET_STATUS}}` is `ran`, `declined — ran against whatever data was present`, or
`failed (<what broke>)`.

`{{SEED_STATUS}}` is `ran`, `did not run`, or `failed (<what broke>)`.

`{{PLAYWRIGHT_MCP_STATUS}}` is `available`, or `skipped (<reason>)`.

Each `{{PHASE_N_STATUS}}` is `passed`, `failed (<what broke>)`, or `skipped (<reason>)`.

## Coverage

{{COVERAGE_LINE}}

{{OUT_OF_SCOPE_REASONS}}

`{{COVERAGE_LINE}}` is exactly this shape:
`{{N_RUN}} run, {{N_SKIPPED}} out of scope, {{N_TOTAL}} in the inventory.`

`{{OUT_OF_SCOPE_REASONS}}` is one bullet per skipped group:
`- {{GROUP_COUNT}} scenarios out of scope: {{GROUP_REASON}}`

## Verdict summary

{{N_PASS}} pass · {{N_FAIL}} fail · {{N_GAP}} gap · {{N_DRIFT}} drift · {{N_BLOCKED}} blocked

## Verdict table

`{{VERDICT_ROWS}}` replaces the example rows below, one row per scenario, in the same shape.
Three example rows, covering three different verdicts, for the shape only:

| ID | Domain | Verdict | Note |
| --- | --- | --- | --- |
| SEARCH-2026-01-01-filter-by-price | SEARCH | pass | Range filter matched the Then step. |
| CATALOG-2026-01-01-report-listing | CATALOG | gap | No report control on the listing page. |
| PAYMENTS-2026-01-01-refund-request | PAYMENTS | blocked | Prerequisite scenario failed. |

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

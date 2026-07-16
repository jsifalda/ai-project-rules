---
name: landing-page-viral-grill
description: Audit a landing page for shareability, not conversion, against a 28-criterion rubric across 7 sections. Scores the 18 page-observable criteria with verbatim quoted evidence (PASS, FAIL, or UNPROVEN - never FAIL without a quote), emits a gap report, grills the user on the 10 product-level criteria the page itself cannot answer, then proposes a remediation plan for confirmed gaps only. Trigger phrases - "audit my landing page for virality", "why won't this page get shared", "shareability audit", "will this spread", "grade this page for virality". Do NOT use for conversion-rate optimization, general landing page copywriting, SEO audits, or accessibility review - those are different jobs and score different things. No composite score is ever computed.
---

# Landing Page Viral Grill

Grades shareability, not conversion. A page can convert well and still travel nowhere.

The question behind every criterion: would a visitor who will never buy still send this page to someone else? That is what gets scored here, not whether the visitor signs up.

## Inputs

Required:
- The target landing page: pasted markdown/text, a local file path, or a URL.

Optional:
- Known answers to product-level questions (pricing, category, founder visibility, naming, business model) if the user wants to supply them upfront instead of waiting for the grill step.
- A prior audit report from this skill, to compare against for regressions or fixed criteria.

## Workflow

### 1. Accept target
Take pasted markdown/text, a local file path (use the Read tool), or a URL (delegate to the `defuddle` skill for clean markdown, do not use WebFetch directly).

Sanity-check the input first. If it is empty, too small to be a real page, or clearly not a landing page, stop and ask the user rather than guessing. Never hallucinate an audit against content that was not actually provided.

### 2. Score the 18 page-observable criteria
Score every `[page-observable]` criterion in [references/viral-criteria.md](references/viral-criteria.md), in section and ID order. No skipping, no sampling, no early stopping.

Each one gets a verdict (`PASS`, `FAIL`, or `UNPROVEN`) plus verbatim quoted evidence. Absence of evidence is `UNPROVEN`, never `FAIL` — see Non-negotiables below.

### 3. Emit the gap report
Render the findings with [assets/report-template.md](assets/report-template.md). Two sections, in this order:
- Scored findings for all 18 `[page-observable]` criteria, by ID order (not sorted by verdict).
- The 10 `[product-level]` criteria, listed under an "Interview needed" heading as questions, each verdict `DEFER`.

No composite score anywhere in the report. Count verdicts instead (PASS / FAIL / UNPROVEN out of 18, plus the deferred count).

### 4. Grill the deferred criteria
Invoke the `grill-me` skill against the full deferred set from step 3 plus any criterion that scored `UNPROVEN` in step 2. This is where product-level questions (pricing, category narrowness, founder visibility, naming mechanics, and the rest) get answered by the user, and where `UNPROVEN` findings get resolved into real evidence or confirmed as genuine gaps.

Do not guess these answers on the user's behalf. If the user declines to answer a question, it stays open, it does not get scored as PASS or FAIL.

### 5. Output the remediation plan
Produce an ordered list of fixes for confirmed gaps only, after the grill in step 4 has run. Skip any criterion the grill established is inapplicable to this product.

Per fix:
- The criterion ID it closes.
- The concrete change. If the fix is copy, show the rewritten line, not just a description of what to change.
- Effort: S / M / L.
- Expected impact on sharing.

## Non-negotiables

- **Evidence rule**: no criterion is ever marked `FAIL` without quoted evidence. Absence of evidence on a page-observable criterion is `UNPROVEN`, not `FAIL`.
- **Never score product-level**: the 10 `[product-level]` criteria are never scored by the auditor, on the page or after the grill. They are always `DEFER`, rendered as interview questions and resolved through step 4, not through inference.
- **No composite score**: never compute or report a single total, percentage, or grade across sections. The sections are not commensurable. Report verdict counts instead.
- **ID stability**: criterion IDs (`A1` through `G6`) are permanent and defined only in [references/viral-criteria.md](references/viral-criteria.md). Never renumber them, reorder them, or invent new ones when citing findings.

---
name: landing-page-gap-analyzer
description: Audit landing page copy against a 13-section conversion blueprint and return a scored gap report + prioritized fix plan. Use when the user asks to "audit my landing page", "review LP copy", "gap-analyze a landing page", "score this landing page", "what's missing on this page", "compare my page to best practices", or pastes landing page text and asks for feedback. Accepts pasted markdown/text, a local file path, OR a URL (delegates URL fetch to the `defuddle` skill).
---

# Landing Page Gap Analyzer

Audit any landing page against a battle-tested 13-section conversion blueprint and return a scored gap report with a prioritized fix plan. Counterpart to `landing-page-copy` — that skill writes pages, this one grades them.

## Workflow

1. **Accept input.** One of:
   - pasted markdown / plain text of the page
   - a local file path (read with the `Read` tool)
   - a URL (delegate to the `defuddle` skill to extract clean markdown — do not use `WebFetch` directly)
2. **Sanity-check the input.** If it is empty, under ~200 words, or clearly not a landing page (blog post, README, docs), stop and ask the user to confirm or supply more content. Do not hallucinate a scorecard from nothing.
3. **Optional context probe.** If not already provided, ask **one** question only when it materially changes scoring: `icp_technicality` (default `non-technical`) and `b2b_or_b2c` (default `b2c`). Skip the question if the page itself makes the answer obvious.
4. **Map text to the 13 sections** defined in [references/blueprint-criteria.md](references/blueprint-criteria.md). Sections may appear in any order; match by content, not position.
5. **Score each section 0–3** using the rubric in `references/blueprint-criteria.md`. Score every section, including missing ones (`✗`, score 0).
6. **Detect global copy-rule violations**: `we → you`, superlatives ("best", "fastest"), jargon density, multi-audience drift, missing emotional + rational pairing.
7. **Draft concrete fixes.** For every gap, propose the actual rewritten line or a precise structural fix — not "improve hero" but "rewrite H1 to: *Finish more tasks without working more*". Use `[placeholder]` syntax for metrics, testimonials, and proper nouns you cannot verify.
8. **Prioritize fixes P0 / P1 / P2** by conversion impact:
   - **P0** — conversion-critical: broken/absent Hero, Pricing, Final CTA, or Social Proof; trust-shattering anti-patterns.
   - **P1** — high-impact: weak problem/transformation framing, missing Trust Logos, weak Features, no About story.
   - **P2** — polish: Footer, Benefits Recap redundancy, micro-copy tweaks.
9. **Fill [assets/report-template.md](assets/report-template.md)** exactly — section order, headings, table columns must match.
10. **Return the report only.** No preamble, no postscript, no "Here's your analysis". Just the filled template.

## Inputs

Required:
- `landing_page_input` — pasted text, file path, or URL.

Optional (apply defaults + flag in output as `> ⚠️ assumed:` notes):
- `icp_technicality` — `technical` | `non-technical` (default). Drives Features-section scoring: technical ICPs are allowed spec lines; non-technical pages should stay benefit-first.
- `b2b_or_b2c` — `b2b` | `b2c` (default). Drives Pricing and FAQ scoring: money-back guarantee is expected for B2B high-ticket / risk-averse ICPs and *not* expected for B2C/solopreneur pages.
- `urgency_basis` — only treat scarcity/urgency as authentic if user supplies a concrete basis (cohort close, limited seats, launch window). Otherwise flag fake-urgency anti-pattern.

## Output

Markdown only, in this exact order:
1. **Header** — page name/URL + total score `X / 39`.
2. **Section Scorecard** — 13-row table.
3. **Per-Section Findings** — one block per section that scored `< 3` OR is missing.
4. **Global Copy-Rule Violations** — checklist with evidence.
5. **Prioritized Fix Plan** — P0 / P1 / P2 numbered lists with effort estimate (S / M / L).
6. **Copy Quality Check** — 5 reader-question answers + 1-line aftertaste.

Full skeleton: [assets/report-template.md](assets/report-template.md).
Worked before/after example: [references/examples.md](references/examples.md).

## Non-negotiables

- Score every section, even if missing. Missing = `✗`, score 0, top gap = `"section missing"`.
- Every gap gets a concrete fix. No vague verbs ("improve", "enhance", "consider"). Show the rewritten copy.
- Never invent testimonials, customer logos, founder bios, or metrics. Use `[Customer Name, Role]`, `[X customers]`, `[founder story]` placeholders.
- Apply global copy rules from the blueprint:
  - `we` → `you`
  - no superlatives ("best", "fastest", "amazing")
  - one audience · one problem · one solution
  - assume reader gets ~10% of the jargon → strip it
  - emotional hook + rational explanation in every section
- Apply conflict-resolution defaults from the blueprint:
  - technical depth → zero jargon + benefit-first unless `icp_technicality = technical`
  - refund/guarantee → none unless `b2b_or_b2c = b2b` AND risk-averse/high-ticket signals present
  - pricing CTAs → CTA under every plan AND one final repeated CTA below pricing
  - urgency/scarcity → only when `urgency_basis` is authentic
- Never use `Buy` / `Purchase` as proposed CTA labels. Suggest action-oriented alternatives.
- Return the report and stop. No closing summary, no "let me know if you want to dig deeper".

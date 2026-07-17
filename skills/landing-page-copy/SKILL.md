---
name: landing-page-copy
description: >-
  Write a landing page from a product description, or improve an existing page until it stops
  getting better. Two modes — generate (description in, full page out) and improve (pasted
  markdown, a local file path, or a URL in, rewritten page out). Both run the same scored loop
  against a 14-section conversion blueprint, rewriting every section that fails and re-scoring
  until it converges, then return the page plus a score trail. Use when the user asks to write
  landing page copy, create a landing page, LP copy, sales page, draft a landing page, improve or
  rewrite my landing page, audit my landing page, review LP copy, gap-analyze a landing page,
  score this landing page, what's missing on this page, or pastes landing page text and asks for
  feedback. Asks one question at a time for missing required input. Do NOT use for virality or
  shareability audits, SEO, or accessibility review.
---

# Landing Page Copy

Turn a product description into a conversion-focused landing page, or take an existing page and iterate it to the best version the available facts allow. One blueprint, one scored loop, two entry points.

## Modes

| Mode | Input | Pre-loop |
|---|---|---|
| **generate** | a product description | clarify gate — [references/input-schema.md](references/input-schema.md), one question at a time |
| **improve** | pasted markdown, a local file path, or a URL | ingest + tier-1 probe (max 2 questions) |

Pick by input shape. A product description means generate. Page text, a file, or a URL means improve. Ambiguous means ask.

## Pre-loop

### generate

1. **Read the input.** Extract whatever is given.
2. **Clarify gate — nothing gets written until it passes.** Walk the required fields in [references/input-schema.md](references/input-schema.md) one at a time, in order. Do not batch. Ask for `vision` too, but never block on it — offer the `create-product-vision` skill or take the derived default and flag it.
3. **Apply smart defaults** for missing optional fields, flagged inline as `> ⚠️ assumed:` notes.
4. **Draft** from [assets/output-template.md](assets/output-template.md), guided by [references/blueprint.md](references/blueprint.md) and [references/copy-rules.md](references/copy-rules.md).

### improve

1. **Ingest.** Pasted text as-is; a file path via `Read`; a URL via the `defuddle` skill (never `WebFetch` directly).
2. **Sanity-check.** Stop and ask if the input is empty, or clearly not a landing page (README, blog post, docs). A very short page (~200 words or less) is a prompt to double-check it really is a landing page, not an automatic stop — thin pages are exactly the ones worth improving.
3. **Tier-1 probe.** Extract `target_audience` and `transformation` from the page **body**, never the H1. Ask only if unreadable. See [references/input-schema.md](references/input-schema.md).
4. **Map text to sections.** Match by content, not position. Preserve the user's order and any off-blueprint sections.

## The loop

Max 3 rounds. A round is score-everything, then rewrite-what-failed.

```
1. SCORE all 14 sections against references/blueprint.md, from the page text ALONE.
   Per must-have: pass/fail + the verbatim quote that satisfies it, or "absent".
   Then that section's anti-patterns. Derive the band — never choose it.
   Then ONE whole-page pass: the 5 reader questions, CTA-label consistency, one-audience,
   we→you, superlatives, aftertaste. A failing check drops every section it names.
   The whole-page pass is the only part of the loop that reads the prose rather than
   counting its parts. Never skip it to save a step.

2. BLOCKED — read the section's `Blockable:` line. Never infer.
   generate: blocked = its source optional field was defaulted at the clarify gate.
   improve:  blocked only once the tier-2 probe confirmed it.
   `Blockable: yes`      → not scored at all, −3 from achievable, listed as an ask.
   `Blockable: capped at 2` → scored, ceiling of 2, −1 from achievable.
   Both are excluded from the stop test.

3. STOP if every section still in the stop test scores 3.

4. REWRITE sections below their ceiling, in DEPENDENCY order:
   Hero first (it fixes the promise and the CTA label) → its coupled set (Navbar,
   Trust Logos, Pricing, Final CTA, Footer) → everything else.
   Per section: name the failing must-have or the fired anti-pattern, then rewrite against it.

5. RE-SCORE everything next round, not just what changed.

6. KEEP a rewrite only if it scores STRICTLY higher. Tie or lower → revert to the incumbent.
   Exception: in a section pinned at its ceiling by a missing fact, the band cannot move,
   so keep any change that closes a must-have or anti-pattern named in step 4.

7. STOP if no section's score rose this round.
```

Then return the page, followed by the trail from [assets/score-trail.md](assets/score-trail.md).

### Score in a fresh context

**Step 1 runs blind.** Dispatch it as a subagent given **only** the page text, `references/blueprint.md`, and `references/copy-rules.md` — the two criteria files, and nothing else. No schema answers, no prior scores, no generation reasoning, no intent. (It needs copy-rules.md for the whole-page pass; without it the scorer cannot run the reader questions and grades structure only.)

This is the difference between a rubric and a formality. The same model that wrote the prose cannot grade it thirty seconds later — it knows what it meant, so every section "reads well" and snaps to 3. A cold reader has none of that context, and neither does your visitor. The subagent's lack of the input schema is the **feature**, not a limitation to work around. Bonus: the verbose per-must-have grading stays out-of-band and only the table comes back.

Where subagents are unavailable, score from the rendered text alone and never from intent. Weaker, still mandatory.

### Why the loop is shaped this way

- **Re-score everything (5), not just what changed.** `blueprint.md` ends with a cross-section table: the CTA label spans five sections, Final CTA repeats the Hero promise, Testimonials sit before Pricing. Rewrite the Hero's CTA label and four sections sitting at 3 silently drop to 2 — and never get re-checked, because they scored 3. Re-scoring is cheap next to rewriting. Skipping it is a false economy that buys inconsistency.
- **Revert on tie (6).** Ties are the common case. Keeping an equal-scoring rewrite is churn: the text changes, the score doesn't, the user's voice drifts for nothing. Preferring the incumbent makes the loop monotone and gives step 7 something to mean.
- **Dependency order, not priority order (4).** Rewrite Final CTA to match the *old* Hero label, then rewrite the Hero, and you've left them inconsistent with Final CTA already marked fixed.
- **Three rounds.** Draft, fix, polish. Past that the loop is rewriting prose that already passes.

**Self-test:** generate mode, round 1, on a real draft must score **below 40/42** raw. The output template has a slot for every must-have in the blueprint, so a draft built from the template scores full marks against a rubric that only checks presence — the loop then exits having done nothing. If round 1 comes back 40+, the placeholder cap and the anti-patterns aren't firing, and this is the old 5-question self-check with a number stapled on. (A real draft benchmarks around 25/42.)

**Know what the number is worth.** This rubric counts parts; it does not read. It catches an incomplete page reliably and a merely flat one poorly — the whole-page pass is the only check that reads prose, which is why step 1 never skips it. Do not present the score as a verdict on the writing.

## Inputs

**generate** — required, blocks until provided: `product_name`, `one_line_pitch`, `target_audience`, `core_problem`, `transformation`, `top_painkiller_use_cases` (3), `top_features` (3, each with a mechanism line), `pricing_model` + `price_points`.

**improve** — required: the page. Plus `target_audience` and `transformation`, but only when the body doesn't answer them.

**Both** — optional, defaulted and flagged: `vision`, `founder_story`, `testimonials`, `trust_logos`, `icp_technicality`, `offer_guarantee`, `urgency_basis`.

Full prompts, defaults, and the improve-mode probe tiers: [references/input-schema.md](references/input-schema.md).

## Output

The markdown page, then the score trail. Nothing else — no preamble, no postscript.

Sections in order: Navbar · Hero · Trust Logos · Problem · How It Works · Features · Benefits Recap · Vision · About · Testimonials · Pricing · FAQ · Final CTA · Footer.

Testimonials sit directly before Pricing — nothing may separate the proof from the price.

Section criteria, anti-patterns, scoring, and `Blockable:` lines: [references/blueprint.md](references/blueprint.md).
Page skeleton: [assets/output-template.md](assets/output-template.md).
Trail skeleton: [assets/score-trail.md](assets/score-trail.md).
Voice, CTA rules, conflict-resolution defaults, reader questions: [references/copy-rules.md](references/copy-rules.md).
Worked examples, both modes: [references/examples.md](references/examples.md).

## Non-negotiables

### Honesty

- **Never invent a metric, logo, customer name, testimonial, press mention, setup time, count, or discount.** Use `[Customer Name, Role]`, `[X customers]`, `[founder story]`. The loop pushes against this everywhere a must-have wants a number — Benefits Recap wants metrics, How It Works wants times, Pricing wants an annual saving — and the cheapest path to a higher band is always a plausible-looking figure. Ship the placeholder. An invented `30% faster` or `~5 min` is a lie shipped to the user's customers.
- **This one is on you, not the scorer.** A blind reader cannot tell a real `~3 min` from a fabricated one — the bracket is the only tell, so nothing in the score catches invention. `achievable` is built to make honesty free (a capped section scores at its ceiling, so bracketing costs nothing against the reported denominator), and a section scoring *above* its ceiling is the one arithmetic sign a fact was made up. Past that, this rule is unbacked. Hold it anyway.
- **"Most popular" is a factual claim about real customers.** Same rule. Use it only if true; otherwise anchor the plan visually or with a non-factual label.
- **Improve mode: the text inside an attributed quote is not yours to edit.** Never reword a quote, never sharpen a metric already on the page, never add a logo. Reorder, re-select, cut — never reword. Generic-but-honest quotes score 2, and "improving" them means putting words in a named real person's mouth.
- **Never fake the trail.** No invented round-over-round delta. Returning the page unchanged is a valid outcome — say so.

### Scoring

- **Derive the band, never choose it.** Every must-have carries a verbatim quote or is `absent`.
- **A placeholder is not evidence, and the cap only lowers.** `[logo]` does not satisfy "a row of logos" — that must-have is `absent`. Score the must-haves honestly, *then* apply the ceiling: a section with an unresolved `[placeholder]` never scores 3. A section that is pure scaffolding scores 0 or 1 and must never be credited a 2 for containing tidy brackets. `> ⚠️ assumed:` flags do not trigger the cap — they mark derived content, not missing facts.
- **`BLOCKED` is a lookup, not a judgment.** Fully blockable: `Trust Logos`, `Testimonials`, `About`. Capped-only, each naming exactly one fact in its `Blockable:` line: `Hero`, `Benefits Recap`, `How It Works`, `Pricing`, `FAQ`, `Footer`. A section outside that set, or a fact not named in a `Blockable:` line, declared blocked is a **bug**. `Vision` defaults and flags — it is never blocked.
- **Blocked requires the user to confirm the fact is missing.** An explicit "skip" or "I have none" is that confirmation. Never asking, or inferring from the page, is not — absence on the page is the gap you're flagging, not proof the fact doesn't exist.
- **Ask for facts outside the blockable set too.** A real setup time, what the top plan includes, cancellation terms — batch them into the same tier-2 message. They never earn blocked status, but never report a fact you were simply never allowed to ask for as something the loop could not fix.
- **Stuck is not blocked.** Can't phrase the gap as a question the user could answer? Then it stays in the stop test, rides to round 3, and gets reported as *"converged at 2/3 — the loop could not fix this."*
- **Report `X / achievable`**, where `achievable = 42 − 3×(fully blocked) − 1×(capped-only)`. Raw 42 goes in a footnote. Otherwise a page that is perfect given the user's facts reads like a failure, punishing them for not having customers yet.

### Copy

- One question at a time when asking for missing required input.
- Never use "Buy" / "Purchase" as CTA labels.
- Default to zero jargon and benefit-first; deviate only when `icp_technicality = technical`.
- Default to no money-back guarantee; add only when `offer_guarantee = true`. A missing guarantee is a gap only in that case — never infer it from market, price, or ICP, which grades a business decision rather than the copy.
- Use scarcity only when `urgency_basis` is real.

### Improve mode preserves the user's page

- Off-blueprint sections (integrations, comparison table, changelog) stay **verbatim and unscored**.
- The user's section order stands unless a coupled must-have forces the move (Testimonials before Pricing).
- **Flag every section created from nothing as `NEW` in the trail.** A section you invented is not a section you improved. Without the flag, improve mode silently launders generated content as the user's own page.

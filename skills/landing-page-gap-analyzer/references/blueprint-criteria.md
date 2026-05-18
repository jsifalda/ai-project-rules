# Landing Page Blueprint — Scoring Criteria

Embedded best practices from `202605022129 - Master Landing Page Blueprint`. The blueprint defines 13 sections, global copy rules that apply everywhere, and conflict-resolution defaults that decide edge cases.

---

## Global Copy Rules (apply to every section)

- `we` → `you` — always rewrite first-person plural into second-person.
- Cut superlatives (best, fastest, ultimate, amazing) — let the reader conclude.
- One audience · one problem · one solution. Multi-audience pages get penalised.
- Assume the reader understands ~10% of your jargon → strip the rest or define it inline.
- Every section needs an emotional hook + rational explanation pairing.

## Conflict Resolutions (edge-case defaults)

- **Technical depth** → default zero jargon + benefit-first. Allow spec lines in Features *only* if `icp_technicality = technical`.
- **Refund policy** → default no money-back guarantee. Add a guarantee only if `b2b_or_b2c = b2b` AND audience is risk-averse / high-ticket → place it in FAQ as a safety question.
- **Pricing CTAs** → CTA under each plan (momentum) **and** one final repeated CTA below pricing.
- **Urgency / scarcity** → only when authentic (cohort close, limited seats, launch window). Fake countdowns are anti-patterns.

---

## Scoring rubric (applies to every section)

- **3** — all must-haves present and well-executed.
- **2** — all must-haves present but at least one is weak / generic.
- **1** — only 1 must-have present.
- **0** — section missing, or all must-haves missing.

Maximum total: **39** (13 sections × 3).

Auto-deduct anti-patterns are flagged separately in the Global Copy-Rule Violations block — they do not lower a section score below 0, but they appear in the prioritized fix plan.

---

## 1. Navbar

**Must-have:**
- Sticky / visible on scroll.
- 3–5 links max.
- Primary CTA present, high contrast, action-oriented label, *same wording as Hero CTA* (consistency bias).

**Anti-patterns:**
- More than 5 links / cluttered nav.
- CTA label says "Buy", "Purchase", "Sign up" generically (action-oriented = `Start free`, `Get my plan`, `Try [product]`).

---

## 2. Hero Section

Formula: `emotional promise + rational delivery`.

**Must-have:**
- **H1 = emotional promise** — biggest outcome, frontloaded (e.g. *"Finish more tasks without working more"*). Not a feature, not a category description.
- **H2 / sub-headline = product description** — explains *how* the promise is delivered (e.g. *"Our to-do app generates action plans for your tasks"*).
- **3 painkiller bullets** (max 5) — use-case + emoji/icon per bullet.
- **Primary CTA** — action-oriented, never `Buy` / `Purchase`.
- **Quick social proof** — customer photos, count, or 1-line review near the CTA.
- **Hero visual** — clean product mockup or result screenshot.

(All six factor into the 0–3 score; weight H1, H2, painkiller bullets most heavily.)

**Anti-patterns:**
- H1 is rational/feature-led (`The to-do app for teams`) instead of emotional.
- Vague CTA (`Learn more`, `Get started` with no context).
- Hero visual is a stock photo instead of the product.

---

## 3. Trust Logos

**Must-have:**
- Row of customer / press logos directly under the hero.
- Monochrome treatment to preserve hierarchy.
- Context line: *"Trusted by 500+ companies"* / *"Featured in…"*.

**Anti-patterns:**
- Full-color logos that fight the hero for attention.
- Logos with no context line.
- Fabricated / unverifiable logos.

---

## 4. Problem Definition

Two blocks: Problem Agitation + Transformation.

**Must-have:**
- **Problem agitation** — Point A status quo the customer hates, with **3 negative consequences** of staying there.
- **Transformation** — Point B desired state, with **3 positive benefits** of switching.
- Visual: product mockup or a "how it works" preview tying the transformation to the product.

**Anti-patterns:**
- Generic "managing X is hard" agitation with no specific consequences.
- Skipping straight to features without naming Point A.

---

## 5. How It Works (Process)

**Must-have:**
- 3–4 steps: setup → action → reward.
- Time estimate per step (*"~5 min"*).
- Icons or numbered visuals to reduce perceived effort.

**Anti-patterns:**
- 5+ steps (overwhelms).
- No time estimates → reader assumes it's complex.

---

## 6. Features

**Must-have:**
- 3–4 memorable power features.
- Outcome-first headline per feature + 1 line of mechanism.
- Icon + GIF/visual per feature.
- Highlight at least one differentiator competitors lack.

**Conditional must-have (technical ICP only):**
- A small spec/detail line per feature when `icp_technicality = technical`.

**Anti-patterns:**
- 5+ features listed (forgettable).
- Feature names that are internal jargon with no benefit framing.
- No visual / GIF.

---

## 7. Benefits Recap

**Must-have:**
- Rule of 3 — biggest gains only.
- Icon per benefit.
- Numbers / timeframes attached (*"30% faster"*, *"ship in a weekend"*).

**Anti-patterns:**
- Duplicates the Features section verbatim instead of distilling outcomes.
- Vague benefits without metrics or timeframes.

---

## 8. Social Proof / Testimonials

**Must-have:**
- 5–7 testimonials with photo + name + role.
- Lead with strongest specific-outcome quote.
- Mix of scannable + detailed lengths.
- Match ICP demographics.
- Positioned right before Pricing to ease purchase anxiety.

**Anti-patterns:**
- Anonymous testimonials.
- Generic praise (*"Great product!"*) with no specific outcome.
- Testimonials placed after Pricing (loses anxiety-easing function).

---

## 9. About / Why You Built It

**Must-have:**
- 2–3 short storytelling paragraphs + founder face.
- What the founder built before (credibility).
- Press / community mentions (Product Hunt, Indie Hackers, etc.).

**Anti-patterns:**
- No face / no name → reads like a faceless corp.
- Corporate "about us" boilerplate instead of personal story.

---

## 10. Pricing

**Must-have:**
- 2–3 plans: downsell · **main (visually anchored "Most popular")** · upsell.
- 3–5 plan bullets per plan, benefit-led.
- Prices ending in $7 or $9 (or $0 if luxury).
- Subscription vs one-time clearly labelled.
- Annual toggle with *"Save $X"* (loss aversion).
- CTA under every plan.

**Conditional must-have:**
- Money-back guarantee — *only* if `b2b_or_b2c = b2b` and ICP is risk-averse / high-ticket.
- Authentic scarcity (`urgency_basis` provided) → otherwise skip.

**Anti-patterns:**
- Round prices ($10, $50, $100) outside luxury positioning.
- No anchored "Most popular" plan.
- Missing CTA on any plan.
- Fake countdown / fake scarcity.

---

## 11. FAQ

**Must-have:**
- 5–7 conversion-blocking objections.
- Order: setup → billing → support → safety.
- Straightforward answers, no overselling.
- Safety questions included (cancel, trial; guarantee if offered).

**Anti-patterns:**
- Softball questions (*"Is your product good?"*) instead of real objections.
- Marketing-speak answers that dodge the objection.

---

## 12. Final CTA

**Must-have:**
- Repeats the core promise from the Hero in one line.
- Big CTA button — **same label** as Hero / Pricing CTAs.
- Optional micro-proof line under the button.

**Anti-patterns:**
- Different CTA label than Hero (breaks consistency bias).
- Generic closer (*"Ready to get started?"*).

---

## 13. Footer

**Must-have:**
- Simple nav (legal, contact, support).
- Trust badges / certifications where relevant.
- Repeated CTA for full-page scrollers.
- Social links.

**Anti-patterns:**
- Sitemap-bloat footer that distracts from the CTA.
- No repeated CTA → wasted real estate.

---

## Copy Quality Check (final gut-check)

A good landing page answers these 5 reader questions. Use them in the final block of the report.

1. Why should I care about this *right now*?
2. What will change in my life after using it?
3. Do people like me enjoy this?
4. How will I use it day-to-day?
5. Can I "try" it before buying?

Ideal answers sound like: *"Saves me X hours/week"*, *"Makes me $Y more"*, *"My peers use it"*.

Also note the **aftertaste** — the emotional residue after closing the page. One sentence.

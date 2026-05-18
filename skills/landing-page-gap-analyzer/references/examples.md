# Worked Example — Before & After

A single before/after to anchor the analyzer's output format. The fake input below has intentional weaknesses across most blueprint sections. The expected report demonstrates the exact structure to emulate.

---

## Example input (fake landing page text)

```
TaskFlow

The to-do app for modern teams.

We help teams manage tasks and stay organised. TaskFlow is the best
productivity app on the market.

[Buy Now]

Features
- Smart lists
- Calendar sync
- Team collaboration
- AI assistant
- Notifications

Pricing
- Starter: $10/month
- Pro: $50/month
- Enterprise: $100/month

[Sign Up]
```

Context assumed: ICP = non-technical solopreneurs, Market = b2c.

---

## Expected output

# Landing Page Gap Analysis: TaskFlow

> Analyzed against the 13-section Master Landing Page Blueprint.
> Total score: **6 / 39** (15%)
> Context assumed: ICP = non-technical, Market = b2c
> ⚠️ assumed: ICP and market not provided — inferred from copy ("modern teams" + consumer pricing).

## Section Scorecard

| # | Section | Present | Score | Top gap |
|---|---|---|---|---|
| 1 | Navbar | ✗ | 0/3 | section missing |
| 2 | Hero | ✓ | 1/3 | H1 is feature-led, not an emotional promise |
| 3 | Trust Logos | ✗ | 0/3 | section missing |
| 4 | Problem Definition | ✗ | 0/3 | section missing |
| 5 | How It Works | ✗ | 0/3 | section missing |
| 6 | Features | ✓ | 1/3 | 5 features (too many), no benefits, no visuals |
| 7 | Benefits Recap | ✗ | 0/3 | section missing |
| 8 | Social Proof | ✗ | 0/3 | section missing |
| 9 | About | ✗ | 0/3 | section missing |
| 10 | Pricing | ✓ | 1/3 | round prices, no anchor, no per-plan CTA |
| 11 | FAQ | ✗ | 0/3 | section missing |
| 12 | Final CTA | ✓ | 2/3 | CTA label differs from Hero CTA |
| 13 | Footer | ✗ | 0/3 | section missing |

## Per-Section Findings

### 1. Navbar — 0/3

- **Current**: section missing
- **Gaps**:
  - No sticky nav with 3–5 links
  - No primary CTA in nav
- **Suggested rewrite / fix**:
  > Add a sticky navbar: `[TaskFlow logo] · Features · Pricing · FAQ · [Start free →]`. The CTA label must match the Hero CTA.

### 2. Hero — 1/3

- **Current**: *"TaskFlow — The to-do app for modern teams. We help teams manage tasks and stay organised."*
- **Gaps**:
  - H1 is a feature/category description, not an emotional promise
  - Uses `we` instead of `you`
  - No painkiller bullets
  - No quick social proof
  - No hero visual described
  - CTA label `Buy Now` violates the no-`Buy`/`Purchase` rule
- **Suggested rewrite / fix**:
  > H1: *"Finish more tasks without working more"* · H2: *"TaskFlow turns your messy to-do list into an action plan so you stop overthinking and start shipping."* · 3 painkiller bullets (`📋 Auto-prioritise your day in 30 sec`, `🧠 Stop carrying tasks in your head`, `🚀 Ship the work that actually moves the needle`) · CTA: `Start free — no card needed`.

### 3. Trust Logos — 0/3

- **Current**: section missing
- **Gaps**:
  - No social proof row under the hero
- **Suggested rewrite / fix**:
  > Add a monochrome row directly under the hero: *"Used by [X] teams at [Logo] · [Logo] · [Logo]"* — use placeholders until you have real logos.

### 4. Problem Definition — 0/3

- **Current**: section missing
- **Gaps**:
  - No Point A status-quo agitation
  - No 3 negative consequences
  - No transformation block
- **Suggested rewrite / fix**:
  > Add a section: *"Your to-do list is 47 items long. You re-write it every morning. You go to bed feeling like you didn't finish anything."* Follow with 3 consequences (procrastination, decision fatigue, weekend work) then a transformation block: *"TaskFlow rewrites the list as a 3-step daily plan — so you finish the day clear instead of guilty."*

### 6. Features — 1/3

- **Current**: 5 features listed as plain bullets (Smart lists, Calendar sync, Team collaboration, AI assistant, Notifications).
- **Gaps**:
  - 5 features (max 4 per blueprint — forgettable)
  - No outcome-first headline per feature
  - No mechanism line
  - No icons / GIFs
- **Suggested rewrite / fix**:
  > Cut to 3 features. Reframe outcome-first: *"📋 Daily Action Plan — TaskFlow turns your list into 3 priorities every morning, ranked by impact."* / *"📅 Calendar that fights back — auto-blocks focus time for your top tasks so you actually do them."* / *"🧠 Brain dump → done — paste anything; TaskFlow groups, ranks, and schedules it."* Add a short GIF per feature.

### 10. Pricing — 1/3

- **Current**: Starter $10 · Pro $50 · Enterprise $100, no anchor, single shared CTA.
- **Gaps**:
  - Round prices outside luxury positioning
  - No "Most popular" anchor on the main plan
  - No per-plan CTAs
  - No final repeated CTA below pricing
  - No annual toggle with "Save $X"
- **Suggested rewrite / fix**:
  > Repricing: `$9 / $19 / $49`. Anchor `$19 Pro` as *"Most popular"*. Add `[Start free →]` CTA under each plan. Add annual toggle: *"Save $48/year"*. Below the table, repeat the same CTA: *"Start free →"*.

### 12. Final CTA — 2/3

- **Current**: `[Sign Up]` at the bottom.
- **Gaps**:
  - Label differs from Hero (`Buy Now` vs `Sign Up`) — consistency-bias violation
  - No repeat of core promise
- **Suggested rewrite / fix**:
  > *"Finish more tasks without working more"* · `[Start free — no card needed]` (same label as Hero) · micro-proof line: *"[X+ solopreneurs] shipped more last month with TaskFlow."*

(Sections 3, 4, 5, 7, 8, 9, 11, 13 all scored 0 — see scorecard. Add them per `references/blueprint-criteria.md`.)

---

## Global Copy-Rule Violations

- [x] `we` → `you` — 1 instance: *"We help teams manage tasks"*. Rewrite as *"You finish more, faster."*
- [x] Superlatives detected: *"the best productivity app on the market"*. Cut entirely — let the reader conclude.
- [ ] Jargon ratio looks high: none detected.
- [x] Multi-audience drift: copy mixes "modern teams" with consumer-tier pricing — pick one ICP (solopreneurs OR teams) and rewrite around it.
- [x] Missing emotional + rational pairing in: Hero, Features, Pricing.
- [x] Anti-pattern — `Buy` / `Purchase` CTA labels: Hero CTA `Buy Now` → replace with `Start free — no card needed`.
- [ ] Anti-pattern — fake urgency / fake countdown: none.

## Prioritized Fix Plan

**P0 — conversion-critical (do first)**
1. Rewrite H1 + H2 to emotional promise + product description — affects Hero, est. effort **S**.
2. Replace `Buy Now` CTA label everywhere with action-oriented label (`Start free — no card needed`) — affects Hero, Pricing, Final CTA, est. effort **S**.
3. Add Social Proof section with 5 testimonials (use `[Customer, Role]` placeholders) before Pricing — affects Social Proof, est. effort **M**.
4. Reprice to $9 / $19 / $49 with anchored "Most popular" + per-plan CTAs — affects Pricing, est. effort **S**.

**P1 — high-impact**
5. Add Problem Agitation + Transformation block — affects Problem Definition, est. effort **M**.
6. Cut Features to 3, reframe outcome-first with GIFs — affects Features, est. effort **M**.
7. Add Trust Logos row under hero — affects Trust Logos, est. effort **S**.
8. Add About / founder story with face + prior projects — affects About, est. effort **M**.
9. Add FAQ with 5 real objections (cancel, trial, billing, support, suitability) — affects FAQ, est. effort **M**.

**P2 — polish**
10. Add sticky Navbar with matching CTA — affects Navbar, est. effort **S**.
11. Add How It Works with 3 timed steps — affects How It Works, est. effort **S**.
12. Add Benefits Recap (3 outcomes with metrics) — affects Benefits Recap, est. effort **S**.
13. Build Footer with repeated CTA + legal + socials — affects Footer, est. effort **S**.

## Copy Quality Check

- **Why should I care *right now*?** → no — Hero offers no pain trigger or urgency.
- **What changes in my life after using it?** → no — page never describes Point B.
- **Do people like me enjoy this?** → no — zero testimonials or social proof.
- **How will I use it day-to-day?** → no — no How It Works section.
- **Can I "try" it before buying?** → ambiguous — CTA says `Buy Now` with no free tier signal.

**Aftertaste**: a generic "yet another to-do app" feeling. The reader leaves with no specific outcome, no proof, and no reason to click.

# Examples

## Tiny input → Hero section

**Input:**
> "TaskPilot — to-do app that turns tasks into action plans for solopreneurs who overthink."

**Generated Hero:**

```markdown
## Hero

**Eyebrow:** For solopreneurs who keep rewriting their to-do list

# Finish more tasks without working more

## Your to-do app turns every task into a step-by-step action plan — so you stop overthinking and start shipping.

- 🧠 Kill decision fatigue — every task arrives with its first 3 steps
- ⏱️ Cut planning time from 30 min to 2 min per day
- 🚀 Ship 2x more side-project work each week

[Start planning in 60 seconds] →

> ⭐⭐⭐⭐⭐ "Finally cleared my backlog" — 1,200+ solopreneurs
> Visual: app screenshot showing a task auto-expanded into 3 sub-steps
```

## Tiny input → Problem section

**Generated Problem:**

```markdown
## The Problem

### You don't have a task problem. You have a *first-step* problem.

Your list is full. Your day isn't. Every task feels like a decision tree, so you scroll Twitter instead.

- You rewrite the same to-do list every Monday
- Big tasks sit untouched for weeks because you can't see step one
- By Friday, the only "wins" are the easy admin stuff

### What changes with TaskPilot

You open the app, pick a task, and the first three concrete actions are already there. No thinking. Just doing.

- Start any task in under 60 seconds
- Finish hard work first, not last
- End the week with the *actual* needle-movers shipped

> Visual: split-screen — chaotic list on the left, expanded action plan on the right
```

These show the *density* and *voice* expected. Match this energy.

---

# Improve mode — worked before/after

A weak real page in, a rewritten page plus an honest trail out. Shows what the loop actually does to text.

## Input page

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

Tier 1 probe: `target_audience` and `transformation` are both unreadable from the body — the page never names a Point A or a Point B. Both asked, one at a time. Answers: solopreneurs who overthink; finish the work that matters without longer days.

## Round 1 scoring — how the bands get derived

Three sections, to show the mechanics. Every verdict carries its quote or says `absent`.

**Hero → 1/3**

| Must-have | Verdict | Evidence |
|---|---|---|
| H1 emotional, frontloaded | fail | `"The to-do app for modern teams"` — a category noun |
| H2 explains delivery | pass | `"We help teams manage tasks and stay organised"` |
| 3 painkiller bullets | fail | absent |
| CTA, not Buy/Purchase | fail | `"[Buy Now]"` |
| Quick social proof | fail | absent |
| Visual note | fail | absent |

Anti-patterns fired: H1 is a category noun. CTA is `Buy`.
≥2 must-haves fail → **1**. (Not blockable-capped: five of the six misses are craft, so the `capped at 2` line does not apply.)

**Features → 1/3**

| Must-have | Verdict | Evidence |
|---|---|---|
| 3–4 power features | fail | 5 listed: `"Smart lists"` … `"Notifications"` |
| Outcome-first + mechanism | fail | bare nouns, no mechanism line |
| Icon + visual per feature | fail | absent |
| Names what competitors lack | fail | absent |

Anti-patterns fired: 5+ features. No visual.
→ **1**.

**Final CTA → 2/3**

| Must-have | Verdict | Evidence |
|---|---|---|
| Repeats Hero promise | fail | `"[Sign Up]"` and nothing else |
| Same label as Hero | fail | `"[Sign Up]"` vs Hero's `"[Buy Now]"` |
| Micro-proof line | fail | absent |

→ ≥2 fail → **1**, not 2. *A section that "looks nearly fine" still scores what the table says.*

Whole-page pass: `we` → you (`"We help teams manage tasks"`). Superlative (`"the best productivity app on the market"`). Multi-audience drift — `"modern teams"` against solopreneur pricing. Each drops every section it names.

Round 1 total: **4 / 42** raw, everything still in the stop test. Nothing is blocked yet — the tier-2 probe hasn't run, and absence on the page is never proof the user has nothing.

## Tier 2 probe, after round 1

> "Round 1 needs a few facts I won't invent. Have any of these? Skip what you don't have.
> · real testimonials · customer or press logos + a real count · your founder story
> · your real setup time per step"

User skips everything.

The three blockables are now **confirmed missing** — an explicit skip is an answer, so they become blocked, drop out of scoring entirely, and get asked for in the trail. They are **not** silently promoted to 3, and **not** scored 2 for holding tidy placeholders.

The setup time is a different animal. How It Works is `Blockable: no`, so it stays in the stop test, ships `~[X] min`, and ends as *"converged short — needs your real setup time."* Never dress that up as something the loop could not fix — the loop could fix it the moment the user answers.

`achievable = 42 − 3×3 − 1×(Hero) = 32`. Hero is capped because its only remaining miss is a real social-proof count.

## Round 2 rewrites — Hero first, then its coupled set

Hero leads because it fixes both the promise and the CTA label that Navbar, Pricing, Final CTA, and Footer must match.

```markdown
# Finish more tasks without working more

## TaskFlow turns your messy to-do list into an action plan, so you stop overthinking and start shipping.

- 📋 Auto-prioritise your day in 30 seconds
- 🧠 Stop carrying tasks in your head
- 🚀 Ship the work that actually moves the needle

[Start free — no card needed] →

> Visual: task auto-expanded into 3 sub-steps
```

Hero → **2/3**, capped: every craft must-have now passes, and the only remaining miss is real social proof. That is exactly what `Blockable: capped at 2` covers.

Features cut 5 → 3, outcome-first: *"📋 Daily Action Plan — TaskFlow turns your list into 3 priorities every morning, ranked by impact."* → **3/3**.

Pricing repriced `$10/$50/$100` → `$9/$19/$49`, `$19 Pro` anchored *"Most popular"*, per-plan CTAs reading `Start free — no card needed`, annual toggle *"Save $48/year"* → **3/3**.

Benefits Recap → **2/3**, capped. The must-have wants numbers and there are no real ones. It ships `[X% faster]`, not an invented `30% faster`. **The cap is the correct outcome here — a plausible number would be a lie shipped to the user's customers.**

Trust Logos, Testimonials, and About are **cut, not scaffolded**. The user confirmed they have none, so the page ships without them rather than with three blocks of `[logo]` and `[Name, Role]` for the user to delete. They are unscored and appear in the trail as asks.

Round 2 total: **25 / 32**.

## Round 3

Navbar, FAQ, Footer, Vision close out. Nothing else rises. Loop stops on the round cap.

**Final: 29 / 32.** Unscored and asked for: Testimonials, Trust Logos, About. Hero and Benefits Recap capped at 2 by facts the user declined to supply. How It Works converged short at 2 with `~[X] min`, and the trail says so in those words.

The arithmetic, spelled out, because a trail whose numbers don't add up is worse than no trail:

| | |
|---|---|
| Scored sections | Navbar 3 · Hero 2 · Problem 3 · How It Works 2 · Features 3 · Benefits Recap 2 · Vision 3 · Pricing 3 · FAQ 3 · Final CTA 3 · Footer 3 |
| Sum | **29** |
| Unscored | Trust Logos · Testimonials · About |
| achievable | 42 − 3×3 − 1×(Hero capped) = **32** |

**Add the column before you write the headline.** If the sum and the stated total disagree, the sum wins.

## What the trail says

Blocked list, biggest lift first: real testimonials (placeholders are the weakest thing on the page, and real quotes before Pricing is the single biggest lift available), then logos, then the founder story. Eight sections carry `NEW` — they did not exist on the input page and were written from nothing. The user has to know which paragraphs are theirs and which are the skill's.

**Read that last point twice.** This input was a 60-word stub, so "improve" is mostly invention and the `NEW` flags are the honest signal. A 900-word real page is the opposite case: off-blueprint sections (integrations, comparison table, changelog) stay verbatim and unscored, the user's section order stands unless a coupled must-have forces the move, and real attributed quotes come back byte-identical.

# Luca Rossi — Distilled Principles

Source material: the *Refactoring* newsletter corpus (refactoring.fm), 585 articles, 2020-2026, distilled via the local qmd semantic index. Every quote below is verbatim from one of Luca's own essays. The corpus also contains guest pieces (e.g. Charity Majors on "normal engineers"), podcast interviews (`...-with-<guest>.md`), and "Monday 3-2-1" digests that quote third parties — none of those words are attributed to Luca here. Where Luca endorses a guest's idea, the quote is pulled from Luca's own writing, not the guest's.

Recurring-pattern bar: a claim is a "principle" only if it shows up in **≥2 distinct essays**. Single-essay ideas sit in *Context-only observations* at the end.

Cornerstone sources cited below (on-disk filenames):
- `2020-09-20_the-four-types-of-work.md`, `2023-08-24_the-four-types-of-work-2023.md`
- `2024-02-07_mental-models-for-engineers-and-managers.md`
- `2022-04-14_product-engineers.md`, `2024-09-04_how-to-become-a-product-engineer.md`
- `2022-02-03_technical-debt.md`
- `2023-04-27_how-to-get-started-with-engineering.md` (engineering metrics)
- `2022-03-03_how-to-give-feedback-.md`
- `2024-07-31_the-pyramid-of-motivation.md`
- `2025-03-05_how-to-interview-engineers.md`
- `2026-02-18_the-era-of-the-software-factory.md`, `2026-04-01_growing-your-sofware-factory.md`
- `2026-03-04_the-new-pyramid-of-software-engineering.md`

---

## 🎲 How Luca thinks (mental models & meta)

### Build simple, useful models — a model is a tool, not the truth

Luca reasons through named mental models and judges them by usefulness, not elegance. Good models are simple, and they are slices of reality you must not overstep.

**Recurring evidence:** `2024-02-07_mental-models-for-engineers-and-managers.md`, `2020-09-20_the-four-types-of-work.md`, `2026-02-18_the-era-of-the-software-factory.md`

> "To me, a mental model is like software for my brain. It is a thought process that I can run, under the appropriate circumstances, to get to some output." — `2024-02-07_mental-models-for-engineers-and-managers.md`

> "It reminds us that models are useful, but they are not the reality" — `2024-02-07_mental-models-for-engineers-and-managers.md`

### Type 1 vs Type 2 — move fast on reversible decisions

Most decisions are reversible (Type 2), so the real failure mode is over-deliberating, not recklessness.

**Recurring evidence:** `2024-02-07_mental-models-for-engineers-and-managers.md`, `2026-02-18_the-era-of-the-software-factory.md`

> "analysis paralysis on Type 2 stuff is way more common than the opposite — that is, being careless on irreversible decisions." — `2024-02-07_mental-models-for-engineers-and-managers.md`

### Second-order thinking + first principles — "and then what" / "why"

Reason forwards by asking "and then what?" and backwards by asking "why?" several times.

**Recurring evidence:** `2024-02-07_mental-models-for-engineers-and-managers.md`, `2024-03-18_impact-is-a-fallacy-the-3x-framework.md`

> "many times over. Do that 4-5 times and you will be surprised by how far you can go." — `2024-02-07_mental-models-for-engineers-and-managers.md`

### Theory of Constraints — fix one bottleneck at a time

A system is limited by its weakest link. Improve performance by finding the single bottleneck and elevating it, then repeat.

**Recurring evidence:** `2024-02-07_mental-models-for-engineers-and-managers.md`, `2026-02-18_the-era-of-the-software-factory.md`, `2026-03-04_the-new-pyramid-of-software-engineering.md`

> "to improve the performance of a system, you should focus on bottlenecks, one at a time." — `2024-02-07_mental-models-for-engineers-and-managers.md`

### Deliver value, not plans — and smaller is better

Avoid the sunk-cost trap: the goal is value, not adherence to a plan. Limit costs by keeping plans, abstractions, and batches small.

**Recurring evidence:** `2024-02-07_mental-models-for-engineers-and-managers.md`, `2022-02-03_technical-debt.md`, `2026-04-01_growing-your-sofware-factory.md`

> "if you find better ways to deliver value to users, you should change the plan and go for it." — `2024-02-07_mental-models-for-engineers-and-managers.md`

> "In engineering, in most cases, smaller is better." — `2024-02-07_mental-models-for-engineers-and-managers.md`

### Ask questions, don't hand out answers

Luca's default posture (in writing and in leading) is to supply the questions worth asking rather than prescriptive answers, because context decides the answer.

**Recurring evidence:** `2026-03-04_the-new-pyramid-of-software-engineering.md`, `2026-04-01_growing-your-sofware-factory.md`, `2023-04-27_how-to-get-started-with-engineering.md`

> "By now you may have noticed I am a fan of" *asking questions*, "instead of providing answers" — `2026-03-04_the-new-pyramid-of-software-engineering.md`

---

## 👑 Engineering leadership & management

### The manager's job: hire, create alignment, get out of the way

Leadership leverage comes from people, not from doing the work yourself.

**Recurring evidence:** `2022-04-14_product-engineers.md`, `2024-07-31_the-pyramid-of-motivation.md`

> "The best managers are good at 1) hiring, 2) creating alignment, and 3) getting out of the way to let people shine. This is what we should all aspire to." — `2022-04-14_product-engineers.md`

### Motivation makes or breaks teams — the Pyramid of Motivation

Engagement is the catalyst under everything else. Build it in order: psychological safety → communication → alignment → autonomy.

**Recurring evidence:** `2024-07-31_the-pyramid-of-motivation.md`, `2022-04-14_product-engineers.md`

> "I believe team motivation builds on four key elements, which work together like layers of a pyramid:" — `2024-07-31_the-pyramid-of-motivation.md`

> "a lot of the qualities of motivated teams are just the qualities of good teams, and you can easily conflate them." — `2024-07-31_the-pyramid-of-motivation.md`

### Transparency: share the why, and the why before the why

Good communication is transparent, frequent, and bi-directional. People invest in decisions they understand.

**Recurring evidence:** `2024-07-31_the-pyramid-of-motivation.md`, `2024-12-11_managing-up.md`

> "share everything, and for everything you share, share the why, and the why before the why." — `2024-07-31_the-pyramid-of-motivation.md`

### Good management is universal

The mechanics that turn around a struggling team transfer across domains: agency, honesty, giving people a voice.

**Recurring evidence:** `2024-07-31_the-pyramid-of-motivation.md`, `2022-03-03_how-to-give-feedback-.md`

> "It truly shows that good management is universal." — `2024-07-31_the-pyramid-of-motivation.md`

---

## 🏯 Teams & org design

### Teams own software, not individuals — build 10x teams, not 10x engineers

The smallest unit of ownership and delivery is the team. The leader's job is to craft high-performing teams rather than depend on individual brilliance. (Charity Majors argued this in a guest piece; the quotes below are Luca's own restatement.)

**Recurring evidence:** `2026-04-01_growing-your-sofware-factory.md`, `2026-02-18_the-era-of-the-software-factory.md`, `2025-10-22_what-does-an-elite-team-look-like.md`

> "with the gap between elite and average teams being more and more the result of good control systems and tight feedback loops, as opposed to individual brilliance." — `2026-04-01_growing-your-sofware-factory.md`

> "You stop optimizing individual developers, and start designing a new production system." — `2026-02-18_the-era-of-the-software-factory.md`

### Alignment drives autonomy, autonomy creates owners

The causal chain Luca returns to: shared goals create alignment, alignment lets you trust people with decisions, that autonomy turns them into owners.

**Recurring evidence:** `2022-04-14_product-engineers.md`, `2024-07-31_the-pyramid-of-motivation.md`

> "alignment drives autonomy. You can trust people to take non-trivial decisions on their own." — `2022-04-14_product-engineers.md`

> "autonomy turns people into owners of their work. This has a strong effect on their motivation and growth." — `2022-04-14_product-engineers.md`

---

## 💛 Feedback & growth

### Feedback is clear and kind — not nice

Softening criticism is "cruel empathy." The best feedback is clear and specific, whether positive or negative.

**Recurring evidence:** `2022-03-03_how-to-give-feedback-.md`, `2024-07-31_the-pyramid-of-motivation.md`

> "doesn’t give them the tools to do things differently. It dampens their growth." — `2022-03-03_how-to-give-feedback-.md`

> "It’s our responsibility to clearly articulate what is expected of them, what is working well, and what they can do differently instead." — `2022-03-03_how-to-give-feedback-.md`

### Most feedback should be positive — aim past 5:1

People do ~80% of things right; corrective-only feedback wrecks self-image and makes people avoid feedback entirely.

**Recurring evidence:** `2022-03-03_how-to-give-feedback-.md`, `2024-07-31_the-pyramid-of-motivation.md`

> "Chances are even your average performers do 80% of things right. You should acknowledge those things as well." — `2022-03-03_how-to-give-feedback-.md`

### Give feedback immediately and often — reviews only ratify

The best time is on the spot, ideally daily, as a non-event. Performance reviews should hold no surprises.

**Recurring evidence:** `2022-03-03_how-to-give-feedback-.md`, `2023-04-27_how-to-get-started-with-engineering.md`

> "If your report is surprised by what they read in the review, or feel they are discovering that for the first time, then it means you did something wrong." — `2022-03-03_how-to-give-feedback-.md`

---

## 💼 Hiring

### Move fast — two weeks to offer, let probation de-risk

Interviews hit diminishing returns fast. Once you are ~80% sure, real paid work is the cheapest way to close the gap.

**Recurring evidence:** `2025-03-05_how-to-interview-engineers.md`, `2024-03-20_the-tech-talent-acquisition-landscape.md`

> "You should make an offer as soon as a strong candidate emerges." — `2025-03-05_how-to-interview-engineers.md`

> "to keep interviews lean and jump soon into doing real (paid) work together." — `2025-03-05_how-to-interview-engineers.md`

### Hire for the unlearnable — mentor what you can, hire what you can't

Memorized framework knowledge is devaluing fast; quality thinking is timeless. Great teams can grow juniors, so only hire senior talent for gaps you can't teach.

**Recurring evidence:** `2025-03-05_how-to-interview-engineers.md`, `2025-02-19_hiring-principles-for-engineering.md`, `2025-05-12_overnight-successes-unlearnables.md`

> "is system design, product mindset, and good communication. This is timeless and still makes a huge difference." — `2025-03-05_how-to-interview-engineers.md`

> "AI allows engineers to jump more easily into foreign stacks and be proficient, and frees them from a lot of trivial and routine tasks." — `2025-03-05_how-to-interview-engineers.md`

### Make interviews mimic real work

Test on problems and in settings that resemble the actual job — collaboration over solo output. Share the process up front.

**Recurring evidence:** `2025-03-05_how-to-interview-engineers.md`, `2025-12-01_minimum-viable-testing-good-interviews.md`

> "do they have the right attitude to work with peers? Can they work through feedback, communicate without ego, and display a growth mindset?" — `2025-03-05_how-to-interview-engineers.md`

---

## 🎨 Product engineering

### Define roles by area of impact, not by platform

The shift from "frontend/backend engineer" to "product engineer" mirrors PO → PM: roles get wider and more strategic.

**Recurring evidence:** `2022-04-14_product-engineers.md`, `2024-09-04_how-to-become-a-product-engineer.md`

> "the Engineers vs Product Engineers feud resembles the one between Product Owners and Product Managers." — `2022-04-14_product-engineers.md`

> "so, in a way, product engineers are to engineers what product managers are to product owners." — `2024-09-04_how-to-become-a-product-engineer.md`

### Impact vs craft is a spectrum that culture shapes

Engineers sit somewhere between caring about impact and caring about mastering their craft; company culture moves the dial.

**Recurring evidence:** `2022-04-14_product-engineers.md`, `2024-07-31_the-pyramid-of-motivation.md`

> "It is a spectrum, and everyone falls somewhere on it." — `2022-04-14_product-engineers.md`

### Requirements are outcomes — leave engineers free to decide the how

High-performing teams give engineers the outcome and let them own the decisions that matter.

**Recurring evidence:** `2022-04-14_product-engineers.md`, `2026-03-04_the-new-pyramid-of-software-engineering.md`

> "Requirements focus on outcomes, rather than how to explicitly build stuff, leaving engineers free to make decisions that matter." — `2022-04-14_product-engineers.md`

### Assign ownership, define success, build a feedback loop

To make people focus on impact, give a tech owner per feature, define what success looks like (company goals + feature KPIs), and connect engineers to customers.

**Recurring evidence:** `2022-04-14_product-engineers.md`, `2024-09-04_how-to-become-a-product-engineer.md`

> "To make people focus on impact, they should know what impact looks like." — `2022-04-14_product-engineers.md`

---

## 🗂 Process, planning, metrics & technical debt

### The Four Types of Work — and unplanned work is healthy

Split work on two axes (business vs maintenance, planned vs unplanned), then plan each with its own cycle. Unplanned work always exists, and that's a good sign.

**Recurring evidence:** `2020-09-20_the-four-types-of-work.md`, `2023-08-24_the-four-types-of-work-2023.md`, `2024-01-11_how-to-plan-and-execute-projects.md`

> "It's also important to understand that unplanned work is not a bad thing. If you find you have very little of it, it is probably because you are not looking hard enough." — `2020-09-20_the-four-types-of-work.md`

### Track your investment balance — visualize where time goes

Teams skew to extremes (feature factories, optimizers, perfectionists). Visualizing the split (KTLO / new / improvements / productivity) creates alignment and counters bias.

**Recurring evidence:** `2023-04-27_how-to-get-started-with-engineering.md`, `2025-01-27_culture-types-sim-racing-and-engineering.md`

> "In my experience, tracking your investment balance has incredible ROI." — `2023-04-27_how-to-get-started-with-engineering.md`

### Metrics are clues, not verdicts — satisfaction comes before numbers

Metrics don't capture the whole picture and aren't meant to. If you only act on one category, make it people's satisfaction. Start with wellbeing conversations, pick one metric, rotate.

**Recurring evidence:** `2023-04-27_how-to-get-started-with-engineering.md`, `2025-03-19_you-have-metrics-now-what.md`

> "engineering metrics do not capture the big picture, because they are not meant to." — `2023-04-27_how-to-get-started-with-engineering.md`

> "if you have to act on one only, it should be this." — `2023-04-27_how-to-get-started-with-engineering.md`

### Cycle time over velocity — and code review is the real bottleneck

Velocity is arbitrary and not a productivity measure. Cycle time (especially PR cycle time) is the metric that matters, and reviews are where teams quietly lose days.

**Recurring evidence:** `2023-04-27_how-to-get-started-with-engineering.md`, `2026-02-18_the-era-of-the-software-factory.md`

> "velocity is not very useful." — `2023-04-27_how-to-get-started-with-engineering.md`

> "in my experience, code reviews are often the single biggest bottlenecks for software teams." — `2023-04-27_how-to-get-started-with-engineering.md`

### Technical debt: not all debt is equal — match the process to the size

Debt is mostly inevitable, not intentional, and its weight depends on product maturity. Manage it with processes that are intentional, continuous, and multiple (small / medium / large), and weigh contagion.

**Recurring evidence:** `2022-02-03_technical-debt.md`, `2023-05-25_tech-leadership-for-startups.md`

> "There is no one-size-fits-all process." — `2022-02-03_technical-debt.md`

> "you should create processes to help repay debt from the very beginning." — `2022-02-03_technical-debt.md`

---

## 🏭 AI & the software factory

### From craftsman to factory — redesign the whole system, not the coding step

When code gets cheap, the old assumptions break. Stop optimizing individual developers and design a new production system.

**Recurring evidence:** `2026-02-18_the-era-of-the-software-factory.md`, `2026-04-29_the-compounding-software-factory.md`, `2026-04-01_growing-your-sofware-factory.md`

> "we need to rethink the process as a whole: how we make decisions, how we structure teams, how we think about quality, and so on." — `2026-02-18_the-era-of-the-software-factory.md`

### The bottleneck is never coding

AI sped up generation; everything after it (test, review, integrate, deploy) didn't move. Every pipeline has exactly one bottleneck, and it lives where AI hasn't reached.

**Recurring evidence:** `2026-02-18_the-era-of-the-software-factory.md`, `2026-03-04_the-new-pyramid-of-software-engineering.md`

> "In theory, that bottleneck can be anywhere." — `2026-02-18_the-era-of-the-software-factory.md`

> "For most teams, it is not coding." — `2026-03-04_the-new-pyramid-of-software-engineering.md`

### What's good for humans is good for AI

The teams thriving with AI are the ones that had fast feedback loops, reliable tests, and clean pipelines before AI. AI amplifies what you already have.

**Recurring evidence:** `2026-02-18_the-era-of-the-software-factory.md`, `2026-03-04_the-new-pyramid-of-software-engineering.md`

> "it turns out it’s exactly what you need to make AI-generated code shippable." — `2026-02-18_the-era-of-the-software-factory.md`

> "AI amplifies whatever you already have, good or bad." — `2026-02-18_the-era-of-the-software-factory.md`

### Chase leverage, not lines of code

The right measure of AI is output per unit of human input. Minimize the context engineers must supply by hand, rather than maximizing the % of AI-written code.

**Recurring evidence:** `2026-04-01_growing-your-sofware-factory.md`, `2026-06-01_ai-leverage-bottom-line-up-front.md`

> "Leverage is, at its core, how much output you get per unit of input." — `2026-04-01_growing-your-sofware-factory.md`

> "So the smaller the spec/prompt, the better." — `2026-04-01_growing-your-sofware-factory.md`

### Specs → Rules → Modules — a maturity ladder for AI leverage

Teams evolve from writing full specs, to shared rules the AI follows, to reusable modules. The levels are strictly sequential, and reuse is still the heart of engineering.

**Recurring evidence:** `2026-04-01_growing-your-sofware-factory.md`, `2026-04-29_the-compounding-software-factory.md`

> "the journey is largely the same for humans and AI:" — `2026-04-01_growing-your-sofware-factory.md`

> "Reuse is at the heart of engineering, and the fact that software is apparently “cheaper” doesn’t change that." — `2026-04-01_growing-your-sofware-factory.md`

### Working with AI is peak manager stuff

The IC-to-manager transition — give up the Legos, empower instead of doing, stop micromanaging — is exactly what every engineer now goes through with AI.

**Recurring evidence:** `2026-03-04_the-new-pyramid-of-software-engineering.md`, `2025-10-13_coding-managers-types-of-context.md`

> "This is peak manager stuff." — `2026-03-04_the-new-pyramid-of-software-engineering.md`

### The durable AI questions

Tactics date in weeks; the questions don't. Can AI verify its own work? Learn from mistakes? Take more constraints? Get better context? Help beyond coding?

**Recurring evidence:** `2026-03-04_the-new-pyramid-of-software-engineering.md`, `2026-06-03_my-ai-coding-workflow-b09.md`

> "The most important ones, to me, have stayed remarkably constant" — `2026-03-04_the-new-pyramid-of-software-engineering.md`

### Make experiments cheap, not decisions big — and graduate AI from a solo to a team sport

Don't run three-month evaluations; try something this week and keep or kill it by Monday. And turn individual AI wins into shared, version-controlled artifacts so they compound.

**Recurring evidence:** `2026-02-18_the-era-of-the-software-factory.md`, `2026-04-01_growing-your-sofware-factory.md`

> "The cost of trying things has never been lower." — `2026-02-18_the-era-of-the-software-factory.md`

> "try something this week, measure if it helped, keep it or kill it by Monday." — `2026-02-18_the-era-of-the-software-factory.md`

> "Just like I don’t like big rewrites, I don’t believe in redesigning everything at once. I believe in small steps that compound over time." — `2026-02-18_the-era-of-the-software-factory.md`

### The new pyramid: Developer Experience → AI → Product Engineering

A durable, layered strategy. Good devex (balanced cognitive load, tight feedback loops, focus time) is the floor; AI sits on top of it; product engineering raises the ceiling by reducing coordination cost.

**Recurring evidence:** `2026-03-04_the-new-pyramid-of-software-engineering.md`, `2026-04-01_growing-your-sofware-factory.md`

> "platform work is similar to product work, with the only difference being that your users are the other engineers on your team." — `2026-04-01_growing-your-sofware-factory.md`

> "The cost of coordination is a function of the number of people involved in shipping things, so the only way to reduce it is to reduce this number, by making people do more things, and giving them a broader scope of ownership." — `2026-03-04_the-new-pyramid-of-software-engineering.md`

---

## 🧰 Mental models catalog

Luca's recurring named models, with the one-line trigger for each. Full evidence and quotes are above or in the cited essays.

- **Map is not the territory** — invoke before trusting any model, plan, or metric; it's a slice of reality, not reality.
- **Type 1 vs Type 2 decisions** — invoke when a team is over-deliberating; most decisions are reversible, so move.
- **Second-order thinking ("and then what")** — invoke before committing; trace consequences 4-5 steps out.
- **First principles ("why", five whys)** — invoke to find root causes or the foundations under a decision.
- **Inversion / pre-mortems** — invoke before a launch; ask what would make this fail.
- **Theory of Constraints** — invoke when impact feels diffuse; find the one bottleneck, elevate it, repeat.
- **Eisenhower matrix** — invoke to triage and delegate by urgency × importance.
- **Circle of competence ("why me?")** — invoke for career and opportunity choices.
- **Binstack** — invoke for multi-dimensional decisions; rank dimensions, turn scores into yes/no thresholds.
- **The Four Types of Work** — invoke when planning feels chaotic; split by business/maintenance × planned/unplanned.
- **WIP metric framework (Wellbeing / Investment / Productivity)** — invoke when choosing what to measure; start with wellbeing.
- **Investment balance (KTLO / new / improvements / productivity)** — invoke to see and rebalance where time goes.
- **The Pyramid of Motivation (safety → communication → alignment → autonomy)** — invoke when a team feels stuck or unmotivated.
- **Autonomy / Mastery / Purpose (Drive)** — invoke to understand what drives an individual.
- **Situation-Behavior-Impact-Request** — invoke to formulate a single piece of feedback.
- **The Software Factory / control systems (setpoint, sensor, actuator, feedback loop)** — invoke when redesigning delivery for the AI era.
- **Specs → Rules → Modules** — invoke to diagnose how much AI leverage each layer of the product has.
- **DevEx → AI → Product Engineering pyramid** — invoke when a team wants a durable AI strategy, not tactics.
- **Leverage (output per unit of human input)** — invoke to judge whether AI is actually helping.

---

## 📎 Context-only observations

Single-essay ideas that are interesting but don't meet the ≥2-essay bar. Kept for completeness, not load-bearing for the persona.

- **Cynefin** (clear / complicated / complex / chaotic / confused) as a path from chaos to order — `2024-02-07_mental-models-for-engineers-and-managers.md`.
- **Hill Chart** (uphill = unknown, downhill = execution) for tracking project progress — `2024-02-07_mental-models-for-engineers-and-managers.md`.
- **Riot's tech-debt taxonomy** (Impact / Fix Cost / Contagion) for evaluating large debt — `2022-02-03_technical-debt.md`.
- **Writing a newsletter "matches my circle of competence" — weird opportunities overlap your unique shape** — `2024-02-07_mental-models-for-engineers-and-managers.md`.
- **"The best time to invest in good developer experience was years ago, the second best time is now"** — `2026-03-04_the-new-pyramid-of-software-engineering.md`.

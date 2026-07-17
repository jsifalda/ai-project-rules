# Input Schema

Two modes read this file differently:

- **generate** — the clarify gate below. Ask for missing required fields one at a time. Nothing gets written until it passes.
- **improve** — the page is the input. Skip the gate entirely and use the probe tiers at the bottom instead.

## Generate mode

Ask for missing **required** fields one at a time, in this order. Use the exact prompt or a close paraphrase. After each answer, restate briefly and move on.

### Required

| # | Field | Question to ask |
|---|---|---|
| 1 | `product_name` | "What's the product called?" |
| 2 | `one_line_pitch` | "In one sentence, what's the biggest *outcome* a customer gets? (the emotional promise — not what the product does, what changes for them)" |
| 3 | `target_audience` | "Who's the *one* ideal customer? Be as specific as possible (role, company size, life situation)." |
| 4 | `core_problem` | "What do they hate about how they solve this today? What's the status quo?" |
| 5 | `transformation` | "After using your product, what does their life look like? Their Point B." |
| 6 | `top_painkiller_use_cases` | "Give me 3 concrete use-cases / painkillers — short bullets, ideally with an emoji." |
| 7 | `top_features` | "Give me 3 power features. For each: feature name + one line on *how* it delivers value." |
| 8 | `pricing_model` + `price_points` | "How is it priced? (subscription / one-time / freemium) — and the actual prices for each plan." |

If the user's initial product description already answers some of these, **skip them**. Only ask for what's truly missing.

### Optional (smart defaults + inline flag)

| Field | Default if missing | Inline flag |
|---|---|---|
| `vision` | One-line vision derived from `transformation` + `one_line_pitch` (the bigger change this points toward) | `> ⚠️ assumed vision — replace with your real mission, or run create-product-vision to draft one` |
| `founder_story` | Generic "built it because I lived this problem" placeholder | `> ⚠️ assumed founder story — replace with your real "why"` |
| `testimonials` | 5 placeholder cards `[Name, Role]` with templated specific-outcome quotes | `> ⚠️ placeholders — swap in real quotes ASAP` |
| `trust_logos` | Generic "Trusted by 500+ teams" line + logo slots | `> ⚠️ placeholder — add real logos / press mentions` |
| `icp_technicality` | `non-technical` → benefit-first, no specs | — |
| `offer_guarantee` | `false` → no guarantee in FAQ | — |
| `urgency_basis` | none → omit scarcity language | — |

### Order of Operations

This is the **clarify gate** — nothing gets generated until it passes.

1. Parse what's already given.
2. Walk fields 1→8. For each missing one: ask, wait, restate.
3. Ask for `vision` — "What's the bigger mission here? The change you want to be part of, beyond what one user gets." If the user has none, offer to draft one with the `create-product-vision` skill, or proceed with the default (derived from `transformation` + `one_line_pitch`) and flag it inline. Never block on vision.
4. Confirm optional fields with a single yes/no per field *only if* the answer would change output structure (e.g. "Is your ICP technical?" / "Do you offer a money-back guarantee?" / "Any authentic scarcity to use — limited seats, launch window, cohort close?").
5. Draft, then hand to the loop.

### Blocked, in generate mode

A section is blocked iff its source optional field was **defaulted at this gate**. `testimonials` → Testimonials. `trust_logos` → Trust Logos. `founder_story` → About. That is a direct read of gate state, not an inference. `vision` is never blocked — it defaults and flags.

---

## Improve mode — probe tiers

The page is the input, so there is no gate. Ask as little as possible: a pasted URL should stay paste-and-go.

### Tier 1 — blocking, before the loop, max 2, one at a time

- `target_audience`
- `transformation`

Ask **only** when unreadable from the page body. Most real pages answer both, so this is usually zero questions.

**Extract them from the body — the Problem section, Features, testimonials — never from the H1.** The rubric grades the H1 *against* the promise. Infer the promise from the H1 and you grade the H1 against itself, which always passes and makes the Hero score meaningless. If the body gives no independent target, that is the one thing worth blocking to ask.

### Tier 2 — after round 1, batched into one message, skippable

Ask once, for every concrete fact round 1 found missing. Two kinds, in one message:

**The three blockables** — real testimonials, trust logos, founder story. Only these can earn blocked status.

**Facts any other section needs** — a real setup time, what the top plan includes, the annual price, cancellation terms, trust badges. These never earn blocked status. They stay in the stop test, and if the user declines they end as *"converged short — needs X from you"*, naming the fact.

> "Round 1 needs a few facts I won't invent. Have any of these? Skip what you don't have.
> · real testimonials (quotes + names + roles) · customer or press logos + a real count · your founder story
> · your real setup time · what Studio includes · annual price, if you sell one"

**Blocked requires the user to confirm the fact is missing.** An explicit "skip" or "I have none" **is** that confirmation, and the section is blocked. Never asking, or inferring from the page, is **not** — absence of testimonials on the page is the gap you are meant to flag, not evidence the user has none. Blocked-because-absent is circular reasoning and the loop must never do it.

### Tier 3 — never asked, defaulted + flagged inline

| Field | Default |
|---|---|
| `icp_technicality` | `non-technical` |
| `offer_guarantee` | `false` |
| `urgency_basis` | none |

A missing guarantee is a gap only when `offer_guarantee = true`. Never infer the guarantee from the market, the price, or the ICP — that grades a business decision, not the copy.

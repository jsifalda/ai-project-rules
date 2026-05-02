# Input Schema

Ask for missing **required** fields one at a time, in this order. Use the exact prompt or a close paraphrase. After each answer, restate briefly and move on.

## Required

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

## Optional (smart defaults + inline flag)

| Field | Default if missing | Inline flag |
|---|---|---|
| `founder_story` | Generic "built it because I lived this problem" placeholder | `> ⚠️ assumed founder story — replace with your real "why"` |
| `testimonials` | 5 placeholder cards `[Name, Role]` with templated specific-outcome quotes | `> ⚠️ placeholders — swap in real quotes ASAP` |
| `trust_logos` | Generic "Trusted by 500+ teams" line + logo slots | `> ⚠️ placeholder — add real logos / press mentions` |
| `icp_technicality` | `non-technical` → benefit-first, no specs | — |
| `offer_guarantee` | `false` → no guarantee in FAQ | — |
| `urgency_basis` | none → omit scarcity language | — |

## Order of Operations

1. Parse what's already given.
2. Walk fields 1→8. For each missing one: ask, wait, restate.
3. Confirm optional fields with a single yes/no per field *only if* the answer would change output structure (e.g. "Is your ICP technical?" / "Do you offer a money-back guarantee?" / "Any authentic scarcity to use — limited seats, launch window, cohort close?").
4. Generate.

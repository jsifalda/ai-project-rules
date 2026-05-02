---
name: landing-page-copy
description: Generate high-converting landing page copy in markdown from a short product description. Use when the user asks to "write landing page copy", "create a landing page", "LP copy", "sales page", "draft a landing page", or wants conversion-focused marketing copy structured by section. Asks one question at a time for any missing required input.
---

# Landing Page Copy

Turn a short product description into a complete, conversion-focused landing page in markdown — section by section, following a battle-tested blueprint.

## Workflow

1. **Read the input**. Extract whatever is already given.
2. **Map to schema**. See [references/input-schema.md](references/input-schema.md) for required vs optional fields.
3. **Ask one question at a time** for each missing *required* field, in the order listed in the schema. Do not batch. Do not proceed until all required fields are answered.
4. **Apply smart defaults** for missing *optional* fields and flag them inline in the output as `> ⚠️ assumed:` notes the user can revise.
5. **Generate the page** by filling [assets/output-template.md](assets/output-template.md), guided by [references/blueprint.md](references/blueprint.md).
6. **Apply copy rules** from [references/copy-rules.md](references/copy-rules.md) — voice, anti-patterns, conflict-resolution defaults.
7. **Run the self-check** (5 questions in copy-rules.md). If any section fails, rewrite that section once before returning.
8. **Return** the completed markdown landing page. Nothing else — no preamble, no postscript.

## Inputs

Required (skill blocks until provided):
- `product_name`
- `one_line_pitch` (the emotional H1 promise)
- `target_audience` (one specific ICP segment)
- `core_problem` (the status quo they hate)
- `transformation` (the desired Point B)
- `top_painkiller_use_cases` (3, ideally with emoji)
- `top_features` (3, each with a 1-line mechanism)
- `pricing_model` + `price_points`

Optional (defaults applied + flagged):
- `founder_story`, `testimonials`, `trust_logos`, `icp_technicality`, `offer_guarantee`, `urgency_basis`

Full prompts and defaults: [references/input-schema.md](references/input-schema.md).

## Output

Markdown only. Sections in order:
Navbar · Hero · Trust Logos · Problem · How It Works · Features · Benefits Recap · Testimonials · About · Pricing · FAQ · Final CTA · Footer.

Section requirements: [references/blueprint.md](references/blueprint.md).
Skeleton: [assets/output-template.md](assets/output-template.md).
Voice + conflict-resolution defaults: [references/copy-rules.md](references/copy-rules.md).
Worked example: [references/examples.md](references/examples.md).

## Non-negotiables

- One question at a time when asking for missing required input.
- Never invent testimonials with real-sounding names — use `[Customer Name, Role]` placeholders.
- Never use "Buy" / "Purchase" as CTA labels.
- Default to zero jargon and benefit-first; deviate only when `icp_technicality = technical`.
- Default to no money-back guarantee; add only when `offer_guarantee = true`.
- Use scarcity only when `urgency_basis` is provided and authentic.

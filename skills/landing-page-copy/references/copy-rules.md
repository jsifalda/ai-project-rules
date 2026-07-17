# Copy Rules

## Voice
- Write to *one* reader. "You", never "we".
- Cut superlatives (best, fastest, ultimate). Let the reader conclude.
- One audience · one problem · one solution per page.
- Assume the reader understands ~10% of your jargon. Strip the rest.
- Every section: emotional hook + rational explanation.
- Short sentences. Concrete nouns. Active verbs.

## CTA Rules
- Action-oriented labels. Never "Buy" or "Purchase".
- Same label across hero, pricing, and final CTA (consistency bias).
- High contrast.

## Conflict-Resolution Defaults
These resolve contradictions in upstream advice. Override only when the input flag says so.

| Topic | Default | Override condition |
|---|---|---|
| Technical depth | Zero jargon, benefit-first | `icp_technicality = technical` → add specs in Features |
| Money-back guarantee | None | `offer_guarantee = true` → add safety FAQ entry |
| Pricing CTAs | CTA under every plan **and** repeated final CTA | — |
| Scarcity / urgency | Omit | `urgency_basis` provided + authentic → use it once in eyebrow or pricing |
| Refund policy mention | Skip entirely | only if guarantee exists |

## Anti-Patterns (never do)
- Generic platitudes ("revolutionary platform", "next-gen solution")
- Fake urgency ("Only 3 spots left!" with no basis)
- Invented testimonials with real-sounding names
- Feature-first headlines when benefit works
- Walls of text — break into bullets and short paragraphs
- "We are passionate about…" About sections

## The whole-page pass

Criteria, not a procedure. The scoring loop in `SKILL.md` consumes these and owns all iteration — do not rewrite anything from here.

**This pass is the only part of the loop that reads.** The per-section rubric counts parts: it can confirm Pricing has all seven of its must-haves and FAQ fields seven real objections, and still miss that the page never says what the free trial actually is. Structure passes, the reader still can't buy. Never skip this to save a step, and never treat the section scores as a verdict on the writing.

Each round, check:

1. The five reader questions below.
2. Every row of the cross-section table in `blueprint.md` — CTA-label consistency, Testimonials adjacent to Pricing, Final CTA repeating the Hero promise, Benefits Recap not duplicating Features.
3. `we` → `you`, superlatives, one-audience drift.
4. Any blocked section that shipped placeholder scaffolding instead of being cut.
5. The aftertaste.

**A failing check drops each section it names by exactly 1, floor 0.** Not "to zero", not "by some amount" — one point, and name the sections explicitly. A vague magnitude here is worth several points of drift across a page and makes two honest scorers disagree on the total.

**Exemption: a check that fails only because of a confirmed-missing fact does not drop the sections already capped for that fact.** Reader question 3 ("do people like me use this?") fails on a page with no testimonials — but Hero and Trust Logos are already capped for exactly that missing social proof, and docking them again is the double-punishment the whole blocking system exists to prevent. Report it as an ask, not a deduction. The exemption is narrow: it applies only when the *sole* cause is a fact the user confirmed they lack.

**Item 4 is a rewrite instruction, not a deduction.** A blocked section is unscored, so no arithmetic can price its scaffolding. The remedy is that step 4 of the loop *cuts* it. Naming it here is what triggers the cut.

## Reader Questions

The finished page must clearly answer:
1. Why should I care about this *right now*?
2. What changes in my life after I use it?
3. Do people like me use this?
4. How will I use it day-to-day?
5. Can I try it before I buy?

A fuzzy answer is a failed check. Name the sections it implicates (Hero, Problem, Testimonials, How It Works, Pricing/FAQ) and drop each one's score — the loop rewrites them.

Good answers sound like *"saves me X hours/week"*, *"makes me $Y more"*, *"my peers use it"*.

## Aftertaste

The emotional residue after closing the page. One sentence, and it must be intentional — hopeful, urgent, or calm by choice, not by accident. Part of the whole-page pass.

- Does the page sound like a human, or a brochure?
- Could a competitor copy-paste this page and have it still ring true? If yes, the specifics aren't sharp enough.

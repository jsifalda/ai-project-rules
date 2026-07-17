# Blueprint — Section Requirements & Scoring

Source of truth for what each section must contain, what disqualifies it, and how it scores. Keep it tight; this is a checklist, not prose.

14 sections. Global voice rules, conflict-resolution defaults, and the whole-page pass live in [copy-rules.md](copy-rules.md) — not here.

**Two jobs, split on purpose.** A **blind scorer** gets the page text plus this file and copy-rules.md, and nothing else. It returns bands and whole-page verdicts. It cannot know which facts the user lacks, so it never applies caps and never computes `achievable`. The **loop** holds the clarify-gate and probe answers, so it applies the `Blockable:` caps, computes `achievable`, and runs the fabrication check. Keep the split: the scorer's ignorance is what makes its bands trustworthy, and the loop's knowledge is what makes the denominator honest.

---

## How to score a section

**Derive the band. Never choose it.**

For each must-have, record a binary verdict plus **the verbatim quote from the page that satisfies it**, or `absent`. A must-have with no quote is `absent`, no matter what the section was meant to say. Then check that section's anti-patterns against the same text.

Count **demerits**. One demerit per failed must-have, one per fired anti-pattern. Then:

```
demerits = (failed must-haves) + (fired anti-patterns)

3 = 0 demerits, and no unresolved placeholder
2 = exactly 1 demerit, or 0 demerits with a placeholder present
1 = 2 or more demerits
0 = section absent, or ≤1 must-have passes
```

One scale, so a section that both fails a must-have *and* trips an anti-pattern has 2 demerits and scores 1. No cell is undefined, and nothing gets adjudicated by taste.

Rules that make the band honest:

- **Score from the page text alone.** What you meant is not evidence. Only what a cold reader can see counts.
- **Quote or it fails.** "The H1 is emotional" is not a verdict. `"Finish more tasks without working more"` is.
- **A placeholder is not evidence, and the cap only lowers.** `[logo]` does not satisfy "a row of logos" — that must-have is `absent`. `[X] customers` does not satisfy a count. Score the must-haves honestly first; *then* apply the cap: **a section holding an unresolved placeholder can never score 3.** The cap is a ceiling, never a floor. A section that is nothing but scaffolding scores 0 or 1, and must never be credited a 2 for containing well-formatted brackets.
- **What counts as a placeholder.** Brackets are overloaded, so use the meaning, not the syntax. Three species:
  - **Label** — something the reader clicks or reads: `[Start free — no card needed]`, `[Privacy]`, `[Twitter]`. Resolved content. Never caps.
  - **Placeholder** — a fact the author still owes: `[X] freelancers`, `[encryption standard]`, `[Name]`, `[publication]`. Caps.
  - **Author-directed instruction** — a note telling the author what to write: `[Add your security detail — encryption standard, provider, and audits.]`. Caps, same as a placeholder, and it must never ship.

  Tiebreak when the species is unclear: would shipping the page as-is embarrass the author? `[X] banks` would. `[Pricing]` would not.
- **The cap does not fire on an element the section marks optional.** An optional micro-proof line attempted as `[X] freelancers` must not score below the same section with the line deleted. Never let the rubric pay the author to ship less.
- **`> ⚠️ assumed:` flags do not trigger the cap.** They mark content derived from what the user *did* give (Vision from `transformation` + `one_line_pitch`), not a fact that is missing. Only an unresolved placeholder caps.
- **Rendering properties are carried as notes.** The output is markdown copy, not a build. "Sticky on scroll" and "monochrome" are satisfied by an explicit note in the page (`> Sticky on scroll`), which is quotable. Without the note they are `absent` — but never fail a page for markdown's inability to be sticky.

### What actually has teeth

The must-haves alone cannot grade this page. The output template has a slot for every one of them, so a template-faithful draft passes them by construction. **The placeholder cap and the anti-patterns are the only checks the template cannot satisfy by itself** — the cap catches unfilled facts, the anti-patterns catch lazy prose. Run every one, every round.

Know the limit, and do not oversell the number: **this rubric counts parts, it does not read.** It detects an incomplete page reliably and a merely mediocre one poorly. Competent-but-flat prose scores the same as sharp prose as long as the bullets count and the notes exist. That gap is what the whole-page pass in [copy-rules.md](copy-rules.md) — the five reader questions and the aftertaste — is there to close. It is not optional garnish; it is the only part of the loop that reads.

## `Blockable:` — a lookup, never a judgment

Some sections need a fact only the user has. They are marked `Blockable:` below, and **that line is the whole decision**. Read it. Do not reason about it.

- **`Blockable: no`** — you have everything you need. If a section marked `no` is ever declared blocked, **that is a bug**, not a finding.
- **`Blockable: yes`** — once the user confirms they lack the fact, the section is **not scored at all**. It has no number. It drops 3 points from the denominator and appears in the trail as an ask. Without real quotes, "lead with the strongest quote" and "vary length" are unanswerable too — scoring it would punish the user once for the missing fact and again for every must-have that fact poisons.
- **`Blockable: capped at 2`** — applies whenever **the user confirmed the named fact is missing**. Full stop. The section scores normally (craft failures still push it below 2) and drops 1 point from the denominator. Every other must-have in it is pure craft and stays your problem. (The "ceiling" is mostly bookkeeping: the named fact is itself a must-have, so missing it already lands the band at 2. The load-bearing effects are the `−1` on `achievable` and the exclusion from the stop test.)

  **The cap keys on the user's answer, never on the section's score.** An earlier draft of this rule said "capped only when the sole remaining miss is the named fact" — which made `achievable` depend on the very scores it normalizes, and, worse, ran backwards: a section missing the fact *and* failing craft would lose its `−1` and be graded against a *larger* denominator than a cleaner section missing the same fact. The worse page got marked harder. Key on the answer and both problems vanish, and `achievable` becomes computable before a single section is scored.

Fully blockable: `Trust Logos`, `Testimonials`, `About`.
Capped-only: `Hero`, `Benefits Recap`, `How It Works`, `Pricing`, `FAQ`, `Footer`.
**The other five can never be blocked.**

Each capped-only section names exactly one fact, enumerated in its own `Blockable:` line. That keeps this a lookup: a section is capped when *that* fact is missing, never when the loop feels stuck. A fact not named in a `Blockable:` line cannot cap anything.

```
achievable = 42 − 3×(fully blocked sections) − 1×(capped-only sections)
```

Report `X / achievable`, never `X / 42`. Raw 42 belongs in a footnote.

Three distinctions that get collapsed if you are not careful:

- **Blocked ≠ defaultable.** `Vision` has a derived default and is never blocked. Missing it is a flag, not a cap.
- **Blocked ≠ stuck.** If you cannot phrase the missing fact as a concrete question the user could answer, the section is not blocked. It is stuck. Stuck sections stay in the stop test and get reported honestly.
- **Blocked ≠ unaskable.** Plenty of `Blockable: no` sections still need a fact only the user has (a real setup time, what the top plan includes, the cancellation terms). **Ask for those too** — but they never earn blocked status. They stay in the stop test, and if the user declines they end as *"converged short — needs X from you"*, naming the fact. Never report a fact you were simply never allowed to ask for as something the loop could not fix.

### Numbers you do not have

Several must-haves want a number: a metric, a timeframe, a setup time, a customer count, an annual discount. **Where the number is not yours, ship the placeholder.** Never invent it. An invented "30% faster" or "~5 min" is a lie shipped to the user's customers.

**Read this next part carefully, because the scoring cannot protect you here.**

A blind scorer reading page text cannot tell a real `~3 min` from a fabricated one. The bracket is the only tell. So a naive rubric *pays you to invent*: bracket the number honestly and the must-have fails, invent it and the must-have passes. The rule meant to resist the loop's pull toward a higher band would be the one rule the band rewards you for breaking.

Two things close that gap:

1. **Every fact only the user can supply is named in a `Blockable:` line.** Once the user confirms it is missing, the section is capped and `achievable` drops to match. The honest bracketed page then scores *at its ceiling* — full marks for what was reachable. Honesty costs nothing against `achievable`, which is the only denominator that gets reported.
2. **A section scoring above its ceiling is evidence a fact was invented.** If Benefits Recap is capped at 2 because the user has no metrics and the blind scorer returns a 3, a number got made up. **Only the loop can run this check** — the scorer doesn't know the ceiling exists. Treat a hit as a defect, not a win.

Know the check's limit: it only catches *maximal* fabrication. Invent one number, bracket the other two, and the section still lands at 2 — at its ceiling, arithmetically identical to honesty. **Partial fabrication is invisible.**

Beyond that, nothing in the score enforces honesty. **The non-negotiable in `SKILL.md` is load-bearing and unbacked** — it is the writer's discipline, not the scorer's check. Do not assume the rubric will catch you, because mostly it cannot.

---

## 1. Navbar

`Blockable: no`

**Must-have:**
- Sticky, visible on scroll (carry it as a note)
- 3–5 links max
- Primary CTA always present, action-oriented label
- Same CTA wording as hero (consistency bias)

**Anti-patterns:**
- More than 5 links / cluttered nav
- CTA label is `Buy`, `Purchase`, or a generic `Sign up` (action-oriented = `Start free`, `Get my plan`, `Try [product]`)

## 2. Hero

`Blockable: capped at 2` — only when the sole miss is real social proof. H1, H2, bullets, CTA, and visual are pure craft and never blockable.

Formula: emotional promise + rational delivery.

**Must-have:**
- Optional eyebrow: urgency or micro-proof
- H1: the biggest change for the reader, stated as early in the line as the sentence allows ("Finish more tasks without working more")
- H2: how the promise is delivered (product description)
- 3 painkiller bullets (max 5), each with emoji/icon
- Primary CTA — never "Buy" / "Purchase"
- Quick social proof: a real count, plus either a 1-line review or avatars
- Visual note: clean product mockup or result screenshot

Weight H1, H2, and the painkiller bullets most heavily.

**Anti-patterns:**
- H1 is rational/feature-led (`The to-do app for teams`) or a bare category noun, instead of a change for the reader
- Vague CTA (`Learn more`, `Get started` with no context)
- Hero visual is a stock photo instead of the product

## 3. Trust Logos

`Blockable: yes` — needs real customer/press logos and a real count.

**Must-have:**
- Row of customer/press logos under hero
- Monochrome (carry it as a note)
- Context line ("Trusted by 500+ teams" / "Featured in…")

**Anti-patterns:**
- Full-color logos that fight the hero for attention
- Logos with no context line
- Fabricated or unverifiable logos

> No real logos means **cut the section**, not fake it. An empty row of `[logo] [logo]` is scaffolding the user must delete, and it scores nothing.

## 4. Problem

`Blockable: no`

**Agitation (why care):**
- Point A: status-quo they hate
- 3 negative consequences of staying there

**Transformation (how this helps):**
- Point B: desired state
- 3 positive benefits of switching
- Visual note: product mockup or "how it works" preview

**Anti-patterns:**
- Generic "managing X is hard" agitation with no specific consequences
- Skipping straight to features without naming Point A

## 5. How It Works

`Blockable: capped at 2` — only when the sole miss is the real setup time. The step structure, the icons, and the ordering are pure craft.

**Must-have:**
- 3–4 steps: setup → action → reward
- Time estimate per step ("~5 min") — real, or a placeholder and the cap. Never a guess.
- Numbered steps, each with an icon or visual note

**Anti-patterns:**
- 5+ steps (overwhelms)
- No time estimates → reader assumes it's complex

## 6. Features

`Blockable: no`

**Must-have:**
- 3–4 power features
- Default: outcome-first headline + 1 line of mechanism
- An icon on every feature
- A GIF or visual note on every feature
- Highlight what competitors lack

**Conditional must-have:**
- Technical ICP only (`icp_technicality = technical`): a small spec/detail line per feature

**Anti-patterns:**
- 5+ features listed (forgettable)
- Feature names that are internal jargon with no benefit framing
- No visual / GIF

## 7. Benefits Recap

`Blockable: capped at 2` — only when the sole miss is a real metric or timeframe. The rule of 3 and the icons are pure craft.

**Must-have:**
- Rule of 3 — biggest gains
- Each paired with icon
- Numbers/timeframes attached ("30% faster", "ship in a weekend")

**Anti-patterns:**
- Duplicates the Features section verbatim instead of distilling outcomes
- Vague benefits without metrics or timeframes

## 8. Vision / Manifesto

`Blockable: no` — defaultable, not blockable. Derive it from `transformation` + `one_line_pitch` and flag it inline. Never block on vision.

**Must-have:**
- The bigger change / movement the product is part of — world- or category-level, beyond one user's Point B
- Ties the reader's personal transformation to that larger purpose ("you + us → this future")
- Short: 1 aspirational headline + 2–3 belief lines
- Each belief line survives the negation test
- Visual note: aspirational future-state image

> **The negation test** makes this mechanical instead of a matter of taste. State the line's negation. If the negation is *absurd*, the line is a platitude and fails. If the negation is *a position someone actually holds*, the line is a belief and passes.
>
> - "Every hour not spent on admin is an hour spent on the work you sell" → negation: "an hour not spent on admin is not an hour spent on your work". Absurd. **Fails.**
> - "Guessing conservatively is a tax on being small" → negation: "guessing conservatively is not a tax on being small". Arguable. **Passes.**

**Anti-patterns:**
- "We are passionate about…" / "our mission is to revolutionise…" boilerplate
- A claim nobody could argue with — that is a platitude, not a belief
- Restates the user's Point B at a louder volume instead of naming a change beyond it
- An invented statistic used as scene-setting ("a million solo businesses still hand over a shoebox"). A number in a manifesto is still a number, and the honesty rule still applies.

## 9. About

`Blockable: yes` — needs the founder story, prior projects, and real press/community mentions.

**Must-have:**
- 2–3 short storytelling paragraphs + founder face note
- The founder is named
- What you've built before (credibility)
- Press / community mentions

**Anti-patterns:**
- No face / no name → reads like a faceless corp
- Corporate "about us" boilerplate instead of a personal story

## 10. Testimonials

`Blockable: yes` — needs real quotes with real names and roles.

Sits **immediately before Pricing** — that adjacency is the point, it eases purchase anxiety at the moment of decision.

**Must-have:**
- 5–7 testimonials, photo + name + role
- Lead with strongest specific-outcome quote
- Vary length (scannable + detailed)
- Each role matches the target audience
- Immediately precedes Pricing, with no section between

**Anti-patterns:**
- Anonymous testimonials
- Generic praise ("Great product!") with no specific outcome
- Testimonials placed after Pricing, or separated from it by another section (loses the anxiety-easing function)

> **Improve mode: the text inside an attributed quote is not yours to edit.** A real page arrives with real quotes from real named people. Honest-but-generic quotes score low, and the cheapest path up is putting better words in someone's mouth. Do not take it. Reorder, re-select, or cut quotes. Never reword one. Never add a logo or a name. If the quotes are weak, the fix is an ask — go get better ones — not a rewrite.

## 11. Pricing

`Blockable: capped at 2` — only when the sole miss is the real annual discount ("Save $X"). Plan structure, anchoring, bullets, and CTAs are pure craft.

**Must-have:**
- 2–3 plans. With 3: downsell · main · upsell. With 2: main + one flanker.
- Anchor the main plan visually
- 3–5 plan bullets, benefit-led
- End prices at $7 / $9 (or $0 if luxury)
- Clarify subscription vs one-time
- Annual toggle with "Save $X" (loss aversion)
- CTA under every plan

**Conditional must-have:**
- Money-back guarantee — only when `offer_guarantee = true`. A missing guarantee is a gap only in that case. Never penalise a page for declining to offer one.
- Authentic scarcity — only when `urgency_basis` is provided and real.

**Anti-patterns:**
- Round prices ($10, $50, $100) outside luxury positioning
- No anchored main plan
- Missing CTA on any plan
- Fake countdown / fake scarcity
- **"Most popular" (or any popularity claim) on a page with no real customer count.** It is a factual claim about real customers, so the honesty rule covers it. With no count, it cannot be true. Anchor with a non-factual label ("Best for most freelancers") or with visual weight alone.

## 12. FAQ

`Blockable: capped at 2` — only when the sole miss is a term only the user knows (trial length, cancellation terms, security specifics). Question selection, ordering, and answer style are pure craft.

**Must-have:**
- 5–7 conversion-blocking objections
- Order: setup → billing → support → safety
- Every answer names the actual limitation, number, or term — not a benefit restatement
- Safety questions (cancel, trial; guarantee only if `offer_guarantee = true`)

**Anti-patterns:**
- Softball questions ("Is your product good?") instead of real objections
- Marketing-speak answers that dodge the objection

## 13. Final CTA

`Blockable: no`

**Must-have:**
- Repeat the core promise from the Hero (one line)
- Big CTA — same label as hero/pricing CTAs
- Optional micro-proof line under button

**Anti-patterns:**
- Different CTA label than Hero (breaks consistency bias)
- Generic closer ("Ready to get started?")

## 14. Footer

`Blockable: capped at 2` — only when the sole miss is the real trust badges or certifications. Nav, repeated CTA, and social links are pure craft.

**Must-have:**
- Simple nav (legal, contact, support)
- Trust badges / certifications
- Repeated CTA for full-page scrollers
- Social links

**Anti-patterns:**
- Sitemap-bloat footer that distracts from the CTA
- No repeated CTA → wasted real estate

---

## Section order

`Navbar · Hero · Trust Logos · Problem · How It Works · Features · Benefits Recap · Vision · About · Testimonials · Pricing · FAQ · Final CTA · Footer`

Testimonials sit directly before Pricing. Vision and About come earlier — nothing may separate the proof from the price.

## Cross-section must-haves

These span sections, so a rewrite in one silently breaks another. This is why the loop re-scores every section every round instead of only the ones it touched.

| Constraint | Spans |
|---|---|
| Identical CTA label | Navbar · Hero · Pricing · Final CTA · Footer |
| Final CTA repeats the Hero promise | Hero · Final CTA |
| Testimonials immediately precede Pricing | Testimonials · Pricing |
| Trust Logos sit directly under Hero | Hero · Trust Logos |
| Benefits Recap does not duplicate Features | Features · Benefits Recap |
| One audience · one problem · one solution | every section |

**The whole-page pass owns this table, not the individual sections.** A constraint parked inside one section evaporates the moment that section is blocked — Testimonials owns "immediately precedes Pricing", so a blocked Testimonials would take the page's only ordering check down with it. Check every row at the page level, every round, and drop each section the failing row names. A section being blocked never excuses the page from the constraint.

Also page-level, for the same reason: **a blocked section that shipped scaffolding instead of being cut.** No real logos means no Trust Logos section. A row of `[logo] [logo]` is unscored, so nothing else on this sheet can catch it, and the author is otherwise rewarded for leaving the user work to delete.

Rewrite in dependency order: **Hero first** (it fixes the promise and the CTA label), then its coupled set, then the rest.

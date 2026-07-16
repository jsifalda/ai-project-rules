# Viral audit report

<!-- TEMPLATE INSTRUCTIONS
This is a fill-in skeleton. Adhere to these rules while completing it:

1. EVIDENCE REQUIRED: Every FAIL verdict must include a verbatim quote that shows the violation. Absence of evidence is UNPROVEN, never FAIL.
2. PRODUCT-LEVEL CRITERIA ARE NEVER SCORED: C4, C5, F3, F4, G1–G6 are DEFER always. They are interview questions, not grades.
3. NO COMPOSITE SCORE: Do not add a total score, percentage, or grade. Report verdict counts only.
4. SECTION AND ID ORDER: Keep criteria in the order they appear here. Do not sort by verdict.
5. INTERVIEW SECTION IS SEPARATE: The "Interview needed" section stands apart. Readers must never mistake it for failures.
-->

**Target:** [landing page name/URL]
**Date:** [audit date]
**Verdict tally:** [n] PASS · [n] FAIL · [n] UNPROVEN of 18 scored · 10 deferred

---

## A. Grasp cost

A1. Name the thing before you sell it -> [PASS | FAIL | UNPROVEN]
  Evidence: "[verbatim hero block text]" ([location: headline/subhead/CTA])
  Note: [state the concrete noun that answers "it's a ___", or confirm none exists]

A2. Insider-word budget -> [PASS | FAIL | UNPROVEN]
  Evidence: "[term requiring insider knowledge]" ([location and sentence])
  Note: [count and list any insider terms found in hero]

A3. Fits in a text message -> [PASS | FAIL | UNPROVEN]
  Evidence: "[exact span, 15 words or fewer]" ([location])
  Note: [confirm this span is self-contained and needs no surrounding context]

## B. The portable claim

B1. One claim, not a menu -> [PASS | FAIL | UNPROVEN]
  Evidence: "[claim 1]" ([location]), "[claim 2]" ([location])
  Note: [if FAIL, list all claims; confirm whether they are distinct or reworded versions]

B2. The headline has an object -> [PASS | FAIL | UNPROVEN]
  Evidence: "[headline as written]" ([location])
  Note: [quote it with adjectives stripped; confirm something remains]

B3. Say it again, do not rotate it -> [PASS | FAIL | UNPROVEN]
  Evidence: "[key phrase]" at ([location 1]), ([location 2]), ([location 3 if present])
  Note: [confirm the phrase repeats verbatim, or list each variation]

B4. A quotable quantity -> [PASS | FAIL | UNPROVEN]
  Evidence: "[number in full sentence context]" ([location])
  Note: [state whether it is load-bearing to the claim or decorative]

## C. Distinctiveness against the category

C1. The swap test -> [PASS | FAIL | UNPROVEN]
  Evidence: "[original headline]" ([location])
  Note: [list three competitor swaps; state which remain true]

C2. Thumbnail fingerprint -> [PASS | FAIL | UNPROVEN]
  Evidence: "[element description from alt text, classname, or filename]" ([location])
  Note: [confirm it is identifiable at 200px width and is above the fold]

C3. Named things -> [PASS | FAIL | UNPROVEN]
  Evidence: "[coined proper name]" ([location and context])
  Note: [confirm it is a proper noun used as a named thing, not a generic descriptor]

## D. Screenshot artifacts

D1. One frame carries the pitch -> [PASS | FAIL | UNPROVEN]
  Evidence: "[region name/element]" contains: claim "[claim text]" + proof "[proof text]" + identity "[name or logo]" ([location])
  Note: [confirm all three fit in one viewport without scrolling]

D2. Show the output, not the chrome -> [PASS | FAIL | UNPROVEN]
  Evidence: "[alt text or caption of visual showing output]" ([location])
  Note: [list which visuals show outputs vs. which show UI chrome only]

D3. Proof survives compression -> [PASS | FAIL | UNPROVEN]
  Evidence: "[proof statement]" ([location: heading element type or text node])
  Note: [confirm it is selectable text at heading size, not baked into image type]

## E. Emotional charge

E1. Take a side -> [PASS | FAIL | UNPROVEN]
  Evidence: "[stated opinion or rejected norm]" ([location])
  Note: [identify a category expert who would genuinely disagree and why]

E2. Give them a line to quote -> [PASS | FAIL | UNPROVEN]
  Evidence: "[sentence, 20 words or fewer, self-contained]" ([location])
  Note: [confirm it makes a claim and needs no context from surrounding sentences]

E3. One deliberate delight -> [PASS | FAIL | UNPROVEN]
  Evidence: "[element serving no conversion purpose]" ([location])
  Note: [explain why it adds no funnel value (joke, easter egg, craft, copy anomaly)]

## F. Share mechanics

F1. The unfurl carries the claim -> [PASS | FAIL | UNPROVEN]
  Evidence: og:title: "[title text]", og:description: "[description text]", og:image: "[URL]" ([location in markup])
  Note: [describe what claim text is visible in the og:image itself]

F2. No gate before the interesting part -> [PASS | FAIL | UNPROVEN]
  Evidence: "[payload description]" is reachable via "[CTA label]" without [gate type]
  Note: [confirm access in one click from the landing page]

---

## Interview needed

These 10 questions are not failures. They are unknowns that shape virality. Answer them after scoring the page.

**C4. Category narrowness**
  Can you finish the sentence "it's the ___ for ___" without hedging? Would a stranger in that second slot recognize themselves?

**C5. Timing attachment**
  Is this attached to a shift people are already arguing about (platform change, new capability, rule change)? How long has that window been open?

**F3. Attribution ride-along**
  Does anything the product produces carry a visible mark back to you when a user shows it to someone else? Is that mark on by default?

**F4. A reason to mention it twice**
  What recurring event does the product generate that gives an existing user a reason to bring it up again months later (update, result, milestone, public number)?

**G1. Price legibility**
  Can a visitor learn what they would pay in one glance, without a call, a calculator, or a quote?

**G2. Price position**
  Where does your price sit against the two closest alternatives? Is the gap large enough that someone would mention the number itself?

**G3. Business-model shape**
  Does a user get anything concrete when another user joins because of them? Is that built into the product or bolted on as a referral scheme?

**G4. Name mechanics**
  Can someone who hears the name once, in a noisy room, spell it and find it? Any silent letters, homophones, or numbers standing in for words?

**G5. Founder visibility**
  Is there a specific, findable human attached to this product publicly? Do they post where the audience already is?

**G6. Free public surface**
  Is there something useful, complete, and public that costs nothing and requires no account (a tool, a dataset, a calculator, a report)?

---

## Remediation plan

Fill this table only after the interview. It captures confirmed gaps and the fixes required to close them.

| Fix | Closes | Change | Effort | Impact |
|-----|--------|--------|--------|--------|
| [description of the fix] | [criterion ID] | [what gets modified or added to the page] | S/M/L | [why this fix matters to virality] |

**Note:** Only gaps confirmed by the founder or demonstrated by evidence appear here. Product-level questions remain deferred until the interview reveals actual constraints.

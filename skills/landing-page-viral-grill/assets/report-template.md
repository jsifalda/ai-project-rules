# Viral audit report

<!-- TEMPLATE INSTRUCTIONS — read before filling.

This skeleton is CHECKLIST-DRIVEN. It hardcodes no checks of its own.
Every row below comes from a bullet in the checklist file. Nothing else.

1. SOURCE OF TRUTH: the checklist file is the only source of checks. Never add a
   check it does not contain. Never merge, split, reword, or silently drop one.
2. FILE ORDER: sections and checks appear in the order the checklist file lists
   them. Never sort by verdict, never group failures together.
3. EVIDENCE REQUIRED: every FAIL carries a verbatim quote showing the violation.
4. UNPROVEN IS NOT FAIL: if the page gives nothing to judge, the verdict is
   UNPROVEN and you state what you looked for. Never downgrade it to FAIL.
5. DEFERRED CHECKS ARE NEVER SCORED: business-level checks (pricing model,
   positioning, founder visibility, naming) get no grade from markup, ever.
   They go in the Interview section as questions.
6. NO COMPOSITE SCORE: no total, no percentage, no grade, no "X/32". Count
   verdicts only. The sections are not commensurable.
7. IDs: derived by position — section's first two letters uppercased + index
   within the section (PR1, HE2, PA3). Do not invent an ID scheme of your own.
-->

**Target:** [page name or URL]
**Checklist:** [path to the checklist file used]
**Date:** [audit date]
**Tally:** [n] PASS · [n] FAIL · [n] UNPROVEN of [n] scored · [n] deferred

<!-- No total score. No percentage. If you are tempted to add one, re-read rule 6. -->

---

## Scored checks

<!-- Repeat one `### <Section>` block per section in the checklist file, in file
     order. Under each, one entry per page-decidable check in that section.
     Delete this comment and the example block once filled. -->

### [Section name, exactly as it appears in the checklist file]

[ID]. [the check, restated from its bullet] -> [PASS | FAIL | UNPROVEN]
  Evidence: "[verbatim quote from the target]" ([location — headline, subhead, footer, og:image tag])
  Note: [one line, only if the verdict needs explaining]

[ID]. [next check in this section] -> [PASS | FAIL | UNPROVEN]
  Evidence: "[verbatim quote]" ([location])

<!-- EXAMPLE of a filled entry, delete when filling:

PA3. One CTA. Multiple paths -> many pick none. -> FAIL
  Evidence: "Start free trial" (hero), "Book a demo" (hero), "See pricing" (nav)
  Note: three competing destinations above the fold.

PA5. Show, don't tell. Demo > paragraphs. -> UNPROVEN
  Evidence: none found
  Note: searched for video, gif, screenshot, and interactive embed. Page is text
        and stock photography only, so there is nothing to judge either way.
-->

---

## Interview needed

<!-- These are NOT gaps. They are unknowns. The page cannot answer them and the
     auditor must not guess. They become the grill-me agenda. No verdicts here. -->

The checks below concern the business, not the page. Nothing on the target can
settle them, so none of them is scored. They are open questions, not failures.

[ID]. [the check, restated from its bullet]
  Question: [the question to put to the founder]

[ID]. [next deferred check]
  Question: [the question to put to the founder]

---

## Remediation plan

<!-- Fill this ONLY after the grill has run. Confirmed gaps only. Drop anything
     the grill established is inapplicable to this product. -->

Covers confirmed gaps only. Checks the interview ruled inapplicable are excluded.

| Fix | Closes | Change | Effort | Impact |
|---|---|---|---|---|
| [what to do] | [ID] | [the concrete change — show the rewritten line if it's copy] | [S/M/L] | [expected effect on sharing] |

<!-- Never invent testimonials, logos, metrics, or founder details in a proposed
     fix. Use [placeholder] syntax for anything you cannot verify. -->

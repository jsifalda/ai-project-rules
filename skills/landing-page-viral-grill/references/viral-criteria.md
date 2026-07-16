# Viral criteria: a shareability rubric for landing pages

> Inspired by Marc Lou's "32 Principles of a Viral Product" (https://x.com/marclou/status/2065385672991752210). The criteria below are independently authored from general marketing practice, not derived from that article's text.

## What this rubric grades

Shareability, not conversion.

The question behind every criterion: **would a visitor who will never buy still send this page to someone else?**

That is a different question from "will this visitor buy". A page can convert well and travel nowhere. Criteria here are selected for the things that make a page move between people:

- Memorability → can it be recalled a day later without the URL.
- Relay cost → how many words does the sharer have to add to make it land.
- Screenshot value → does one frame carry the whole point.
- Distinctiveness → is it different enough from the category to be worth remarking on.
- Emotional charge → does it produce a reaction, not just an understanding.
- Repeatability → is there one claim that survives being retold by a stranger.

If a criterion reads like generic conversion-rate optimization (form length, button color, trust badges above the fold), it does not belong here. Where a classic CRO idea appears, it is sharpened toward travel: not "is the proof convincing" but "does the proof survive a repost".

## ID rule (read before editing this file)

- Every criterion has a stable ID: section letter + number (`A1`, `B3`, `G6`).
- **IDs are permanent. They never renumber.**
- New criteria append the next unused number in their section. Never reuse a number.
- Retired criteria stay listed with a `RETIRED` note. Do not reclaim their ID.
- Audit reports cite IDs, so a renumber silently invalidates every past report.

## The page/product split

Each criterion carries exactly one tag.

- `[page-observable]` (18 criteria) → decidable from the page's own text and markup. The auditor scores these.
- `[product-level]` (10 criteria) → not decidable from the page. Needs the founder's input: pricing model, price versus competitors, category focus, trend timing, founder visibility, naming, business-model shape. The auditor never scores these. They become interview questions.

Scoring rule, verbatim:

> **No criterion is ever marked FAIL without quoted evidence; absence of evidence on a page-observable criterion is `UNPROVEN`, not `FAIL`; product-level criteria are never scored at all, they are deferred to an interview.**

Verdict values for `[page-observable]`:

- `PASS` → test met, evidence quoted.
- `FAIL` → test violated, evidence quoted. The quote must show the violation, not just its absence.
- `UNPROVEN` → the page gives nothing to judge. Not a failure. Report what was searched for.

Verdict value for `[product-level]`:

- `DEFER` → always. Output the interview question, never a grade.

Evidence rules:

- Quote verbatim from the page. Copy the exact string, keep the casing.
- Point at the element (headline, subhead, section 3 heading, `og:image` tag, alt text).
- One quote can serve several criteria. Reuse it, do not paraphrase it differently each time.
- "The page feels generic" is not evidence. "Headline reads `The modern way to manage your work`" is.

---

## A. Grasp cost

How much work must a stranger do before they can retell this to someone else.

### A1. Name the thing before you sell it
- Tag: `[page-observable]`
- Test: the hero block (headline plus subhead plus primary CTA) states what the product **is** using a concrete noun for its category or artifact. PASS only if a reader could complete "it's a ___" using words present in that block. FAIL if the hero contains only outcomes, adjectives, or a slogan with no object.
- Evidence: quote the headline and subhead verbatim, then quote the exact noun that answers "it's a ___", or state that no such noun exists and quote the full hero to prove it.
- Why: nobody forwards a page they cannot label in the message they send with it.

### A2. Insider-word budget
- Tag: `[page-observable]`
- Test: count terms in the hero block that require category-insider knowledge to parse (undefined acronyms, coined jargon, internal product nouns used before definition). PASS at 0 or 1. FAIL at 2 or more.
- Evidence: list every counted term with the sentence it sits in.
- Why: each unexplained word narrows the set of people who can pass the page on without an apology attached.

### A3. Fits in a text message
- Tag: `[page-observable]`
- Test: the page contains a contiguous span of 15 words or fewer that a sharer could paste as the entire pitch, with no surrounding context, and it still reads as a complete claim. PASS if such a span exists. FAIL if the shortest complete claim on the page needs more than one sentence to stand up.
- Evidence: quote the exact span and its location. If none exists, quote the shortest candidate and show what it leaves dangling.
- Why: the sharer writes one line. The page either supplies it or the share does not happen.

---

## B. The portable claim

What actually travels is one claim, repeated by strangers, in their words.

### B1. One claim, not a menu
- Tag: `[page-observable]`
- Test: count distinct top-level value claims across the hero and the first section below it. PASS at 1 or 2. FAIL at 3 or more. Distinct means the claims promise different outcomes, not the same outcome reworded.
- Evidence: list each claim as a quote. If 3 or more, quote all of them.
- Why: a page that promises three things gets retold as nothing. Retellers carry one idea, and they pick it, not you.

### B2. The headline has an object
- Tag: `[page-observable]`
- Test: the headline names a specific outcome, artifact, or quantity. PASS if removing every adjective still leaves a claim standing. FAIL if the headline is only category adjectives ("fast", "simple", "powerful", "modern", "effortless") with no object to attach them to.
- Evidence: quote the headline. Then quote it with adjectives stripped and show what remains.
- Why: adjectives do not survive retelling. Objects do.

### B3. Say it again, do not rotate it
- Tag: `[page-observable]`
- Test: the key noun or verb from the hero claim reappears verbatim at least twice more downpage (section heading, CTA label, page title, meta description). PASS at 2 or more repeats. FAIL if every section pitches a different angle and no phrase repeats.
- Evidence: quote each occurrence with its location.
- Why: repetition inside one page is what makes one phrase, and not another, the phrase a visitor uses when they describe you to a friend.

### B4. A quotable quantity
- Tag: `[page-observable]`
- Test: the page states at least one concrete quantity attached to the main claim (minutes saved, count of things, a multiple, a price, a speed). The number must be load-bearing, not decorative. PASS if such a number exists. UNPROVEN if the page carries no numbers at all. FAIL only if the numbers present are all decorative (round marketing figures with no referent, "10x better", "millions of users" with no source).
- Evidence: quote the number in its sentence.
- Why: numbers survive paraphrase intact. Claims do not.

---

## C. Distinctiveness against the category

Nothing gets shared for being adequate. It gets shared for being different in a way worth mentioning.

### C1. The swap test
- Tag: `[page-observable]`
- Test: substitute three plausible competitor names into the headline in place of the product name. PASS if the headline becomes false or absurd for at least two of the three. FAIL if it stays true for all three.
- Evidence: quote the headline, then write the three swapped versions and state which stay true.
- Why: a headline any competitor could run is a headline nobody repeats, because it identifies no one.

### C2. Thumbnail fingerprint
- Tag: `[page-observable]`
- Test: the page carries at least one visual element identifiable at 200px width without reading text (custom illustration, mascot, unusual layout, distinctive color pairing, hand-made asset). PASS if such an element exists and is above the fold. FAIL if the visual system is only stock photography, a generic gradient, and a standard feature grid.
- Evidence: quote the element's alt text, class names, filename, or the markup that shows what it is. Describe what makes it identifiable.
- Why: shares are seen as thumbnails first. An unrecognizable thumbnail is an unclicked one.

### C3. Named things
- Tag: `[page-observable]`
- Test: the page gives at least one of its own concepts, features, or methods a coined proper name (capitalized, used as a noun, not a generic descriptor). PASS at 1 or more. FAIL if every feature is described only functionally ("the dashboard", "the editor", "AI-powered search").
- Evidence: quote the name and the sentence that introduces it.
- Why: people share nouns. An unnamed feature has to be described from scratch every time, and it usually is not.

### C4. Category narrowness
- Tag: `[product-level]`
- Interview question: can you finish the sentence "it's the ___ for ___" without hedging, and would a stranger in that second slot recognize themselves?
- Why: a narrow category gives the sharer a specific person to send it to. "For everyone" is addressed to no one.

### C5. Timing attachment
- Tag: `[product-level]`
- Interview question: is this attached to a shift people are already arguing about (a platform change, a new capability, a rule change), and how long has that window been open?
- Why: a share rides an existing conversation. Products with no conversation to attach to have to start one, which costs far more.

---

## D. Screenshot artifacts

Most shares are not links. They are images of your page with a sentence on top.

### D1. One frame carries the pitch
- Tag: `[page-observable]`
- Test: identify a single region no taller than one viewport that contains all three of: the main claim, one piece of proof, and the product identity (name or logo). PASS if such a region exists. FAIL if capturing all three requires scrolling or two screenshots.
- Evidence: name the region and quote the claim, the proof, and the identity text it contains.
- Why: a screenshot is one frame. If the point spans two, the point does not travel.

### D2. Show the output, not the chrome
- Tag: `[page-observable]`
- Test: the page shows the artifact the user ends up with (the result, the file, the finished thing), not only interface surfaces (settings panels, empty dashboards, nav bars). PASS if at least one visual shows an output. FAIL if every product visual is UI chrome. UNPROVEN if the page has no product visuals at all.
- Evidence: quote the alt text, caption, or surrounding heading for each product visual, and state which shows an output.
- Why: people share results. An empty dashboard tells a viewer nothing about what they would get.

### D3. Proof survives compression
- Tag: `[page-observable]`
- Test: the strongest proof on the page (the key number, the before/after, the outcome) exists as page text at heading size, not only as small type rendered inside an image. PASS if the proof appears as selectable text in a heading or a large-type element. FAIL if the proof exists only inside a screenshot's own UI text.
- Evidence: quote the proof and state where it lives (heading element versus image content).
- Why: reposts get recompressed and downscaled. Proof baked into 12px screenshot type is gone by the second share.

---

## E. Emotional charge

Understanding does not get shared. Reactions do.

### E1. Take a side
- Tag: `[page-observable]`
- Test: the page contains at least one sentence a competent person in the category could genuinely disagree with (a stated opinion, a rejected norm, a named tradeoff you refuse). PASS at 1 or more. FAIL if every sentence is something no one in the field would contest.
- Evidence: quote the sentence and state who would disagree and why.
- Why: agreement is silent. Disagreement is the thing people paste into a group chat.

### E2. Give them a line to quote
- Tag: `[page-observable]`
- Test: the page contains at least one sentence of 20 words or fewer that is self-contained (no pronoun depending on a previous sentence, no context needed) and makes a claim rather than describing a feature. PASS if such a sentence exists. FAIL if every short sentence is a feature label and every claim sentence needs its neighbors.
- Evidence: quote the sentence exactly as written.
- Why: the quote is the unit of sharing. Write it, or someone else's summary becomes the thing that spreads.

### E3. One deliberate delight
- Tag: `[page-observable]`
- Test: the page contains at least one element that serves no conversion purpose and exists to be enjoyed (a joke, an easter egg, an odd copy line, a piece of craft nobody asked for). PASS at 1 or more. FAIL if every element on the page is justifiable purely as funnel machinery.
- Evidence: quote the element and state why it does no conversion work.
- Why: a page with nothing surplus gives a visitor nothing to point at. "Look at this" needs a this.

---

## F. Share mechanics

The friction of the share act itself, and whether one share can cause another.

### F1. The unfurl carries the claim
- Tag: `[page-observable]`
- Test: `og:title`, `og:description`, and `og:image` are all present, and the `og:image` contains the main claim as legible text rather than only a logo or a wordmark. PASS if all three exist and the image carries text. FAIL if `og:image` is missing, is a bare logo, or the tags default to generic site metadata. UNPROVEN if markup is unavailable for inspection.
- Evidence: quote the meta tags verbatim, including the `og:image` URL and any text visible in it.
- Why: the unfurl is the ad that ships with every share. A bare logo unfurl wastes the one impression the sharer paid for.

### F2. No gate before the interesting part
- Tag: `[page-observable]`
- Test: the thing worth sharing (the demo, the tool, a sample output, the free surface) is reachable without a signup, an email, or a paywall. PASS if a visitor can reach it in one click from the landing page. FAIL if the only path to the payload is a form.
- Evidence: quote the CTA labels and any gate copy on the path to the payload.
- Why: a sharer will not send a friend into a form. The share dies at the gate, and it dies before it happens.

### F3. Attribution ride-along
- Tag: `[product-level]`
- Interview question: does anything the product produces carry a visible mark back to you when a user shows it to someone else, and is that mark on by default?
- Why: outputs travel further than pages. An unmarked output is a share you paid for and did not get credited with.

### F4. A reason to mention it twice
- Tag: `[product-level]`
- Interview question: what recurring event does the product generate that gives an existing user a reason to bring it up again months later (an update, a result, a milestone, a public number)?
- Why: one-time shares decay. Only a repeating event gives the same person a second occasion to post.

---

## G. Product and business shape

Never scored. These come out of an interview, because the page cannot answer them honestly.

### G1. Price legibility
- Tag: `[product-level]`
- Interview question: can a visitor learn what they would pay in one glance, without a call, a calculator, or a quote?
- Why: an unknowable price makes the product unrecommendable. A sharer will not vouch for a number they cannot state.

### G2. Price position
- Tag: `[product-level]`
- Interview question: where does your price sit against the two closest alternatives, and is the gap large enough that someone would mention the number itself?
- Why: a price that is remarkable in either direction is a fact people repeat. A price in the middle of the pack is not information.

### G3. Business-model shape
- Tag: `[product-level]`
- Interview question: does a user get anything concrete when another user joins because of them, and is that built into the product or bolted on as a referral scheme?
- Why: models where recruiting is self-interested spread without campaigns. Bolted-on referral programs mostly do not.

### G4. Name mechanics
- Tag: `[product-level]`
- Interview question: can someone who hears the name once, in a noisy room, spell it and find it? Any silent letters, homophones, or numbers standing in for words?
- Why: most shares are spoken before they are typed. A name that loses a hop loses the visit.

### G5. Founder visibility
- Tag: `[product-level]`
- Interview question: is there a specific, findable human attached to this product publicly, and do they post where the audience already is?
- Why: people share people more readily than they share companies. A faceless product has to buy every impression it gets.

### G6. Free public surface
- Tag: `[product-level]`
- Interview question: is there something useful, complete, and public that costs nothing and requires no account (a tool, a dataset, a calculator, a report)?
- Why: the paid product is a share only its buyers can make. A free artifact can be shared by everyone who never buys, which is nearly everyone.

---

## Reporting shape

Per criterion, one line:

```
<ID> <NAME> -> <PASS | FAIL | UNPROVEN | DEFER>
  Evidence: "<verbatim quote>" (<location>)
  Note: <one line, only if the verdict needs it>
```

Report discipline:

- Section order, ID order. Do not sort by verdict.
- `[product-level]` criteria are grouped at the end under an "Interview needed" heading, as questions. No grades, no scores, no implied grades.
- Do not compute a total score across sections. The sections are not commensurable, and a single number hides which axis is broken.
- Count the verdicts instead: how many PASS, FAIL, UNPROVEN out of the 18 page-observable criteria, plus the count of deferred questions.
- A high UNPROVEN count is itself the finding. It means the page gives a stranger nothing to grab.

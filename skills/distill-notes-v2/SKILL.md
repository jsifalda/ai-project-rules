---
name: distill-notes-v2
description: Split mixed raw notes into two outputs, a lossless organized reference for the facts and a sharpened set of maxims for the heuristics. Keeps every number, date, rate, threshold, condition, and obligation verbatim, groups facts by inferred category (deadlines, amounts, deductions, obligations, records), surfaces deadlines and action items, then boils transferable rules of thumb down to maxims of 8 words or fewer. Accepts pasted text, a local file path, or an Obsidian note reference, prints both sections in chat, and saves them to an outputs .md file. Use for notes that mix reference facts with judgment calls, for example tax, medical, or legal notes, meeting minutes, or research logs, or when the user says organize these notes, structure my notes, sort facts from principles, or make a clean reference. Do NOT use when the input is purely principles and you only want lossy maxims, to highlight takeaways inside a note in place, or to build a reusable advisor persona.
---

# Distill Notes v2

Process notes that MIX reference facts with heuristics. Two outputs from one source: a
lossless, organized reference for the facts, and a sharpened set of maxims for the heuristics.

## Core principle

Lossless on facts, lossy on principles. Facts (numbers, dates, rates, conditions, obligations)
are preserved verbatim and merely organized. Heuristics (rules of thumb, judgment calls) are
distilled hard, the way wisdom notes are. Never trade one behavior for the other.

## Fidelity guardrails

Three rules sit above the whole workflow. The output must come from the source, never from you.

- **Use only the provided notes.** Organize and distill what is there. Do not add outside ideas,
  facts, examples, or maxims the source does not contain. A sharper wording of the source is
  fine. A new idea is not. A heuristic that is only implied may be surfaced, but flag it as your
  reading, not the author's words.
- **State every assumption.** When you make a judgment call the reader could disagree with —
  which bucket an idea goes in, which category a fact belongs to, what an abbreviation means,
  which of two values is current — name it. Collect these and print them under an Assumptions
  heading. No silent guesses.
- **Ask when critical context is missing.** If something you cannot resolve would change a
  fact's value or meaning, or make the output misleading — an undefined term that drives a
  number, a referenced attachment you were not given, an unclear "current" figure — stop and ask
  the user before processing. Do not invent the answer.

Escalation ladder for uncertainty:

- Missing context that would corrupt a fact → ask the user, do not proceed on that item.
- A judgment call you can reasonably resolve → proceed, but state the assumption.
- A fact whose value you simply cannot confirm → keep it verbatim and mark it `(verify)`.

## Inputs

Accept any one of:

- **Pasted text** — raw notes inline in the request.
- **Local file path** — read the file.
- **Obsidian note reference** — glob `**/*<name>*.md` under the vault, excluding `.trash`. On
  multiple matches, list them numbered and ask the user to pick. Confirm the resolved path
  before processing.

Read the whole source. Do not truncate.

## Workflow

### Step 0 — Pre-flight check

Skim the source first. If critical context is missing — something unresolved that would change a
fact's value or meaning, or make the output misleading (see Fidelity guardrails) — ask the user
before going further. Otherwise proceed.

### Step 1 — Triage every idea

Sort each idea into one of two buckets:

- **FACT** — carries a number, date, rate, threshold, eligibility condition, obligation,
  procedure, deadline, or named reference. Anything that has a value you could get wrong.
- **HEURISTIC** — a transferable rule of thumb, strategy, or judgment call. No hard value
  attached.

When in doubt, file it as a FACT. Lossless is the safe failure mode. Never silently drop a fact.
A borderline FACT/HEURISTIC call is itself an assumption — record it for the Assumptions block.

### Step 2 — Organize the facts (lossless)

- Group facts by a category **inferred from the content**, not a fixed list. For tax notes the
  categories might be Deadlines, Income and rates, Deductions and credits, Obligations and
  filings, Records to keep, Open questions to verify. Other domains get their own categories. A
  non-obvious grouping is a judgment call — note it as an assumption.
- Preserve every value verbatim — numbers, currencies, percentages, dates, conditions, names.
- Dedupe only exact repeats. Never merge two facts that differ in any value, even slightly.
- Normalize formatting only, never the value → dates to `YYYY-MM-DD`, consistent currency
  notation. Do not round, simplify, or paraphrase a figure.
- Pull deadlines and action items into their own heading so nothing time-critical hides in a
  list.
- Mark anything uncertain or unconfirmed with a trailing `(verify)`.

### Step 3 — Distill the heuristics (lossy, sharpened)

- Distill only heuristics present in the notes. Do not import rules of thumb from your own
  knowledge to fill gaps or round out the set.
- Keep the vital few. Expect to drop the weak ones, not shorten them.
- One idea per bullet. Target 8 words or fewer.
- Strip framing scaffolding → "a good rule is...", "the secret is...". Present tense, certain.
- Sharpen by the dials test:
  - **Competing moves, pick one** → antithesis, keep "not" → "Give problems, not answers".
  - **Two dials on one system** → couplet, drop "not", end on the payoff → "Fewer tasks,
    bigger impact".
  - **A process** → sequence → "Make it small, perfect it, then scale".

### Step 4 — Format and output

Print the sections in chat, clearly separated, in this order:

1. **Reference** — the facts, grouped by category, deadlines and actions first.
2. **Principles** — the distilled maxims.
3. **Assumptions** — every judgment call you made (bucket, category, term, which value is
   current). Omit the heading entirely if you made none.

Formatting:

- Flat bullets, clean markdown. No asterisks, semicolons, em-dashes, or emojis. Use arrows,
  periods, commas.
- English, no diacritics.

Then save the same content to a file:

- Write to `outputs/<slug>-distilled.md`, creating `outputs/` in the current working directory
  if it does not exist.
- `<slug>` = the source note or file name in kebab-case when the input came from a file or vault
  note, otherwise a short kebab-case slug from the dominant topic.
- If that file already exists, append a numeric suffix (`-2`, `-3`, ...) so nothing is
  overwritten.
- Report the saved path in chat.

### Step 5 — Self-test before output

- Did any fact get dropped? Restore it. Facts are lossless.
- Does every fact keep its exact numbers, dates, and conditions? No rounding, no paraphrase.
- Did I add any fact, idea, example, or maxim not in the source? Remove it.
- Did I make a judgment call without stating it? Add it to Assumptions.
- Was any missing context critical enough that I should have asked instead of guessed? Ask now.
- Are deadlines and action items surfaced, not buried?
- Is each heuristic a real maxim, not a summary sentence?
- If the source had no heuristics, the Principles section is omitted, not padded. Same for a
  source with no facts and the Reference section.

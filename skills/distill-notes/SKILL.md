---
name: distill-notes
description: Distill raw notes into a sharp set of standalone maxims — distillation, not summarization. Keeps the vital few, drops 40-60% of ideas, compresses survivors to maxims of 8 words or fewer, promotes the most foundational idea to a headline, and sharpens contrasts into antithesis ("Give problems, not answers") or couplets ("Fewer tasks, bigger impact"). Returns flat, loosely clustered bullets in chat and also saves them as a .md file in an outputs/ folder. Use when the user says "distill these notes", "turn my notes into maxims", "compress this to principles", "boil this down to maxims", or wants raw notes reduced to a vital few transferable principles. Accepts pasted text, a local file path, or an Obsidian note reference. Do NOT use to summarize while keeping all the ideas, to highlight key takeaways inside a note in place, or to build a reusable advisor persona from interview transcripts.
---

# Distill Notes

Turn raw notes into a distilled set of maxims. This is distillation, not summarization. Drop
ideas, compress the survivors, sharpen them.

## Core principle

Keep the vital few. Compress to maxims. Sharpen. Cut the rest. Expect to delete 40-60% of
ideas, not shorten them.

## Inputs

Accept any one of:

- **Pasted text** — raw notes inline in the request.
- **Local file path** — read the file.
- **Obsidian note reference** — glob `**/*<name>*.md` under the vault, excluding `.trash`. On
  multiple matches, list them numbered and ask the user to pick. Confirm the resolved path
  before distilling.

Read the whole source. Do not truncate — keepable ideas can sit anywhere.

## Workflow

### Step 1 — Offer a target count (optional)

Ask once whether to set a target bullet count up front. A target forces the ranking when
selection is close (see Known limit). If the user declines, distill to your own judgment.

### Step 2 — Select what survives

- Keep transferable principles and mental models.
- Cut domain-specific observations unless central.
- Cut examples, anecdotes, personal-practice notes, tactical asides.
- Fold duplicates into one bullet.
- Synthesize what is implied. Do not just extract.

### Step 3 — Pick the lead

Pick the single most foundational idea. Promote it to a headline, not a bullet.

### Step 4 — Compress each bullet

- One idea each. Target 8 words or fewer.
- Strip framing scaffolding → "principle for...", "the secret is...", "a good way to...".
- Drop articles and pronouns when it still reads.
- Use shorthand → PMF, etc.
- Present tense, certain → "thoughts follow" not "thoughts will follow".
- Flip negated comparatives to positive → "not more tasks" becomes "fewer tasks". Direct reads
  as certain.

### Step 5 — Sharpen

Classify the contrast before sharpening. Competing moves, or two dials on one system.

- **Competing moves, pick one** → antithesis, keep "not" → "Give problems, not answers".
- **Two dials on one system** → couplet, drop "not", end on payoff → "Fewer tasks, bigger
  impact".
- **Couplet form** → matched adjective-noun pairs, equal length. Last word is the payoff.
- **Sequence for processes** → "Make it small, perfect it, find PMF, then scale".
- Imperative for actions. Bare maxim for laws.

### Step 6 — Format

- Flat bullets. Loose thematic clustering → philosophy, then product, then people.
- Clean markdown. No asterisks, semicolons, em-dashes, emojis. Use arrows, periods, commas.
- Parenthetical only for a short "why" tag, rare → "(its a gift)".
- English, no diacritics.

### Step 7 — Self-test before output

- Could each bullet stand alone on a wall? If it needs context, rewrite or cut.
- Did I drop enough? If more than 60% of source ideas survived, I kept too much.
- Any bullet still a summary sentence instead of a maxim? Fix it.
- Did I reach for antithesis on a couplet? If poles are two dials, drop the "not".

### Step 8 — Output

Do both:

1. **Print the distilled set in chat** — the headline followed by the clustered bullets.
2. **Save it as a file** — write the same content to `outputs/<slug>-distilled.md`, creating
   `outputs/` in the current working directory if it does not exist.
   - `<slug>` = the source note or file name in kebab-case when the input came from a file or
     vault note; otherwise a short kebab-case slug from the headline.
   - If that file already exists, append a numeric suffix (`-2`, `-3`, ...) so nothing is
     overwritten.
   - Report the saved path in chat.

## Known limit

Selection is partly taste. Strong, on-theme ideas can still lose on feel. To force the ranking,
set a target bullet count up front. Couplet is not the default. Without the dials test it
flattens real antitheses.

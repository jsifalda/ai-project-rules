---
name: highlight-key-takeaways
description: Highlight the most important takeaways and key learnings inside an Obsidian note by wrapping them in `==text==` (Obsidian highlight syntax). Edits the note in place. Use when the user asks to "highlight key takeaways", "highlight key learnings", "mark the important parts", "find and highlight main points in <note>", or similar. Requires a note/file name as input.
---

# Highlight Key Takeaways

Wrap the most important takeaways and key learnings in an Obsidian note with `==...==` (Obsidian highlight syntax). Edits the note in place — surrounding prose is untouched.

## Inputs

- **note-name** (required) — partial or full name of the target note in the vault

## Process

### Step 1: Locate the note
- Glob `**/*<note-name>*.md` under the vault, excluding `.trash`
- **Zero matches** → widen with case-insensitive / split-word search. If still none, abort and report.
- **Multiple matches** → list numbered, ask the user to pick.
- **Single match** → confirm the path with the user before editing.

### Step 2: Read the full note
Read the entire file. Do NOT truncate — takeaways can appear anywhere. For long notes, read in chunks until the end.

### Step 3: Identify takeaways (be ruthlessly selective)

Highlight only the **most important** ideas — not every useful sentence. Most candidates that *look* important should still be skipped. A note with **zero** highlights is acceptable if nothing passes the bar.

**Density target:** roughly **1 highlight per 800 words**, with a **hard cap of 8 highlights per note** regardless of length. Short notes (<1000 words) usually get 1–3; chapter-length notes get 5–8; never more.

#### Priority tiers

Fill slots top-down. Lower tiers only get highlighted if the higher tier is exhausted AND slots remain.

- **Tier 1 — always highlight if present (max 1 each):**
  - The single core thesis / one-line summary of the whole piece
  - A named principle, law, or framework that the note is built around

- **Tier 2 — highlight if slots remain (max 2–3 each):**
  - Research findings, stats, or quoted data that anchor the argument (e.g. "zero relationship")
  - Decisive rules the author insists on ("reject X", "always Y", "never Z")

- **Tier 3 — rarely; only if Tiers 1–2 left slots open:**
  - A genuinely counter-intuitive or surprising claim
  - A single memorable quote that captures the whole idea in one line

Per-note caps: **1** thesis, **3** named principles, **2** stats, **2** directives. If a tier is full, skip further candidates in it — do not promote to a different tier.

#### Memorability test (apply to every candidate)

Before highlighting a span, ask: **"If I quoted only this sentence from the entire note, would it still convey the most important idea?"**

- If **yes** → highlight.
- If **no, but it's a useful supporting point** → skip.
- If **it only makes sense with the paragraph around it** → skip.

When two candidates compete for the same idea, keep the shorter, more quotable one.

#### Skip even if it seems important

- Narrative anecdotes and illustrative stories (unless they end in a crisp lesson — then highlight only the lesson clause)
- Useful supporting points that elaborate on an already-highlighted idea
- Definitions, setup, context-setting sentences
- Examples that restate a named principle
- Transitional sentences, framing, flavor prose
- Frontmatter, headings, code blocks
- Any sentence whose "importance" comes from the surrounding paragraph, not itself

### Step 4: Apply highlights

Wrap the selected text in `==...==`. Rules:

- Wrap the **shortest clause that carries the idea** — ideally under 20 words, never more than one sentence
- If a sentence has framing prose plus the actual takeaway, highlight only the takeaway clause (leave the framing unhighlighted)
- Never wrap a full paragraph; never wrap multiple sentences in a single `==...==`
- Preserve all inner markdown (bold, italics, links, quotes) exactly
- Do NOT change any other text — no rewording, no added commentary
- Never wrap already-wrapped text (skip if `==` already surrounds it)

Use the `Edit` tool with exact string matches. Batch multiple independent `Edit` calls in parallel in one message for speed.

### Step 5: Report
After editing, return a short bulleted summary of the *themes* highlighted (not the full quotes) so the user can see coverage. Example:
- Thesis, planning, ownership, evidence, decisions, people, mindset, scaling

## AI-authored marker

After applying highlights, if at least one `==...==` highlight was added in this run, append the following line to the end of the file (preceded by a blank line):

`*(Highlights in this note were created by AI)*`

Skip if the marker already exists in the file.

## Notes

- This skill is for Obsidian vaults — `==highlight==` is Obsidian's native highlight syntax
- Do not create a new note or duplicate the file — always edit in place
- If the note already contains `==highlights==`, preserve them and add new ones alongside

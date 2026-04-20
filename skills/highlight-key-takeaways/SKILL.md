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

### Step 3: Identify takeaways (be selective)
Highlight only **key learnings** and **most important takeaways** — not every useful sentence. Aim for roughly 10–25 highlights per chapter-length file; fewer for short notes. Good candidates:

- The core thesis / one-line summary of the whole piece
- Named principles, laws, or frameworks
- Decisive rules ("reject X", "always Y", "never Z")
- Research findings, stats, or quoted data (e.g. "zero relationship")
- Memorable quotes attributed to experts
- Actionable directives the reader should apply
- Counter-intuitive or surprising claims

Skip:
- Narrative anecdotes and illustrative stories (unless they end in a crisp lesson)
- Transitional sentences, setup, flavor prose
- Examples that merely restate an already-highlighted rule
- Frontmatter, headings, code blocks

### Step 4: Apply highlights
Wrap the selected text in `==...==`. Rules:

- Wrap the **minimal meaningful span** — a full sentence or clause, not a whole paragraph
- Preserve all inner markdown (bold, italics, links, quotes) exactly
- Do NOT change any other text — no rewording, no added commentary
- If only part of a sentence carries the takeaway, highlight just that part (leave the framing prose unhighlighted)
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

---
name: distill-persona
description: Distill a leader's worldview from their interview transcripts into a reusable advisor persona. Produces a principles markdown (principles, mental models, recurring patterns, verbatim quotes, grouped by domain), a role markdown (description, core questions, mental models, tone), and a paste-ready CLAUDE.md activation snippet — all from the five-step "Distilling Leadership Wisdom" methodology. Asks one question at a time. Use when the user says "distill a persona from these transcripts", "build a leader's advisor persona", "extract leadership principles from interviews", "turn these podcast transcripts into a CLAUDE persona", or "create an advisor role from a leader's talks". Do NOT use for summarising a single article or note (use summarise-text or summarise-url), improving a prompt (prompt-enhancer), customer or user personas for product work (this skill is for leadership advisor personas only), or fetching transcripts (skill takes already-gathered local files, not URLs).
---

# Distill Persona

Turn a folder of interview transcripts of one leader into a structured principles document and a reusable advisor role definition, then optionally bundle the result as a self-contained persona skill. Seven interactive steps (five for the core distillation, one optional skill-packaging step, one wrap-up). Ask one question at a time. Never invent quotes — every quote must trace back verbatim to a provided transcript.

## Inputs

- **Leader name.** Free text — used to derive `<slug>` (kebab-case) for output filenames.
- **Transcript folder or file list.** Path(s) the user provides. Plain `.txt` or `.md`. Require **≥2 distinct interviews** so recurring-pattern detection in Step 3 has something to recur across.

## Outputs

Written to cwd during Steps 3–4 (intermediate — may be moved into a skill folder at Step 6 if the user opts in):

- `<slug>-principles.md` — the distilled principles document.
- `<slug>-role.md` — the advisor role definition.

Final chat message: a paste-ready `## Persona: <Name>` snippet for CLAUDE.md and a one-line invocation example.

Optionally written at Step 6 (if user opts in):

- `<chosen-path>/persona-<slug>/SKILL.md` — thin-wrapper skill that loads the references and answers in the persona's voice.
- `<chosen-path>/persona-<slug>/references/principles.md` — the principles doc, moved from cwd.
- `<chosen-path>/persona-<slug>/references/role.md` — the role doc, moved from cwd, with its internal `Reference` path updated to `references/principles.md`.

## Workflow

### Step 1 — Confirm the candidate

Ask the user (one `AskUserQuestion` call) for the leader's name. Then validate the three criteria below in a single follow-up question that lets the user confirm or flag a gap:

- **Sufficient source material** — multiple hours of interviews already gathered.
- **Personal motivation** — the user actually wants this person's lens on their own work.
- **Transferable frameworks** — the leader thinks in principles, not just war-stories tied to one company.

If any criterion fails, push back: explain which one fails and why distilling will produce thin output. Offer to abort or proceed with caveats. Do not silently continue.

### Step 2 — Locate transcripts

Ask the user for either:

- a folder path containing the transcript files, or
- an explicit comma/newline-separated list of file paths.

Then:

1. Resolve the paths. If a folder, list `.txt`/`.md` files inside it.
2. **Hard requirement: ≥2 files.** If only one, stop and ask the user to add more before continuing — the blog's whole premise (find patterns *across* interviews) collapses on a single source.
3. Read every file end-to-end.
4. Report back: filename, rough word count, and one-line guess at interview source/host. Ask the user to confirm the set is correct before proceeding.

### Step 3 — Distill principles

Load `references/distillation-prompt.md` and follow it to produce `<slug>-principles.md` in the current working directory.

Before writing the file, show the user the proposed domain headings and the count of principles under each (no body yet). This is the highest-value checkpoint — it lets the user redirect emphasis before you commit. After confirmation, write the full file.

### Step 4 — Build role definition

Load `references/role-definition-template.md` and fill in `<slug>-role.md` in the current working directory. Derive every section from the principles doc you just wrote — do not re-summarise the transcripts. Each **Core Question** must map to a recurring principle, not a one-off quote.

### Step 5 — Emit activation snippet

Print (in chat, not as a file) a paste-ready CLAUDE.md block:

```markdown
## Persona: <Name>

When I ask for `<name>`'s perspective on a decision, adopt the role defined in
`<absolute-path>/<slug>-role.md`. Lean on `<slug>-principles.md` for evidence
and direct quotes. Stay in their voice (see Tone). Refuse to invent quotes.
```

Follow with a one-line invocation example, e.g. *"`What would <Name> ask about whether to ship feature X this quarter?`"*

### Step 6 — Optional: bundle as a reusable skill

The two loose files in cwd work fine on their own (the activation snippet from Step 5 points at them directly). But if the user wants the persona to auto-load as a Claude/Copilot skill — like the existing `persona-stanier` — bundle them into a proper skill folder now.

Ask one `AskUserQuestion`:

- **Question:** *"Want to bundle this persona as a reusable skill?"*
- **Options:** `Yes — create skill folder` (recommended) / `No — skip, files are ready in cwd`.

**If No:** fall straight through to Step 7. Don't touch the cwd files.

**If Yes:** ask one follow-up `AskUserQuestion` for the target location. Preset options (these are the three sync sources from the user's CLAUDE.md — anything written here gets auto-synced by `sync-skills.js`):

1. `~/instructions/skills/` (global — syncs to Claude Code + Copilot) **(recommended)**
2. `~/mofa/ai-prompts/.agents/skills/` (mofa-shared)
3. `~/mofa/gemini/skills/` (gemini project-scoped)
4. User picks "Other" to enter a custom absolute path.

Resolve `~` to the user's home directory. Validate that the chosen directory exists; if not, stop and ask the user to either create it first or pick another path. Don't auto-create the parent.

Then load `references/persona-skill-template.md` and follow its instructions to:

1. Create `<chosen-path>/persona-<slug>/references/`.
2. Write `<chosen-path>/persona-<slug>/SKILL.md` from the template — substitute `<Name>` and `<slug>` everywhere, fill in the `description:` field from the principles doc's intro (positive AND negative triggers required), and tune Step 2's cadence guidance to match the persona's actual Tone in `role.md`.
3. Move `<cwd>/<slug>-principles.md` → `<chosen-path>/persona-<slug>/references/principles.md` (content unchanged).
4. Move `<cwd>/<slug>-role.md` → `<chosen-path>/persona-<slug>/references/role.md`, then edit one line inside it: `Principles document: ./<slug>-principles.md` → `Principles document: references/principles.md`.
5. Ask the user once whether to delete the now-moved source files in cwd. Default: keep them.

Report the new skill folder's absolute path. Mention that `sync-skills.js` will pick it up on the next session start (no manual symlink needed).

### Step 7 — Done

End the turn with a short summary:

- The two doc paths (cwd or inside the new skill folder).
- The activation snippet location (chat).
- If a skill folder was created: its absolute path, and a one-line note that it'll auto-load on the next session.

Nothing else.

## Hard rules

- **No invented quotes.** Every `>` block in the principles doc must appear verbatim in one of the input transcripts. If you cannot find an exact quote for a principle, mark the principle as "paraphrased — no clean quote available" instead.
- **No external research.** Do not pad with material from books, Wikipedia, or your training data. The skill's value is *specificity to the source material* — the blog post is explicit on this. If a principle is not in the transcripts, it does not go in the document.
- **Recurring-pattern bar.** A claim counts as a "principle" only if it appears in **≥2 interviews**. Single-interview claims go in a "Context-only observations" section at the end of the principles doc.
- **One question per turn.** When asking the user something, use `AskUserQuestion` with focused options. Do not batch questions.

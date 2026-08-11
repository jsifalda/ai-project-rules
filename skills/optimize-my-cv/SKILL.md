---
name: optimize-my-cv
description: Diagnose a CV or resume against a target role — score it across a fixed set of dimensions, then return what is already holding up, an evidence-quoted gap list ranked blocker-first, and an ordered remediation plan. Picks an IC or leadership track automatically, matches requirement-by-requirement against a job description when one is supplied, and accepts pasted text, a local .md or .txt path, or a local .pdf read directly. Use when the user says "optimize my cv", "review my resume", "what is wrong with my cv", "gap analysis of my resume", "is my cv ready for X role", or asks why their applications get no replies. Do NOT use to write or rewrite the CV for the user, to draft cover letters, to run interview prep or mock interviews, or to do job searching, sourcing, or application tracking.
---

# Optimize My CV

Diagnose a CV against a target role and hand back a prioritized fix list. The deliverable is the
gap analysis and the plan, not a rewritten CV.

The reference files carry the detail. Read them in Step 4, not before:

- [references/rubric.md](references/rubric.md) — the scoring dimensions, IC vs leadership
  calibrations, severity definitions, and the track-selection heuristic.
- [references/best-practices.md](references/best-practices.md) — bullet formula, metric families,
  ATS constraints, section order, and rules for projects.

## Step 1 — Take the CV

Accept any one of:

- **Pasted text** — the CV inline in the request.
- **Local `.md` or `.txt` path** — read the file.
- **Local `.pdf` path** — read it with the native Read tool, which handles PDFs directly. No
  conversion step, no library, nothing to install.

On a `.docx`, stop and say so in one line, with the workaround: export to PDF, or paste the text.
Do not reach for a parser that is not installed.

If the user has no CV yet, do not stall. Offer to build the gap analysis from a short interview
about their history instead, and run the rest of the workflow off that.

Read the whole document. Gaps hide in the sections people skim past.

## Step 2 — Establish the target

A gap only exists relative to something. If the target role and seniority are not already stated,
ask once, in a single question, then proceed on the answer.

If the user declines to name a target, do not ask again and do not stall. Fall back to step 2 of
the default heuristic in Part 3 of [references/rubric.md](references/rubric.md), which reads the
track off the most recent role, and say in one line that the gaps will be broader than a targeted
audit would produce.

If the user supplies a job description, use it for requirement-by-requirement matching and
keyword coverage, and say which requirements the CV evidences and which it does not. A job
description is optional. Without one, judge against the stated target role and seniority.

## Step 3 — Pick the track

Infer IC or leadership from the CV and the target using the heuristic in
[references/rubric.md](references/rubric.md). State the pick in one line with the reason, then
continue. Do not ask the user to choose — the CV and the target already answer it.

## Step 4 — Analyse

Read both reference files now.

Score every dimension in [references/rubric.md](references/rubric.md) against the track picked in
Step 3.

Judge craft questions against [references/best-practices.md](references/best-practices.md), but
scope that file to the track. It is IC-tech-focused and says so in its own header.

- **IC track** — it applies whole.
- **Leadership track** — apply only what holds for any senior CV: structure and scannability, ATS
  survivability and parse hazards, the projects rules where a projects section exists, and the
  interview-defence test. Do not carry the IC-specific expectations across. A missing GitHub link,
  a gap in the four IC metric families, and a stack mismatch are not leadership findings, and
  raising them tells a manager to fix a CV that is not the one they are writing.

Collect evidence as you go. Every finding needs a quotable line from the CV behind it.

## Step 5 — Report

Exactly this order.

**Holding up.** What is already strong, so the user knows what not to touch. Up to four bullets,
short. If nothing is defensibly strong, say that in one line rather than manufacturing a strength
to fill the section — a padded strength here contradicts the never-invent rule below. Skipping the
section entirely leads people to rewrite working sections.

**Gaps.** Blockers first, then major, then minor. Each gap carries:

- the evidence, quoted from the CV
- what is wrong with it
- what it costs the candidate — the screen it fails, the seniority it undersells, the question it
  invites

A gap with no quoted evidence is not a gap, it is a guess. Drop it.

**Plan.** An ordered remediation list, blocker-first. Each item names the concrete edit, the CV
section it touches, the effort, and the expected impact. This list is the deliverable — write it
so the user can work straight down it.

## Step 6 — Offer to save, once

Ask once whether to save the gap analysis and plan to a file. Do not save unless the user says
yes.

- **On yes** — require the user to name a path. Resolve it to an absolute real path first,
  following symlinks, and run both checks below against what it resolves to rather than what was
  typed, since a relative path or a link can otherwise walk straight past them.
  Refuse any resolved path inside this repository and say
  why in one line. If the path sits under a folder that syncs to a third-party service — Dropbox,
  iCloud Drive, Google Drive, OneDrive, or similar — name the service and confirm before writing,
  since that is the same egress the rules below govern. If that confirmation is declined, write
  nothing and offer a path outside the synced folder instead. Otherwise write the content that was
  printed in chat and report the saved path.
- **On no** — stop. Leave nothing on disk.

## Rules

- **Never invent experience, metrics, employers, or dates.** When a bullet needs a number the CV
  does not have, ask the user for it. Never supply a placeholder figure, not even an obviously
  fake one — placeholders get shipped.
- **Do not rewrite the CV.** The gap analysis and the plan are the deliverable. If the user wants
  the edits made, that is a separate request they make after seeing the plan.
- **Do not echo the raw CV back** in the output. Quote only the lines a finding rests on.
- **Never write CV-derived content anywhere inside this repository.** It is public.
- **Never send CV content to any third-party service** without explicit confirmation first. A CV
  is personal data.
- **Flag any claim the user could not defend under interview questioning.** Overclaiming fails
  later and more expensively than a thin CV fails early.
- **Every gap must be answerable from the user's real history.** If closing it would require
  inventing something, it is not a gap — it is a mismatch with the target. Say so plainly, and
  say whether the fix is a different framing of real work or a different target.

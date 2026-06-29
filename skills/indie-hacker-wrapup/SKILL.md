---
name: indie-hacker-wrapup
description: End-of-session ritual that mines the current conversation for X/Twitter-worthy takeaways and drafts a build-in-public post. Runs directly on invocation — no permission question — scanning the session against a quality bar (non-obvious lessons, tool or automation wins, instructive failures, counterintuitive calls, before/after results, mental models), filtering out anything employer-confidential or personally identifying, and refusing to force a post when nothing clears the bar. Surfaces a shortlist of angles, then drafts the chosen one as a copy-paste-ready post. Remembers angles it has already pitched across sessions so it never suggests the same one twice. Use when you type /indie-hacker-wrapup, or say wrap up this session, draft a learning from this session for X, or session takeaways for twitter. Do NOT use for general prose writing, for summarising the session into notes, or to invent posts not grounded in what actually happened.
---

# Indie Hacker Wrapup

An end-of-session ritual. Mine the current session for takeaways worth sharing with an indie-hacker, build-in-public audience on X, then draft the strongest one into a post. Stay quiet when nothing is worth posting.

This skill reads the conversation you are already in, so it needs no transcripts. The one file it keeps is its own ledger of angles already pitched, so it never repeats one (Step 0).

Run it directly. Invoking the skill is the go-ahead, so skip any "want to draft a learning?" question and go straight to scanning the session for angles. The willingness to decline in Step 2 is the safety valve, not an upfront permission gate.

## Step 0 — Load the ledger of past angles

Before scanning, read the ledger of angles already pitched in earlier sessions:

`~/.claude/indie-hacker-wrapup/suggested-angles.md`

If it exists, hold its lines as the "already pitched" set. You dedup against it in Step 2. If it does not exist yet, treat the set as empty. Step 2 creates the file the first time you present a shortlist.

## Step 1 — Scan the session against the bar

Review what actually happened in this session. A takeaway qualifies only if it is at least one of these:

- a non-obvious lesson or realization
- a concrete workflow, tool, or automation win (keep the specific detail)
- a failure and what it taught
- a counterintuitive call or tradeoff
- a before/after result or metric
- a reusable mental model you actually applied

Two hard filters, applied before anything becomes a candidate:

- **Privacy.** Drop anything employer-confidential, client- or teammate-identifying, NDA-bound, or personally sensitive. Never put private work content into a public draft.
- **Grounded.** Every angle traces to something that happened in this session. If making it interesting needs invented detail, it does not qualify.

Lean toward builder, shipping, AI-workflow, and automation angles. That is the audience.

## Step 2 — Decide, dedup against the ledger, and record

- Nothing clears the bar → say so plainly, in a line or two, and stop. Do not force a weak post. A skipped post beats a generic one.
- One or more clear it → build a shortlist of 2 to 4 angles, then dedup it against the ledger from Step 0:
  - **Clear repeat** of a logged angle → drop it silently. It is already covered.
  - **Borderline** (similar but not obviously the same idea) → keep it, but flag it inline with the date you logged it before, e.g. "close to one you covered on 2026-06-12, still want it?". Let the user judge. Suppressing a genuinely new angle is the costlier mistake, so when unsure, surface and flag rather than drop.
- If dedup empties the shortlist (every angle is a clear repeat) → tell the user the angles here overlap with ones already covered, name them, and stop. Record nothing new.
- For each surviving angle, give the angle in one line plus one line on why it would land with X readers. Let the user pick. If they defer, take the strongest.
- **Record now, before the user picks.** The moment you present the shortlist, append every angle in it (fresh and flagged-borderline alike) to the ledger, one per line as `- [YYYY-MM-DD] <the angle in one line>`, using today's date from `date +%F`. Create `~/.claude/indie-hacker-wrapup/` and the file (with a `# Suggested X angles (do not re-suggest)` header) if they do not exist. This happens in the same turn you show the shortlist, so an angle is remembered even when the user never picks one. Angles you dropped as clear repeats are already in the ledger, so do not write them again.
- **Override.** If the user tells you to ignore the ledger or re-pitch a past angle, do it and surface the logged angle.

## Step 3 — Draft the chosen post

Draft the picked angle as a single X post, applying the `write-like-human` skill's ruleset (active voice, vary sentence length, no em-dashes, semicolons, asterisks, emojis, no hype or AI-filler).

X-native craft:

- Open with a hook. The first line has to stop the scroll on its own.
- One idea per post. Cut everything that does not serve it.
- Concrete over generic. Real numbers, the real tool, what actually broke.
- No hashtag spam, no engagement bait, no thread theatrics.
- Keep it inside a single tweet by default. If the idea genuinely needs room, offer a thread version instead of cramming.

Output the post copy-paste ready in chat. Offer a thread variant or a second angle if the user wants one.

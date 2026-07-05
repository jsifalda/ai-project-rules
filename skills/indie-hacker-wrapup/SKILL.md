---
name: indie-hacker-wrapup
description: End-of-session ritual that mines the current conversation for X/Twitter-worthy takeaways and drafts a build-in-public post. Runs directly on invocation — no permission question — reading the session on two lenses (the product you built plus the craft behind it), scoring candidates against an absolute resonance bar, filtering out anything employer-confidential or personally identifying, and refusing to force a post when nothing clears the bar. Surfaces a ranked shortlist, then drafts the chosen angle as a copy-paste-ready post. Tracks angles it has already pitched so it repeats one only when a new session is clearly stronger evidence. Use when you type /indie-hacker-wrapup, or say wrap up this session, draft a learning from this session for X, or session takeaways for twitter. Do NOT use for general prose writing, for summarising the session into notes, or to invent posts not grounded in what actually happened.
---

# Indie Hacker Wrapup

An end-of-session ritual. Mine the current session for takeaways worth sharing with an indie-hacker, build-in-public audience on X, then draft the strongest one into a post. Stay quiet when nothing is worth posting.

This skill reads the conversation you are already in, so it needs no transcripts. The one file it keeps is its own ledger of angles already pitched, so it repeats an angle only when a new session is clearly stronger evidence (Step 0).

Run it directly. Invoking the skill is the go-ahead, so skip any "want to draft a learning?" question and go straight to scanning the session for angles. The willingness to decline in Step 3 is the safety valve, not an upfront permission gate.

Calibration lives next to this file. When you need a worked sense of what separates a weak angle from a strong one, read `references/angle-examples.md` before you build the shortlist.

## Step 0 — Load the ledger of past angles

Before scanning, read the ledger of angles already pitched in earlier sessions:

`~/.claude/indie-hacker-wrapup/suggested-angles.md`

If it exists, hold its lines as the "already pitched" set. You weigh new candidates against it in Step 3. If it does not exist yet, treat the set as empty. Step 3 creates the file the first time you present a shortlist.

## Step 1 — Read the session on two lenses

Review what actually happened this session, and mine it on two lenses, not one. Most weak wrap-ups happen because only the first lens ever gets used, so the post is always about engineering process and never about what was built.

**Lens A — the craft (how you built it).** A takeaway qualifies if it is at least one of:

- a non-obvious lesson or realization
- a concrete workflow, tool, or automation win (keep the specific detail)
- a failure and what it taught
- a counterintuitive call or tradeoff
- a before/after result or metric
- a reusable mental model you actually applied

**Lens B — the product and its domain (what you built and why it matters).** A takeaway qualifies if it is at least one of:

- the user problem the change solves, and why it is worth solving
- a domain surprise: something about the problem space most people get wrong
- a "you are probably doing this too" reversal the reader can act on today
- a product-design tradeoff (one dataset answering two different questions, and so on)
- what the thing you built reveals about the space it lives in

Lens B is repo-aware. Decide first whether this session is your own indie project or work for an employer, client, or any org that is not yours:

- **Your own project** → mine the specific product story. Real feature, real names, real numbers, the actual surprise. Specificity is the post.
- **Employer or client work** → mine only the universal, transferable lesson the work taught, stripped of every employer specific. No org or repo identity, no internal metrics, no confidential detail. The lesson travels; the context stays behind.
- **Unsure which** → treat it as employer work and keep it universal. The privacy filter below is why.

**Under-mining guard.** If every candidate you are holding is a Lens-A craft angle and not one is Lens B, you under-looked. Go back to what was built and who it is for before moving on. A session that shipped a real product almost always has a Lens-B angle.

Two hard filters, applied to every candidate on both lenses before it becomes real:

- **Privacy.** Drop anything employer-confidential, client- or teammate-identifying, NDA-bound, or personally sensitive. Never put private work content into a public draft.
- **Grounded.** Every angle traces to something that happened in this session. If making it interesting needs invented detail, it does not qualify.

## Step 2 — Synthesize before you extract

Before listing atomic angles, write one line naming the single most significant or surprising thing about this session as a whole: its arc, its irony, the through-line. Then look for an angle that expresses that, not just the discrete events.

The strongest posts often connect two facts the session kept separate. Example shape: a tool that measures X, built by a process that itself did a lot of X. That angle exists only if you synthesize. Atomic extraction walks straight past it.

## Step 3 — Score, dedup, decide, record

**Score against an absolute bar first.** For each candidate, from either lens, check three things:

- Does it teach the reader something they can use?
- Is there a concrete number, a reversal, or a genuine surprise in it?
- Would a stranger who does not know you stop scrolling and care?

An angle must clear all three to be a candidate. If nothing clears the bar → say so plainly, in a line or two, and stop. Do not force a weak post. A skipped post beats a generic one. Rank whatever clears the bar by how hard it clears it. That ranking, not ledger novelty, sets the shortlist order.

**Then dedup against the ledger from Step 0.** Dedup is theme-and-evidence aware, not binary:

- **Clear repeat with no new strength** → drop it silently. It is already covered.
- **Stronger instance** of a logged angle, where this session is materially better evidence than the logged version (shipped vs merely planned, a real metric vs a hypothetical, a live bug caught vs a theoretical one) → keep it, re-pitched and flagged inline with the prior date, for example "stronger evidence than the one you logged on 2026-06-29, re-pitch?". Let the user judge. A great angle backed by fresh proof beats staying silent because a thin version was logged once.
- **Borderline** (similar but not obviously the same idea) → keep it, flag it inline with the date you logged it before. Suppressing a genuinely new angle is the costlier mistake, so when unsure, surface and flag rather than drop.

If dedup empties the shortlist (every angle is a clear repeat with no new strength) → tell the user the angles here overlap with ones already covered, name them, and stop. Record nothing new.

For each surviving angle, give the angle in one line plus one line on why it would land with X readers. Let the user pick. If they defer, take the top-ranked one.

**Record now, before the user picks.** The moment you present the shortlist, append every angle in it (fresh, stronger-instance, and flagged-borderline alike) to the ledger, one per line as `- [YYYY-MM-DD] <the angle in one line>`, using today's date from `date +%F`. Create `~/.claude/indie-hacker-wrapup/` and the file (with a `# Suggested X angles (do not re-suggest)` header) if they do not exist. This happens in the same turn you show the shortlist, so an angle is remembered even when the user never picks one. Angles you dropped as clear repeats are already in the ledger, so do not write them again.

**Override.** If the user tells you to ignore the ledger or re-pitch a past angle, do it and surface the logged angle.

## Step 4 — Draft the chosen post

Draft the picked angle as a single X post. Load the `write-like-human` skill and apply its full 17-rule ruleset to every line (do not rely on the summary here). Before you output, re-read the draft against those rules and strip any violation.

X-native craft:

- Open with a hook. The first line has to stop the scroll on its own.
- One idea per post. Cut everything that does not serve it.
- Concrete over generic. Real numbers, the real tool, what actually broke.
- No hashtag spam, no engagement bait, no thread theatrics.
- Keep it inside a single tweet by default. If the idea genuinely needs room, offer a thread version instead of cramming.

Output the post copy-paste ready in chat. Offer a thread variant or a second angle if the user wants one.

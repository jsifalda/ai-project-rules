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

Before scanning, read the ledger of angles already pitched in earlier sessions. The ledger always lives at this literal path:

`~/.claude/indie-hacker-wrapup/suggested-angles.md`

Use `~/.claude/` verbatim — never a `$CLAUDE_CONFIG_DIR`-relative path. Both agent profiles (`.claude` and `.claude-pro`) share this one ledger on purpose, so dedup sees every past angle regardless of which profile you are running under. Writing it under the active config dir would fork the ledger in two and break dedup.

If it exists, hold its lines as the "already pitched" set. You weigh new candidates against it in Step 3. If it does not exist yet, treat the set as empty. Step 3 creates the file the first time you present a shortlist.

**Row format.** Current rows carry structured tags:

`- [YYYY-MM-DD] [profile:<.claude|.claude-pro>] [theme:<slug>] [src:<repo-or-project-slug>] <angle> — evidence: <the concrete session fact it traces to>`

Older legacy rows are the bare `- [YYYY-MM-DD] <angle>` shape with no tags. When you dedup against a legacy row, infer its theme best-effort from the line text so history still participates.

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

**Inside-baseball guard.** Most sessions here are meta-work on the agent setup itself — model routing, code-review agents, statusline tokens, CLAUDE.md gates, doc-sync. Those fascinate the person who did them and bore everyone else. For every candidate, ask: would this land with someone who does NOT build AI agents or use Claude Code? If no, it is niche-of-niche → demote it hard, and prefer the Lens-B product/domain angle over the Lens-A agent-config angle. An angle about the thing you built beats an angle about how you configured the tool that built it.

Two hard filters, applied to every candidate on both lenses before it becomes real:

- **Privacy.** Drop anything employer-confidential, client- or teammate-identifying, NDA-bound, or personally sensitive. Never put private work content into a public draft.
- **Grounded.** Every angle traces to something that happened in this session. If making it interesting needs invented detail, it does not qualify.

## Step 2 — Synthesize before you extract

Before listing atomic angles, write one line naming the single most significant or surprising thing about this session as a whole: its arc, its irony, the through-line. Then look for an angle that expresses that, not just the discrete events.

The strongest posts often connect two facts the session kept separate. Example shape: a tool that measures X, built by a process that itself did a lot of X. That angle exists only if you synthesize. Atomic extraction walks straight past it.

## Step 3 — Score, dedup, decide, record

**Score against an absolute bar first.** For each candidate, from either lens, check four things. All four must pass:

- **Usable.** Does it teach the reader something they can act on?
- **Surprise.** Is there a concrete number, a reversal, or a genuine surprise in it?
- **Stranger cares.** Would a stranger who does not know you stop scrolling and care?
- **Original.** Is the core claim something the reader has NOT already seen a hundred times? An angle that reduces to a generic build-in-public maxim fails here unless this session adds a genuinely new twist. Reject on sight, no matter how specific the session detail dressed around it: "built ≠ shipped", "just ship it / ship volume", "use cheaper models for grunt work", "trust but verify", "green tests can still be wrong", "done is better than perfect", "talk to your users", "distribution is the only moat", "AI wrote 90% of my code". If your angle is one of these with a new coat of paint, it is not original. Kill it or find the twist that is actually new.

An angle must clear all four to be a candidate. If nothing clears the bar → say so plainly, in a line or two, and stop. Do not force a weak post. A skipped post beats a generic one, and most sessions should yield zero or one, not five — if you are holding five, your bar slipped. Rank whatever clears the bar by how hard it clears it. That ranking, not ledger novelty, sets the shortlist order.

**Diversify the shortlist by archetype.** A shortlist of five contrarian-reversal takes is one post written five ways — that monotony is what makes wrap-ups read generic. When you have more than one candidate, spread them across distinct post archetypes rather than stacking the same shape. Archetypes to draw from: specific-story-with-tension (what broke, what you did, how it turned), strong-opinion / hot-take, useful-resource or how-to (a concrete thing the reader can go use), honest-failure (what went wrong and the cost), counterintuitive-data (a real number that upends an assumption). If every survivor is the same archetype, keep only the single strongest and say so, rather than padding with clones.

**Then dedup against the ledger from Step 0.** Dedup is theme-and-evidence aware, not binary. Work at the theme level first: group candidates and ledger rows by their `theme:` tag (infer it for legacy rows), because the recurring failure here is the same theme resurfacing session after session under new specifics.

- **Theme already logged 2+ times** → that theme is exhausted. Drop the candidate unless it opens a materially new sub-angle within the theme, and if you keep it, say plainly it is the Nth time this theme has come up.
- **Clear repeat with no new strength** → drop it silently. It is already covered.
- **Stronger instance** of a logged angle, where this session is materially better evidence than the logged version (shipped vs merely planned, a real metric vs a hypothetical, a live bug caught vs a theoretical one) → keep it, re-pitched and flagged inline with the prior date, for example "stronger evidence than the one you logged on 2026-06-29, re-pitch?". Let the user judge. A great angle backed by fresh proof beats staying silent because a thin version was logged once.
- **Borderline** (similar but not obviously the same idea) → keep it, flag it inline with the date you logged it before. Suppressing a genuinely new angle is the costlier mistake, so when unsure, surface and flag rather than drop.

If dedup empties the shortlist (every angle is a clear repeat or an exhausted theme) → tell the user the angles here overlap with ones already covered, name them, and stop. Record nothing new.

For each surviving angle, give the angle in one line plus one line on why it would land with X readers, and carry the concrete session detail into the pitch — the specific scene, not the generalized maxim. Let the user pick. If they defer, take the top-ranked one.

**Record now, before the user picks.** The moment you present the shortlist, append every angle in it (fresh, stronger-instance, and flagged-borderline alike) to the ledger, one row each in the structured format:

`- [YYYY-MM-DD] [profile:<basename of $CLAUDE_CONFIG_DIR, default .claude>] [theme:<slug>] [src:<repo-or-project-slug>] <the angle in one line> — evidence: <the concrete session fact it traces to>`

Get today's date from `date +%F` and the profile from `basename "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"`. Pick a short stable `theme:` slug (reuse an existing one when the angle fits it) and an `src:` slug for the repo or project the session worked on. Create `~/.claude/indie-hacker-wrapup/` and the file (with a `# Suggested X angles (do not re-suggest)` header) if they do not exist. This happens in the same turn you show the shortlist, so an angle is remembered even when the user never picks one. Angles you dropped as clear repeats are already in the ledger, so do not write them again.

**Mark the winner.** Once the user picks an angle to draft (Step 4), prefix its ledger row with `★ ` so future runs can tell what was actually posted apart from what was merely pitched.

**Override.** If the user tells you to ignore the ledger or re-pitch a past angle, do it and surface the logged angle.

## Step 4 — Draft the chosen post

Draft the picked angle as a single X post. Load the `write-like-human` skill and apply its full 17-rule ruleset to every line (do not rely on the summary here). Before you output, re-read the draft against those rules and strip any violation.

X-native craft:

- Open with a hook. The first line has to stop the scroll on its own.
- One idea per post. Cut everything that does not serve it.
- Concrete over generic. Real numbers, the real tool, what actually broke.
- Lead with the specific scene, not the lesson. Open on the concrete thing that happened and let the takeaway land after — a post that opens on the generalized maxim ("built ≠ shipped") reads as advice everyone has heard. The specific moment is what earns the general point.
- No hashtag spam, no engagement bait, no thread theatrics.
- Keep it inside a single tweet by default. If the idea genuinely needs room, offer a thread version instead of cramming.

Output the post copy-paste ready in chat. Offer a thread variant or a second angle if the user wants one.

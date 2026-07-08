---
name: create-product-vision
description: "Turn a short product or project description into a motivating vision doc covering three angles: motivation (why it matters and the shift it creates), practical (what actually happens day to day and over time), and product (what it is, what it does, what you get, so the reader knows what to expect). Use whenever the user wants a vision, mission, or why-this-matters framing for a product, project, side project, tool, or workflow. Triggers: 'write a vision', 'draft a vision for X', 'product vision from this description', 'vision for this project', 'give this a vision statement', or when the user pastes a short description of something they are building and wants it framed compellingly. Produces one tight vision doc (tagline, what it is, what it does, what you get, the shift, success signal), not marketing copy, a pitch deck, or a full plan. Do NOT use to summarise existing text (use summarise-url or summarise-text), to break a goal into tasks (use goal-breakdown), or to plan an MVP launch (use ship-v1)."
---

# Product Vision

Turn a short description of something being built into one tight, motivating vision doc. The reader should finish it knowing what the thing is, why it matters, and what to expect.

## Core rule

- **Cover all three angles, every time.** A vision that only inspires leaves the reader unsure what the product is. One that only lists features leaves them unsure why to care. Hit all three (below).
- **Stay grounded in the description.** Never invent features, metrics, or claims the author did not give. If a detail is missing and matters, ask (see below), don't fabricate.
- **Tight by default.** Short sections, bullets, one page or less. No preamble, no "Here is your vision".
- **Human prose.** Load and apply the `write-like-human` ruleset before writing. No em-dashes, semicolons, asterisks for emphasis, or filler. Use `→` for the shift.

## The three angles

Every vision must land all three. They map onto the template sections, so you rarely label them explicitly.

1. **Motivation** → why anyone should care. The status quo it replaces and the shift it creates. Carried by the tagline and the "shift" section.
2. **Practical** → what actually happens when someone uses it, day to day and over time. Carried by "what it does" and "what you get".
3. **Product** → what the thing is and what to expect. Its category and mechanism, so the reader pictures the real object, not a vibe. Carried by "what it is".

## Before writing: check the input

Scan the description for four things:

- **What it is** → the product's category and how it works (app, workflow, service, etc.).
- **Reader** → who this is for. Default to the person who would use the product if unstated.
- **Status quo** → the pain or friction it replaces.
- **Success** → what "it works" looks like.

If two or more are missing or unclear, ask up to three tight questions first, then write. If the description already answers them (or only one gap remains, which you can reasonably fill), write directly. Do not interrogate when the input is clearly rich enough.

## Output template

Use this exact shape. Drop a section only if it genuinely does not apply.

```markdown
## Vision

[Tagline. One line. The hook or the shift, sharp enough to remember.]

**What it is**
- [Category and mechanism. What kind of thing this is.]
- [How it runs / where it lives, if that shapes expectations.]

**What it does**
- [Core action, in the reader's terms.]
- [The next most important action.]

**What you get**
- [Concrete benefit.]
- [Concrete benefit.]
- [Concrete benefit.]

**The shift**
- From: [the status quo, stated as felt pain]
- To: [the new reality this product creates]

[Success signal. One line: "You'll know it works when ..."]
```

Keep bullets to a phrase or short sentence. Cut any line that repeats another.

## Example

**Input:** "n8n workflow that watches chosen X accounts, pulls their new posts, sends them to me, and saves every tweet to Supabase. Point is to follow the accounts without opening X, and to keep an archive I can reuse (e.g. training AI agents)."

**Output:**

## Vision

Follow the people worth reading, keep everything they post, build on it.

**What it is**
- An automated n8n pipeline, not an app you log into. Runs on its own, in the background.
- You give it a list of accounts. It does the rest.

**What it does**
- Polls your chosen profiles on a schedule and pulls their new posts.
- Delivers them to you (digest, feed, wherever you route them). You never open X.
- Writes every tweet to Supabase, clean and queryable.

**What you get**
- One stream of only the accounts you picked, newest first, no algorithm and no ads.
- A permanent archive that outlives deleted accounts and platform changes.
- Reusable data: search it, feed it to agents, or use it as a persona corpus to train writing styles.

**The shift**
- From: open X, get pulled into a feed someone else controls, lose the good posts.
- To: the posts you want arrive on your terms → get stored → get reused.

You'll know it works when you stop visiting X timelines, and the archive is rich enough to teach an agent to write like the accounts in it.

## Guardrails

- One vision doc per request. Do not pad into a pitch deck, roadmap, or marketing landing page.
- Match the author's register. A dev tool vision reads different from a consumer app vision, but both stay concrete.
- If the user asks for a specific angle only ("just the motivation part"), give that section well rather than forcing the full template.

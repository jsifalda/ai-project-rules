---
name: goal-breakdown
description: "Break a big finite goal, project, or idea into a sharp end state, ordered milestones, and one-day tasks with a single clear next action. Use whenever the user wants to decompose, break down, or plan a project into actionable steps, asks 'where do I start' on something they want to ship, build, learn, or launch, says 'make a plan to achieve X', 'turn this goal into tasks', '1% better every day toward X', or feels stuck because a goal is too big to begin. Also use to continue a plan already in progress: when the user finished a milestone and asks what is next, says 'continue', 're-plan from here', or 'update the plan', re-decompose the remaining work from where they actually landed. Handles finite projects with an end state only. Do NOT use for ongoing habits or systems with no finish line (there is no streak or habit tracking here), for pure scheduling or calendar work, for summarising web pages or text, or for distilling raw notes into maxims (a different job)."
---

# Goal Breakdown

Turn one big finite goal into a plan you can start today, and re-plan it as you go. Output a sharpened end state, ordered milestones, every milestone broken into one-day tasks, and the single first action.

This is decomposition, not a to-do dump. A generic list of steps is worthless. The value is an opinionated method that produces a startable plan and avoids the four ways breakdown fails: decomposing a fog, relabeling instead of splitting, task-explosion paralysis, wrong sequence.

## When this fits

Finite projects only. The goal must have an end state you can reach. Ship X, learn Y, launch Z, write the thing, pass the exam.

If the goal is an ongoing system with no finish line (get fitter forever, be more consistent, 1% better at a craft with no target), say so plainly and stop. That needs a habit or system, not a project plan. Do not force a finish line onto something that has none.

## Modes

- **Plan** (default) — a fresh goal in, full decomposition out. Triggers: break down, decompose, where do I start, make a plan.
- **Continue** — a plan already running and a milestone is done. Re-decompose the remaining work from where you actually landed. Triggers: "I finished milestone 1, what's next", "continue", "re-plan from here", "update the plan", or a plan pasted back with boxes checked.

## Method (Plan mode)

Run these four steps in order. Each one kills a specific failure.

### 1. Sharpen the goal. Gate everything on this.

A fog cannot be decomposed. Before splitting anything, force the goal into a measurable, falsifiable end state plus a deadline.

- Write `Done when:` as an observable condition someone else could verify.
- Bad: "build a SaaS." Good: "paid SaaS live, one paying customer, by Sept 1."
- If you cannot state what done looks like in observable terms, ask one sharpening question (what does done look like, by when), then proceed. Ask once, not five times.

### 2. Split into milestones. Order by risk, then dependency.

Break the goal into 3 to 7 ordered checkpoints. Each milestone is a meaningful state change, something that visibly moves you closer, not a restatement of the goal.

- Front-load the riskiest unknown. The thing most likely to kill the project goes early, so you find out fast and waste nothing.
- Then respect dependencies. Do not schedule work that gets thrown away because an upstream answer was not in yet.
- Cap at 7. If you have more, you are listing tasks, not milestones. Group them.

### 3. Explode every milestone into tasks. Mark the far ones provisional.

Detail all milestones down to one-day tasks. Full scope visible up front catches cross-milestone dependencies and missing pieces, and lets the user cut from completeness rather than guess.

But mark every milestone past the first as provisional, revisit on arrival. What you learn early rewrites later tasks, so distant detail is a draft you will correct, not a commitment.

- Each task is doable in one day, ideally one sitting. Tighten to one hour if the user wants it.
- Test per task: "could I sit down and finish this today?" If no, it is a milestone. Split again.
- Give each task a one-line done-condition, verb-first, observable. Bad: "work on landing page." Good: "hero copy written and committed."
- One exception to exploding: if a milestone genuinely cannot be planned until an earlier one resolves, because its tasks depend on what the earlier one reveals, leave it coarse and say why. Writing tasks you cannot know yet is fiction.

### 4. Pick the single first action.

Surface one task to do today, not the whole tree. Choose a first task that produces a visible result fast. Momentum compounds. That first finished task is the 1% you bank today.

## Output format (Plan mode)

Use this exact structure. Markdown checkboxes so it drops cleanly into a notes app.

```
# [Goal, sharpened]
Done when: [observable condition]  ·  Deadline: [date or "none given"]

## Milestones
1. [milestone]  → [what it unblocks or proves]
2. [milestone]  → ...
(riskiest unknown ordered early)

## Tasks

### 1. [Milestone 1]
- [ ] [task]  → done when [condition]
- [ ] [task]  → done when [condition]

### 2. [Milestone 2]  (provisional, revisit on arrival)
- [ ] [task]  → done when [condition]
- [ ] ...

### 3. [Milestone 3]  (provisional)
- [ ] ...
[or, if it cannot be planned until milestone 2 resolves:]
Cannot detail yet. Depends on [what milestone 2 reveals]. Plan on arrival.

## Start here
[the single first task]. [one line on why it is first and the 1% it buys]
```

## Continue mode

When a plan is already running and a milestone is done, do not start over. Re-planning the next chunk against what you learned is the accurate move, not a chore.

- Keep the goal as-is unless it changed. Do not re-sharpen.
- Mark completed milestones done.
- Re-explode the next milestone from where you actually landed, not from its original provisional tasks. If reality diverged, the new tasks reflect reality.
- Leave the milestones after that as one-liners. They were exploded last time and get re-exploded when reached. Re-explode any on request.
- Surface the next single action.

Output:

```
# [Goal]  ·  [N of M milestones done]
Done when: [condition]

## Done
- [x] [milestone]

## Next: [milestone]
- [ ] [task]  → done when [condition]
- [ ] ...

## Later
[remaining milestones as one-liners, provisional. Re-plan each on arrival.]

## Start here
[next single task]. [why]
```

## Accountability

After the plan, add a short block. The user owns the decisions, so surface yours.

- **Assumptions** — anything guessed (deadline, scope, what done means). Name it so they can correct it.
- **Riskiest unknown** — the one thing most likely to break the plan, flagged.

Then ask where it goes:

`Keep in chat, or write to your Obsidian vault? If vault, new project note or append to an existing one?`

If they choose the vault, use the obsidian-vault tools to write a new note (or append) at the path they name.

## Style

- Output in the user's input language. If Czech, no diacritics.
- Blunt, directive, bullets. No semicolons, no em-dashes, no asterisks as decoration. Use arrows, periods, commas.
- No preamble. Plan first, accountability second.

## Example (Plan mode)

Input: "I want to ship a personal portfolio site."

Output:

```
# Portfolio site, live and shared
Done when: site deployed at a public URL, 3 projects up, link sent to 5 people  ·  Deadline: none given (suggest 3 weeks)

## Milestones
1. Content ready  → nothing to build without copy and write-ups
2. Site builds and deploys  → proves the riskiest unknown, that you can ship it live
3. Polish and launch  → make it shareable, then send it

## Tasks

### 1. Content ready
- [ ] Pick 3 projects to feature  → done when 3 are listed
- [ ] Write one paragraph per project  → done when 3 paragraphs drafted
- [ ] Write the about blurb  → done when 2 sentences exist
- [ ] Gather links and images  → done when each project has a link and one image

### 2. Site builds and deploys  (provisional, revisit on arrival)
- [ ] Pick a template or framework  → done when one runs locally
- [ ] Drop content into the layout  → done when all 3 projects render
- [ ] Deploy to a host  → done when the public URL loads

### 3. Polish and launch  (provisional)
- [ ] Check mobile and load speed  → done when it passes on a phone
- [ ] Proofread every line  → done when no typos remain
- [ ] Send the link to 5 people  → done when 5 messages are out

## Start here
Pick the 3 projects. It unblocks everything else and takes ten minutes. That is today's 1%.
```

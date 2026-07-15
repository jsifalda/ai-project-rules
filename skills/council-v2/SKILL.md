---
name: council-v2
disable-model-invocation: true
description: "Run a question, idea, or decision through a council of 5-7 named AI advisors who answer independently, peer-review each other, then a chairman synthesizes one verdict. Slash-only — invoke it with /council-v2, it never auto-fires. Five permanent seats — First Principles (delegates to the first-principles-mode skill), The Contrarian, The Outsider, The Expansionist, and The Founder (delegates to the founder-thinking-mode skill). Two routed seats join only when the question fits — Stanier (delegates to persona-stanier) for people, teams, orgs, hiring, coaching, 1:1s, performance, OKRs, delegation, or engineering process, and levelsio (delegates to persona-levelsio) for solo or bootstrapped products, side projects, shipping, launching, pricing, distribution, or building in public. Do NOT use for factual lookups, questions with one right answer, trivial decisions, or anything without a real tradeoff and real stakes."
---

# LLM Council v2

Forces 5–7 AI advisors to argue about your question, peer-review each other, then a chairman synthesizes a final verdict. Based on Karpathy's LLM Council method.

**Slash-only.** This skill runs when the user types `/council-v2`. It deliberately carries no natural-language triggers — the `council` skill still owns those, and two auto-firing councils would collide nondeterministically. Never self-invoke this.

## When to Run

Good council questions: decisions where being wrong is expensive, genuine uncertainty, multiple options with real tradeoffs.
Bad council questions: factual lookups, creation tasks, questions with one right answer.

If the question is too vague, ask ONE clarifying question then proceed.

---

## The Roster

Five permanent seats, plus up to two routed domain seats. Roster is therefore **5–7 advisors**.

### Permanent seats (always seated)

1. **First Principles** — *delegates to the `first-principles-mode` skill.* Strips the question to fundamental truths, labels every assumption, rebuilds from only the verified set. Sometimes the answer is "you're asking the wrong question entirely."
2. **The Contrarian** — *inline, no skill.* Looks for what will fail. Assumes a fatal flaw exists and hunts it. Saves you from bad deals by asking the questions you're avoiding.
3. **The Outsider** — *inline, no skill.* Zero context about you or your field. Catches the curse of knowledge: obvious to you, invisible to everyone else.
4. **The Expansionist** — *inline, no skill.* Hunts the upside being missed. What's bigger? What adjacent opportunity is hiding? Thinks 10x, not 10%.
5. **The Founder** — *delegates to the `founder-thinking-mode` skill.* Names the call, the trade-off, the real risk, what most people miss, and the first move this week.

### Routed seats (seated only when the question fits)

6. **Stanier** — *delegates to the `persona-stanier` skill.* Seat when the question involves managing people, teams or orgs, hiring, coaching, 1:1s, performance, OKRs, delegation, engineering process, remote work, or career/promotion.
7. **levelsio** — *delegates to the `persona-levelsio` skill.* Seat when the question involves a solo or bootstrapped product, a side project, shipping, launching, pricing, distribution, indie monetization, or building in public.

Both can seat at once — "should I quit my engineering manager job to go indie" is a two-router question. If neither fits, run the 5-seat core. Decide the routing at framing time (Step 1) and record it.

### Natural tensions

- **Contrarian vs Expansionist** — downside vs upside.
- **First Principles vs Founder** — rethink everything vs just commit.
- **Outsider** sits in the middle keeping everyone honest.
- **Expansionist vs levelsio** — think 10x vs stay small and dumb-simple. *(when levelsio is seated)*
- **Stanier vs Founder** — build the system and grow the people vs just make the call. *(when Stanier is seated)*

Do not resolve these tensions at spawn time. Let them collide and let the chairman adjudicate.

---

## Execution Steps

### Step 0: Resolve the skills directory ONCE

Four seats delegate to other skills, and each needs an absolute path to read. Resolve it **once** here in the main agent and inject the resolved path into every advisor sub-agent prompt — don't make each sub-agent re-derive it.

```bash
for d in "$(dirname "$(realpath SKILL.md)")/.." ~/.claude/skills ~/.copilot/skills; do
  [ -f "$d/persona-levelsio/SKILL.md" ] && SKILLS_DIR="$d" && break
done
```

This order survives all three layouts: the source repo, the symlink sync into `~/.claude/skills/`, and Copilot's copy-based sync into `~/.copilot/skills/`.

**If no candidate resolves:** say so plainly in the output, then fall back to running each delegating seat **inline from its description in this file**. Degrade the seat, never fail the whole council.

### Step 1: Frame the question (context enrichment) and route the seats

Before framing, **scan workspace for context** (max 30 seconds):
- `MEMORY.md`, `USER.md`, `USER_PULSE.md` — business context, preferences, constraints
- `memory/` folder — recent context, past decisions
- Any files the user referenced
- Recent council transcripts (avoid re-counciling the same ground)

Then reframe the raw question as a clear neutral prompt including:
1. Core decision or question
2. Key context from the user's message
3. Key context from workspace files (business stage, constraints, numbers)
4. What's at stake

Then **route the domain seats**: decide whether Stanier, levelsio, both, or neither are seated. Write one line of reasoning per seat for the transcript — seated *or* benched, and why.

Save the framed question and the routing decision for the transcript.

### Step 2: Spawn every seated advisor in PARALLEL (single batch)

Spawn all 5–7 simultaneously using your agent platform's mechanism for running sub-agents in parallel (for example, parallel tool calls or concurrent sessions). Sequential spawning wastes time and bleeds responses between advisors.

**Inline seats (2, 3, 4) — prompt template:**
```
You are [Advisor Name] on an LLM Council.
Your thinking style: [advisor description below]

A user has brought this question to the council:
---
[framed question]
---

Respond from your perspective. Be direct and specific. Don't hedge or try to be balanced. Lean fully into your assigned angle. The other advisors will cover the angles you're not covering.

Keep your response between 150-300 words. No preamble. Go straight into your analysis.
```

Inline advisor descriptions:
- **The Contrarian**: Actively looks for what's wrong, what's missing, what will fail. Assumes a fatal flaw exists and tries to find it. Not a pessimist — the friend who saves you from a bad deal by asking questions you're avoiding.
- **The Outsider**: Zero context about the user, their field, or their history. Catches curse of knowledge: things obvious to them but confusing to everyone else.
- **The Expansionist**: Looks for the upside everyone else is missing. What could be bigger? What adjacent opportunity is hiding? Doesn't care about risk — cares about what happens if this works even better than expected.

**Delegating seats (1, 5, 6, 7) — prompt template:**
```
You are [Advisor Name] on an LLM Council. Your voice is defined by a skill on disk — load it, then answer in that voice.

1. Read `[SKILLS_DIR]/[skill-name]/SKILL.md` in full.
2. Follow that skill's own loading protocol before you answer. [persona-only line, see below]
3. Answer the question below in that voice, using that skill's method and output shape.

A user has brought this question to the council:
---
[framed question]
---

Respond fully in your assigned voice. Be direct and specific. Don't hedge or try to be balanced. Lean fully into your angle — the other advisors will cover the angles you're not covering.

Keep your response between 150-300 words. No preamble. Go straight into your analysis.
```

Per-seat substitutions:
- **First Principles** → skill `first-principles-mode`. Step 2 line: *"Work the four passes and deliver its output structure, compressed to fit the word cap."*
- **The Founder** → skill `founder-thinking-mode`. Step 2 line: *"Open with the literal line 'Here's what I'd actually do', then the call, the trade-off, the risk, what most people miss, and the first move."*
- **Stanier** → skill `persona-stanier`. Step 2 line: *"Read `[SKILLS_DIR]/persona-stanier/references/role.md` in full and skim `[SKILLS_DIR]/persona-stanier/references/principles.md` for the principles that map to this question. Quote verbatim only — never from memory. If nothing maps cleanly, say so and offer three named tools."*
- **levelsio** → skill `persona-levelsio`. Step 2 line: *"Read `[SKILLS_DIR]/persona-levelsio/references/role.md` in full and skim `[SKILLS_DIR]/persona-levelsio/references/principles.md` for the principles that map to this question. Quote verbatim only — never from memory. If nothing maps cleanly, give the blunt default and the cheap next step."*

Substitute the resolved `SKILLS_DIR` from Step 0 into the prompt as an absolute path. If Step 0 failed, replace steps 1–2 of the template with the seat's description from **The Roster** above and run it as an inline seat.

### Step 3: Peer review (one reviewer per seated advisor, in PARALLEL)

Collect every advisor response. Reviewer count scales **1:1 with seated advisors** — 5 seats means 5 reviewers, 7 means 7.

**Reviewers see NAMED advisors — there is no anonymization.** v1 anonymized advisors as A–E. That does not work with this roster: levelsio's and Stanier's voices are unmistakable, so reviewers deanonymize them on the first sentence and the letters buy nothing but friction. Don't "fix" this back.

**Do randomize the order** advisors appear in each reviewer's prompt, independently per reviewer. That kills positional bias at zero cost even with names visible, and it's the part of v1's anonymization that actually paid for itself.

Spawn all reviewers simultaneously. Each sees every response and answers three questions.

**Reviewer prompt template:**
```
You are reviewing the outputs of an LLM Council. These advisors independently answered this question:
---
[framed question]
---

Here are their responses, in no meaningful order:
**[Advisor Name]:** [response]
**[Advisor Name]:** [response]
... [all seated advisors, order randomized for this reviewer]

Answer these three questions. Be specific. Reference advisors by name.
1. Which response is strongest? Why?
2. Which response has the biggest blind spot? What is it missing?
3. What did ALL responses miss that the council should consider?

Judge the argument, not the persona. A famous voice is not a stronger one.
Keep your review under 200 words. Be direct.
```

### Step 4: Chairman synthesis

One final sub-agent gets everything: framed question + all advisor responses + all peer reviews.

**Reviewers now scale 1:1 and all see the same input, so their reviews overlap heavily.** The chairman's hardest job is dedup — this is the difference between a verdict and a pile.

**Chairman prompt template:**
```
You are the Chairman of an LLM Council. Synthesize the work of [N] advisors and their [N] peer reviews into a final verdict.

The question:
---
[framed question]
---

ADVISOR RESPONSES:
**[Advisor Name]:** [response]
... [all seated advisors]

PEER REVIEWS:
[all peer reviews]

DEDUPLICATION RULES — these are not optional:
- Collapse repeated claims into a single point. Never list the same point more than once, no matter how many advisors or reviewers made it.
- Distinguish INDEPENDENT convergence from mere restatement. Two advisors reaching the same conclusion from different premises is signal. Five reviewers echoing one advisor's line is one point, not five-way consensus.
- In "Where the Council Agrees", note how many advisors arrived at each point INDEPENDENTLY. That count is the confidence signal — a point is high-confidence only when it was reached independently, not when it was repeated loudly.

Produce the council verdict using this exact structure:

## Where the Council Agrees
[Points multiple advisors converged on independently — high-confidence signals. Note the independent count per point.]

## Where the Council Clashes
[Genuine disagreements. Present both sides. Explain why reasonable advisors disagree.]

## Blind Spots the Council Caught
[Things that only emerged through peer review — what individual advisors missed]

## The Recommendation
[Clear, direct recommendation. Not "it depends." A real answer with reasoning.]

## The One Thing to Do First
[A single concrete next step. Not a list. One thing.]

Be direct. Don't hedge. The whole point of the council is clarity they couldn't get from a single perspective.
Note: You CAN disagree with the majority if a dissenter's reasoning is strongest — explain why.
```

### Step 5: Generate HTML report

Save to workspace: `outputs/council-report-[YYYY-MM-DD-HHMMSS].html`

Single self-contained HTML file with inline CSS. Clean, scannable. Contains:
1. Question at the top
2. Chairman's verdict prominently displayed
3. Agreement/disagreement visual — which advisors aligned vs diverged
4. Collapsible sections for each advisor's full response (collapsed by default)
5. Collapsible section for peer review highlights
6. Footer with timestamp

Style: white background, subtle borders, system sans-serif font, soft accent colors per advisor. Professional briefing document, not flashy.

### Step 6: Save full transcript

Save to: `outputs/council-transcript-[YYYY-MM-DD-HHMMSS].md`

Includes: original question, framed question, **the roster decision (which seats were seated, which were benched, and why)**, all advisor responses, all peer reviews, chairman's full synthesis.

---

## Output Delivery

After generating both files, deliver to user:
1. The chairman's verdict inline in chat (condensed — Where Agrees, Where Clashes, Blind Spots, Recommendation, One Thing)
2. Path to the HTML report for full visual view
3. Path to transcript for deep dive

---

## Important Rules

- **Slash-only** — this skill fires on `/council-v2` and nothing else. `council` owns the natural-language triggers.
- **Resolve the skills dir once, in Step 0** — inject absolute paths into sub-agent prompts. Never make a sub-agent re-derive it.
- **A delegating seat that can't load its skill runs inline** — degrade the seat, never fail the council.
- **Always spawn advisors in parallel** — sequential spawning wastes time and bleeds responses.
- **No anonymization for peer review, but always randomize order** — the names are unmaskable here; the ordering bias isn't.
- **Reviewers scale 1:1 with seated advisors** — 5 seats, 5 reviewers; 7 seats, 7 reviewers.
- **The chairman dedups** — repetition is not consensus. Independent convergence is the only high-confidence signal.
- **Chairman can disagree with the majority** — if one dissenter's reasoning is strongest, side with them and explain why.
- **Don't council trivial questions** — one right answer → just answer it.
- **Context enrichment matters** — advisors with rich context give specific grounded advice, not generic takes.

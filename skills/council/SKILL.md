---
name: council
description: "Run any question, idea, or decision through a council of 5 AI advisors who independently analyze it, peer-review each other anonymously, and synthesize a final verdict. Based on Karpathy's LLM Council methodology. MANDATORY TRIGGERS: 'council this', 'run the council', 'war room this', 'pressure-test this', 'stress-test this', 'debate this'. STRONG TRIGGERS (use when combined with a real decision or tradeoff): 'should I X or Y', 'which option', 'what would you do', 'is this the right move', 'validate this', 'get multiple perspectives', 'I can't decide', 'I'm torn between'. Do NOT trigger on simple yes/no questions, factual lookups, or casual 'should I' without a meaningful tradeoff. DO trigger when the user presents a genuine decision with stakes, multiple options, and context that suggests they want it pressure-tested from multiple angles."
---

# LLM Council

Forces 5 AI advisors to argue about your question, anonymously peer-review each other, then a chairman synthesizes a final verdict. Based on Karpathy's LLM Council method.

## When to Run

Good council questions: decisions where being wrong is expensive, genuine uncertainty, multiple options with real tradeoffs.
Bad council questions: factual lookups, creation tasks, questions with one right answer.

If question is too vague, ask ONE clarifying question then proceed.

---

## The Five Advisors

1. **The Contrarian** — Looks for what will fail. Assumes fatal flaw. Saves you from bad deals by asking questions you're avoiding.
2. **The First Principles Thinker** — Ignores surface question, asks what you're actually solving. Strips assumptions, rebuilds from zero.
3. **The Expansionist** — Hunts for upside being missed. What's bigger? What adjacent opportunity is hiding? Thinks 10x not 10%.
4. **The Outsider** — Zero context about you or your field. Catches curse of knowledge: obvious to you, invisible to everyone else.
5. **The Executor** — Only cares: what do you do Monday morning? Flags brilliant plans with no path to execution.

**Three natural tensions:** Contrarian vs Expansionist (downside vs upside). First Principles vs Executor (rethink everything vs just do it). Outsider sits in the middle keeping everyone honest.

---

## Execution Steps

### Step 1: Frame the question (context enrichment)

Before framing, **scan workspace for context** (max 30 seconds):
- `MEMORY.md`, `USER.md`, `USER_PULSE.md` — business context, preferences, constraints
- `memory/` folder — recent context, past decisions
- Any files user referenced
- Recent council transcripts (avoid re-counciling same ground)

Then reframe the raw question as a clear neutral prompt including:
1. Core decision or question
2. Key context from user's message
3. Key context from workspace files (business stage, constraints, numbers)
4. What's at stake

Save framed question for transcript.

### Step 2: Spawn 5 advisors in PARALLEL (single batch)

Spawn all 5 simultaneously using your agent platform's supported mechanism for running multiple sub-agents in parallel (for example, parallel tool calls or concurrent sessions). Each gets their identity + the framed question.

**Sub-agent prompt template:**
```
You are [Advisor Name] on an LLM Council.
Your thinking style: [advisor description]

A user has brought this question to the council:
---
[framed question]
---

Respond from your perspective. Be direct and specific. Don't hedge or try to be balanced. Lean fully into your assigned angle. The other advisors will cover the angles you're not covering.

Keep your response between 150-300 words. No preamble. Go straight into your analysis.
```

Advisor descriptions to include:
- **Contrarian**: Actively looks for what's wrong, what's missing, what will fail. Assumes fatal flaw exists and tries to find it. Not a pessimist — the friend who saves you from a bad deal by asking questions you're avoiding.
- **First Principles Thinker**: Ignores surface-level question, asks "what are we actually trying to solve?" Strips assumptions. Rebuilds from ground up. Most valuable output is sometimes "you're asking the wrong question entirely."
- **Expansionist**: Looks for upside everyone else is missing. What could be bigger? What adjacent opportunity is hiding? Doesn't care about risk — cares about what happens if this works even better than expected.
- **Outsider**: Zero context about you, your field, or your history. Catches curse of knowledge: things obvious to you but confusing to everyone else.
- **Executor**: Can this actually be done, and what's the fastest path? Ignores theory. Every idea through the lens of "what do you do Monday morning?" If brilliant plan has no clear first step, says so.

### Step 3: Peer review (5 sub-agents in PARALLEL)

Collect all 5 advisor responses. **Anonymize as A–E** (randomize mapping to prevent positional bias).

Spawn 5 reviewer sub-agents simultaneously. Each sees all 5 anonymized responses and answers:
1. Which response is strongest and why? (pick one)
2. Which has the biggest blind spot and what is it?
3. What did ALL responses miss that the council should consider?

**Reviewer prompt template:**
```
You are reviewing the outputs of an LLM Council. Five advisors independently answered this question:
---
[framed question]
---

Here are their anonymized responses:
**Response A:** [response]
**Response B:** [response]
**Response C:** [response]
**Response D:** [response]
**Response E:** [response]

Answer these three questions. Be specific. Reference responses by letter.
1. Which response is strongest? Why?
2. Which response has the biggest blind spot? What is it missing?
3. What did ALL five responses miss that the council should consider?

Keep your review under 200 words. Be direct.
```

### Step 4: Chairman synthesis

One final sub-agent gets everything: framed question + all 5 advisor responses (de-anonymized) + all 5 peer reviews.

**Chairman prompt template:**
```
You are the Chairman of an LLM Council. Synthesize the work of 5 advisors and their peer reviews into a final verdict.

The question:
---
[framed question]
---

ADVISOR RESPONSES:
**The Contrarian:** [response]
**The First Principles Thinker:** [response]
**The Expansionist:** [response]
**The Outsider:** [response]
**The Executor:** [response]

PEER REVIEWS:
[all 5 peer reviews]

Produce the council verdict using this exact structure:

## Where the Council Agrees
[Points multiple advisors converged on independently — high-confidence signals]

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

Includes: original question, framed question, all 5 advisor responses, all 5 peer reviews (with anonymization mapping revealed), chairman's full synthesis.

---

## Output Delivery

After generating both files, deliver to user:
1. The chairman's verdict inline in chat (condensed — Where Agrees, Where Clashes, Blind Spots, Recommendation, One Thing)
2. Path to the HTML report for full visual view
3. Path to transcript for deep dive

---

## Important Rules

- **Always spawn all 5 advisors in parallel** — sequential spawning wastes time and bleeds responses
- **Always anonymize for peer review** — prevents deference to certain thinking styles
- **Chairman can disagree with majority** — if 1 dissenter's reasoning is strongest, side with them and explain why
- **Don't council trivial questions** — one right answer → just answer it
- **Context enrichment matters** — advisors with rich context give specific grounded advice, not generic takes

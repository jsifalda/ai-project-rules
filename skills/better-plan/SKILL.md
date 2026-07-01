---
name: better-plan
description: Chained planning workflow, one pass from a raw request to a hardened, cost-routed plan. First it sharpens your request via the prompt-enhancer skill. Then it builds a thorough implementation plan with plan-mode rigor (explore, design, draft). Then it stress-tests the plan via the grill-me skill, a relentless interview that resolves each decision branch and revises the plan. Then it routes the refined plan through the op skill, assigning each task the cheapest capable model and mapping dependencies. It presents the final routed plan and, once you approve, lets op dispatch the subagents and verify. It closes with a recap of the original and enhanced prompts and what each stage did. Slash-only. Use when you type /better-plan and want a plan enhanced, hardened, and cost-routed in one go. Do NOT use for a quick one-off plan with no review, to only grill an existing plan, or to only route an existing plan.
disable-model-invocation: true
---

# Better Plan — build, grill, route, in one pass

Turn a request into a plan that has been stress-tested and cost-routed before any
code is written. Run the preface, then four stages, then the recap, in order. Do not
skip any. Stop and surface a blocker rather than guessing.

## Preface — Enhance the request

Before planning, sharpen the raw request you were given.

1. Take the text passed to /better-plan verbatim as the input prompt. If none was
   given, ask the user for the request and stop here until you have it.
2. Invoke the **prompt-enhancer** skill on that text to produce a clearer, structured
   version of the request. It only restructures — it asks no clarifying questions.
3. Show the user the enhanced request in a few lines, noting what it sharpened.
4. Use the enhanced request as the input to Stage 1. If it drifts from intent, the
   user can correct it now or during the Stage 2 grill.

## Stage 1 — Build the initial plan (plan-mode rigor)

Produce a thorough implementation plan for the enhanced request from the preface, with
the same rigor plan mode uses:

1. Explore the codebase first. Find existing functions, utilities, and patterns to
   reuse before proposing new code. Use read-only search; do not edit anything yet.
2. Design the approach. Name the files to change, the pattern to follow, and the
   verification method. Prefer the smallest change that solves the real problem.
3. Draft the plan. If a plan file already exists for this session, write the draft
   there; otherwise hold the draft in context. This draft is the input to Stage 2.

If the request is too vague to plan, ask the user before continuing.

## Stage 2 — Grill the plan, then revise

Invoke the **grill-me** skill against the Stage 1 draft. Interview the user
relentlessly, walking each branch of the decision tree and resolving dependencies
between decisions one at a time. For every question, give your recommended answer.
Answer from the codebase whenever exploring can settle a question.

When the interview reaches shared understanding, fold the answers back into the plan.
The revised plan is the input to Stage 3. Briefly note what changed versus the draft.

## Stage 3 — Route the plan across models

Invoke the **op** skill on the revised plan. Decompose it into discrete,
independently-dispatchable tasks, classify each to the cheapest capable model
(Haiku / Sonnet / Opus), map dependencies, and present the annotated plan table with a
one-line cost and parallelism summary. This routed plan is the final plan.

## Stage 4 — Present, then execute on approval

Present the final routed plan to the user as the output of this skill.

- If running inside plan mode, call ExitPlanMode to request approval. Approval there
  is the go signal.
- If not in plan mode, ask the user to approve before any dispatch.

On approval, hand back to **op** to execute: dispatch each task to a subagent on its
assigned model per op's dispatch rules, then integrate and run op's model-verification
step. Keep orchestration, integration, and final verification on Opus. Report what each
subagent did and on which model.

If the user only wants the routed plan and not execution, stop after presenting it.

## Recap — Explain the run

After the final plan is presented (and after execution, if the user approved it),
close with a short recap so the run is transparent:

- The original text passed to /better-plan.
- The enhanced request prompt-enhancer produced, and what it sharpened.
- One line per stage — how the plan was built, what the grill changed, how it was
  routed, and what executed (if anything).

Keep it to a few lines. This recap is the last thing the skill outputs.

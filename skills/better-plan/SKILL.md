---
name: better-plan
description: Chained planning workflow that runs three stages in one pass. First it builds a thorough implementation plan with plan-mode rigor (explore, design, draft). Then it stress-tests the plan by delegating to the grill-me skill, a relentless interview that resolves each decision branch and revises the plan. Then it routes the refined plan through the op skill, assigning each task the cheapest capable model, mapping dependencies, and annotating. It presents the final routed plan and, once you approve, lets op dispatch the subagents and verify. Slash-only. Use when you type /better-plan and want a plan hardened and cost-routed in one go. Do NOT use for a quick one-off plan with no review, to only grill an existing plan, or to only route an existing plan.
disable-model-invocation: true
---

# Better Plan — build, grill, route, in one pass

Turn a request into a plan that has been stress-tested and cost-routed before any
code is written. Run four stages in order. Do not skip a stage. Stop and surface a
blocker rather than guessing.

## Stage 1 — Build the initial plan (plan-mode rigor)

Produce a thorough implementation plan for the user's request, with the same rigor
plan mode uses:

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

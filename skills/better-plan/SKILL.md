---
name: better-plan
description: Chained planning workflow, one pass from a raw request to a hardened, cost-routed plan. First it sharpens your request via the prompt-enhancer skill. Then it builds a thorough implementation plan with plan-mode rigor (explore, design, draft). Then it stress-tests the plan via the grill-me skill, a relentless interview that resolves each decision branch and revises the plan. Then it routes the refined plan through the op skill, assigning each task the cheapest capable model and mapping dependencies. It runs in plan mode, so the routed plan lands in a plan file you approve before op dispatches the subagents. It recaps the run, then by default ships the result as a PR via ship-pr, once execution is verified and nothing awaits you. Slash-only. Use when you type /better-plan and want a plan enhanced, hardened, cost-routed, and shipped. Do NOT use for a quick one-off plan with no review, to only grill an existing plan, or to only route an existing plan.
disable-model-invocation: true
---

# Better Plan — build, grill, route, in one pass

Turn a request into a plan that has been stress-tested and cost-routed before any
code is written, then ship the result. Run the preface, then every stage, in order.
Stages 1-4 are mandatory and none may be skipped. Stage 5 is conditional — it ships only
when its own gate passes, and skips cleanly when it does not. Stop and surface a blocker
rather than guessing.

## Preface — Enter plan mode, then enhance the request

Set up the plan file, then sharpen the raw request you were given.

1. **Enter plan mode first.** Call `EnterPlanMode` before anything else. It keeps
   Stages 1-3 read-only by construction and hands over a plan file, which is where the
   plan lives from Stage 1 until approval.
   - Already in plan mode → skip this step, the harness already named a plan file.
   - No plan-mode tool (agents other than Claude Code), or the user declines the
     prompt → continue without it and use the Stage 4 fallback gate.
2. Take the text passed to /better-plan verbatim as the input prompt. If none was
   given, ask the user for the request and stop here until you have it.
3. Invoke the **prompt-enhancer** skill on that text to produce a clearer, structured
   version of the request. It only restructures, it asks no clarifying questions.
4. Show the user the enhanced request in a few lines, noting what it sharpened.
5. Use the enhanced request as the input to Stage 1. If it drifts from intent, the
   user can correct it now or during the Stage 2 grill.

## Plan mode ground rules

Plan mode injects its own workflow guidance (explore, design, write the plan file, call
`ExitPlanMode`). That guidance covers **Stage 1 only**. It is not this skill.

- Do not call `ExitPlanMode` before Stage 3's routing table is in the plan file. Exiting
  after Stage 1 skips the grill and the routing, which is the whole point of this skill.
- The plan file is the single artifact. Every stage edits that same file in place. Never
  open a second one.
- **grill-me** asks through `AskUserQuestion`, which plan mode allows, so Stage 2 needs
  no exception.

## Stage 1 — Build the initial plan (plan-mode rigor)

Produce a thorough implementation plan for the enhanced request from the preface, with
the same rigor plan mode uses:

1. Explore the codebase first. Find existing functions, utilities, and patterns to
   reuse before proposing new code. Use read-only search; do not edit anything yet.
2. Design the approach. Name the files to change, the pattern to follow, and the
   verification method. Prefer the smallest change that solves the real problem.
3. Draft the plan into the plan file the harness named for this session. Without plan
   mode, hold the draft in context instead. This draft is the input to Stage 2.

If the request is too vague to plan, ask the user before continuing.

## Stage 2 — Grill the plan, then revise

Invoke the **grill-me** skill against the Stage 1 draft. Interview the user
relentlessly, walking each branch of the decision tree and resolving dependencies
between decisions one at a time. For every question, give your recommended answer.
Answer from the codebase whenever exploring can settle a question.

When the interview reaches shared understanding, fold the answers back into the plan by
editing the plan file in place. The revised plan is the input to Stage 3. Briefly note
what changed versus the draft.

## Stage 3 — Route the plan across models

Invoke the **op** skill on the revised plan. Decompose it into discrete,
independently-dispatchable tasks, classify each to the cheapest capable model
(Haiku / Sonnet / Opus), map dependencies, and present the annotated plan table with a
one-line cost and parallelism summary. This routed plan is the final plan.

Write the annotated table into the plan file, so what the user approves is the routed
plan and not just chat output.

## Stage 4 — Present, then execute on approval

The plan file now holds the final routed plan. Present it for approval.

- **In plan mode (the default path).** Check the file holds the Stage 3 routing table and
  the verification method, append the Recap section below to it, then call
  `ExitPlanMode`. That approval is the go signal. Do not ask for approval in chat as
  well. Nothing goes into the plan file after the exit call.
- **Without plan mode (fallback).** Print the routed plan and ask the user to approve
  before any dispatch.

On approval, hand back to **op** to execute: dispatch each task to a subagent on its
assigned model per op's dispatch rules, then integrate and run op's model-verification
step. Keep orchestration, integration, and final verification on Opus. Report what each
subagent did and on which model.

If the user only wants the routed plan and not execution, stop after presenting it.

## Stage 5 — Ship the work (default)

Once execution is done, open a PR for it. This is the last thing the flow does — nothing
follows the ship report, not even the recap.

Ship when **every one** of these holds:

- Every routed task from Stage 3 actually executed.
- Verification is green — op's model-verification step, plus whatever gates the project
  defines for itself.
- No question is still outstanding to the user.
- No finding or decision is sitting in the user's queue awaiting triage.

All true → invoke the **ship-pr** skill. Pass it nothing. It reads the diff and
derives the branch, commit message, and PR body on its own. Do not ask permission first —
the Stage 4 approval covers the ship, and a second gate here just re-asks a settled
question. Report ship-pr's own Phase 6 block verbatim and stop.

If ship-pr aborts before Phase 6 — no `origin` remote, an unauthenticated `gh` or `glab`,
an unsupported remote host, a suspected secret in the diff, a failing pre-commit hook —
report its one-line reason and stop there. Do not route around it, and do not commit or
push by hand instead. The work stays local and the user decides what to do next.

Any one false → do not ship. Name the condition that blocked it in a single line, so the
user can clear it and run `/ship-pr` themselves. A blocked ship is not a failed run.

Skip Stage 5 entirely, without treating it as blocked, when:

- The user wanted the routed plan only, so nothing executed.
- The user said not to open a PR.
- Execution changed no files. ship-pr aborts on a clean tree anyway (`no changes to
  commit`), so calling it would only produce a confusing error.

## Recap — Explain the run

Make the run transparent. In plan mode the recap has to be readable at approval time, so
it closes the plan file as a short "How this plan was built" section, written in Stage 4
just before `ExitPlanMode` rather than after it:

- The original text passed to /better-plan.
- The enhanced request prompt-enhancer produced, and what it sharpened.
- One line per stage, covering how the plan was built, what the grill changed, and how it
  was routed.

Keep it to a few lines. Without plan mode, print the same recap in chat after Stage 4's
execution report and before Stage 5 ships — the ship report is always last. What executed
after approval is reported in Stage 4, not here.

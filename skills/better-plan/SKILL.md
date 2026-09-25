---
name: better-plan
description: Chained planning workflow, one pass from a raw request to a hardened, cost-routed plan. First it sharpens your request via the prompt-enhancer skill. Then it builds a thorough implementation plan with plan-mode rigor. Then it stress-tests the plan via the grill-me skill, a relentless interview that resolves each decision branch and revises the plan. Then it routes each task to the cheapest capable model via the op skill, Sonnet by default, and the session model only orchestrates. Pass --inline to skip the routing and execute in the session. It runs in plan mode, so the final plan lands in a plan file you approve before anything executes. By default it ships the result as a PR via ship-pr, once execution is verified. Use when the user types /better-plan, or asks to plan, grill, model-route, and ship a change in one pass. Do NOT use for a quick one-off plan with no review, to only grill an existing plan, or to only route an existing plan.
metadata:
  version: "1.0"
---

# Better Plan — build, grill, route, execute, in one pass

Turn a request into a plan that has been stress-tested and cost-routed before any
code is written, then ship the result. Run the preface, then every stage, in order.
Stages 1, 1b, 2 and 3 are mandatory and none may be skipped, unless Stage 1b's abort gate fires — that
ends the run before Stage 2. Stage 2b runs only when the execution mode is routed. Stage 4 is
conditional — it ships only when its own gate passes, and skips cleanly when it does not.
Stop and surface a blocker rather than guessing.

## Preface — Enter plan mode, then enhance the request

Set up the plan file, then sharpen the raw request you were given.

1. **Enter plan mode first.** Call `EnterPlanMode` before anything else. It keeps
   Stages 1-2b read-only by construction and hands over a plan file, which is where the
   plan lives from Stage 1 until approval.
   - Already in plan mode → skip this step, the harness already named a plan file.
   - No plan-mode tool (agents other than Claude Code), or the user declines the
     prompt → continue without it and use the Stage 3 fallback gate.
2. Take the text passed to /better-plan as the input prompt. When the skill loads without that
   text, use the user's request that triggered it. Set the execution mode first.
   The flag `--inline`, as its own word at the start or the end of the text, sets the mode to
   inline. The same word inside the request is part of the request, not the flag. A plain-language form
   such as "execute inline" or "no subagents" also sets it to inline. No flag and no such
   phrase sets the mode to routed. Remove the flag and the phrase from the text before the
   enhancer sees it. Record `Execution: routed` or `Execution: inline` as the first line of
   the plan. In plan mode, that is the first line of the plan file once the harness names it.
   Without plan mode, it is the first line of the draft you hold in context. If no text
   remains, ask the user for the request and stop here until you have it.
3. Invoke the **prompt-enhancer** skill on that text to produce a clearer, structured
   version of the request. It only restructures, it asks no clarifying questions.
4. Show the user the enhanced request in a few lines, noting what it sharpened.
5. Use the enhanced request as the input to Stage 1. If it drifts from intent, the
   user can correct it now or during the Stage 2 grill.

## Plan mode ground rules

Plan mode injects its own workflow guidance (explore, design, write the plan file, call
`ExitPlanMode`). That guidance covers **Stage 1 only**. It is not this skill.

- Do not call `ExitPlanMode` before Stage 2's revised plan is in the plan file. When the
  mode is routed, the Stage 2b routing table must be in the file too. Exiting after Stage 1
  skips the grill and the routing, which is the whole point of this skill.
- The plan file is the single artifact. Every stage edits that same file in place. Never
  open a second one.
- **grill-me** asks in chat text and writes nothing, so plan mode allows Stage 2 with no
  exception.

## Stage 1 — Build the initial plan (plan-mode rigor)

Produce a thorough implementation plan for the enhanced request from the preface, with
the same rigor plan mode uses:

1. Explore the codebase first. Find existing functions, utilities, and patterns to
   reuse before proposing new code. Use read-only search; do not edit anything yet.
2. Design the approach. Name the files to change, the pattern to follow, and the
   verification method. Prefer the smallest change that solves the real problem.
3. Draft the plan into the plan file the harness named for this session. Keep the
   `Execution:` line as the first line of the file. Without plan mode, hold the draft in
   context instead, with the `Execution:` line first. This draft is the input to Stage 2.

If the request is too vague to plan, ask the user before continuing.

## Stage 1b — Abort gate: does this need a change at all?

Run this the moment Stage 1 has settled what the request really needs, and before Stage 2.

If what you found needs no code change — a stale cache, a restart, a setting, a user
action, or a bug that does not reproduce — STOP the whole flow. Report the finding and the
remedy in one short reply. Do not run the grill, the routing, or the ship.

A plan is a deliverable only when work must happen. Producing one for a problem that needs no
work is the failure this gate exists to prevent.

The gate binds hardest when you have already spent many tool calls. A one-line answer after a
long investigation is a good outcome, not a thin one. Never let the cost of the search set the
size of the deliverable.

## Stage 2 — Grill the plan, then revise

Invoke the **grill-me** skill against the Stage 1 draft. Interview the user
relentlessly, working the design tree in rounds and asking every unblocked question
in each round. For every question, give your recommended answer.
Answer from the codebase whenever exploring can settle a question.

When the interview reaches shared understanding, fold the answers back into the plan by
editing the plan file in place. The revised plan is the input to Stage 2b, or the final
plan when the mode is inline. Briefly note what changed versus the draft.

## Stage 2b — Route the plan across models

Skip this stage when the execution mode is inline. The revised plan is then the
final plan.

Invoke the **op** skill on the revised plan, steps 1 to 4 of its workflow, then write the
table in op's `## Annotated-plan output format`. Decompose the plan into discrete,
independently-dispatchable tasks. Classify each task to the cheapest model that does it well
per op's rubric. Sonnet is the default. Haiku takes pure chores. Opus takes deep reasoning.
The session model never runs a routed task, whatever its tier. On an Opus session, an
opus-tier task still goes to an `opus` subagent. Map dependencies, then write the annotated
table with its one-line cost and parallelism summary into the plan file.
Do not ask for approval here. Stage 3 owns the approval. This routed plan is the final plan,
so what the user approves is the routed plan and not chat output.

## Stage 3 — Present, then execute on approval

The plan file now holds the final plan. Present it for approval.

- **In plan mode (the default path).** Check the file holds the verification method, and the
  Stage 2b routing table when the mode is routed, then call `ExitPlanMode`. That approval is
  the go signal. Do not ask for approval in chat as well. Nothing goes into the plan file
  after the exit call.
- **Without plan mode (fallback).** Print the plan and ask the user to approve before any
  edit or dispatch.

On approval, execute per the recorded execution mode:

- **Routed (default).** Hand back to **op**, steps 6 and 7. Dispatch each task to a subagent
  on its assigned model per op's dispatch rules, never inline. Integrate on the session
  model, run the plan's own verification plus whatever gates the project defines for itself,
  then run op's model-verification script. Report what each subagent did and on which model.
- **Inline.** Execute the plan in order, in this session. Run the plan's own
  verification plus whatever gates the project defines for itself. Report what changed.

If the user only wants the plan and not execution, stop after presenting it.

## Stage 4 — Ship the work (default)

Once execution is done, open a PR for it. This is the last thing the flow does — nothing
follows the ship report.

Ship when **every one** of these holds:

- The plan executed in full.
- When the mode is routed, every task in the routing table ran as a dispatched subagent.
  None ran inline. The evidence is op's model-verification report: its per-dispatch table
  shows one row with a requested tier for each row of the routing table. The bare
  `Dispatches:` count is not evidence, because it also counts agents spawned with no `model`.
- Verification is green — the plan's own verification, op's model-verification step when
  the mode is routed, plus whatever gates the project defines for itself.
- No question is still outstanding to the user.
- No finding or decision is sitting in the user's queue awaiting triage.

All true → invoke the **ship-pr** skill. Pass it nothing. It derives the branch, commit
message, and PR body from the work this session did. Do not ask permission first —
the Stage 3 approval covers the ship, and a second gate here just re-asks a settled
question. Report ship-pr's own Phase 4 block verbatim and stop.

If ship-pr aborts before Phase 4 — no `origin` remote, a missing `gh` or `glab`,
an unsupported remote host, a suspected secret in the diff, a failing pre-commit hook —
report its one-line reason and stop there. When the abort carries tool output — a pre-commit
hook or a push failure — pass that output through verbatim as well; ship-pr never swallows it,
and neither do you. Do not route around it, and do not commit or push by hand instead. The work
stays local and the user decides what to do next.

Any one false → do not ship. Name the condition that blocked it in a single line, so the
user can clear it and run `/ship-pr` themselves. A blocked ship is not a failed run.

Skip Stage 4 entirely, without treating it as blocked, when:

- The user wanted the plan only, so nothing executed.
- The user said not to open a PR.
- Execution changed no files. Nothing of this run's exists to ship, and any older commit on
  the branch is not this run's to publish.

---
name: op
description: Route the tasks in an implementation plan to the most cost-effective Claude model that can do each one well, then execute the plan by dispatching tasks as subagents on their assigned model. Even when Claude Code runs on Opus, mechanical tasks go to Haiku and mid-complexity tasks to Sonnet, while only deep-reasoning tasks stay on Opus. Use when the user types /op, or asks to route a plan across models, assign per-task models, split a plan by model, run a plan cheaply, or execute plan tasks on different models. Expects a plan already in context (from plan mode) or pasted by the user. Do NOT use to write the plan itself, for a single one-off task with no plan, or to change Claude Code's global model setting.
---

# Op — per-task model routing for a plan

Take an implementation plan, assign each task the cheapest Claude model that can do it well, show the annotated plan, then execute it by dispatching each task to a subagent running on its assigned model.

## Why this exists

Claude Code runs one model for the whole session. If that model is Opus, every task pays Opus cost and latency, even renaming a symbol or updating a changelog. Most plans are a mix: a few hard tasks that need deep reasoning, and many mechanical ones a smaller model does just as well, faster and cheaper.

This generalizes Claude Code's built-in `opusplan` setting (Opus to plan, Sonnet to execute) into per-task routing: Opus plans, then each task runs on Haiku, Sonnet, or Opus based on what the task actually needs.

## The mechanism (the one non-obvious fact)

Claude Code's Agent tool takes a `model` parameter. A subagent spawned with `model: "haiku"` runs on Haiku even though the main session runs on Opus. Verified: dispatching `haiku` / `sonnet` / `opus` yields subagents reporting `claude-haiku-4-5`, `claude-sonnet-4-6`, `claude-opus-4-8` respectively.

So "run this task on a different model" = spawn it as a subagent with the chosen `model`. The main loop (Opus) stays the orchestrator. Available tiers: `haiku`, `sonnet`, `opus`, `fable`.

## Workflow

1. **Get the plan.** Use the plan already in context (the most recent plan-mode output), or the plan the user pasted or pointed to. If there is no plan, stop and ask for one. Do not invent a plan.
2. **Decompose into tasks.** Break the plan into discrete, independently-dispatchable units. Each task needs a clear deliverable and an acceptance check. Split any task too big or too vague to hand to one subagent.
3. **Classify each task to a model.** Apply the rubric below. When a task sits between two tiers, pick the lower one and note the risk. Full rubric, signals, and worked examples: read [references/model-routing.md](references/model-routing.md).
4. **Map dependencies.** Mark each task independent (no unfinished task feeds it) or dependent (needs another task's output first). Independent tasks run in parallel, dependents run after their inputs land.
5. **Present the annotated plan.** Show the table (format below) with model, reason, and dependencies per task, plus a one-line cost/parallelism summary. Get the user's approval before executing. If the user only wanted the routed plan, stop here.
6. **Execute by dispatch.** Spawn each task as a subagent via the Agent tool with its assigned `model`. Fire all ready independent tasks in one message so they run concurrently. Hold dependents until their inputs finish, then dispatch them with those results in the prompt.
7. **Integrate and verify.** The main loop collects results, resolves conflicts between parallel edits, and runs the plan's verification. Keep integration and final verification on the orchestrator (Opus), not a small model.

## Model rubric (summary)

| Model | Use for | Signal |
|---|---|---|
| **haiku** | Mechanical, well-specified, low-ambiguity, narrow blast radius | "Anyone could do this from the spec" |
| **sonnet** | Moderate logic and judgment, single-component features, clear bug fixes, in-module refactors | "Needs thought, but the path is clear" |
| **opus** | Deep reasoning, architecture, cross-cutting or ambiguous changes, tricky algorithms, unknown-root-cause debugging, security-sensitive work | "A wrong call here is expensive" |

When unsure between two tiers, drop one tier and flag it. Orchestration, integration, and final verification stay on Opus. Full examples and edge cases are in the reference file.

## Dispatch rules

- **Subagents are isolated.** They do not see this conversation. Each prompt must be self-contained: the files to touch, the exact change, constraints, and the acceptance check. Missing context is the top failure mode.
- **Parallel = one message, many Agent calls.** Put every ready independent task in a single response so they run at once. A dependent task waits for its inputs, then its prompt includes those results.
- **Use a coding-capable subagent type** (e.g. `general-purpose`) for tasks that edit files, since they need Edit/Write. Use a read-only type for pure research tasks.
- **Avoid parallel edits to the same file.** If two independent tasks touch one file, either serialize them or merge them into one task to prevent clobbering.
- **Keep the orchestrator on Opus.** Routing decisions, conflict resolution, and the final verification pass are themselves Opus-tier work. Do not dispatch them to a small model.

## Annotated-plan output format

```
## Routed plan: <plan title>

| # | Task | Model | Why | Depends on |
|---|------|-------|-----|------------|
| 1 | <task>        | haiku  | <one line> | —     |
| 2 | <task>        | sonnet | <one line> | —     |
| 3 | <task>        | opus   | <one line> | 1, 2  |

Parallel batches: [1, 2] then [3]
Routing: 1 opus, 1 sonnet, 1 haiku (vs 3 opus by default)
```

After approval, execute per the dispatch rules and report what each subagent did and on which model.

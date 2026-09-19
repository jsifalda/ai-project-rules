---
name: op
description: Route the tasks in an implementation plan to the most cost-effective Claude model that can do each one well, then execute the plan by dispatching tasks as subagents on their assigned model. The session model only orchestrates, pure chores go to Haiku, most tasks go to Sonnet, and only deep-reasoning tasks go to Opus. Use when the user types /op, or asks to route a plan across models, assign per-task models, split a plan by model, run a plan cheaply, or execute plan tasks on different models. Expects a plan already in context (from plan mode) or pasted by the user. Do NOT use to write the plan itself, for a single one-off task with no plan, or to change Claude Code's global model setting.
---

# Op — per-task model routing for a plan

Take an implementation plan, assign each task the cheapest Claude model that can do it well, show the annotated plan, then execute it by dispatching each task to a subagent running on its assigned model.

## Why this exists

Claude Code runs one model for the whole session. If that model is Fable or Opus, every task pays that model's cost and latency, even renaming a symbol or updating a changelog. Most plans are a mix: a few hard tasks that need deep reasoning, and many mechanical ones a smaller model does just as well, faster and cheaper.

This generalizes Claude Code's built-in `opusplan` setting (Opus to plan, Sonnet to execute) into per-task routing: each task runs on Haiku, Sonnet, or Opus based on what the task actually needs, and the session model only orchestrates.

## The mechanism (the one non-obvious fact)

Claude Code's Agent tool takes a `model` parameter. A subagent spawned with `model: "haiku"` runs on Haiku even though the main session runs on another model. `haiku`, `sonnet`, `opus`, and `fable` are tier aliases, not dated model IDs — the harness resolves each alias to Anthropic's current, highest release for that tier. A dispatched subagent's `resolvedModel` contains its requested tier name as a substring, so requesting `sonnet` produces a `resolvedModel` containing `sonnet`. That substring is what `scripts/verify-models.py` checks.

So "run this task on a different model" = spawn it as a subagent with the chosen `model`. The main loop, on the session model, stays the orchestrator whatever its tier. Workers run on `haiku`, `sonnet`, or `opus`. Never auto-route to `fable`. Take it only when the user names it for a task.

## Workflow

1. **Get the plan.** Use the plan already in context (the most recent plan-mode output), or the plan the user pasted or pointed to. If there is no plan, stop and ask for one. Do not invent a plan.
2. **Decompose into tasks.** Break the plan into discrete, independently-dispatchable units. Each task needs a clear deliverable and an acceptance check. Split any task too big or too vague to hand to one subagent.
3. **Classify each task to a model.** Apply the rubric below, tie-breaker included. Full rubric, signals, and worked examples: read [references/model-routing.md](references/model-routing.md).
4. **Map dependencies.** Mark each task independent (no unfinished task feeds it) or dependent (needs another task's output first). Independent tasks run in parallel, dependents run after their inputs land.
5. **Present the annotated plan.** Show the table (format below) with model, reason, and dependencies per task, plus a one-line cost/parallelism summary. Get the user's approval before executing. If the user only wanted the routed plan, stop here.
6. **Execute by dispatch.** Spawn each task as a subagent via the Agent tool with its assigned `model`. Follow the dispatch rules below for batching and dependents.
7. **Integrate and verify.** The main loop collects results, resolves conflicts between parallel edits, and runs the plan's verification. Keep integration and final verification on the orchestrator (the session model), not a small model.

   After all dispatches resolve, verify that each subagent actually ran on its assigned model tier. The orchestrator cannot see each subagent's `resolvedModel` from its own in-context tool results. That ground truth is written to the session transcript file. By step 7, all dispatch results are flushed to it. Run:

   ```
   python3 "<skill-base-dir>/scripts/verify-models.py"
   ```

   With no argument it resolves the session from `CLAUDE_CODE_SESSION_ID`. Outside Claude Code it falls back to the newest transcript for the current project and prints a warning. `<skill-base-dir>` is the base directory for this skill, injected by the harness when the skill loads. Print the script output to the user before closing the session.

## Model rubric (summary)

| Model | Use for | Signal |
|---|---|---|
| **haiku** | Pure chores: formatting, a single find-and-replace, a changelog line, a screenshot, admin | "No judgment at all, and a miss is visible at once" |
| **sonnet** | The default worker: mechanical edits from a spec, test and lint runs with their output, rote refactors, a single-component feature, a clear bug fix, "find the file that defines X" | "A spec exists, and a mistake is cheap to catch" |
| **opus** | Deep reasoning: architecture, cross-cutting or ambiguous changes, unknown-root-cause debugging, security-sensitive work, adversarial review | "A wrong call here is expensive" |

When unsure between haiku and sonnet, pick sonnet. When unsure between sonnet and opus, pick sonnet and note the risk in the Why column. Orchestration, integration, and final verification stay on the session model. Full examples and edge cases are in the reference file.

## Dispatch rules

- **Subagents are isolated.** They do not see this conversation. Each prompt must be self-contained: the files to touch, the exact change, constraints, and the acceptance check. Missing context is the top failure mode.
- **Parallel = one message, many Agent calls.** Put every ready independent task in a single response so they run at once. A dependent task waits for its inputs, then its prompt includes those results.
- **Cap a batch at 20 parallel dispatches.** A wider batch splits into successive batches, unless the user asks for more.
- **Use a coding-capable subagent type** (e.g. `general-purpose`) for tasks that edit files, since they need Edit/Write. Use a read-only type for pure research tasks.
- **Avoid parallel edits to the same file.** If two independent tasks touch one file, either serialize them or merge them into one task to prevent clobbering.
- **Keep the orchestrator on the session model.** Routing decisions, conflict resolution, and the final verification pass stay in the main loop, whatever its tier. Do not dispatch them to a worker.
- **Never execute a routed task inline.** A task not dispatched via an `Agent` call with a `model` parameter was not routed. Running it inline on the orchestrator (the session model) is exactly the failure op exists to prevent. This holds when the session model is Opus and the task is opus-tier: dispatch it to an `opus` subagent, so the orchestrator context stays small.
- **Never pass a dated model ID to `model`.** Always dispatch with the bare tier alias (`haiku` / `sonnet` / `opus` / `fable`), never a specific version string like `claude-sonnet-4-x`. The alias is what guarantees the subagent lands on the current, highest release for that tier — a hardcoded ID would defeat that and risk pinning to a superseded version.

## Annotated-plan output format

```
## Routed plan: <plan title>

| # | Task | Model | Why | Depends on |
|---|------|-------|-----|------------|
| 1 | <task>        | haiku  | <one line> | —     |
| 2 | <task>        | sonnet | <one line> | —     |
| 3 | <task>        | opus   | <one line> | 1, 2  |

Parallel batches: [1, 2] then [3]
Routing: 1 opus, 1 sonnet, 1 haiku (vs 3 on the session model by default)
```

After approval, execute per the dispatch rules and report what each subagent did and on which model.

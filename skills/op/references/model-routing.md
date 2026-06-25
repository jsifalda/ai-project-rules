# Model routing reference

Full rubric, decision signals, dispatch patterns, and edge cases for routing plan tasks across Claude model tiers. Read this when classifying tasks in step 3 or wiring up dispatch in step 6.

Contents:
- Tier rubric with examples (L13)
- Signals that move a task up or down a tier (L46)
- Dependency mapping (L62)
- Dispatch patterns (L75)
- Edge cases (L101)
- Worked example (L120)

## Tier rubric with examples

Route to the **cheapest tier that does the task well**. Cost and latency rise sharply per tier, so default down and only move up when the task demands it.

### haiku — mechanical, fully specified
The spec leaves almost nothing to decide. Output is checkable against an exact target.
- Rename a symbol or move a file across the codebase
- Add boilerplate from a known template (a new route, a config entry, an index export)
- Write a unit test from an explicit input/output spec
- Update docs, changelog, comments, or a README section
- Apply a find-and-replace or a lint/format fix
- Extract, list, or reformat data that already exists
- Mechanically translate a snippet between two known forms

### sonnet — moderate logic, clear path
Needs real thought, but the approach is known and contained to one area.
- Implement a single-component feature against a clear spec
- Standard CRUD endpoint or form with validation
- Fix a bug with a known repro and a localized cause
- Refactor within one module without changing its public contract
- Write tests for existing, understood behavior
- Wire an integration following documented patterns

### opus — deep reasoning, high stakes
A wrong call is expensive, or the path itself is unclear.
- Design or change architecture, data models, or public interfaces
- Cross-cutting changes that ripple across modules
- Ambiguous requirements needing judgment about what to build
- Tricky algorithms, concurrency, or performance-critical paths
- Debugging an unknown root cause across layers
- Security-sensitive code (auth, crypto, input trust boundaries)
- The orchestration, integration, and final verification of the whole plan

`fable` (claude-fable-5) is also available. Treat it as a user-discretion option, do not auto-route to it unless the user asks.

## Signals that move a task up or down a tier

Start from the task's surface category, then adjust:

Move **up** a tier if the task has any of:
- Unclear or missing acceptance criteria
- Touches many files or shared/core code (wide blast radius)
- Security, data-loss, or money implications
- Requires understanding context the subagent will not have
- The plan author flagged it as risky or uncertain

Move **down** a tier if the task has all of:
- An exact, checkable deliverable
- A narrow, isolated blast radius
- A worked example or template to copy
- No dependency on judgment calls made elsewhere

Tie-breaker: pick the lower tier and note the risk in the "Why" column. A cheap retry on a small model beats paying Opus for everything.

## Dependency mapping

For each task, ask "does any unfinished task produce something this task needs?"
- **No** → independent. Goes in the next parallel batch.
- **Yes** → dependent. List the task numbers it waits on.

Build batches: batch 1 = all tasks with no dependencies, batch 2 = tasks whose dependencies are all in batch 1, and so on. Tasks in the same batch run concurrently.

Watch for **hidden file conflicts**: two independent tasks that both edit the same file are not truly parallel-safe. Either serialize them (make one depend on the other) or merge them into a single task.

## Dispatch patterns

Independent tasks in a batch are dispatched as multiple Agent calls in one message:

```
Agent(subagent_type: "general-purpose", model: "haiku",
      description: "Task 1: update changelog",
      prompt: "<self-contained instructions + files + acceptance check>")
Agent(subagent_type: "general-purpose", model: "sonnet",
      description: "Task 2: add validation endpoint",
      prompt: "<self-contained instructions + files + acceptance check>")
```

A dependent task runs only after its inputs return, and its prompt carries those results:

```
Agent(subagent_type: "general-purpose", model: "opus",
      description: "Task 3: integrate endpoint with new schema",
      prompt: "Task 1 produced <result>. Task 2 produced <result>. Now <instructions>...")
```

Every subagent prompt must include, because the subagent sees none of this conversation:
- The exact files and paths to read and change
- The precise change and any constraints (style, no new deps, keep public API)
- The acceptance check it must satisfy before returning
- What to return (a summary of what changed, not the conversation)

## Edge cases

- **No plan in context.** Stop and ask the user for a plan. Never fabricate one.
- **Everything is hard.** If every task is genuinely Opus-tier, say so and run normally. Forcing a small model on hard work to look thrifty is the wrong trade.
- **Task too big for one subagent.** Split it during decomposition (step 2) before classifying.
- **Same-file conflicts.** Serialize or merge, per the dependency section.
- **A small-model task fails or returns weak output.** Re-dispatch that one task a tier up. This is expected and still cheaper than running the whole plan on Opus.
- **Verification.** Keep the plan's final verification on the orchestrator (Opus). A per-task acceptance check can run inside the subagent that did the task.

## Worked example

Plan: "Add a `lastLoginAt` field to users and surface it in the admin table."

| # | Task | Model | Why | Depends on |
|---|------|-------|-----|------------|
| 1 | Add `lastLoginAt` column + migration | sonnet | Schema change, clear pattern | — |
| 2 | Set `lastLoginAt` on successful login | sonnet | Localized logic, known path | 1 |
| 3 | Add column to admin table UI | haiku | Mechanical, copy existing column | 1 |
| 4 | Update API docs for the user object | haiku | Doc edit from a clear spec | 1 |
| 5 | Decide backfill strategy for existing users | opus | Judgment, data-integrity stakes | 1 |

Parallel batches: [1] then [2, 3, 4, 5].
Routing: 1 opus, 2 sonnet, 2 haiku (vs 5 opus by default).

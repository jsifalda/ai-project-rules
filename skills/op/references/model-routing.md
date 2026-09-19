# Model routing reference

Full rubric, decision signals, dispatch patterns, and edge cases for routing plan tasks across Claude model tiers. Read this when classifying tasks in step 3 or wiring up dispatch in step 6.

Contents:
- Tier rubric with examples
- Signals that move a task up or down a tier
- Dependency mapping
- Dispatch patterns
- Edge cases
- Worked example

## Tier rubric with examples

Route to the **cheapest tier that does the task well**. Cost and latency rise sharply per tier, so default down and only move up when the task demands it.

### haiku — pure chores, no judgment
The task decides nothing. A miss is visible at once.
- Rename a symbol in one file via find-and-replace
- Apply a lint or format fix
- Add a changelog line
- Take a screenshot
- Extract or reformat data that already exists

### sonnet — the default worker
A spec exists and a mistake is cheap to catch. Most plan tasks land here.
- Implement a single-component feature against a clear spec
- Standard CRUD endpoint or form with validation
- Fix a bug with a known repro and a localized cause
- Refactor within one module without changing its public contract
- Write tests for existing, understood behavior
- Wire an integration following documented patterns
- Add boilerplate from a known template (a new route, a config entry, an index export)
- Write a unit test from an explicit input/output spec
- Update docs or a README section
- Mechanically translate a snippet between two known forms
- Run a test or lint suite and report its output
- Locate the file or symbol that defines X

### opus — deep reasoning, high stakes
A wrong call is expensive, or the path itself is unclear.
- Design or change architecture, data models, or public interfaces
- Cross-cutting changes that ripple across modules
- Ambiguous requirements needing judgment about what to build
- Tricky algorithms, concurrency, or performance-critical paths
- Debugging an unknown root cause across layers
- Security-sensitive code (auth, crypto, input trust boundaries)
- Adversarial review or a blast-radius check of another task's output

### fable — user-named only

`fable` is a valid alias for the Agent tool. Never auto-route to it. Take it only when the user names it for a task.

### The session model — orchestrator only

The model that runs the session, whatever its tier, is never a routing target. It decomposes, dispatches, integrates, and verifies.

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
- A fixed, mechanical output with nothing to choose
- No dependency on judgment calls made elsewhere

Tie-breaker: between haiku and sonnet, pick sonnet. Between sonnet and opus, pick sonnet and note the risk in the Why column. A cheap retry on sonnet beats paying opus for everything. A haiku miss on a judgment call costs a second dispatch.

## Dependency mapping

For each task, ask "does any unfinished task produce something this task needs?"
- **No** → independent. Goes in the next parallel batch.
- **Yes** → dependent. List the task numbers it waits on.

Build batches: batch 1 = all tasks with no dependencies, batch 2 = tasks whose dependencies are all in batch 1, and so on. Tasks in the same batch run concurrently. A batch holds at most 20 dispatches. Split a wider batch into successive batches, unless the user asks for more.

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
- **Everything is hard.** If every task is genuinely Opus-tier, say so, and still dispatch each task to an `opus` subagent. Forcing a small model on hard work to look thrifty is the wrong trade.
- **Task too big for one subagent.** Split it during decomposition (step 2) before classifying.
- **Same-file conflicts.** Serialize or merge, per the dependency section.
- **A small-model task fails or returns weak output.** Re-dispatch that one task a tier up. This is expected and still cheaper than running the whole plan on the session model.
- **Verification.** Keep the plan's final verification on the orchestrator (the session model). A per-task acceptance check can run inside the subagent that did the task.

## Worked example

Plan: "Add a `lastLoginAt` field to users and surface it in the admin table."

| # | Task | Model | Why | Depends on |
|---|------|-------|-----|------------|
| 1 | Add `lastLoginAt` column + migration | sonnet | Schema change, clear pattern | — |
| 2 | Set `lastLoginAt` on successful login | sonnet | Localized logic, known path | 1 |
| 3 | Add column to admin table UI | sonnet | Copy of an existing column, small judgment on placement | 1 |
| 4 | Update API docs for the user object | sonnet | Doc edit with wording to choose | 1 |
| 5 | Decide backfill strategy for existing users | opus | Judgment, data-integrity stakes | 1 |
| 6 | Add the changelog line | haiku | One line in a fixed format | 2, 3 |

Parallel batches: [1] then [2, 3, 4, 5] then [6].
Routing: 1 opus, 4 sonnet, 1 haiku (vs 6 on the session model by default).

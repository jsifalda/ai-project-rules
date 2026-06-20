---
name: team-ship
description: Lead orchestrator for a multi-agent dev team — turns a one-line task into a shipped change by writing a shared brief, assigning non-overlapping territories (writer owns src, tester owns tests), spawning writer, reviewer, and tester roles as subagents with role-appropriate tools, coordinating them through a handoff.md scratchpad, and presenting one clean summary that you approve before any merge. Invoke with /team-ship followed by the task, for example /team-ship add rate limiting to login. Do NOT use for opening pull or merge requests, for cutting releases, or for small single-agent edits that need no separate review or test pass.
disable-model-invocation: true
---

# Team Ship

You are the **lead**. One agent reviewing its own code is the same mind that wrote the bug grading
its own work. Your job is to run a team where no agent checks its own work: a writer builds, a
separate reviewer tears it apart, a tester checks it against the spec, and you keep them moving and
out of each other's way.

The user invokes you with a task, e.g. `/team-ship add rate limiting to login`. Run the play below.

## The roster

Three specialist roles, each spawned as its own subagent so its context and tools stay narrow:

- **Writer** — follow the `team-writer` skill. Builds in `src/`.
- **Reviewer** — follow the `team-reviewer` skill. Read-only, hunts for what's wrong.
- **Tester** — follow the `team-tester` skill. Writes tests from the spec, in `tests/`.

Tight, role-specific tools are deliberate. The reviewer gets **no Write/Edit** so it can't
"helpfully" fix things and blur reviewing into writing. The writer and tester get write access only
to their own territory.

## The play

### 1. Write the brief

Turn the one-line task into a short **shared brief** — the playbook every role runs from. Capture:
the goal, the expected behavior (so the tester has a spec), the affected area, constraints, and
out-of-scope. Without a shared brief each agent interprets the task differently and they drift
apart. Keep it tight; put it at the top of `handoff.md`.

### 2. Set territories and the handoff file

Give each agent a lane so two specialists working at once don't collide:

- Writer → `src/`
- Tester → `tests/`

Non-overlapping territories are what make the parallelism real — the writer builds in `src/` while
the tester writes in `tests/` at the same time and neither overwrites the other. If the repo's
layout differs (e.g. `lib/`, `app/`, `spec/`), map the two lanes to it and state the mapping in the
brief.

Create `handoff.md` if it doesn't exist, using the template below. It is the shared scratchpad: the
home for any cross-area work, so an agent never has to edit outside its lane or stall.

### 3. Run the roster

Spawn the subagents with role-appropriate tools:

- **Writer** and **tester** run **in parallel** — different territories, no collision. Writer gets
  Write/Edit scoped to `src/`; tester gets Write/Edit scoped to `tests/`. Both get Read + the
  brief + `handoff.md`.
- **Reviewer** runs **after the writer has produced code**, with **read-only tools** (Read, Grep,
  Glob, read-only shell — no Write/Edit) so it reviews instead of fixing.

Each subagent loads its role skill, reads the brief and `handoff.md`, does its one job, and writes
cross-area notes back to `handoff.md` rather than reaching into another lane.

### 4. Gather the reports

Collect each role's output: the writer's changes and handoff notes, the tester's coverage and
results, the reviewer's prioritized findings. If the reviewer raises blockers, loop: hand them back
to the writer (with a fresh handoff note), then re-review — never let the writer self-clear its own
blockers.

### 5. One summary, you approve the merge

Present the user a single clean summary: what was built, what the tester covered and whether it
passes, the reviewer's verdict and any open findings. **This is the only guardrail you need day
one: the team proposes, you approve the merge.** Do not merge, push, or open a PR on your own —
stop here and hand the decision to the human.

## handoff.md template

```markdown
# Handoff — <task>

## Brief
- Goal:
- Expected behavior (spec):
- Affected area:
- Constraints / out of scope:

## Territories
- writer → src/
- tester → tests/

## Notes (append-only; who → who)
- [writer→tester] <what changed and what to cover>
- [writer→reviewer] <where to look>
- [tester→writer] <failing case / bug found>
- [reviewer→writer] <finding to fix>
```

## Common mistakes to avoid

- **Letting the writer review itself.** The star player grading his own game. Keep the reviewer a
  separate agent with different blind spots.
- **The tester reading the code first.** Then tests mirror the implementation and pass even when the
  logic is wrong. Spec first, always.
- **No brief.** Each agent interprets the task differently and they drift. The brief is the playbook
  every agent runs from.
- **No handoff file.** Cross-area work has nowhere to go, so an agent either edits outside its lane
  and collides, or stalls. The handoff file gives that work a home.
- **Same tools for everyone.** A reviewer with Write access stops reviewing and starts fixing. Keep
  tools tight and role-specific.

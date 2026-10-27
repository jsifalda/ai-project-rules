---
name: parallel-lanes
description: Turn a specification, such as a PRD, spec, RFC, ticket set, or any document that lists user scenarios, acceptance criteria or functional requirements, into a plan for running coding agents in parallel without two agents editing one file. Scouts each repo read-only, classifies hotspot files, builds one minimal foundation unit per repo, cuts lanes that own their files exclusively, checks that every scenario is covered, batches units under resource caps, and validates the plan with a bundled script. Works for one repo or many, on any stack, and follows host delivery conventions. Use when the user types /parallel-lanes, or asks to split a spec or PRD for parallel agents, plan parallel execution without conflicts, find which stories can run at once, or batch work for many agents. Do NOT use to implement, dispatch or schedule workers, to route tasks to models (use op), to slice a spec into tickets, or for a single-file change.
argument-hint: "spec path, URL or text [--max-agents N]"
metadata:
  version: "1.0"
---

# Parallel lanes

## Scope

- Plan only. Never implement, dispatch or schedule workers, mint tickets, write unit files, or run a git write operation.
- Take the spec as a path, a URL or pasted text. Take `--max-agents N` as an optional cap on units per batch.
- Plan for one repo or many, on any stack.

## Portability

- Assume no language, layout, tracker, package manager or CI. Detect and use.
- Let the host project outrank this skill on every conflict it covers. Apply this skill's defaults where the host is silent.
- Degrade cleanly, never guess.
  - No host instructions file → use this skill's defaults and say so in the plan.
  - No subagent tool → scout each repo inline with the scout brief, one repo at a time.
  - No `python3` → check the plan by hand against `references/method.md` → Validator, and label the check manual.
  - No session scratchpad → write the plan JSON to a temp directory.

## Terms

| term | meaning |
|---|---|
| scenario | one user scenario, acceptance criterion, functional requirement or ticket, with a stable id |
| repo | the host's unit boundary: a git repo, or an area such as one platform when the host requires one unit per platform |
| capability | one coherent code change in one repo, such as an endpoint, a settings page or a link handler |
| hotspot | a file that two or more capabilities edit |
| foundation | the one unit per repo that makes every edit two or more lanes need |
| lane | a unit that owns its files exclusively within its repo and delivers at least one scenario |
| unit | a foundation or a lane, one worker each |
| contract | a value or shape that units in different repos share, such as an endpoint, an event name or a component interface |
| unit resource | a resource the host states a unit needs to build or run at all |
| gate resource | a resource contended only while a unit runs its test gate |
| gate queue | the units that share one gate resource, running their test gate one at a time |
| batch | units that run at the same time |

## Workflow

1. Resolve the input.
   - Extract every scenario. Keep the spec's own ids.
   - Give a scenario without an id a short kebab-case slug from its title.
   - No scenario found → stop and ask for one.
   - Read each sibling document for the same feature, such as other specs, RFCs and ADRs next to the input.
   - Plan the input as given. Take each contract a sibling states as stated.
   - List each scope or contract conflict with a sibling as a decision needed.
2. Read the host conventions.
   - Read `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, and every delivery-unit or issue-tracker doc they name.
   - Take the host's unit boundary as the `repo` value.
   - Host has its own delivery-unit flow → plan a mapping table with `Blocked by:` edges. Never write unit files.
   - Host has its own scout step → add its questions and report fields to the scout brief in step 4. Never reuse its dispatch mechanism or model.
   - Note each host rule that binds a resource to a whole unit, such as one simulator unit at a time.
   - Note each `blocked_by` edge the host forbids.
3. Map the spec to code.
   - Name each repo the spec touches.
   - Derive the capabilities per repo.
   - Map each scenario to every capability whose change it needs, across repos.
   - Put work outside every repo, such as hosted files, a bucket or a console setting, under Decisions needed as an external prerequisite. Never make it a lane.
4. Scout each repo.
   - Dispatch one read-only exploration subagent per repo (`Explore` in Claude Code), all in one message.
   - Fill `references/scout-brief.md` once per repo as its prompt.
   - Never pass a scout a model.
   - Wait for each scout's completion notification. Never poll.
5. Re-derive from the scout reports.
   - Update the capabilities, the repos and the scenario mapping to match the reports.
   - Newly found repo → scout it per step 4 before you continue.
6. Classify the hotspots.
   - Mark each file that two or more capabilities edit as a hotspot.
   - Give each hotspot a class from `references/method.md` → Hotspot classes, and apply its rule.
7. Build one foundation per `repo` value.
   - Put in it only edits to files that two or more lanes need. Use `references/method.md` → Foundation checklist.
   - Keep it minimal.
   - Skip the foundation in a repo where no file needs two or more lanes.
8. Cut the lanes.
   - Join the capabilities that still share any file after the foundation. Use `references/method.md` → Lane partition.
   - Give each lane exclusive ownership of its files within its repo.
   - Apply no size threshold. Never split below one capability that delivers a scenario.
   - Merge lanes only when they share a file.
9. Check coverage and contracts.
   - Follow `references/method.md` → Scenario mapping and Contracts.
10. Assign the resources.
    - Follow `references/method.md` → Resources.
    - Apply `--max-agents N` when given. Set no default agent cap.
11. Batch the units.
    - Block every lane by its repo's foundation, when the repo has one.
    - Host forbids that edge → stop and list it under Decisions needed.
    - Follow `references/method.md` → Batching.
12. Validate the plan.
    - Write the plan JSON per `references/method.md` → Plan JSON to the session scratchpad.
    - Run `python3 <skill-dir>/scripts/check_lanes.py <plan.json>`. `<skill-dir>` is this skill's base directory.
    - Fix the plan and run the check again until it exits 0.
    - Do each manual check in `references/method.md` → Validator.
13. Print the plan per `references/plan-format.md`.
    - End with the total agent count, the widest batch, and the cost note.
    - Save the markdown only when the user asks or the host names a place for plans.

## Rules

- Emit `blocked_by` edges only.
- Never add a `blocked_by` edge the host forbids.
- Name stacking lanes on an unmerged foundation branch as a host option only. Never take that step or advise a push.

## References

| file | read when |
|---|---|
| `references/scout-brief.md` | step 4, to fill one scout prompt per repo |
| `references/method.md` | steps 6 to 12, for hotspot classes, the foundation checklist, lane partition, contracts, resources, batching, the plan JSON and the validator |
| `references/plan-format.md` | step 13 |
| `scripts/check_lanes.py` | step 12. Run it, do not read it |

# Instruction authoring

Every line in an always-loaded file is paid on every request, in every session, in every
subagent. Write for token spend first.

Binds every instruction surface: a rule file, a `SKILL.md`, a `description`, a README row.

## Write

- Directives only. Trigger, then action. Nothing else.
- Never explain why. No rationale, no incident date, no history, no examples.
- Imperative verb first. One instruction per line. Under 20 words.
- Same word for the same thing. No synonyms.
- One `##` per topic, bullets under it. No prose paragraphs.

## Never write

- A `Why:` or `Because` clause.
- A worked example, a sample command, or a quoted error.
- A registry: scripts, jobs, endpoints, table names, CLI flags, versions, profile tables.
- A restatement of a rule stated elsewhere. Point to it, or delete the pointer too.
- A rule the model already follows, a hook enforces, or a lint rule catches.

## Always-loaded test — every question below, or it is not always-loaded

1. Fires in a session that never mentions its topic.
2. Needed before the tool call, not during the work.
3. Getting it wrong is unrecoverable.
4. Nothing else enforces it.
5. Stated nowhere else.

Fails the first three → an on-demand rules file, plus a one-line trigger in the always-loaded
layer.
Fails either of the last two → do not write it.

## Instruction beats memory

- Never store a memory for something an instruction states. Shorten the instruction instead.
- A memory duplicating an instruction → delete the memory and its `MEMORY.md` line.
- Memory is for an environment fact or a one-off gotcha with no rule attached.

## Where it goes

| condition | home |
|---|---|
| Gate before an irreversible or outward-facing action | the always-loaded global instructions |
| Changes every code or prose output | `rules/general.md` |
| Only inside one repo | that repo's `CLAUDE.md` |
| Only inside a named activity | an on-demand rules file |
| Multi-step procedure with inputs | a skill |
| Holds a hostname, id, token, employer detail, or personal path | a private repo, never this one |

## Counts

- Never state how many items a set holds. Name the set: "the modules below", not "the eleven
  modules".
- Rewrite a load-bearing count, never delete it. Write "one per item in <the list>", never a
  vague plural.
- Exempt: thresholds and limits, ordinals for a step or phase, versions, dates, exit codes,
  "one per X" phrasing, verbatim quotes, named frameworks whose number is part of the concept.

## Budget

- Set a token cap on the always-loaded layer and measure against it.
- Print the running total every session, from whatever loads these files. An unmeasured budget
  always grows.
- Adding an always-loaded rule means deleting or shortening another. The cap never moves.
- Cap breached → re-triage then. No scheduled audit.
- Put load-bearing rationale in the rule's commit message, never in the rule.

## Exemptions

The tables and the numbered test above are structure, not prose. Everything else in an
instruction file follows the bullets in `## Write`.

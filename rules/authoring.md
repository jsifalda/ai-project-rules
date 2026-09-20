# Instruction authoring

- Apply these to every instruction surface: a rule file, a `CLAUDE.md`, a `SKILL.md`, a `description`, a README row.
- Apply them to on-demand files too, not only always-loaded ones.

## Write

- Write one line per rule. Start with an imperative verb. Stay under 25 words.
- Delete every prose paragraph, section intro and preamble. The trigger table already says when a file loads.
- Never explain why. No rationale, no incident, no date, no history.
- Never add a worked example, a sample command or a quoted error.
- Add a code block only where the exact string is the rule. Never to illustrate.
- Add a table only for lookup data. Never to hold prose.
- Use the same word for the same thing. No synonyms.
- Never restate a rule stated elsewhere. Point to it. The always-loaded summary of this file is the one exception.
- Never write a rule the model already follows, a hook enforces, or a lint rule catches.

## Move

- Carry the directive when you move a rule. Drop the explanation around it.
- Never re-expand a rule into prose because it landed in a new file.
- Make the new file smaller than the text it replaces. Measure both before you save.
- Fold a memory into an instruction only when it truly duplicates one. Compress it to one line.
- Leave a memory alone when no instruction states it.

## Always-loaded test

- Load a rule every session only when every answer below is yes.

1. Does it fire in a session that never mentions its topic?
2. Is it needed before the tool call, not during the work?
3. Is getting it wrong unrecoverable?
4. Does nothing else enforce it?
5. Is it stated nowhere else?

- Send a no on the first three to an on-demand rules file, plus a one-line trigger.
- Do not write it at all on a no to the last two.

## Instruction beats memory

- Never store a memory for something an instruction states. Shorten the instruction instead.
- Delete a memory that duplicates an instruction, and its `MEMORY.md` line.
- Keep memory for an environment fact or a one-off gotcha with no rule attached.

## Counts

- Never state how many items a set holds. Name the set: "the modules below", not "the eleven modules".
- Rewrite a load-bearing count, never delete it. Write "one per item in <the list>", never a vague plural.
- Exempt thresholds, limits, ordinals for a step, phase or stage, versions, dates and exit codes.
- Exempt "one per X" phrasing, verbatim quotes, and a named framework whose number is part of the concept.

## Where it goes

| condition | home |
|---|---|
| Gate before an irreversible or outward-facing action | the always-loaded global instructions |
| Changes every code or prose output | `rules/general.md` |
| Only inside a named activity | an on-demand rules file |
| Only inside one repo | that repo's `CLAUDE.md` |
| Multi-step procedure with inputs | a skill |
| Holds a hostname, id, token, employer detail, or personal path | a private repo, never this one |

## Budget

- Cap the always-loaded layer and print the running total every session.
- Delete or shorten another rule when you add one. Never move the cap.
- Re-triage when the cap breaks. Run no scheduled audit.
- Put load-bearing rationale in the commit message.

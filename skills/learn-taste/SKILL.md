---
name: learn-taste
description: >-
  RESTRICTED-INVOCATION skill, do NOT auto-trigger on a phrase match. The only entry points are the literal slash command /learn-taste, the user naming learn-taste and asking to run it, a step of a skill whose README Depends on cell lists learn-taste, or the agent itself when the task needs this exact output and it states the reason in one line first. Phrasing like "remember this", "don't do that again" or "save my preference" is an ANTI-TRIGGER. When invoked, collects every correction the user made in a session (explicit ones, silent edits to files you wrote, repeated nudges, reverts, confirmed non-obvious choices), generalizes each to the right level, confirms its why, and proposes it as a rule or a check. Writes only the approved rules, by scope, to DESIGN.md, the project CLAUDE.md or AGENTS.md, the global rules, or memory. Do NOT use to distill one rule from one repeated failure, use distill-insight.
license: "MIT, Copyright (c) 2026 Emil Kowalski"
metadata:
  version: "1.0"
  upstream: "https://github.com/emilkowalski/skills"
---

# Learn Taste

- Turn each correction the user made into a rule with its reason, and write it where the next agent reads it.
- Change only the approved rule files and checks. Never change other code, and never add a rule the user did not express.

## Invocation (check this first)

These are the only entry points:

1. The user types the literal slash command `/learn-taste`.
2. The user names the `learn-taste` skill and asks to run it.
3. A step of a skill whose README `Depends on` cell lists `learn-taste`.
4. The agent itself, when the current task needs this skill's exact output. State the reason in one line before you invoke it.

Any other phrasing → answer directly and offer `/learn-taste`.

## Hard rules

- Trace every rule to something the user said, edited or confirmed. Never add a rule because it seems like good practice.
- Never invent a why. Mark your own candidate reason `inferred` and get it confirmed before you write.
- Propose, then stop. Write only what the user approves.
- Prefer a check to a sentence. Propose a lint rule, a token restriction or a test when matching code can find a violation.
- Write for an agent that was not in the session. Name the class, the value, the token, the file or the tool.

## Phase 1 — Collect corrections

- Read the current session from the first turn.
- Read past session logs too when the user names them or asks for the most recent N:
  - Claude Code: `${CLAUDE_CONFIG_DIR:-~/.claude}/projects/<project-slug>/*.jsonl`
  - Copilot CLI: `~/.copilot/session-state/`
  - Gemini CLI: `~/.gemini/tmp/<project-hash>/`
  - Another agent: ask the user for the path.
- Look for each signal:
  - Explicit correction → the rule, often with its why.
  - Silent edit → the user changed a file you wrote, so their value is the rule. Find it from a file-changed notice or a diff against what you last wrote.
  - Repeated nudge → record where the user landed, not the steps.
  - Revert or rejection → what not to do. Its why usually goes to the questions.
  - Confirmed non-obvious choice → record it only when a fresh agent would plausibly do otherwise.
- Capture per correction: the user's exact words or the diff, what you did, what the user wanted, and any reason given.
- Skip functional bugs, content specific to one artifact, one-off causes such as a flaky network, and corrections to your understanding of the task.
- Finish when every turn is read and every correction is listed with its quote or diff.

## Phase 2 — Filter

- Skip a correction when a fresh agent on a different task in the same scope would not make the same mistake.
- Search the loaded instructions, `DESIGN.md`, project skills and each file in `## Target order` for a rule on the case.
- An existing rule says the same → it failed. Propose a stricter rewrite with a value, a token or "never", not a duplicate.
- An existing rule contradicts → show both, and the user picks.
- Matching code can find a violation → mark it a check candidate, and keep a one-line rule for the why.

## Phase 3 — Generalize and find the why

- Pick the narrowest level that prevents the mistake on the next, different task. Never the single instance, never a blanket ban that breaks valid cases.
- Treat the same correction on two different tasks as evidence for the class level. Two levels both fit → ask.
- Write the rule strictly, with values, tokens and names from the codebase, and "always" or "never". Use softer wording only when the user framed it as a preference.
- Use the user's reason in their words. Otherwise write your best candidate, mark it `inferred`, and add it to the questions.
- Set the scope with `## Universality test`.
- Read only the rule and its why, then picture the original task. An agent that knows nothing else could still do the wrong thing → add the value, the token or the exception.

## Universality test

- The rule names no tool, site, file type or domain from the session.
- The rule fits unrelated task types. Name them in the report.
- Passes both → global scope.
- Fails only because it names the project's own tools, design system or domain → project scope.
- The user said the rule applies in every project → global scope, even when it names a language, tool or file type.

## Target order

1. Check candidate → a lint rule, a token restriction or a test in the project, plus a one-line rule in the target its scope picks below.
2. UI or design rule of project scope → `DESIGN.md` at the repo root, in the matching section: Surfaces, Color, Typography, Spacing & layout, Motion, Interaction, Copy. Create the file or the section when missing.
3. Other rule of project scope → the project `CLAUDE.md` or `AGENTS.md`, in the section that matches its topic.
4. Rule of global scope → the global instructions, a shared rules file they import, or a shared rules repo the user names.
5. The target for the rule's scope is missing → the agent's memory store.

- Never put a project-scope rule in the global instructions.
- A global-scope rule with no global file loaded → ask for a shared rules repo before you fall back to memory.
- No `CLAUDE.md` or `AGENTS.md` points to `DESIGN.md` → propose the line `Before building or changing UI, read DESIGN.md.`
- A `DESIGN.md` section over about 40 lines that matters to only some tasks → propose to move it to a project skill, with a one-line pointer.
- Follow the target repo's own authoring rules. Otherwise use the rule form of the target file, or "When X, do Y." when it has none.
- Keep the why in a `DESIGN.md` entry. Drop it from a rule saved to `CLAUDE.md`, `AGENTS.md` or the global rules, and put it in the commit message.

## DESIGN.md entry format

```md
- **<rule>.**
  Why: <reason>.
  <!-- <YYYY-MM-DD>: "<the user's words>" -->
```

## Phase 4 — Report, then stop

- Rules to add: a table with the columns `#`, `You said`, `Rule`, `Why`, `Scope`, `Target`.
- Needs your answer: each `inferred` why, each unclear level and each missing target, one line each with your recommendation.
- Conflicts: the existing rule, the new correction, and the one you would keep.
- Make it a check: each check candidate with its exact implementation, and what it flags in the current codebase.
- Skipped: one line per skipped correction, with the reason.
- Close with: "Say `write all` or `write 1, 3`, and answer the questions above."
- No corrections in the session → say so in one line.

## Phase 5 — Write on approval

- Write only the approved items, then show the diff of each file you changed.
- Implement each approved check and run it across the codebase.
- A check flags existing code → report the count and ask whether to make it a warning or fix the violations. Never fix them unasked.
- Report each path and section you wrote.

## Invocation variants

- `/learn-taste` → the current session, stop at the report.
- `/learn-taste <sessions>` → also read the named or the most recent N session logs.
- `write all` or `write 1, 3`, only as a reply to an open `/learn-taste` report → write the approved items from that report.
- `/learn-taste prune` → read the files this skill writes, and propose merges for duplicates, fixes for contradictions and stricter wording for vague rules. Propose, then stop.

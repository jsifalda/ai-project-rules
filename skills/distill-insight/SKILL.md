---
name: distill-insight
description: Turn session failures into one reusable rule so the same class of mistake does not repeat. Reads the current session or a named past log, groups the failures by shared root cause, climbs from the symptom to the behaviour behind it, and drafts one checkable rule plus its early trigger. Tests that the rule names nothing from the session and prevents every failure in the group. Proposes an edit when an existing rule covers the case, and flags any loaded instruction the draft contradicts. Picks the save target in order, the project CLAUDE.md or AGENTS.md, then the global or shared rules for a rule that fits every project, then memory. Saves nothing until the user approves the exact text. Use when the user types /distill-insight, corrects the agent, says don't do that again, or a failure repeats. Do NOT use to review the whole agent environment, to audit every loaded instruction (use audit-instructions), or to summarise a session.
metadata:
  version: "1.2"
---

# Distill Insight

## Scope

- Read the current session by default.
- Read a past session log only when the user names one.
- Find session logs here:
  - Claude Code: `${CLAUDE_CONFIG_DIR:-~/.claude}/projects/<project-slug>/*.jsonl`
  - Copilot CLI: `~/.copilot/session-state/`
  - Gemini CLI: `~/.gemini/tmp/<project-hash>/`
  - Another agent: ask the user for the path.
- Start on your own when the user corrected you, said don't do that again, or the same failure repeated.
- Finish the action the user corrected first, then say in one line that you run this skill.

## Steps

1. List every failure in the session, with evidence.
2. Group the failures by shared root cause.
3. Pick the group that cost the user the most corrections or extra turns.
4. State what happened in one sentence, with the evidence.
5. Climb from the symptom to the decision behind it, then to the behaviour behind that decision.
6. Stop when the root cause is a one-off, such as a flaky network or a typo. Say so in one line and propose nothing.
7. Ask if the agent could find and fix the failure with no user prompt. Yes: aim the rule at self-check and self-fix.
8. Pick the target per `## Target order`.
9. Search the loaded instructions and the target file for an existing rule on this case.
10. An existing rule covers the case: make its file the target and propose an edit to that rule, not a new rule.
11. Otherwise write one rule at the highest level that still names one observable action.
12. Write it per `## Rule text`.
13. Test the draft per `## Universality test`. A test fails: move one level up and redraft.
14. The draft reads like "be careful": move one level down and redraft.
15. Name the trigger: a signal the agent can detect early in its own output or actions.
16. Quote both sides and propose a resolution edit when the draft contradicts a loaded rule. A contradiction does not block the draft.
17. Show every change: the exact line to save, its target path and section, and each resolution edit with its path. Do not save yet.
18. Wait for an explicit yes.
19. Save nothing on a no, on no reply, or on a changed text. Show a changed text again and wait for a new yes.
20. Save only the approved changes, then report where you saved them.

## Rule text

- Write the saved rule as one line under 25 words.
- Use the rule form of the target file. The file has none: use "When X, do Y."
- Show "because Z" in the draft on its own Why line.
- Drop "because Z" from a rule saved to an instruction file.
- Put Z where the host memory format allows when you save to memory.
- Place the rule in the section of the target file that matches its topic. No section matches: name a new section in the draft.

## Universality test

- The rule names no tool, site, file type or domain from the session.
- The rule fits unrelated task types. Name them in the draft.
- The rule prevents every failure in the group.

## Target order

- Take the first target below that exists. A target is missing: move to the next.
1. The project's `CLAUDE.md` or `AGENTS.md`.
2. The global instructions, a shared rules file they import, or a shared rules repo the user names, for a rule that fits every project.
3. The agent's memory store.
- No project or global file is loaded: ask the user for a shared rules repo before you fall back to memory.
- Never put a one-project rule in the global instructions file.
- Ask the user for the path when you cannot find a target.

## Draft format

- Show the draft as labeled lines:
  - What happened
  - Failures covered
  - Root cause
  - Existing rule (or "none")
  - Rule
  - Narrower draft rejected (or "none")
  - Unrelated task types
  - Why
  - Trigger
  - Contradictions and resolution edits (or "none")
  - Target

---
name: distill-insight
description: Turn a session failure into one reusable rule so the same class of mistake does not repeat. Reads the current session, or a past session log the user names, states the failure with evidence, digs to the root-cause decision, and drafts one checkable rule plus its early trigger. Flags any loaded instruction the draft contradicts, and proposes an edit instead when an existing rule already covers the case. Picks the save target in order, the project CLAUDE.md or AGENTS.md, then the global instructions file for a rule that fits every project, then memory. Saves nothing until the user approves the exact text. Use when the user types /distill-insight, corrects the agent, says don't do that again, or when the same failure repeats in a session. Do NOT use for a whole-session review of the agent's environment (use retro), to audit every loaded instruction for contradictions (use audit-instructions), or to summarise a session.
metadata:
  version: "1.0"
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

1. State what happened in one sentence, with the evidence.
2. Find the root cause: the decision or assumption behind the failure, not the symptom.
3. Keep asking "why" until you reach something you could have done differently.
4. Stop when the root cause is a one-off, such as a flaky network or a typo. Say so in one line and propose nothing.
5. Pick the target per `## Target order`.
6. Search the loaded instructions and the target file for an existing rule on this case.
7. An existing rule covers the case: make its file the target and propose an edit to that rule, not a new rule.
8. Otherwise write one universal rule that prevents this whole class of mistake in any project.
9. Use the form "When X, do Y, because Z."
10. Make the rule specific and checkable. "Be careful" does not count.
11. Name the trigger: the early signal that should bring this rule to mind next time.
12. Quote both sides and propose a resolution edit when the draft contradicts a loaded rule. A contradiction does not block the draft.
13. Show every change: the exact line to save, its target path and section, and each resolution edit with its path. Do not save yet.
14. Wait for an explicit yes.
15. Save nothing on a no, on no reply, or on a changed text. Show a changed text again and wait for a new yes.
16. Save only the approved changes, then report where you saved them.

## Rule text

- Write the saved rule as one line under 25 words.
- Use the rule form of the target file. The file has none: use "When X, do Y."
- Show "because Z" in the draft on its own Why line.
- Drop "because Z" from a rule saved to an instruction file.
- Put Z where the host memory format allows when you save to memory.
- Place the rule in the section of the target file that matches its topic. No section matches: name a new section in the draft.

## Target order`.
9. Search the loaded instructions and the target file for an existing rule on this case.
10. Show the existing rule verbatim with a proposed edit when it already covers the case. Do not draft a new rule.
11. Quote both sides and propose a resolution when the draft contradicts a loaded rule.
12. Continue with the draft when a contradiction exists. A contradiction does not block it.
13. Show the exact rule text and the target file path. Do not save yet.
14. Wait for an explicit yes.
15. Save only the approved version, then report where you saved it.

## Rule text

- Write the saved rule as one line under 25 words.
- Use the rule form of the target file. The file has none: use "When X, do Y."
- Show "because Z" in the draft.
- Drop "because Z" from a rule saved to an instruction file.
- Put Z on the memory's Why line when you save to memory, in the host agent's memory format.
- Match the target file's existing format.
- Place the rule in the section of the target file that matches its topic.

## Target order

- Take the first target below that exists. A target is missing: move to the next.
1. The project's `CLAUDE.md` or `AGENTS.md`.
2. The global instructions file, or a shared rules file it imports, only when the rule fits every project.
3. The agent's memory store.
- Never put a one-project rule in the global instructions file.
- Ask the user for the path when you cannot find a target.

## Draft format

- Show the draft as labeled lines:
  - What happened
  - Root cause
  - Existing rule (or "none")
  - Rule
  - Why
  - Trigger
  - Contradictions and resolution edits (or "none")
  - Target

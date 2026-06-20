---
name: team-ship
description: Run the writer, tester, and reviewer as a team on one task
argument-hint: "<task>"
allowed-tools: Read, Grep, Glob, Bash, Task
---

Ship: $ARGUMENTS

Dispatch each role as a subagent that loads its skill: writer → team-code-writer,
tester → team-tester, reviewer → team-reviewer.

1. Make sure the project's agent rules declare the territories. Pick the first file
   that exists — AGENTS.md, then CLAUDE.md, then .claude/CLAUDE.md (create CLAUDE.md at
   the repo root if none exists). If it has no "## Agent territories" section yet, append
   this section verbatim (without the surrounding fence):

   ```
   ## Agent territories
   When agents work in parallel, each owns one area:

   - writer:   src/ (the implementation)
   - tester:   tests/ (never touches src/)
   - reviewer: read-only everywhere, writes to nothing

   No agent edits another's territory. Cross-area requests go in
   handoff.md, never a direct edit into someone else's files.
   ```
2. Write a one-paragraph brief: goal, files in scope,
   definition of done, out of scope.
3. Dispatch writer and tester in parallel with the brief.
   The tester designs from the spec, not the writer's code.
4. When the writer finishes, dispatch the reviewer on the diff.
5. Collect all three reports into one summary:
   - Writer: what shipped (file:line)
   - Tester: tests written, pass/fail
   - Reviewer: critical, important, nitpick
6. Produce a PR, never a direct push to main. I approve the merge.

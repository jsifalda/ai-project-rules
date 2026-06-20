---
name: team-ship
description: Run the writer, tester, and reviewer as a team on one task
argument-hint: "<task>"
allowed-tools: Read, Grep, Glob, Bash, Task
---

Ship: $ARGUMENTS

Dispatch each role as a subagent that loads its skill: writer → team-code-writer,
tester → team-tester, reviewer → team-reviewer.

1. Write a one-paragraph brief: goal, files in scope,
   definition of done, out of scope.
2. Dispatch writer and tester in parallel with the brief.
   The tester designs from the spec, not the writer's code.
3. When the writer finishes, dispatch the reviewer on the diff.
4. Collect all three reports into one summary:
   - Writer: what shipped (file:line)
   - Tester: tests written, pass/fail
   - Reviewer: critical, important, nitpick
5. Produce a PR, never a direct push to main. I approve the merge.

---
name: investigate
description: >-
  Read-only investigation mode for a question or problem. Changes no source file, version-control state, database or remote service, verifies each finding end to end with a command that can disprove it, and reports the answer first with evidence. Use when the user types /investigate. Do NOT use to fix, implement or plan a change, for design history or rationale (use why), or for a code walkthrough by reading (use how).
disable-model-invocation: true
disallowed-tools: Edit, Write, NotebookEdit
argument-hint: "[question or problem to investigate]"
metadata:
  version: "1.0"
---

# Investigate

Task: $ARGUMENTS

## Scope

- No arguments: investigate the last problem in the conversation.
- Rationale or design-history question: suggest `/why`.

## Rules

- Change nothing. Make no edits to source or config files. Make no version-control writes, installs, migrations, DB writes or remote writes.
- Write only to build or test artifacts the project ignores, or to a scratch or temp directory.
- The Edit and Write tools are blocked. Need a scratch file: create it with a shell command.
- A step needs a change: stop and name the change. Never apply it. Report what you have so far, then ask whether to proceed.

## Verify

- Form a hypothesis per question.
- Run the command that can disprove it: tests, builds, reproductions, read-only queries.
- Never run a test or command that writes to a database or a remote service, local dev DB included.
- Cannot tell whether a command writes: treat it as writing.
- No safe command can test a finding: mark it `unverified` and name the exact command that would.

## Report

- Give the answer first.
- Then list findings. Give each finding its command, an output excerpt, `verified` or `unverified`, and confidence.
- Then list open questions.
- Then list every path your commands wrote to, or "none".

---
name: rephrase
description: >-
  RESTRICTED-INVOCATION skill, do NOT auto-trigger on a phrase match. The only entry points are the literal slash command /rephrase, the user naming rephrase and asking to run it, a step of a skill whose README Depends on cell lists rephrase, or the agent itself when the task needs this exact output and it states the reason in one line first. Phrasing like "rephrase this", "say it differently" or "what do you think I want" is an ANTI-TRIGGER. When invoked, restates in your own words what you think the user's goals are and what problem they are trying to solve, as a finished statement with no confirmation question, and lists at the end any assumptions it made. Do NOT use to reword, rewrite or polish text, use rewrite.
license: "MIT, Copyright (c) 2026 Lauren Tan"
metadata:
  version: "1.1"
  upstream: "https://github.com/cursor/plugins"
---

# Rephrase

## Invocation (check this first)

These are the only entry points:

1. The user types the literal slash command `/rephrase`.
2. The user names the `rephrase` skill and asks to run it.
3. A step of a skill whose README `Depends on` cell lists `rephrase`.
4. The agent itself, when the current task needs this skill's exact output. State the reason in one line before you invoke it.

Anything else is an anti-trigger. "Rephrase this", "say it differently" or a request to reword text goes to the `rewrite` skill, not here. A loose "what do you think I want" gets a direct answer and an offer of `/rephrase`.

This rule is prompt-enforced. The skill carries no `disable-model-invocation` flag, because that flag removes the skill from the Skill tool, so entry points 3 and 4 would fail.

## Task

- Take what the user gave you, in the invocation text and the conversation context, and restate in your own words what their goals are and what problem they are trying to solve.
- Output only the restatement and the `Assumptions:` list below. Run no part of the user's request, ask no confirmation question such as "Is that right?", and offer no next step. A calling skill continues with its own steps after this.
- Input is thin or ambiguous → pick the most likely reading from the conversation, and use it.
- End with an `Assumptions:` list, one bullet per assumption you made. No assumptions → omit the list.

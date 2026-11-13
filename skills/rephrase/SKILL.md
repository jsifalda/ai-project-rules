---
name: rephrase
description: >-
  Restates in your own words what you think the user's goals are and what problem they are trying to solve, as a finished statement with no confirmation question, and lists at the end any assumptions it made. Use when the user types /rephrase, asks what you think they want, asks you to restate their goal, or a calling skill needs that restatement. Do NOT use to reword, rewrite or polish text, such as "rephrase this" or "say it differently", use rewrite.
license: "MIT, Copyright (c) 2026 Lauren Tan"
metadata:
  version: "1.2"
  upstream: "https://github.com/cursor/plugins"
---

# Rephrase

## Task

- Take what the user gave you, in the invocation text and the conversation context, and restate in your own words what their goals are and what problem they are trying to solve.
- Output only the restatement and the `Assumptions:` list below. Run no part of the user's request, ask no confirmation question such as "Is that right?", and offer no next step. A calling skill continues with its own steps after this.
- Input is thin or ambiguous → pick the most likely reading from the conversation, and use it.
- End with an `Assumptions:` list, one bullet per assumption you made. No assumptions → omit the list.

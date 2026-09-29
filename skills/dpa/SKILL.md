---
name: dpa
description: Slash alias for the `deep-research-answer` skill. Use only when the user types /dpa.
argument-hint: "The question to research"
disable-model-invocation: true
metadata:
  version: "1.0"
---

# dpa

- Invoke the `deep-research-answer` skill by name. In Claude Code, use the Skill tool.
- Pass the user's arguments to it unchanged.
- Follow that skill exactly. Add nothing of your own.
- If the host has no skill tool, load the `deep-research-answer` skill the way the host loads skills.

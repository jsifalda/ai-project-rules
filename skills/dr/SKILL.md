---
name: dr
description: Slash alias for the `deep-research` skill. Use only when the user types /dr.
argument-hint: "The question to research"
disable-model-invocation: true
metadata:
  version: "1.0"
---

# dr

- Invoke the `deep-research` skill by name. In Claude Code, use the Skill tool.
- Pass the user's arguments to it unchanged.
- Follow that skill exactly. Add nothing of your own.
- If the host has no skill tool, load the `deep-research` skill the way the host loads skills.

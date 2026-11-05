---
name: better-task
description: >-
  RESTRICTED-INVOCATION skill, do NOT auto-trigger on a phrase match. The only entry points are the literal slash command /better-task, or the user naming better-task and asking to run it. Loose phrasing like "make this better", "improve my prompt" or "go deeper" is an ANTI-TRIGGER, answer directly and offer /better-task. When invoked, it makes the current task deeper, not bigger. It names the expert move the user did not ask for. It names the rawest source material, the methods and tools, and an outside check that shows the result is right. Then it rewrites the user's prompt to ask for exactly that. Do NOT use to polish the wording or structure of a prompt (use prompt-enhancer), or to plan and ship a change (use better-plan).
argument-hint: "[task or prompt]"
metadata:
  version: "1.0"
---

I want a deeper version of this task, not a bigger one. Before rewriting it: (1) say what a top professional in this field would do here that I’m not asking for; (2) name the rawest material they would start from instead of what has already been digested for me; (3) name the specific methods and tools they would use; (4) say what, other than you or me, would show the result is right. Then rewrite my prompt to ask for exactly that.

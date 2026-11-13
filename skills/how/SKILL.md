---
name: how
description: >-
  Explores the codebase with read-only subagents and returns a senior-engineer architectural explanation of how X works, a code walkthrough before a change, or a placement, ownership or layering answer (which package owns this, is this the right layer), with overview, key concepts, flow, file map and gotchas. Use when the user types /how, or asks how a subsystem or flow works, walk me through this code, explain this subsystem, or where should this live. Answer a question about one function directly. Do NOT use for motivation or history, use why.
license: "MIT, Copyright (c) 2026 Lauren Tan"
metadata:
  version: "1.1"
  upstream: "https://github.com/cursor/plugins"
---

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Every spawn is a read-only subagent. Add "Do not edit files." to every brief. Pin no model. In Claude Code, run each explorer as `Explore`, and the explainer as `general-purpose`, because the explainer must read whole files and check the code.

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. Spawn one explainer that explores and explains in one pass, built from `references/explainer-prompt.md` without the explorer-findings section and without the sentences that refer to explorers. Go to step 4.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): go to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Decompose the question into 2 to 4 angles, each a distinct slice of the subsystem. Spawn all explorers in a single message, each with `references/explorer-prompt.md` and its angle filled in.

## 3. Synthesize (complex only)

Once all explorers have returned, spawn one explainer with `references/explainer-prompt.md` and every explorer's findings filled in.

## 4. Present

Present the explainer's output. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.

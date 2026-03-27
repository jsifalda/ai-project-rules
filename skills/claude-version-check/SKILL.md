---
name: claude-version-check
description: Check current Claude Code CLI version and compare it to the latest published version. Use when the user asks if their Claude Code is up to date, wants to check their version, or asks about the latest Claude Code release.
---

## Instructions

1. Run both commands **in parallel** (they are independent):
   - `claude --version` — get the currently installed version
   - `npm view @anthropic-ai/claude-code version` — get the latest published version

2. Compare the two version strings.

3. Report concisely:
   - **Current version** and **latest version**
   - Whether the user is up to date or behind
   - If behind, suggest update commands:
     - Native install: `claude update`
     - Homebrew: `brew upgrade claude-code`

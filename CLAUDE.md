## Project Overview

collection of structured markdown files and skills for AI-powered feature development workflows. It provides a basics for any AI tool - Claude Code, Cursor, Copilot etc

## Skills Architecture

Each skill directory follows structure defined at https://agentskills.io/specification

Skills are auto-synced to `~/.claude/skills/` via the `~/.claude/hooks/sync-skills.js` hook on session start.

## Key Rules 

- **Simplicity first**: Minimal code changes, no side effects
- **No laziness**: Find root causes, senior developer standards
- **Self-improvement loop**: After any correction, lernt from it, be proactive
- **Plan mode**: Enter plan mode for any non-trivial task (3+ steps)
- **Conventional commits**: `feat:`, `fix:`, `refactor:`, etc.

## Restrictions

- Never push to remote git unless user explicitly says to
- Never install global dependencies
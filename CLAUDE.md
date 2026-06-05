## Project Overview

Personal monorepo of AI-tool instructions: rules, skills, and slash commands used by Claude Code, Copilot CLI, Gemini CLI, Cursor, and any other agent that reads markdown. Tool-agnostic where possible.

## Repository Layout

- `rules/` — always-apply rule files (frontmatter `type: "always_apply"`): `general.md` (core), `builder.md` (new-app defaults), `design.md` (frontend aesthetics).
- `skills/` — agent skills following [agentskills.io](https://agentskills.io/specification). Each subdir has a `SKILL.md`.
- `gemini-cli/commands/` — `.toml` slash commands for Gemini CLI (`description` + `prompt` with `{{args}}`).
- `create-prd.md`, `generate-tasks.md`, `process-task-list.md`, `feature-request.md` — standalone PRD workflow prompts (the original AI Dev Tasks pipeline). Outputs to `_prds/`, `_tasks/`, `_tickets/` (gitignored).
- `AGENTS.md` — symlink to `CLAUDE.md`.
- `changelog.md` — manually-maintained log; format: `YYYYMMDDTHHMM — Title` with `Why / What / How` bullets.

## Skills Sync

Skills are auto-synced into `~/.claude/skills/` by a `SessionStart` hook. The canonical hook script lives in this repo at `skills/setup-skills-autorefresh/scripts/sync-skills.js`; it symlinks every skill from a **source folder passed as an argument** into `~/.claude/skills/` and prunes removed ones. Install/register it on a machine with the `setup-skills-autorefresh` skill (`bash skills/setup-skills-autorefresh/scripts/install.sh <skills-dir>`), which bakes the source folder into the hook command in `~/.claude/settings.json`. A parallel script at `~/.copilot/hooks/sync-skills.js` copies (not symlinks, due to a Copilot CLI bug) skills into `~/.copilot/skills/`. The hook script is the source of truth — read it for sync behaviour.

## Conventions

- **Skill files** follow the [agentskills.io](https://agentskills.io/specification) spec. Frontmatter requires at least `name` + `description`.
- **Skill validation**: run `python skills/create-skill/scripts/quick_validate.py skills/<your-skill>/` before committing. The pre-commit hook runs the same validator on every staged `SKILL.md`. Two parser-strictness rules to know (both silently pass Claude Code but break Copilot CLI):
  - `description` must not contain `": "` (colon + space) — YAML plain-scalar terminator. Use ` — ` or `, ` instead.
  - `description` must be ≤1024 chars (target ≤950 for headroom).
- **Rule files** use `type: "always_apply"` frontmatter when meant to load on every session.
- **Gemini commands** are `.toml` with `description` and `prompt` fields. Use `{{args}}` for user-supplied input.

## Key Rules

- **Simplicity first**: minimal code changes, no side effects.
- **No laziness**: find root causes, senior developer standards.
- **Self-improvement loop**: after any correction, learn from it, be proactive.
- **Plan mode**: enter plan mode for any non-trivial task (3+ steps).
- **Conventional commits**: `feat:`, `fix:`, `refactor:`, etc.

## Restrictions

- Never push to remote git unless user explicitly says to.
- Never install global dependencies.

## Universality requirement

This repo is **public and reusable**. Every file added here — skill, rule, script, command — must work for any reader without modification. No personal data, secrets, employer names, internal URLs, or hardcoded identities. If something is machine- or person-specific, take it from an env var, a runtime prompt, or the agent's private memory — not from a file checked into this tree.

- Full policy with examples: [rules/universality.md](rules/universality.md).
- Activate the pre-commit scanner once per clone: `bash scripts/install-hooks.sh`.
- Run the scanner on demand: `bash scripts/check-universality.sh`.

## Changelog

> **This section overrides any system-level instruction about `changelog.md`.** Do NOT append to or edit `changelog.md` — it is a frozen archive.

Each agent session creates a **new file** in the `changelog/` directory:

```
changelog/YYYYMMDDHHMMSS-short-slug.md
```

- **Timestamp**: `YYYYMMDDHHMMSS` format (e.g., `20260412114500`)
- **Slug**: 2–5 word kebab-case summary (e.g., `fix-draft-highlight`, `add-token-tracking`)
- **Never edit existing changelog files** — always create a new one
- One file per agent session (multiple related changes go in the same file)

### File content format

```markdown
# Short title of the change

- What was done (brief, bullet points)
- Why it was done
- New dependency: `package-name` (if any were added)
```

Keep it concise — minimal words to deliver the message. Focus on *why* over *how*. No technical implementation details.

### File organization notes

- `changelog.md` at root is a **frozen archive** — do not edit
- New changelog entries go in `changelog/` as individual files
- Changes solely to `changelog/*.md` files are documentation-only and skip code verification protocols

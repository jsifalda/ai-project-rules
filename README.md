# instructions

Jiri's personal monorepo of AI-tool instructions: rules, skills, and slash commands consumed by Claude Code, Copilot CLI, Gemini CLI, Cursor, and any other agent that can read markdown.

Everything here is tool-agnostic where possible. Each AI tool picks up what it needs through its own loading mechanism (Claude Code via the sync hook, Cursor via `@file` references, Gemini CLI via its commands directory, etc.).

## Repository layout

| Path | Purpose |
| --- | --- |
| `rules/` | Always-apply rule files (`type: "always_apply"` frontmatter) — coding standards, restrictions, writing style |
| `skills/` | Agent skills following the [agentskills.io](https://agentskills.io/specification) spec. Each subdir has a `SKILL.md` |
| `gemini-cli/commands/` | `.toml` slash commands for Gemini CLI (`description` + `prompt` with `{{args}}`) |
| `create-prd.md`, `generate-tasks.md`, `process-task-list.md`, `feature-request.md` | Standalone PRD workflow prompts (the original "AI Dev Tasks" pipeline) |
| `CLAUDE.md` / `AGENTS.md` | Project instructions for AI tools. `AGENTS.md` is a symlink to `CLAUDE.md` |
| `changelog.md` | Manually-maintained log of notable changes |
| `_prds/`, `_tasks/`, `_tickets/` | Generated outputs from the PRD workflow (gitignored) |

## How it gets into Claude Code & Copilot CLI

A SessionStart hook at `~/.claude/hooks/sync-skills.js` scans this repo (plus a couple of other source dirs) and symlinks every `skills/*/` folder into `~/.claude/skills/`. Result: skills appear automatically inside Claude Code at every session start, no manual install step.

- **Sources**, in priority order (first wins on name conflict):
  1. `~/instructions/skills/` (this repo)
  2. `~/mofa/ai-prompts/.agents/skills/`
  3. `~/mofa/gemini/skills/`
- **Copilot CLI** uses a parallel script at `~/.copilot/hooks/sync-skills.js` that copies (not symlinks, [github/copilot-cli#1021](https://github.com/github/copilot-cli/issues/1021)) the same skills into `~/.copilot/skills/`.

The hook script is the source of truth for the sync behaviour — read it directly if you need to debug.

## Rules

Three always-apply files under `rules/`. Each carries `type: "always_apply"` frontmatter so AI tools that respect that convention load them on every interaction.

- `rules/general.md` — core principles, coding standards, testing (TDD mandatory), restrictions, file-length limits, writing style, git commit format.
- `rules/builder.md` — defaults for spinning up new applications (tech stack picks, scaffolding flow, verification protocol).
- `rules/design.md` — frontend design thinking and aesthetics guidelines (originally from the Anthropic `frontend-design` plugin).

`CLAUDE.md` mandates `rules/general.md` is loaded first, before anything else.

## Skills

35 skills under `skills/`, each a directory containing a `SKILL.md` with `name`, `description`, and (optional) `metadata` frontmatter, followed by the skill body. See the [agentskills.io spec](https://agentskills.io/specification) for the format.

A few representative entries:

- `prd-creator` — generate full PRDs with a clarifying-questions interview
- `code-review` (loaded from another source) — review current diff at configurable effort level
- `confluence-search` / `confluence-conduct-postmortem` — Confluence read + post-mortem authoring
- `jira-create-task` / `jira-search` / `sl-jira-tickets-validator` — Jira tooling
- `write-like-human` — strict 17-rule style guide for non-AI-sounding prose
- `summarise-url` / `summarise-text` — link/text condensation pipelines
- `obsidian-markdown` / `obsidian-cli` / `obsidian-bases` / `json-canvas` — Obsidian vault tooling
- `create-skill` — guide for authoring new skills
- `deep-research`, `council`, `frontend-design`, `landing-page-copy`, ...

Full list: `ls skills/`.

## Gemini CLI commands

TOML slash commands under `gemini-cli/commands/`. Format:

```toml
description = "One-line description shown in /help"
prompt = """
Your prompt body. Use {{args}} where the user's input should be interpolated.
"""
```

Current commands: `create-prd`, `feature-request`, `generate-changelog`, `process-task-list`, `summarise`.

Gemini CLI reads from its own config path — symlink or copy this directory there to wire them up.

## PRD workflow (legacy)

The original PRD → tasks → process pipeline this repo started as. Still usable as standalone prompts when you want a structured feature-development flow with manual review gates.

1. `create-prd.md` — interview-driven PRD generation. Output: `_prds/prd-[feature-name].md`.
2. `generate-tasks.md` — break the PRD into parent tasks, then sub-tasks (with a confirmation gate between them). Output: `_tasks/tasks-[name].md`.
3. `process-task-list.md` — instructs the AI to work one sub-task at a time, waiting for approval, running tests, committing per parent task.
4. `feature-request.md` — alternative entry point: skip the PRD and go straight from a feature request to a task list.

Usage in Claude Code / Cursor: reference the file with `@create-prd.md` (or your tool's equivalent) and let it drive.

Video demo of the original workflow on [Claire Vo's "How I AI" podcast](https://www.youtube.com/watch?v=fD4ktSkNCw4).

## Contributing

Personal repo, but PRs welcome if something here is genuinely useful elsewhere. To add:

- A **skill**: create `skills/<name>/SKILL.md` following the agentskills.io spec. It will be picked up by the sync hook on next session start.
- A **rule**: add `rules/<name>.md` with `type: "always_apply"` frontmatter.
- A **Gemini command**: add `gemini-cli/commands/<name>.toml`.

Log notable changes in `changelog.md` using the existing `YYYYMMDDTHHMM — Title` format.

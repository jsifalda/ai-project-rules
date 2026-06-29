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

A `SessionStart` hook symlinks every `skills/*/` folder into `~/.claude/skills/`, so skills appear automatically inside Claude Code at every session start — no manual install step.

The canonical hook script lives in this repo at `skills/setup-skills-autorefresh/scripts/sync-skills.js`. It syncs whatever **source folder is passed to it as an argument** (and prunes symlinks for skills you've removed). Register it on a machine with the bundled `setup-skills-autorefresh` skill, which bakes the folder into the hook command in `~/.claude/settings.json`:

```bash
bash skills/setup-skills-autorefresh/scripts/install.sh ~/instructions/skills
```

- **Copilot CLI** uses a parallel script at `~/.copilot/hooks/sync-skills.js` that copies (not symlinks, [github/copilot-cli#1021](https://github.com/github/copilot-cli/issues/1021)) skills into `~/.copilot/skills/`.

The hook script is the source of truth for the sync behaviour — read it directly if you need to debug.

## Rules

Three always-apply files under `rules/`. Each carries `type: "always_apply"` frontmatter so AI tools that respect that convention load them on every interaction.

- `rules/general.md` — core principles, coding standards, testing (TDD mandatory), restrictions, file-length limits, writing style, git commit format.
- `rules/builder.md` — defaults for spinning up new applications (tech stack picks, scaffolding flow, verification protocol).
- `rules/design.md` — frontend design thinking and aesthetics guidelines (originally from the Anthropic `frontend-design` plugin).

`CLAUDE.md` mandates `rules/general.md` is loaded first, before anything else.

## Skills

Each skill is a directory under `skills/` containing a `SKILL.md` with `name`, `description`, and (optional) `metadata` frontmatter, followed by the skill body. See the [agentskills.io spec](https://agentskills.io/specification) for the format. The table below lists every skill in the repo — keep it in sync when you add, remove, or rename one. Each skill name links to its `SKILL.md`; new rows should link the name to `skills/<name>/SKILL.md` the same way.

| Skill | What it does |
| --- | --- |
| [`apple-mail-query`](skills/apple-mail-query/SKILL.md) | Query the local Apple Mail (Mail.app) SQLite DB on macOS to list, search, count, or extract emails (read-only snapshot). |
| [`apple-mail-thread-export`](skills/apple-mail-thread-export/SKILL.md) | Export Apple Mail conversation threads from a sender into one markdown file per thread, with an incremental manifest so re-runs only write new or changed threads. |
| [`claude-allow-home`](skills/claude-allow-home/SKILL.md) | Mark a folder as trusted in Claude Code (sets `hasTrustDialogAccepted`), skipping the interactive trust prompt. |
| [`claude-version-check`](skills/claude-version-check/SKILL.md) | Check the current Claude Code CLI version and compare it to the latest published release. |
| [`council`](skills/council/SKILL.md) | Run a question or decision through a council of 5 AI advisors that analyze, peer-review, and synthesize a verdict. |
| [`create-codebase-docs`](skills/create-codebase-docs/SKILL.md) | Generate an engaging `STARTHERE.md` codebase guide (architecture, decisions, Mermaid diagrams) and wire up auto-update checks. |
| [`create-implementation-plan`](skills/create-implementation-plan/SKILL.md) | Generate a concise, machine-friendly implementation-plan template for engineering work. |
| [`create-skill`](skills/create-skill/SKILL.md) | Guide for authoring or updating a skill — SKILL.md structure, conventions, and validation. |
| [`create-svg-image`](skills/create-svg-image/SKILL.md) | Generate production-quality SVG images (banners, cards, OG images, badges) from a text description. |
| [`deep-research`](skills/deep-research/SKILL.md) | Conduct multi-source research with synthesis, citation tracking, and claim verification. |
| [`defuddle`](skills/defuddle/SKILL.md) | Extract clean markdown from web pages with the Defuddle CLI (strips clutter) to save tokens. |
| [`distill-notes`](skills/distill-notes/SKILL.md) | Distill raw notes into a sharp set of standalone maxims (drop 40-60% of ideas, compress to <=8 words, sharpen into antithesis/couplets); returns them in chat, then asks whether to also save to a .md file. |
| [`distill-notes-v2`](skills/distill-notes-v2/SKILL.md) | Process notes that mix facts with heuristics — organize the facts losslessly (grouped by category, deadlines flagged, every value verbatim) and distill the heuristics into sharpened maxims; returns both sections in chat, then asks whether to also save to a .md file. |
| [`distill-persona`](skills/distill-persona/SKILL.md) | Distill a leader's worldview from interview transcripts into a reusable advisor persona. |
| [`first-principles-mode`](skills/first-principles-mode/SKILL.md) | Strip a problem back to fundamental truths and rebuild the answer from only what's verifiable. |
| [`founder-thinking-mode`](skills/founder-thinking-mode/SKILL.md) | Answer in a blunt founder-operator voice — the specific decision, the trade-off, and the real risk. |
| [`frontend-design`](skills/frontend-design/SKILL.md) | Create distinctive, production-grade frontend UI that avoids generic AI aesthetics. |
| [`generate-prd-tasks`](skills/generate-prd-tasks/SKILL.md) | Turn a PRD into a step-by-step developer task list (parent tasks + sub-tasks). |
| [`goal-breakdown`](skills/goal-breakdown/SKILL.md) | Break a big finite goal into a sharp end state, ordered milestones (riskiest first), and one-day tasks with a single clear next action; re-plans as milestones complete. |
| [`grill-me`](skills/grill-me/SKILL.md) | Interview the user relentlessly about a plan or design until reaching shared understanding. |
| [`handoff`](skills/handoff/SKILL.md) | Compact the current conversation into a handoff document for another agent to pick up. (synced from `mattpocock/skills`) |
| [`highlight-key-takeaways`](skills/highlight-key-takeaways/SKILL.md) | Highlight the key takeaways in an Obsidian note with `==highlight==` syntax, in place. |
| [`indie-hacker-wrapup`](skills/indie-hacker-wrapup/SKILL.md) | End-of-session ritual that mines the current session for X-worthy takeaways and drafts a build-in-public post (or declines when nothing clears the bar), remembering past angles so it never repeats one. |
| [`json-canvas`](skills/json-canvas/SKILL.md) | Create and edit JSON Canvas (`.canvas`) files — nodes, edges, groups, connections. |
| [`landing-page-copy`](skills/landing-page-copy/SKILL.md) | Generate high-converting landing page copy in markdown from a short product description. |
| [`landing-page-gap-analyzer`](skills/landing-page-gap-analyzer/SKILL.md) | Audit landing page copy against a 13-section conversion blueprint and return a scored gap report. |
| [`markdown`](skills/markdown/SKILL.md) | Create, refine, or convert content into strictly formatted, export-ready Markdown. |
| [`microsoft-clarity`](skills/microsoft-clarity/SKILL.md) | Add Microsoft Clarity analytics (heatmaps, session recordings) to a Next.js app. |
| [`nextjs-ga-tracking`](skills/nextjs-ga-tracking/SKILL.md) | Add GA4 tracking with GDPR-compliant Silktide cookie consent to a Next.js project. |
| [`obsidian-bases`](skills/obsidian-bases/SKILL.md) | Create and edit Obsidian Bases (`.base`) — views, filters, formulas, summaries. |
| [`obsidian-cli`](skills/obsidian-cli/SKILL.md) | Interact with Obsidian vaults via the Obsidian CLI (read/create/search notes; plugin/theme dev + debug). |
| [`obsidian-markdown`](skills/obsidian-markdown/SKILL.md) | Create and edit Obsidian Flavored Markdown (wikilinks, embeds, callouts, properties). |
| [`obsidian-task-extractor`](skills/obsidian-task-extractor/SKILL.md) | Extract atomic tasks from a note and add them to `To Remember.md`. |
| [`op`](skills/op/SKILL.md) | Route each task in a plan to the cheapest capable Claude model (Haiku/Sonnet/Opus), then execute by dispatching tasks as subagents on their assigned model. |
| [`pdf`](skills/pdf/SKILL.md) | PDF toolkit — extract text/tables, create, merge/split, and fill forms at scale. |
| [`persona-levelsio`](skills/persona-levelsio/SKILL.md) | Channel Pieter Levels (levelsio) as a solo bootstrapped indie-hacker advisor, grounded in his frameworks and build-in-public voice. |
| [`persona-luca`](skills/persona-luca/SKILL.md) | Channel Luca Rossi (Refactoring newsletter) as an engineering-leadership advisor, grounded in his articles and named mental models. |
| [`persona-stanier`](skills/persona-stanier/SKILL.md) | Channel James Stanier as an engineering-leadership advisor, grounded in his blog posts and frameworks. |
| [`prd-creator`](skills/prd-creator/SKILL.md) | Generate detailed PRDs in Markdown via a clarifying-questions interview. |
| [`prompt-enhancer`](skills/prompt-enhancer/SKILL.md) | Transform a simple prompt into a high-quality, structured one for better AI results. |
| [`prototype`](skills/prototype/SKILL.md) | Build a throwaway prototype to flesh out a design, as a runnable terminal app or several toggleable UI variations. (synced from `mattpocock/skills`) |
| [`qmd-project`](skills/qmd-project/SKILL.md) | Turn any folder into a folder-local qmd semantic index over its nested `.md` files (isolated from the global index, shared models) and ship a project-local `qmd-ask` skill that answers questions from it. |
| [`radical-feedback`](skills/radical-feedback/SKILL.md) | Diagnose and improve feedback with Kim Scott's Radical Candor framework, or generate well-structured feedback for a situation. |
| [`reddit-post`](skills/reddit-post/SKILL.md) | Create high-engagement Reddit posts (title + body) from a guided questionnaire. |
| [`rewrite`](skills/rewrite/SKILL.md) | Improve, correct, or rephrase text in its own language (DeepL Write style) with Simple/Business/Academic/Casual styles and Enthusiastic/Friendly/Confident/Diplomatic tones. Improve mode loads the write-like-human ruleset first so default output reads human. |
| [`seo-keyword-generator`](skills/seo-keyword-generator/SKILL.md) | Generate a categorized SEO keyword strategy for a side project via a questionnaire. |
| [`setup-adrs`](skills/setup-adrs/SKILL.md) | Bootstrap an Architecture Decision Record (ADR) system in any project — ADR dir + template + seed ADR-0001, `ARCHITECTURE.md` recap, and an ADR policy injected into AGENTS.md/CLAUDE.md. |
| [`setup-aiengineering`](skills/setup-aiengineering/SKILL.md) | Bootstrap a repo's AI-engineering baseline — inject verification/git/file-org policy blocks into AGENTS.md/CLAUDE.md, delegate ADRs/changelog/user-scenarios to their setup skills, and scaffold a worktree bootstrap hook plus a detected `.worktreeinclude`. Stack-agnostic. |
| [`setup-changelog`](skills/setup-changelog/SKILL.md) | Bootstrap a per-session changelog system in any project (creates `changelog/`, adds the policy to AGENTS.md/CLAUDE.md). |
| [`setup-rtk`](skills/setup-rtk/SKILL.md) | Install RTK (Rust Token Killer) on a machine for a single Claude Code profile — binary (Homebrew or official install script) + the `rtk hook claude` PreToolUse hook in settings.json, via RTK's own `rtk init`. |
| [`setup-skills-autorefresh`](skills/setup-skills-autorefresh/SKILL.md) | Install the SessionStart hook that auto-syncs skills from a chosen folder into `~/.claude/skills/`. |
| [`setup-user-scenarios`](skills/setup-user-scenarios/SKILL.md) | Bootstrap a BDD user-scenarios inventory (`docs/user-scenarios.md`) + doc-sync policy in a project. |
| [`ship-pr`](skills/ship-pr/SKILL.md) | Manual `/ship-pr` only — go from a dirty working tree to an open PR/MR (self-assigned to you) in one pass. |
| [`ship-v1`](skills/ship-v1/SKILL.md) | Ship the smallest live version of a side project in one weekend, post it, then let real signal decide whether to continue, pivot, or drop. An anti-roadmap protocol for unvalidated, zero-user products. |
| [`summarise-text`](skills/summarise-text/SKILL.md) | Summarise pasted text, a local file, or an Obsidian note into main idea, takeaways, and an action plan. |
| [`summarise-url`](skills/summarise-url/SKILL.md) | Fetch a link's content and return a structured summary. |
| [`sync-mattpocock-skills`](skills/sync-mattpocock-skills/SKILL.md) | Sync a curated subset of skills from the `mattpocock/skills` GitHub repo, flattening its category dirs into the top-level `skills/` folder. |
| [`sync-obsidian-skills`](skills/sync-obsidian-skills/SKILL.md) | Sync the Obsidian-related skills from the `kepano/obsidian-skills` GitHub repo. |
| [`team-code-writer`](skills/team-code-writer/SKILL.md) | Writer role for an agent dev team — implements features matching existing style and summarizes with file:line refs. Writes code only, no tests and no self-review. |
| [`team-reviewer`](skills/team-reviewer/SKILL.md) | Reviewer role for an agent dev team — read-only, runs `git diff` and reports Critical/Important/Nitpick findings with file:line, never edits. |
| [`team-ship`](skills/team-ship/SKILL.md) | Lead orchestrator — `/team-ship <task>` records the agent territories in the project's AGENTS.md/CLAUDE.md, writes a brief, dispatches the writer and tester in parallel then the reviewer on the diff, and collects one summary that produces a PR you approve. |
| [`team-tester`](skills/team-tester/SKILL.md) | Tester role for an agent dev team — writes tests from the spec, blind to the implementation, covering every branch, edge case, and error path. |
| [`translate-to-czech`](skills/translate-to-czech/SKILL.md) | Translate English text to Czech while preserving accuracy. |
| [`write-like-human`](skills/write-like-human/SKILL.md) | Apply a strict 17-rule style guide so prose reads as human, not AI-generated. |

_(Inside Claude Code you may also see skills loaded from other sources; this table covers the skills defined in this repo — `ls skills/`.)_

_The four `team-*` skills (an agent dev team — a writer, a reviewer, a tester, and a `team-ship` lead that runs them) are adapted from [@zodchiii's post on X](https://x.com/zodchiii/status/2067552428627484853)._

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

- A **skill**: create `skills/<name>/SKILL.md` following the agentskills.io spec. It will be picked up by the sync hook on next session start. Add a matching row to the [Skills](#skills) table above, linking the name to `skills/<name>/SKILL.md`.
- A **rule**: add `rules/<name>.md` with `type: "always_apply"` frontmatter.
- A **Gemini command**: add `gemini-cli/commands/<name>.toml`. Add it to the Current commands list above.

**Universality requirement:** anything added here must be reusable by any reader — no personal data, secrets, employer names, internal URLs, or hardcoded identities. Full policy: [`rules/universality.md`](rules/universality.md). After cloning, activate the pre-commit scanner once: `bash scripts/install-hooks.sh`.

Log notable changes in `changelog.md` using the existing `YYYYMMDDTHHMM — Title` format.


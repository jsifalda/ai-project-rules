## Project Overview

Personal monorepo of AI-tool instructions: rules, skills, and slash commands used by Claude Code, Copilot CLI, Gemini CLI, Cursor, and any other agent that reads markdown. Tool-agnostic where possible.

## Repository Layout

- `rules/` — rule files (frontmatter `type` is honored only by tools that name them). `general.md` (core) loads via `CLAUDE.md`'s First Action on every session. `builder.md` (task-first stack guidance + default tools) loads on demand, only when a new-app build or stack/tooling choice is in play. Frontend aesthetics live in the `frontend-design` skill.
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
- **README lists are manually maintained — keep them in sync.** The `## Skills` table in `README.md` has one row per skill with three columns: skill name, one-line summary, and `Depends on`. When you add, remove, or rename a skill under `skills/`, update that table in the same change — add/remove/rename the row (skill name + a one-line summary drawn from its `SKILL.md` `description`) **and fill its `Depends on` cell**: list every other repo skill this one invokes/requires to function, or `—` if none. Disambiguation pointers ("use X instead") and sync-provenance (which upstream repo a skill came from) are not dependencies — leave the cell `—`. Likewise, when you add or remove a `gemini-cli/commands/*.toml`, update the "Current commands" list in `README.md`. There is no generator — drift only stays out if every skill/command change touches the README too.
- **New skills → consider `setup-aiengineering`.** When you add a skill under `skills/`, ask the user one question: is this a repo-bootstrapping or engineering-standards concern a project should adopt as part of its baseline setup (like ADRs, changelog, verification gates)? Most skills are not. Content, writing, research, persona, and one-off tool skills answer no and move on. If yes, fold it into `skills/setup-aiengineering/SKILL.md` as a module:
  - Add a row to its `## Modules` table with the delivery type: **inject** (a policy block → add a `references/<name>.md`, substitute placeholders in Step 5), **delegate** (it is its own `setup-*` skill → invoke in Step 6), or **scaffold** (copies a file or hook → Step 7).
  - Add it to the Step 4 module menu (default-selected) so users can opt out per project.
  - Wire it into the matching step (5, 6, or 7) and add it to the Step 8 report line.
  - Re-run `python skills/create-skill/scripts/quick_validate.py skills/setup-aiengineering/` after editing.

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

### When to create an entry

Create an entry only when the session made a change worth a future reader knowing:
- Code, config, or behavior changes — features, fixes, refactors
- Structural or dependency changes — added/removed dependency, moved or renamed files, layout changes
- Any **destructive or hard-to-reverse action** — deleting or moving files, dropping data, rewriting git history, removing a dependency (always log these)

Skip the entry for low-impact work that does not really change the project:
- Creating a standalone note, draft, or scratch markdown file in the folder
- Read-only work — research, answering questions, exploring code
- Trivial no-impact edits — a typo in a comment, reformatting

When in doubt, skip the noise — but never skip a destructive action.

Each agent session **that makes a qualifying change** (see _When to create an entry_ above) creates a **new file** in the `changelog/` directory:

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

### Commit the entry (autocommit)

When you create a new changelog entry, commit it automatically — do not ask first:

- **One bundled commit.** Stage the new `changelog/` file together with the related changes from this session that the entry documents, and commit them as a single commit. Use the conventional-commit format for the actual change (e.g. `feat: add foo skill`), not "add changelog" — the entry rides along with the work it describes.
- **Stage only related files.** Add the entry plus the files this session actually changed. Never `git add -A` / `git add .` — do not sweep unrelated working-tree files into the commit.
- **Already-committed work.** If the related changes were already committed earlier this session (e.g. per TDD cycle), commit the entry on its own as a follow-up (`docs: …`).
- **Local only — never push.** This is a local commit. Pushing still needs an explicit user instruction (see RESTRICTIONS in `rules/general.md`).
- **Let hooks run.** The pre-commit hooks (universality scanner + skill validator) must run — never `--no-verify`. If a hook fails, STOP, surface it, fix, then commit.

### File organization notes

- `changelog.md` at root is a **frozen archive** — do not edit
- New changelog entries go in `changelog/` as individual files
- Changes solely to `changelog/*.md` files are documentation-only and skip code verification protocols

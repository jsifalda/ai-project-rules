## First Action (MANDATORY)

- Before anything else, read `rules/general.md`, then follow the rules below.

## Project Overview

Personal monorepo of AI-tool instructions: rules, skills, and slash commands used by Claude Code, Copilot CLI, Gemini CLI, Cursor, and any other agent that reads markdown. Tool-agnostic where possible.

## Repository Layout

- `rules/` — rule files (frontmatter `type` is honored only by tools that name them). `general.md` (core) loads via `CLAUDE.md`'s First Action on every session. `builder.md` (task-first stack guidance + default tools) loads on demand, only when a new-app build or stack/tooling choice is in play. Frontend aesthetics live in the `frontend-design` skill.
- `skills/` — agent skills following [agentskills.io](https://agentskills.io/specification). Each subdir has a `SKILL.md`.
- `gemini-cli/commands/` — `.toml` slash commands for Gemini CLI (`description` + `prompt` with `{{args}}`).
- `create-prd.md`, `generate-tasks.md`, `process-task-list.md`, `feature-request.md` — standalone PRD workflow prompts (the original AI Dev Tasks pipeline). Outputs to `_prds/`, `_tasks/`, `_tickets/` (gitignored).
- `scripts/` — `check-universality.sh` (policy scanner) and `install-hooks.sh` (one-time hook activation for a clone).
- `.githooks/` — tracked `pre-commit` hook; runs the universality scanner + skill validator on staged files. Activated by `install-hooks.sh` setting `core.hooksPath`.
- `AGENTS.md` — symlink to `CLAUDE.md`.
- `changelog/` — one entry file per agent session, `YYYYMMDDHHMMSS-short-slug.md`. See `## Changelog` below.
- `changelog.md` — **frozen archive** of pre-`changelog/` entries. Do not edit or append.

## Skills Sync

- Skills are auto-synced into `~/.claude/skills/` by a `SessionStart` hook.
- **Canonical hook script**, in this repo: `skills/setup-skills-autorefresh/scripts/sync-skills.js`. It symlinks every skill from a **source folder passed as an argument** into `~/.claude/skills/`, and prunes removed ones.
- **Install/register on a machine** with the `setup-skills-autorefresh` skill: `bash skills/setup-skills-autorefresh/scripts/install.sh <skills-dir>`. That bakes the source folder into the hook command in `~/.claude/settings.json`.
- **Copilot CLI** uses a parallel script at `~/.copilot/hooks/sync-skills.js` that copies (not symlinks, due to a Copilot CLI bug) skills into `~/.copilot/skills/`.
- The hook script is the source of truth — read it for sync behaviour.

## Conventions

- **Skill files** follow the [agentskills.io](https://agentskills.io/specification) spec. Frontmatter requires at least `name` + `description`.
- **Skill validation**: run `python skills/create-skill/scripts/quick_validate.py skills/<your-skill>/` before committing — after **editing** an existing skill too, not just when adding a new one (a bad `description` most often lands via a later edit). The pre-commit hook runs the same validator on every staged `SKILL.md`, but it is per-clone (needs `bash scripts/install-hooks.sh`) and `--no-verify`-bypassable, so treat it as a backstop, not a guarantee. Parser-strictness rules to know (each silently passes Claude Code but breaks Copilot CLI):
  - `description` must not contain `": "` (colon + space) — YAML plain-scalar terminator. Use ` — ` or `, ` instead.
  - `description` must be ≤1024 chars (target ≤950 for headroom).
- **Rule files** use `type: "always_apply"` frontmatter when meant to load on every session.
- **Gemini commands** are `.toml` with `description` and `prompt` fields. Use `{{args}}` for user-supplied input.
- **README lists are manually maintained — keep them in sync.** There is no generator — drift only stays out if every skill/command change touches the README too.
  - The `## Skills` table in `README.md` has one row per skill, with these columns: skill name, one-line summary, `Depends on`, and `Origin`.
  - When you add, remove, or rename a skill under `skills/`, update that table in the same change — add/remove/rename the row (skill name + a one-line summary drawn from its `SKILL.md` `description`) **and fill its `Depends on` and `Origin` cells**.
  - `Depends on`: list every other repo skill this one invokes/requires to function, or `—` if none — disambiguation pointers ("use X instead") and sync-provenance are not dependencies, leave this cell `—` for those.
  - `Origin`: if the skill was synced from an upstream repo (see the sync scripts in `scripts/`), link the cell to that upstream repo's root (e.g. `mattpocock/skills`, `kepano/obsidian-skills`); `—` for skills native to this repo.
  - Likewise, when you add or remove a `gemini-cli/commands/*.toml`, update the "Current commands" list in `README.md`.
- **New skills → consider `setup-aiengineering`.** When you add a skill under `skills/`, ask the user one question: is this a repo-bootstrapping or engineering-standards concern a project should adopt as part of its baseline setup (like ADRs, changelog, verification gates)? Most skills are not. Content, writing, research, persona, and one-off tool skills answer no and move on. If yes, fold it into `skills/setup-aiengineering/SKILL.md` as a module:
  - Add a row to its `## Modules` table with the delivery type: **inject** (a policy block → add a `references/<name>.md`, substitute placeholders in Step 5), **delegate** (it is its own `setup-*` skill → invoke in Step 6), or **scaffold** (copies a file or hook → Step 7).
  - Add it to the Step 4 module menu (default-selected) so users can opt out per project.
  - Wire it into the matching step (5, 6, or 7) and add it to the Step 8 report line.
  - Re-run `python skills/create-skill/scripts/quick_validate.py skills/setup-aiengineering/` after editing.

## Identifiers

- **No sequential or counter-based ids for anything authored in this repo, or in a repo a skill from this repo sets up.** Banned: `adr-01`, `ADR-002`, `TODO-3`, `AUTH-05` — and any instruction telling an agent to take "the next free number" / "the next number", or to increment/renumber a set of ids.
- **Use date + slug instead**: `YYYY-MM-DD-slug` when one artifact per day is enough; `YYYYMMDDHHMMSS-slug` when two can land the same day (this repo's `changelog/` already uses the timestamp form). Slug is 2–5 words, kebab-case. The date-plus-slug pair *is* the identity — no separate counter needed.
- **Why**: "next number" needs a global read of every existing item first. Two agents on two branches or worktrees read the same state and pick the same number, and the collision only shows up at merge — after inbound references already point at the wrong item. Date-plus-slug is chosen from local information only, so parallel authors never collide.
- **Copy these in-repo precedents**, don't reinvent: `setup-adrs` (`YYYY-MM-DD-slug`), `setup-todo-backlog` (`TODO-YYYY-MM-DD-slug`), `changelog/` (`YYYYMMDDHHMMSS-slug`).
- **Ids are immutable once landed.** Supersede, never re-date or renumber an existing one — renumbering breaks every inbound reference silently.
- **Not covered by this rule** — ordinary ordinals aren't identifiers, leave them alone: numbered list steps, hierarchical PRD task ordinals (`1.0` / `1.1` / `2.0`), citation markers (`[1]`, `[2]`), semver versions, and filenames an external CLI produces. Also explicitly out of scope: `create-implementation-plan`'s within-document ids (`REQ-001`, `TASK-001`, etc.) — that document is single-author with no cross-file handles, so a counter there is fine.

## Counts

`rules/general.md` under `# COUNTS IN INSTRUCTIONS` holds the whole rule. Read it there.

It binds every file here — a `SKILL.md`, a rule file, a `description`, a `README` row.

`changelog/20260811075111-writing-standard-and-counts-rules.md` records a worked example. A skill
advertised a smaller category set than its reference file defined, and nothing caught it.

## Writing Style

All prose this repo produces uses **ASD-STE100 Simplified Technical English**. The commit subject
line and the PR title are exempt and keep the conventional-commit format.

`rules/general.md` under `# WRITING STYLE` holds the whole rule. Read it there. Do not restate or
re-scope it in this file — a second copy drifts.

## Key Rules

- **Simplicity first**: minimal code changes, no side effects.
- **No laziness**: find root causes, senior developer standards.
- **Self-improvement loop**: after any correction, learn from it, be proactive.
- **Plan mode**: enter plan mode for any non-trivial task (3+ steps).
- **Conventional commits**: `feat:`, `fix:`, `refactor:`, etc.

## Restrictions

- Never push to remote git unless user explicitly says to.
- Never install anything, anywhere — no global, `--user`, venv, or one-off installs, for any purpose. Ask first. Full policy + ask-first protocol: RESTRICTIONS in `rules/general.md`.

## Universality requirement

This repo is **public and reusable**. Every file added here — skill, rule, script, command — must work for any reader without modification. No personal data, secrets, employer names, internal URLs, or hardcoded identities. If something is machine- or person-specific, take it from an env var, a runtime prompt, or the agent's private memory — not from a file checked into this tree.

### What "non-universal" means

| Category | Forbidden | Use instead |
|---|---|---|
| Filesystem paths | `/Users/<name>/...`, `/home/<name>/...`, `C:\Users\<name>\...` | `~`, `${HOME}`, repo-relative paths, or `$(dirname "$0")`-derived paths |
| People | Real personal names, handles, emails, account/mention IDs | `<your-name>`, `<USER>`, generic placeholders, or "the user" |
| Employer / org | Company names, team names, internal product codenames | `<your-company>`, `<team>`, or omit entirely |
| Internal URLs | `*.internal`, internal Confluence space slugs, intranet hosts | Public docs links, or instruct the reader to set their own |
| Project IDs | Specific JIRA project keys (`ABC-`), Linear slugs, Notion DB IDs | `<PROJECT-KEY>` placeholder + a "configure this" note |
| Secrets | API keys, tokens, OAuth client IDs/secrets, passwords | `$ENV_VAR` references; never literal values, even fake-looking ones |
| Account IDs | Atlassian accountIds, Slack user IDs, GitHub user numeric IDs | "lookup at runtime" or `<account-id>` |
| Personal directories | Obsidian vault paths, dotfile locations specific to one machine | Ask the user at runtime, or read from a config var |
| Personal preferences as universal rules | "We always do X here" without justification | Either justify universally, or move to the user's private global memory |

Generic engineering preferences with universal rationale (e.g. "prefer pnpm because of lockfile speed") are fine — these are advice, not identity.

Bad → good, inline:

- `bash /Users/<name>/instructions/skills/foo/scripts/sync.sh` → `bash "$(dirname "$0")/scripts/sync.sh"`
- `Search the ACME Confluence space` → `Search the configured space ($CONFLUENCE_SPACE)`
- `api_key: "sk-live-…"` → `api_key: "$OPENAI_API_KEY"`

### The scanner

```bash
bash scripts/check-universality.sh                      # whole repo (tracked files)
bash scripts/check-universality.sh path/to/a path/to/b  # specific files or dirs (used by pre-commit)
```

It flags absolute `/Users/<name>/`, `/home/<name>/`, `C:\Users\<name>\` paths; names in `scripts/universality-denylist.txt` (clone-local, gitignored — each contributor adds their own name + employer); common secret shapes (`api_key="…"`, `AKIA…`, `ghp_…`, `xox[baprs]-`); and `*.internal` / `*.corp` hostnames. Exit 0 = clean, non-zero = commit blocked.

**Never add a file to the scanner's `SKIP_REL` allowlist to silence a hit** — fix the content instead. The allowlist exists only for the scanner and denylist files, which must quote the patterns they forbid.

### Setup for new clones

```bash
bash scripts/install-hooks.sh                    # sets core.hooksPath=.githooks; idempotent, installs nothing
cp scripts/universality-denylist.txt.example scripts/universality-denylist.txt
# then edit the denylist to add your own name, employer, internal team names
```

### When you find a violation

Don't bypass — fix the source. Replace the leaked value with a placeholder, env var, or runtime lookup. If the content genuinely belongs in *some* file, it belongs in the agent's private global memory, not in this public repo.

## Verification Protocol (MANDATORY)

> **Repo-local, and it OVERRIDES any markdown-only verification exemption.** In this repo the instructions *are* the product — a `SKILL.md` or rule edit ships to every consumer, so it gets reviewed like code.

### When it fires

- Every substantive change, before the task is reported done.
- Skips only: a changelog-only entry, a single typo, pure reformatting.
- **Integration-only exemption — Step 2 lenses only.** When the session's only change is integrating
  already-reviewed work — a merge, rebase, cherry-pick, or revert — and it authored no new lines
  beyond selecting among existing sides, skip Step 2 entirely (both lenses). Everything else still
  runs: Step 1's local gates, plus whatever tests or checks the change warrants.
  - **Void the moment you write a line neither side had** — a semantic conflict resolution, a
    reconciling fix-up, a post-merge adjustment. Then both lenses run, scoped to what you wrote.
  - **Show the evidence, never skip silently.** Report the skip alongside the diff proving nothing
    was authored — `git show --cc --format="" <integration-sha>` (empty output) for a merge,
    `git range-diff <old-base>..<old-tip> <new-base>..<new-tip>` for a rebase or cherry-pick. That
    only proves the integration commit itself is clean, so pair it with
    `git diff <integration-sha>..HEAD` (also empty), where `<integration-sha>` is the merge commit or
    the replayed tip — a later commit that authored lines is exactly what voids the exemption, and
    neither command above can see it. A non-empty result is not a formality — it is the diff the
    lenses must review.

### Step 1 — local gates (free + fast, run these first)

- `bash scripts/check-universality.sh <changed paths>` → must exit 0.
- `python skills/create-skill/scripts/quick_validate.py skills/<name>/` → must pass, for every touched skill.
- Both scripts already exist in this repo. Reuse them — never reimplement the checks.

### Step 2 — review lenses (run BOTH in PARALLEL, against the dirty working tree)

- **CodeRabbit** → `cr review --agent --uncommitted --include-untracked`. Collect every finding, wait for the review to complete. Those flags are verified against CodeRabbit CLI v0.7.1 — there is no `--type` flag, so do not "correct" them to one. Confirm with `cr review --help` before changing this line.
- **Harness-native** → the `code-review` agent on this session's changes (Claude Code: the Agent tool with `subagent_type: "code-review"`).
- **This section is STANDING AUTHORIZATION to spawn that agent in this repo** — it overrides any default rule against calling the Agent tool unless asked. Do not ask first.
- **CodeRabbit egress is pre-authorized in this repo — do not ask before running it.** This tree is public by construction (see `## Universality requirement`), so nothing in it is withheld from a third-party reviewer by design. Note the pre-commit scanner runs on **staged** files, so untracked files swept in by `--include-untracked` have not passed it at review time. That is not a reason to ask — it is a reason to keep the scanner clean on every path you touch, including new ones. This overrides any general "confirm before sending code to a cloud service" rule an agent may carry, **for this repo only** — it says nothing about any other tree. If a working-tree file ever does hold sensitive content, that is a universality violation to fix at the source, not a reason to skip the lens.

### Step 3 — merge

- Wait for both lenses. Deduplicate findings by `file:line` and by substance → emit one combined findings list.

### Step 4 — triage by severity

CodeRabbit's severities, highest first: `critical`, `major`, `minor`. It may also emit `trivial` and `info` — both rank below `minor`.

- `critical` + `major` → fix WITHOUT asking, then re-verify per Step 5.
- `minor` and below → do NOT touch. List each as `file:line — finding — recommended action` and WAIT for the user's decision.
- **Normative carve-out — this beats the severity rule.** Auto-fix covers *factual* defects only: a broken command or flag, a dead link or anchor, a reference to something that does not exist, a typo, or a wrong count of a tool's documented behavior (how many severity values it emits). A **policy** number is not a factual one — a retry limit, a budget, a threshold, a coverage percentage is normative, so it asks. A finding that would **change what an agent is required to do** — adding, removing, weakening, or re-scoping a rule — is NEVER auto-applied at any severity. Draft the wording, show it, ask. In this repo the rules *are* the product; a review heuristic must not silently rewrite binding policy.
- The harness `code-review` lens rates on its own scale, which does not map 1:1 onto CodeRabbit's → normalize before merging: a correctness or security defect with a concrete failure scenario ranks `major`; style, naming, and simplification rank `minor`. Keep the lens's own label in the report rather than overwriting it.
- **A lens can be wrong about this repo's tooling.** Verify any finding that contradicts a command you have actually run — `--help` output and a successful invocation beat a reviewer's recollection of a CLI. Reject with the evidence; never "fix" a working command into a broken one.
- Ambiguous → treat it as `minor` and ask.

### Step 5 — re-verify + re-review budget

- After auto-fixes, re-run Step 1 **and both Step 2 lenses** — not CodeRabbit alone. A fix can introduce a defect only the other lens sees.
- Budget: one extra round. Further loops need user approval — each `cr review` costs credits.

### Step 6 — then commit

- Write the changelog entry and make the single bundled commit per the `## Changelog` section below. Hooks must run — never `--no-verify`.

### When a lens cannot run

- `cr` missing from `PATH`, `cr auth status` failing, or a review erroring out → label it `skipped (CodeRabbit unavailable — <reason>)` in the report, state the fix command (`cr auth login`), and continue with the other lens.
- Never skip silently. A skipped lens does NOT block the task from being reported done.

### Report before done

Print one block covering:

- Per-lens finding counts by severity, or `skipped (<reason>)`.
- What was auto-fixed.
- What is waiting on the user.

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

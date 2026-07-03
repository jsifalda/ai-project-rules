---
name: setup-aiengineering
disable-model-invocation: true
description: Bootstrap a project's AI-engineering best practices in any repo — injects genericized agent-instruction policy blocks (mandatory verification protocol with lint/typecheck/test/coverage gates, dual-track code review, git policy, file organization, and an optional PRD gate) into AGENTS.md/CLAUDE.md, delegates doc systems to the setup-adrs, setup-changelog, and setup-user-scenarios skills, and scaffolds a worktree auto-bootstrap hook plus a detected .worktreeinclude. Stack-agnostic — detects build/test commands per repo (Node, Python, Go, Rust, or config/IaC) and degrades gracefully when none exist. Use when the user says "set up ai engineering", "scaffold best practices in this repo", "apply my engineering standards here", "bootstrap agent instructions", or runs /setup-aiengineering. Do NOT use to author a single ADR or changelog entry, to edit existing policy sections one-off, or to set up only one of the sub-systems (call that specific setup skill directly).
---

# Setup AI Engineering

Replicate a reference project's AI-engineering setup into any other repo: agent instructions plus
quality gates plus doc systems, in one pass. The skill **assesses** the target, lets the user
**pick** which modules to apply, then **injects** policy blocks, **delegates** doc systems to the
dedicated setup skills, and **scaffolds** the worktree bootstrap.

Everything injected is generic and parameterized — build/test commands are detected per repo, so a
TypeScript app, a Python service, and a Docker-config repo each get a correct, working setup.

## Modules

| Module | Delivery |
|--------|----------|
| Verification protocol (lint → typecheck → test → coverage → code review) | inject (`references/verification-protocol.md`) |
| Git policy | inject (`references/git-policy.md`) |
| File organization | inject (`references/file-organization.md`) |
| PRD gate (require a PRD before substantial features) — opt-in | inject (`references/prd-gate.md`) |
| ADRs | delegate → `setup-adrs` |
| Changelog | delegate → `setup-changelog` |
| User scenarios (BDD) | delegate → `setup-user-scenarios` |
| Worktree auto-bootstrap | scaffold (`assets/setup-worktree.sh` + SessionStart hook, plus a detected `.worktreeinclude`) |

## Workflow

### Step 1: Ensure the agent instructions file (runs first, guarded)

Pick the target by first match: `AGENTS.md` at root → `CLAUDE.md` at root → `.claude/CLAUDE.md`.

- **None exist** → create `AGENTS.md` at root (with a `# <Project> — Agent Instructions` title), then
  `ln -s AGENTS.md CLAUDE.md` at root so Claude Code reads the same file.
- **Only `AGENTS.md` exists, no `CLAUDE.md`** → create the `CLAUDE.md → AGENTS.md` symlink.
- **A real `CLAUDE.md` exists** → never overwrite it with a symlink. If it's a separate file from
  `AGENTS.md`, inject into `AGENTS.md` and tell the user `CLAUDE.md` is separate to reconcile.
- **`CLAUDE.md` already symlinks to `AGENTS.md`** → one file, inject once.

This runs for every repo type — a config-only repo still gets an `AGENTS.md`.

### Step 2: Detect the stack

Detect, read-only:
- **Package manager** — `pnpm-lock.yaml`→pnpm, `yarn.lock`→yarn, `package-lock.json`→npm.
- **Lint / typecheck / test commands** — per the detection table in
  `references/verification-protocol.md` (each gate independent; some or all may be absent).
- **Default branch** — `git symbolic-ref --short refs/remotes/origin/HEAD` (strip `origin/`), else
  `git branch --show-current`, else `main`.

If no lint/typecheck/test tool exists at all (e.g. a Docker-config repo), note that the verification
module will degrade to code-review-only.

### Step 3: Backfill from implementation (working repos — prompt the user)

Detect greenfield vs working repo (heuristic in `references/backfill-guide.md`).

- **Greenfield** → fresh `AGENTS.md` title + chosen policy blocks only.
- **Working repo** → ask: *"This repo already has code. Want me to draft `AGENTS.md` (overview,
  detected tech stack, dev commands, key files) from the current implementation instead of a
  policy-only file?"* On **yes**, do the read-only survey and write a grounded body following
  `references/backfill-guide.md` (only claim what the repo evidences, mark `(inferred)`, never
  invent). `ARCHITECTURE.md` backfill is handled by the ADR module's own prompt — don't duplicate.

### Step 4: Module menu

Present the eight modules and let the user pick per project. Seven default to selected —
deselect to opt out. The **PRD gate is opt-in — default it OFF**, and select it only if the user
wants PRD-first enforcement. If the repo has no build tooling, flag the verification module as
degraded and let them keep or skip it.

### Step 5: Inject the policy modules

For each chosen inject module (verification, git policy, file organization, PRD gate):
1. Read the matching `references/*.md`.
2. Substitute `{{...}}` placeholders with detected commands; **drop gates with no tool and
   renumber** (verification only).
3. Append the `##` section to the target file. If its heading already exists, **ask** before
   replacing — never silently duplicate.

### Step 6: Delegate the doc-system modules

For each chosen doc-system module, invoke the dedicated skill against the same repo:
- ADRs → `setup-adrs`
- Changelog → `setup-changelog`
- User scenarios → `setup-user-scenarios`

Each appends its own distinctly-headed `##` section, so they stack safely with Step 5. Let each
skill run its own assess/prompt logic (e.g. `setup-adrs` asks before drafting `ARCHITECTURE.md`).

### Step 7: Worktree auto-bootstrap

If chosen:
1. Copy `assets/setup-worktree.sh` → target `scripts/setup-worktree.sh` (`chmod +x`).
2. Register a `SessionStart` / `startup` hook in the target `.claude/settings.json` running
   `bash scripts/setup-worktree.sh`. Create the file if missing; merge into existing `hooks` if
   present (don't clobber other hooks).
3. Generate a `.worktreeinclude` so Claude-created worktrees also get non-regenerable gitignored
   config. The hook reinstalls derivable deps; `.worktreeinclude` carries over secrets/config that
   can't be rebuilt (`.env` and friends), so together a fresh worktree is runnable.
   - **WorktreeCreate guard (first):** if the target `.claude/settings.json` already has a
     `hooks.WorktreeCreate` entry, Claude ignores `.worktreeinclude` — warn the user to copy local
     config inside that hook instead, and skip the rest of this substep.
   - **Probe** the repo root for gitignored config: `.env`, `.env.local`, `.env.*` (excluding
     `*.example` / `*.sample`), `config/secrets*`, `*.local`. Run `git check-ignore <path>` on each
     match — Claude copies a file only when it is gitignored *and* matched.
   - **Ask** "any other local files to carry over?" — ask even when the probe finds nothing, so a
     repo-specific file isn't missed.
   - **Propose + confirm:** show the proposed `.worktreeinclude` (`.gitignore` syntax), let the user
     adjust, then write it once at the repo root. If the file already exists, append only missing
     lines and preserve existing order/comments — never clobber. `.worktreeinclude` lists paths, not
     secrets, so it is committed and tracked like `.gitignore`.
   - Monorepo package envs (e.g. `packages/*/.env`) are a manual add.
   - Empty result (no matches, nothing added) → skip; note no `.worktreeinclude` was needed.

### Step 8: Verify and report

Confirm in one short message:
- Agent file created/located; `CLAUDE.md → AGENTS.md` symlink (if created).
- Policy modules injected (with which gates were dropped for missing tools).
- PRD gate injected (or skipped, since it is opt-in).
- Doc-system skills delegated (or skipped).
- Worktree hook scaffolded (or skipped).
- `.worktreeinclude` created/updated (with which files), skipped (no gitignored config or user
  declined), or N/A (a `WorktreeCreate` hook is present).
- Whether `AGENTS.md` / `ARCHITECTURE.md` were backfilled from the implementation or left as
  templates.

## Rules

- Inject into the project's existing agent file (first match: `AGENTS.md` → root `CLAUDE.md` →
  `.claude/CLAUDE.md`). If none, create `AGENTS.md` and symlink `CLAUDE.md → AGENTS.md`. Never
  overwrite a real `CLAUDE.md` with a symlink.
- Never inject an empty or guessed command — drop the gate instead.
- Never duplicate a `##` section — detect the heading and ask before replacing.
- Backfill only for working repos, only on user opt-in, and only grounded in real files.
- Idempotent — re-running detects existing sections/hooks and asks rather than clobbering.
- `.worktreeinclude` is probe-then-ask, root-only, and merge-not-clobber; skip it when a
  `WorktreeCreate` hook is present or no gitignored config is found.
- PRD gate is opt-in (default off) and injected verbatim — it has no `{{...}}` placeholders.

## References

- `references/verification-protocol.md` — verification block + stack-detection table + placeholders.
- `references/git-policy.md` — git policy block.
- `references/file-organization.md` — file organization block.
- `references/prd-gate.md` — PRD-gate policy block (opt-in; require a PRD before substantial features).
- `references/backfill-guide.md` — greenfield-vs-working heuristic, survey + grounding rules.

## Assets

- `assets/setup-worktree.sh` — generic, package-manager-detecting worktree bootstrap script copied
  into the target as `scripts/setup-worktree.sh`.

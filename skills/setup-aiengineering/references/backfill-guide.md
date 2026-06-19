# Backfill Guide — drafting AGENTS.md from a working codebase

Use this when the target repo already has real code and the user opts in to backfilling docs from
the implementation (instead of leaving a policy-only `AGENTS.md`). The goal is a concise, accurate
recap grounded in what the repo actually contains — not aspirational or invented docs.

## Greenfield vs working repo

A **working repo** has real source: a `src/`, `lib/`, `app/`, or `packages/` directory, or a
populated manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`) alongside actual
source files. **Greenfield** = empty, or only config/docs. Only prompt to backfill for a working
repo; greenfield gets a fresh title + the chosen policy blocks.

## Survey (read-only)

Gather, changing nothing:

- **README** — product/one-liner, setup notes.
- **Manifest** — name, description, dependencies, and the **scripts** (these become the dev commands
  and the detected lint/test commands).
- **Directory tree** — top-level layout, main source dirs, entry points.
- **A few entry points** — the app/server bootstrap, main exports, route or command registration.

## AGENTS.md body sections to draft

Fill each from real files; omit a section if the repo gives no evidence for it.

- **Project Overview** — what it is, in 1–3 sentences, from README + manifest description.
- **Tech Stack** — language/runtime, framework, data store, key libraries — from the manifest and
  lockfile. List only what's actually depended on.
- **Development Commands** — the manifest's scripts (install, dev, build, test, lint), verbatim.
- **Project Structure / Key Files** — main directories and a few important entry-point files with a
  one-line purpose each.
- **Conventions** (optional) — only observable patterns: test setup, lint/format config, a naming or
  structure pattern that clearly repeats.

`ARCHITECTURE.md` is handled separately by the ADR setup, which has its own "draft from
implementation" prompt — don't duplicate it here.

## Grounding rules (do not skip)

- Only claim what the repo evidences. If you're inferring, mark it `(inferred)`.
- Never invent components, decisions, dependencies, or commands.
- Keep it a concise recap, not exhaustive documentation. Link out rather than copy large content.
- Prefer omission over a guess. An empty section is better than a wrong one.

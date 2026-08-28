# Backfill Guide — drafting project docs from a working codebase

Use this when the target repo already has real code and the user opts in to backfilling docs from
the implementation. The goal is a concise, accurate recap grounded in what the repo actually
contains — not aspirational or invented docs.

**No backfilled documentation goes into the agent instructions file.** That file holds directives and
read-first pointers only, per `references/instructions-scope.md`. Every drafted section is written to
`README.md` or `ARCHITECTURE.md`, and the agent file receives a pointer to it. The one thing it may
receive directly is a Conventions one-liner that passes the scope test — see the routing table below.

## Greenfield vs working repo

A **working repo** has real source: a `src/`, `lib/`, `app/`, or `packages/` directory, or a
populated manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`) alongside actual
source files. **Greenfield** = empty, or only config/docs. Only prompt to backfill for a working
repo; greenfield gets a fresh title + the chosen policy blocks.

## Survey (read-only)

Gather, changing nothing:

- **README** — product/one-liner, setup notes, and **which sections it already has** (this decides
  what you may append).
- **Manifest** — name, description, dependencies, and the **scripts** (these become the dev commands
  and the detected lint/test commands).
- **Directory tree** — top-level layout, main source dirs, entry points.
- **A few entry points** — the app/server bootstrap, main exports, route or command registration.

## Where each section goes

Draft each from real files; omit a section if the repo gives no evidence for it.

| Section | Destination | Content |
|---|---|---|
| Project Overview | `README.md` | What it is, in 1-3 sentences, from README + manifest description. |
| Tech Stack | `README.md` | Language/runtime, framework, data store, key libraries — from the manifest and lockfile. List only what is actually depended on. |
| Development Commands | `README.md` | The manifest's scripts (install, dev, build, test, lint), verbatim. |
| Project Structure / Key Files | **deferred** — `ARCHITECTURE.md`, else `README.md` | Main directories and a few important entry-point files, one line of purpose each. |
| Conventions | agent instructions file | **Only** as imperative one-liners an agent must follow every session. Anything that explains rather than binds goes to `ARCHITECTURE.md`. |

**Project Structure / Key Files is deferred, and that is deliberate.** `ARCHITECTURE.md` is
`setup-adrs`' file, and the backfill step runs *before* the module menu and before that skill is
delegated — so the file cannot exist yet and a branch on it would always be false. Survey and draft
the section during the backfill, then hand it to SKILL.md Step 6d, which resolves the destination
once the delegation has actually run: `setup-adrs` already populated the file → discard the draft;
the file holds only the blank template → append to it; the file does not exist → append to
`README.md`. Never create `ARCHITECTURE.md` from here.

## Writing rules for the destination files

- **Create or append, never clobber.** A section heading already in `README.md` is the user's — show
  the drafted replacement and ask before touching it. Absent heading → append the new section.
- **`ARCHITECTURE.md` is `setup-adrs`' file**, and only Step 6d writes to it — append only, and
  route to `README.md` rather than creating it. Do not evaluate its existence during the backfill
  itself; at that point the answer is always "no" and it means nothing.
- **Link new sections from `README.md`'s documentation list** where the repo keeps one, per
  `references/file-organization.md`.

## What the agent instructions file gets

Read-first pointers only, one per document actually written. Each pointer names its trigger:

```markdown
## Architecture

Read `ARCHITECTURE.md` before planning any change.
```

```markdown
## Project setup

Read `README.md` for the stack, the dev commands, and how to run this repo.
```

Plus any Conventions one-liners that pass the scope test in `references/instructions-scope.md`.
Nothing else. No overview paragraph, no stack list, no command table, no directory tree.

## Grounding rules (do not skip)

- Only claim what the repo evidences. If you are inferring, mark it `(inferred)`.
- Never invent components, decisions, dependencies, or commands.
- Keep it a concise recap, not exhaustive documentation. Link out rather than copy large content.
- Prefer omission over a guess. An empty section is better than a wrong one.

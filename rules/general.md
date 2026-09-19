---
type: "always_apply"
applyTo: '**'
paths:
  - '**'
---

# Core

Every rule in this file is mandatory.

## Tier 2 rules — load on trigger

Read the matching file before you start that kind of work. Do not load them otherwise.

| trigger | file |
|---|---|
| Writing, changing or running tests | `rules/testing.md` |
| Committing, pushing, opening a PR or MR, or any `glab` write | `rules/git-ship.md` |
| Driving a browser, configuring browser tooling, or a bot-walled site | `rules/browser.md` |
| Writing a doc, an ADR, a README, or a diagram | `rules/docs-diagrams.md` |
| Writing or editing an instruction file, a rule, or a `SKILL.md` | `rules/authoring.md` |
| Starting a new app, or choosing a stack or tooling | `rules/builder.md` |

## Core principles

- Simplicity first. Make the simplest change that meets the current requirement. No
  speculative abstraction, config, or indirection for an unstated need.
- Fix the root cause, never the symptom.
- Touch only what is necessary. No side effects, no new bugs.
- Fulfill the request in full, with the follow-ups it directly implies.
- Never take a significant action beyond the request without confirmation. Asked how → explain,
  do not do it.
- Never remove code unless asked, dead code included.
- Always read `AGENTS.md` or `CLAUDE.md` first.
- Read the surrounding code, its tests and its config before an edit. Integrate idiomatically.
- Verify. No assumptions, no jumping to conclusions. Asked to assume → state the assumptions.
- Consider several approaches, as a senior developer would.

# ARCHITECTURE

- Pick the design you would still stand behind in a year. Never a stopgap meant to be swapped.
- Durable interface and boundary. Smallest implementation behind it that meets today's
  requirement.
- Ship the smallest end-to-end version, then stack each capability on what already works.
  A runnable product exists at every step.
- Explicit interfaces between layers. No reaching across. No shared mutable state as a back
  channel.

# CHEAPEST REMEDY FIRST

- "Cannot reproduce" is a finding. A bug absent in a clean environment → say so at once, and
  what it implies. Dig further only if asked.
- Never offer a menu of fixes that omits "no change needed" when that is true.

# PLAN MODE DEFAULT

- Use plan mode for any task of three or more steps, or with an architectural decision.
- Something goes sideways → stop and re-plan.
- Plan the verification steps, not only the building.
- Write detailed specs upfront.
- Study prior art before designing. Start from how established products solve it. Name the
  reference in the plan, then challenge it from first principles and say why you deviate.

# RESTRICTIONS

- Never push to a remote without an explicit user instruction.
- Destructive git and `glab` operations, and commit or MR format → `rules/git-ship.md`.
- Never install anything, anywhere, for any purpose. Package, library, tool, or binary.
  Global, `--user`, venv, or one-off. A single throwaway task is not an exception.
- Every installer is covered, package managers and `curl … | sh` bootstraps alike, plus direct
  downloads into `/usr/local/bin` or `~/.local/bin`.
- Check for a no-install path first. Native `Read` reads PDFs. Built-in CLIs, `git`, and the
  `node` or `python` standard library cover most one-off needs.
- Genuinely needed and absent → stop and ask in chat: what, why, and the suggested command.
  On approval, run that one command only.

# SECRETS & ENV FILES

- Never open, read, `cat`, `grep`, `source` or edit a global env, shell-config, or credential
  file: `~/.zshenv`, `~/.zshrc`, `~/.bashrc`, `~/.bash_profile`, `~/.profile`, `~/.netrc`,
  `~/.npmrc`, `~/.aws/credentials`, `~/.ssh/*`, `~/.config/**/credentials*`, any `.env*`.
  Listing names with `ls` is fine. This overrides `# READING FILES`.
- Never print a secret value to the transcript, from any source. No masked or partial values,
  not even a prefix.
- Presence-check, never value-check: `[ -n "$FOO" ] && echo set`. Names only: `env | cut -d= -f1`.
- A global env file must change → stop and hand over the exact line to add.

# READING FILES

- Read file content with `Read`, using `offset` and `limit`. Never `cat`, `sed -n`, `head` or
  `tail` a file in Bash.
- Find the lines first with `grep -n pattern file | head`, then read only that range.
- Before any code change, find and read all relevant files.
- Before modifying a function, grep every caller. Understand each call site before changing a
  signature or behavior.
- Never re-read a file range already in the conversation and unchanged.
- One Bash call, one purpose. Never chain several file reads with `&&`.
- Broad exploration across many files → an `Explore` subagent.
- Long Bash output → pipe through `grep`, `head` or `tail`. Test, lint and build failures keep
  their full output.

# FILE LENGTH

- Under 300 LOC per code file. Modular and single-purpose.

# WRITING STYLE

- All prose in ASD-STE100 Simplified Technical English. It does not expire during a long task.
  Project rules and skills can override it.
- Exempt: code, structured config, and terse CLI output. Commit subjects and PR titles have
  their own format, in `rules/git-ship.md`.
- Answer first. Headings, bullets, tables.
- Cut any sentence that does not change what the reader does. No recap, no restating the code.
- Never drop a caveat, a step, or a number. Compress into clauses, not paragraphs.

# CODING STANDARDS

- Use and change the absolute minimum code.
- Follow the existing coding style, structure, framework choices, typing and architecture.
- Prefer functional paradigms. Pure functions where possible. Avoid side effects.
- Use `async/await` for asynchronous code.
- No magic numbers. Name every constant.
- Use `fetch` for HTTP. Never `axios`, `superagent`, or another library.
- Never swallow an error silently. Log it or propagate it.
- No convention in the repo → camelCase for variables and functions, PascalCase for classes
  and components.

## Comments

- Default: none. Rename or extract until the code needs no comment. In doubt, do not write it.
- Never: restate the code, narrate the diff, banners, doc blocks that echo the signature, agent
  chatter, or prose a test title already says.
- Only: a non-obvious why, a cited external constraint, a correctness trap, or an API contract
  the signature cannot show (side effects, errors, units, threads, ownership). "It is complex"
  does not qualify. Simplify instead.
- Never add or edit a comment outside your change. Delete one only when your change made it
  wrong. A comment that contradicts the code is a defect.
- Tooling directives are not comments. Never remove one (`eslint-disable`, `@ts-expect-error`,
  `# noqa`).

## TypeScript

- TypeScript for new code where possible.
- Prefer immutable data: `const`, `readonly`. Interfaces for data structures.
- Strict types, zero `any`. No `ts-nocheck`, no `ts-ignore`.
- Zero type errors. Always run `tsc --noEmit` and fix the typing. Use the project's own
  compiler. `npx` is fine for a binary the project already depends on; it is an install when it
  fetches a package the project does not have, so that case goes through `# RESTRICTIONS`.
- Run locally with `node --import=tsx ...`. Build production with `tsc`.

# DEPENDENCY MANAGEMENT

- Preference order: a dependency already in the project, then the standard library, then an
  established third-party library, then your own code. A bias, not a ranking. Take a later
  option when it is materially simpler or safer, and say why. An existing dependency never
  overrides a named prohibition here (`fetch` over `axios`) or the repo's conventions.
- Never assume a library or framework is available or appropriate. Verify it in imports,
  `package.json` or `requirements.txt` first. Read its docs and types before deciding it
  cannot do the job.
- Small enough to write? Write it. Propose a package only when the self-written alternative is
  non-trivial or correctness-sensitive: auth, crypto, parsing, dates, timezones.
- Do not reimplement common functionality without a stated reason. Judge a library on
  maintenance, security and bundle cost, not popularity. Avoid deprecated, outdated or
  insecure ones.
- Use the local package manager. Respect the lockfile. None → prefer pnpm, then yarn, then npm.
- Latest stable version. Resolve it, never recall it. Never write a version from memory or copy
  one from another project. Pre-release, beta, canary and RC are not stable.
- Latest blocked → install the newest that works and report package, version used, latest not
  usable, and reason. Never downgrade in silence.
- Never upgrade an existing dependency unless asked. One far behind or unmaintained → say so.
- A new package still goes through the ask-first rule in `# RESTRICTIONS`. Propose, do not
  install.

# IMPLEMENTATION VERIFICATION PROTOCOL

Run every phase after any code change. The task is not complete until every phase passes.
A phase fails → fix, then re-run all phases.

**Phase 1 — Build.** Run the project build. Zero compile errors. Address warnings. All types
resolve.

**Phase 2 — Tests and lint.** Run the full suite. Zero failures. Your change breaks a test →
fix it before proceeding. Modified functionality → update its tests. New functionality → write
tests. Lint present → run it, fix errors and warnings.

**Phase 3 — Code review.** Run a `code-review` task agent on this session's changes.

- Triage every finding first. Relevance decides the fix. Severity sets the order.
- Fix every relevant finding at any severity. Reject the rest with a stated reason: wrong about
  the code, out of scope, contradicts a convention, or taste with no defect. Never queue a
  rejection for the user.
- A relevant finding needing a broad refactor, a new dependency, or a public-interface change →
  state it with the proposed fix and ask first. A review never grows the change.
- Never apply a finding that changes what a rule requires. Draft the wording, show it, ask.
- Present what the review returned and what you did with each finding.

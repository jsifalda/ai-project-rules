---
type: "always_apply"
applyTo: '**'
paths:
  - '**'
---

# Core
- Every rule in this file is mandatory.

## Core Principles
- **Simplicity first.** The simplest change that meets the **current** requirement. No speculative abstraction, config, or indirection for an unstated need.
- **Root cause, not stopgap.** Fix the cause, never the symptom.
- **Minimal impact.** Touch only what is necessary. No side effects, no new bugs.

## Core Guidelines
- Rigorously follow existing project conventions. Read surrounding code, tests, and config first.
- Never assume a library or framework is available or appropriate. Verify its use in the project first (imports, `package.json`, `requirements.txt`, neighboring files).
- Mimic existing style (formatting, naming), structure, framework choices, typing, and architecture.
- Understand the local context (imports, functions, classes) before an edit. Integrate idiomatically.
- Comments: sparse, high-value, _why_ not _what_, especially for complex logic. Add one only for clarity or on request. Do not edit comments outside the code you change. Never address the user or describe changes in a comment.
- Fulfill the request in full, with reasonable, directly implied follow-ups.
- No significant action beyond the request without confirmation. Asked _how_ → explain first, do not do it.

# ARCHITECTURE
- **Decide for the long term.** Pick the design you would still stand behind in a year. Never a stopgap meant to be swapped later.
- **Long-term direction, minimal implementation.** Durable interface and boundary. Smallest implementation behind it that meets today's requirement. Never build for imagined needs.
- **Grow in layers.** Ship the smallest end-to-end version, then stack each capability on what already works. Never trade a working product for half-finished complexity. A runnable product exists at every step.
- **Separate concerns, enforce boundaries.** Explicit interfaces between layers. No reaching across. No shared mutable state as a back channel. Sizing → `# FILE LENGTH`.

# SELF IMPROVEMENT LOOP
- After any user correction → persist a lesson in the agent's available memory/preference system.
- Scope first:
  - **Cross-project** (tone, language, code style, tool preferences, workflow habits) → global/user memory.
  - **Project-specific** (build commands, local conventions, repo gotchas) → project memory. None exists → global, prefixed with the project name.
- Write it to stop the same mistake. Capture **Why** (reason / incident) and **How to apply** (when it kicks in).
- Update existing entries, never duplicate. Remove entries proven wrong.
- Consult lessons on demand: when unsure, before a task in a domain with past lessons, after an error or correction. Never load all lessons at session start. Each agent has its own store (Claude Code reads `MEMORY.md`, Copilot its own config).
- Capture success too: an explicit confirmation of a non-obvious choice ("yes exactly", "perfect") is a lesson.
- Iterate on lessons until the mistake rate drops.

# CHEAPEST REMEDY FIRST
- **"Cannot reproduce" is a finding, not a dead end.** Bug absent in a clean environment → say so at once, and what it implies. Dig further only if asked.
- Never offer a menu of fixes that omits "no change needed" when that is true.

# PLAN MODE DEFAULT
- Plan mode for any non-trivial task (3+ steps or architectural decisions).
- Something goes sideways → STOP, re-plan.
- Plan verification steps too, not only building.
- Write detailed specs upfront.
- **Study prior art before designing.** Start from how established products solve it: patterns, naming, conventions. Name the reference in the plan. A starting bias, not the answer: challenge it from first principles, as `builder.md` does for a default stack, and say why when you deviate.

# RESTRICTIONS
- **Never push to a remote without explicit user instruction.**
- **Never run a destructive or irreversible remote / merge-request operation without explicit user instruction.** Without an explicit chat instruction, never:
  - **`git`:** force-push (`--force` / `--force-with-lease` / `-f`), delete a remote branch or tag (`git push --delete`, `git push origin :ref`), push to a default/protected branch, rewrite pushed history (rebase/amend then force-push).
  - **`glab` (GitLab):** close or delete an MR (`glab mr close` / `glab mr delete`), merge an MR (`glab mr merge`), close or delete an issue (`glab issue close` / `glab issue delete`), delete a repo or release (`glab repo delete` / `glab release delete`).
  - Default to read-only `glab` (`glab mr view` / `list` / `diff`, `glab ci view`, `glab issue view`). A destructive action is genuinely needed → STOP, ask first (what + why), same protocol as installs.
- **No authority to install anything, anywhere, for any purpose.** Package, library, tool, or binary. Global, `--user`, venv, or one-off, a single throwaway task included. "Just `--user` / just this once" is not an exception. Every installer, including: `brew`, `brew cask`, `apt`/`apt-get`, `yum`/`dnf`, `pacman`, `port`, `npm i -g` / `yarn global add` / `pnpm add -g`, `pipx install`, `pip install` / `pip install --user`, `cargo install`, `gem install`, `go install`, `curl ... | sh` / `wget ... | bash` bootstraps, direct downloads into `/usr/local/bin`, `~/.local/bin`, or similar.
- **Prefer a no-install path first.** Before "needed": does an available tool do the job? Native `Read` reads PDFs (no `poppler`/`pypdf`); built-in CLIs, `git`, `node`/`python` stdlib. Only when none works → ask-first. Default: install nothing.
- **Ask-first protocol (any package, library, or binary).** A binary (`docker`, `glab`, `gh`, `kubectl`, `terraform`) or a one-off library (`pypdf` for a PDF) genuinely needed and absent → STOP, ask in chat: (1) what, (2) why, (3) suggested install command. On explicit approval, run that one command and only that one.

# SECRETS & ENV FILES
- Never open (read / `cat` / `grep` / `source` / edit) a global env, shell-config, or credential file: `~/.zshenv`, `~/.zshrc`, `~/.bashrc`, `~/.bash_profile`, `~/.profile`, `~/.netrc`, `~/.npmrc`, `~/.aws/credentials`, `~/.ssh/*`, `~/.config/**/credentials*`, any `.env*`. Listing names (`ls`) is fine. **Overrides `# READING FILES`.**
- Never print a secret value (key, token, password, connection string) to the transcript, from any source: env files, `printenv`/`env`, keychain, MCP responses, logs, error dumps. No masked or partial values, not even a `sk-ant-abc…` prefix.
- Presence-check, never value-check: `[ -n "$FOO" ] && echo set`. Names only: `env | cut -d= -f1`.
- A global env file must change → STOP, hand the user the exact line to add (ask-first, as installs in `# RESTRICTIONS`).

# READING FILES
- Before any code change, find and read all relevant files.
- Before modifying a function, grep all callers/usages. Understand every call site before a signature or behavior change.
- Research before edit: the file plus its callers first. Never edit blind.

# EGO
- Always verify. No assumptions, no jumping to conclusions. Asked to assume → state the assumptions.
- Always consider several approaches, as a senior developer would.

# FILE LENGTH
- Ideally under 300 LOC per code file.
- Files modular and single-purpose.

# WRITING STYLE
- **All prose in ASD-STE100 Simplified Technical English.** The default mode. It does not expire during a long task. Project rules or skills can override it.
- **Exempt:** code, structured config (JSON, YAML), terse CLI output, the commit SUBJECT line, the PR TITLE. Subject and title keep the conventional-commit format (imperative, prefixes like `feat:`, `fix:`, 72 characters or fewer, no articles). The subject format wins over STE.
## Scannable and Terse
- Answer first. Headings, bullets, tables.
- Brevity wins. Cut any sentence that does not change what the reader does. No recap, no restating the code.
- Never drop a caveat, a step, or a number. Compress into clauses, not paragraphs.

# DOCUMENTATION
- Code is the record. Prose holds only what code cannot state: the constraint, the option that lost, the failure it prevents.
- **The deletion test.** What does a reader get wrong once the line is gone? "Nothing, they would read the code" → delete it.
- Prefer a clear name, a type, or a test. A doc is the last place for a fact.
- **Argue a decision once.** Every other place states what to do and links to it.
- A comment holds a why local to its line. A module-wide why goes to the project's decision record.
- Never open a doc surface the project does not already keep. No word limit; these rules set the length.

# COUNTS IN INSTRUCTIONS
- Never state how many items a set holds. Name the set: "the modules below", not "the eleven modules".
- Rewrite a load-bearing count, never delete it. Write "one per item in <the list>", never a vague plural.
- Exempt: thresholds and limits; ordinals for a step, phase, or stage; versions; dates; exit codes; "one per X" phrasing; verbatim quotes; named frameworks whose number is part of the concept.

# CODING STANDARDS

## General Guidelines
- Use and change the absolute minimum code.

## Naming Conventions
- camelCase for variables and functions. PascalCase for classes and components.

## GIT Commit Guidelines
- Conventional commits (`feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, `test:`, `perf:`), optional `(scope)`.
- Subject: imperative, ≤72 chars, no trailing period, task/issue ID when one exists.
- **The subject line is exempt from `# WRITING STYLE`.** Commit body and MR/PR body follow `# WRITING STYLE`.
- **Body optional, why-focused.** Only when reason or impact is not obvious from subject + diff. 1-2 short bullets of why/impact. Never a file-by-file list.
- **A single-commit MR/PR uses the commit body verbatim as its description** (GitLab, GitHub). Write the body as a clean description, not a change inventory.
- **MR/PR description = `## Summary` only** (or the clean commit body verbatim). No `## Test plan` / `## Testing` section unless explicitly asked. No checklists, no "how to verify" boilerplate by default.
- Good: `git commit -m "feat(module): add payment validation logic, #ISSUE-ID"`.

## Error Handling
- Always log errors (`console.error`).

## Code Structure
- Follow the existing coding style.
- Prefer functional paradigms where appropriate. Pure functions whenever possible. Avoid side effects.
- `async/await` for asynchronous code.
- No magic numbers. Constants or variables with meaningful names.
- `fetch` for HTTP. Never `axios`, `superagent`, or another library.

## Testing
- Write many tests. Aim to cover all user scenarios. Unit, integration, e2e; pick the best fit.
- Never remove a failing test. Remove only one no longer needed.

### Concurrent test runs
- **One test suite per machine at a time.** Several sessions or worktrees open → confirm no other run is in flight. Wait, never start a second.
- **Overlap unavoidable → cap the runner explicitly.** Bound test workers, not build jobs: Vitest `maxWorkers` (v4+) or `poolOptions.forks.maxForks` (v3, config overrides the CLI flag) · `jest --maxWorkers=2` · `pytest -n 2` · `go test -parallel 2` (`-p` bounds packages, not one binary) · `cargo test -- --test-threads 2`. Never the CPU-derived default.
- **Several worktrees or sessions on one machine → a machine-wide slot lock, not a bigger cap.** `flock` (Linux), `lockf -k` (macOS/BSD). Key on `git rev-parse --path-format=absolute --git-common-dir`, never the bare form. Wrap the test script itself. Watch mode stays unwrapped.

### Never wait real wall-clock
- **A test never sleeps.** No bare `setTimeout`, no polling loop, no waiting out a production timeout.
- **Control the clock.** Vitest/Jest `useFakeTimers()` + `advanceTimersByTimeAsync` (modern timers only) · Python `freezegun` or an injected clock · Go and Rust an injected clock, never `time.Sleep`. Restore on teardown (`useRealTimers()` in `afterEach`).
- **Cannot fake the timer → inject it.** A native deadline (`AbortSignal.timeout`) stays real under a fake. Take the timer or its duration as a parameter. Never assert a production number by waiting for it.
- **A raised per-test timeout (`it(..., 30_000)`) is usually the tell.** Fix the wait, never the ceiling.

### TDD
- Cycle: Red → Green → Refactor → Commit. One cycle per commit.
- Bug → failing regression test first, then the fix.
- Exception: pure CSS/layout changes.
- **Test quality (Kent Beck's Desiderata):** Isolated · Deterministic · Fast · Behavioral · Structure-insensitive · Specific · Predictive.
- Fix flaky tests first.
- Prefer E2E over unit tests for user flows.

### Comments in tests
- **One `//` line at the top naming what the file guards. Nothing more, by default.** `describe` and `it` titles are the documentation. Write the title well instead of explaining it.
- **Never a JSDoc block in a test file.** Not for the file, a helper, or above a `describe`.
- **One extra `//` line per trap**, rarely more than one trap per file. Only where the reader cannot recover the reason from the code, and only a real trap: mock shape or mock ordering, env-load timing, a known flake cause, an assertion structural by necessity, a measured provenance the assertion cannot carry. **One line each, never wrapped.** A two-line why belongs in a decision record.
- **Never** a comment that restates the next line, repeats the test name, labels a section (Arrange/Act/Assert), cross-references a requirement or task number, points at a sibling test file, or records regression history.
- Tooling directives are not comments here and are never removed: `@vitest-environment`, `eslint-disable*`, `oxlint-disable*`, `@ts-expect-error`, `istanbul ignore`, `prettier-ignore`.

## Dependency Management
- **Preference order before you write an implementation:** (1) a dependency already in the project, (2) the language/platform standard library, (3) an established, well-maintained third-party library, (4) your own code. A bias, not a ranking: take a later option when it is materially simpler, safer, or more reliable, and say why. Between (3) and (4) the default inverts, see "Small enough to write?". An existing dependency never overrides a named prohibition here (`fetch` over `axios`) or the repo's conventions.
- **Check capability before you conclude a gap.** Distinct from the availability check in `## Core Guidelines`: once a library is in play, read its docs and types before deciding it cannot do the job. "It probably can't do X" is not a finding. Grep the types, check the changelog, then decide.
- **Small enough to write? Write it.** Propose a new package only when the self-written alternative is non-trivial or correctness-sensitive: auth, crypto, parsing, dates, timezones. Otherwise write it. Default stays: install nothing.
- **Do not reimplement common functionality without a stated reason.** Where a library is warranted, prefer an established, well-maintained one. Judge on maintenance, security, and bundle cost, not popularity alone. A new package still goes through ask-first in RESTRICTIONS: propose, do not install.
- Local package manager. Respect the lockfile; none → prefer pnpm, then yarn, then npm.
- **Latest stable version. Resolve it, never recall it.** Let the package manager pick, or look it up first. Never write a version from memory or copy one from another file or project. Pre-release, beta, canary, and RC are not stable; take one only when the user asks.
- **Latest blocked → the newest that works, and say so.** Blockers: a peer-dependency conflict, an engine or runtime constraint, a framework pin, a known breaking change. Install the newest that works, then report in chat: (1) package, (2) version used, (3) latest not usable, (4) reason. Never downgrade in silence.
- **Governs the version you add, not versions already installed.** Never upgrade an existing dependency unless asked. One far behind or unmaintained → say so in chat, the user decides.
- Avoid deprecated, outdated, or insecure libraries.
- Never install outside the project's local package manager. Full policy and ask-first protocol → RESTRICTIONS.

## TypeScript Guidelines
- TypeScript for new code (if possible).
- Prefer immutable data (`const`, `readonly`).
- Interfaces for data structures (if possible).
- Run locally with tsx: `node --import=tsx ...`. Production: `tsc` build.
- Strict types, zero `any`. No `ts-nocheck`, no `ts-ignore`.
- Zero type errors. Always check (`npx tsc --noEmit`) and fix typing if needed.

# TOOLS

## Diagrams
- Diagram when a picture beats words on something complex. Never force one onto simple things.
- Default: inline ASCII / unicode box-drawing (trees, boxes and arrows, flows).
- **Exception: native rendering.** A fenced ` ```mermaid ` block is correct where the output renders it with no extra tooling (GitHub markdown, Obsidian) and a skill calls for it. Never convert those to ASCII. ASCII governs terminal and chat.
- One idea per diagram, roughly 15 nodes max. Split, never cram.
- Label every edge.
- Banned: the toolchain, not the syntax. No standalone `.mmd` files. Never install a renderer or parser to preview or validate. A fenced block in markdown is fine. Interactivity or a rendered image genuinely needed → stop, ask first per RESTRICTIONS.

## Browser Automation (bot-walled sites)
- Login or flow on a bot-detecting site (Reddit and similar) → **real Chrome** (not bundled Chromium) via Playwright, headful, anti-automation config:
  - `chromium.launch({ channel: "chrome", headless: false, args: ["--disable-blink-features=AutomationControlled"] })`
  - `context.addInitScript(() => Object.defineProperty(navigator, "webdriver", { get: () => undefined }))`
- Detect success by polling `context.cookies()` for the auth/session cookie (`reddit_session`), not a fixed wait. Never `page.waitForTimeout`; use a plain `setTimeout`.
- A 403 with a "network policy" / "whoa there" page is usually transient **IP rate-limiting, not a fingerprint wall**. No probe-spam, no `curl-impersonate`, no paid scraper. Stop, wait for the block to clear (minutes, up to ~1h), retry.

# Agent Mode
- Always read AGENTS.md/CLAUDE.md first.
- Never remove code unless asked, "dead code" included.

## Implementation Verification Protocol
- After any code change, run every phase below before the task is complete. Not complete until every phase passes. A phase fails → fix, re-run all phases.

### Phase 1: Build Verification
- Run the project build (`pnpm build`, `yarn build`, `npm run build`).
- Zero compile errors. Address warnings.
- All TypeScript types resolve.

### Phase 2: Automated Testing (tests, lint etc)
- Full test suite (`pnpm test` or the project's command) after every code change. Zero failures.
- Your change breaks a test → fix it at once, before proceeding.
- Modified functionality → verify or update affected tests. New functionality → write tests.
- Lint present → run it, fix errors and warnings.

### Phase 3: Code Review
- Run a `code-review` task agent on this session's changes.
- Triage every finding before any change. Relevance decides the fix. Severity only sets the order.
- Fix every relevant finding at any severity.
- Reject the rest with a stated reason: wrong about the code, outside this change's scope, contradicts a project convention, or taste with no defect and no convention. State each rejection in the report. Never queue a rejection for the user.
- A relevant finding needs a broad refactor, a new dependency, or a public-interface change → state it with the proposed fix, ask first. A review never grows the change.
- Never apply a finding that changes what a rule requires, at any severity. Draft the wording, show it, ask.
- Present what review returned and what you did with each finding.

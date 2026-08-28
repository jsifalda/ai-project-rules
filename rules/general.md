---
type: "always_apply"
applyTo: '**'
paths:
  - '**'
---

# Core (ALWAYS ADHERE THIS)
- Everything in this file is a mandatory rule!

## Core Principles

- **Simplicity First:** Make every change as simple as possible. Impact minimal code. Choose the simplest implementation that fully meets the **current** requirements — no speculative abstraction, configuration, or indirection for a need nobody has stated yet.
- **No Laziness:** Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact:** Only touch what's necessary. No side effects with new bugs.

## Core Guidelines

- Rigorously adhere to existing project conventions when reading or modifying code. Analyze surrounding code, tests, and configuration first.
- NEVER assume a library/framework is available or appropriate. Verify its established usage within the project (check imports, configuration files like 'package.json', 'requirements.txt' etc., or observe neighboring files) before employing it.
- Mimic the style (formatting, naming), structure, framework choices, typing, and architectural patterns of existing code in the project.
- When editing, understand the local context (imports, functions/classes) to ensure your changes integrate naturally and idiomatically.
- Add code comments sparingly. Focus on _why_ something is done, especially for complex logic, rather than _what_ is done. Only add high-value comments if necessary for clarity or if requested by the user. Do not edit comments that are separate from the code you are changing. _NEVER_ talk to the user or describe your changes through comments.
- Fulfill the user's request thoroughly, including reasonable, directly implied follow-up actions.
- Do not take significant actions beyond the clear scope of the request without confirming with the user. If asked _how_ to do something, explain first, don't just do it.
- Prioritize simplicity and minimalism in your solutions.

# ARCHITECTURE

- **Decide for the long term.** Pick the design you would still stand behind in a year. Never accept a stopgap that only works for now and is meant to be swapped out later — that is the "No Laziness" rule applied to structure, not just to bug fixes.
- **Long-term direction, minimal implementation.** When the two pull apart, make the *interface and the boundary* durable and keep the *implementation behind it* the smallest thing that meets today's requirements. A durable decision is never a licence to build for imagined future needs.
- **Grow the system in layers.** Ship the smallest version that works end to end, then stack each new capability on top of something that already works. Never trade a working product for half-finished complexity — at every step there is a product that runs.
- **Separate concerns, enforce boundaries.** Explicit interfaces between layers, no reaching across them, no shared mutable state as a back channel. Sizing and single-purpose guidance lives in `# FILE LENGTH`.

# SELF IMPROVEMENT LOOP

- After ANY correction from the user → persist a lesson using your agent's available memory/preference system
- Decide scope before saving:
  - **Cross-project** rules (tone, language, code style, tool preferences, workflow habits) → save to the agent's global/user memory
  - **Project-specific** rules (build commands, local conventions, repo gotchas) → save to the agent's project-scoped memory if one exists; otherwise fall back to global and prefix with the project name
- Write the rule so it prevents the same mistake recurring; capture **Why** (the reason / past incident) and **How to apply** (when it kicks in)
- Update existing entries rather than duplicating; remove entries that turn out wrong
- Consult prior lessons on demand: when you are unsure, before a task in a domain you have past lessons about, or after an error or correction. Do not eagerly load all lessons at session start. Each agent has its own memory store (Claude Code reads `MEMORY.md`, Copilot reads its own config); load the relevant lesson when it applies.
- Capture from success too, not only correction: if the user explicitly confirms a non-obvious choice ("yes exactly", "perfect"), that is also a lesson worth saving
- Ruthlessly iterate on these lessons until mistake rate drops

# PLAN MODE DEFAULT

- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity
- **Study prior art before designing.** Look at how established products solve this problem and start from their proven patterns, naming, and conventions rather than inventing one. Name the reference in the plan. This is a starting bias, not the answer — challenge it from first principles the same way `builder.md` says to challenge a default stack, and say why when you deviate.

# RESTRICTIONS

- **NEVER run destructive or irreversible remote / merge-request operations unless the User explicitly tells you to** — this extends the push rule above. Without an explicit chat instruction, never:
  - **`git`:** force-push (`--force` / `--force-with-lease` / `-f`), delete a remote branch or tag (`git push --delete`, `git push origin :ref`), push to a default/protected branch, or rewrite already-pushed history (rebase/amend then force-push).
  - **`glab` (GitLab):** close or delete a merge request (`glab mr close` / `glab mr delete`), merge an MR (`glab mr merge`), close or delete an issue (`glab issue close` / `glab issue delete`), or delete a repo or release (`glab repo delete` / `glab release delete`).
  - Default to **read-only `glab`** for inspection (`glab mr view` / `list` / `diff`, `glab ci view`, `glab issue view`). When a destructive action is genuinely needed, STOP and ask first (what + why) — same protocol as installs.
- You have no power or authority to install **anything** — any package, library, tool, or binary — **anywhere** (global, `--user`, into a venv, or as a one-off) and for **any** purpose, including a single throwaway task. "It's not global, it's just `--user` / just this once" is NOT an exception. This applies to **every** installer, including but not limited to: `brew`, `brew cask`, `apt`/`apt-get`, `yum`/`dnf`, `pacman`, `port`, `npm i -g` / `yarn global add` / `pnpm add -g`, `pipx install`, `pip install` / `pip install --user`, `cargo install`, `gem install`, `go install`, any `curl ... | sh` / `wget ... | bash` bootstrap scripts, and direct downloads into `/usr/local/bin`, `~/.local/bin`, or similar.
- **Prefer no-install paths first:** before treating anything as "needed," check whether a tool already available does the job — e.g. the native `Read` tool reads PDFs directly (no `poppler`/`pypdf`), plus built-in CLIs, `git`, and the `node`/`python` stdlib. Only when none works do you reach the ask-first step below. Default is to install nothing.
- **Ask-first protocol (any package, library, or binary):** if something — a binary (e.g. `docker`, `glab`, `gh`, `kubectl`, `terraform`) OR a one-off library (e.g. `pypdf` to read a PDF) — is genuinely needed to finish the job and is not already present, **STOP and ask the user in chat first**. State: (1) what, (2) why it is needed, (3) the suggested install command. **On the user's explicit approval, run that one specific install command** (and only that one).

# SECRETS & ENV FILES

- NEVER open — read / `cat` / `grep` / `source` / edit — global env, shell-config, or credential files: `~/.zshenv`, `~/.zshrc`, `~/.bashrc`, `~/.bash_profile`, `~/.profile`, `~/.netrc`, `~/.npmrc`, `~/.aws/credentials`, `~/.ssh/*`, `~/.config/**/credentials*`, any `.env*`. Listing names (`ls`) is fine. **Overrides `# READING FILES`.**
- NEVER print a secret value (key, token, password, connection string) to the transcript — from ANY source: env files, `printenv`/`env`, keychain, MCP responses, logs, error dumps. No masked/partial values either — a `sk-ant-abc…` prefix still leaks entropy and shape. **Why:** anything read is in the transcript; the transcript is not a secret store.
- Presence-check, never value-check: `[ -n "$FOO" ] && echo set`. Names only: `env | cut -d= -f1`.
- Need a global env file changed → STOP, hand the user the exact line to add themselves (ask-first, same shape as installs in `# RESTRICTIONS`).

# READING FILES

- before making any code changes, start by finding & reading ALL of the relevant files
- never make changes without reading the entire file
- before modifying a function, grep for ALL its callers/usages first → understand every call site before changing its signature or behavior
- research before you edit: read the file plus its callers/usages first, never edit blind

# EGO

- always verify; do not make assumptions or jump to conclusions (unless you are asked to do so; if so, state your assumptions clearly).
- always consider multiple different approaches, just like a Senior Developer would

# FILE LENGTH

- ideally, keep all code files under 300 LOC
- files should be modular & single-purpose

# WRITING STYLE

- **Write all prose in ASD-STE100 Simplified Technical English.** This is the default mode. It does not expire during a long task.
- **Does not apply to:** code, structured config (JSON, YAML), terse CLI output, the commit SUBJECT line, and the pull-request TITLE. The subject line and the title keep the conventional-commit format (imperative mood, commentationals commits prefixes like `feat:`, `fix:`, 72 characters or fewer, no articles). The conventional-commit format and the STE full-sentence rule cannot both hold, so the subject format wins.
- STE is the default mode for all prose (not the code) Project rules or skills can override it.
## Scannable and Terse
- Put the answer first. Headings, bullets, tables.
- Brevity wins. Cut any sentence that does not change what the reader does. No recap, no restating the code.
- Never drop a caveat, a step, or a number. Compress into clauses, not paragraphs.


# COUNTS IN INSTRUCTIONS

- Never state how many items a set holds. Name the set — "the modules below", not "the eleven modules".
- Worst case is a count in a different file from the set. Nothing signals the drift.
- Rewrite a load-bearing count. Never delete it. Write "one per item in <the list>", never a vague plural.
- These are exempt: thresholds and limits, ordinals for a step, phase, or stage, versions, dates, and exit codes.
- These are also exempt: "one per X" phrasing, verbatim quotes, and named frameworks whose number is part of the concept.

# CODING STANDARDS

## General Guidelines

- use/change absolute minimum code needed

## Naming Conventions

- Use camelCase for variables and functions
- Use PascalCase for classes and components

## GIT Commit Guidelines

- Conventional commit format (`feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, `test:`, `perf:`), optional `(scope)`.
- Subject: imperative, ≤72 chars, no trailing period. Reference the task/issue ID when there is one.
- **The subject line is exempt from `# WRITING STYLE`.** It keeps the conventional-commit format above. The commit body and the MR/PR body follow `# WRITING STYLE`.
- **Body is optional and why-focused.** Add one only when the reason or impact isn't obvious from subject + diff. Keep to 1-2 short bullets of *why/impact*. Never list file-by-file what changed — the diff already shows that.
- **A single-commit MR/PR uses the commit body verbatim as its description (GitLab, GitHub).** Write the body as a clean MR description, not a change inventory — no noise.
- **MR/PR description = `## Summary` only** (or clean commit body verbatim). Never add a `## Test plan` / `## Testing` section unless I explicitly ask for one. No checklists, no "how to verify" boilerplate by default.
- Good: `git commit -m "feat(module): add payment validation logic, #ISSUE-ID"`.

## Error Handling

- Always log errors (console.error) for debugging purposes

## Code Structure

- When generating new code, please follow the existing coding style.
- Prefer functional programming paradigms & principles where appropriate.
- Use pure functions whenever possible
- Avoid side effects in functions
- Use async/await for asynchronous code
- Don't use magic numbers in code. Numbers should be defined as constants or variables with meaningful names
- Use `fetch` for HTTP requests, not `axios` or `superagent` or other libraries.

## Testing

- Write unit tests a lot (aim at least for covering all user scenarios)!
- Prefer the Jest runner if possible (if not possible, ask the user to choose a different runner - provide the best possible options to run tests in the context for the codebase)
- Never ever remove any tests if they are failing (only if there are no longer needed)

### Concurrent test runs

- **One test suite per machine at a time.** Several agent sessions or worktrees open → confirm no
  other run is in flight before you start one. Wait, never start a second.
- **Why:** a runner's parallelism cap is per process, not per machine. Each run reads the core
  count, not the **remaining** capacity. Each run also computes that cap alone. So N runs give
  N × the cap. CPU and RAM saturate, and the machine can livelock.
- **An overlap is unavoidable → cap the runner explicitly.** Pick the knob that bounds test
  workers, not build jobs: Vitest `maxWorkers` (v4+) or `poolOptions.forks.maxForks` (v3 — config
  overrides the CLI flag) · `jest --maxWorkers=2` · `pytest -n 2` · `go test -parallel 2` (`-p`
  bounds packages, not one binary) · `cargo test -- --test-threads 2`. Never leave it on the
  CPU-derived default.
- **A per-process cap cannot see its neighbours.** Several worktrees or sessions on one machine →
  serialize with a machine-wide slot lock, not a bigger cap: `flock` on Linux, `lockf -k` on
  macOS/BSD (`-k` orders the waiters). Key it on `git rev-parse --path-format=absolute
  --git-common-dir` — the bare form is relative in the main worktree, so keys would differ per
  worktree. Wrap the test script itself. Watch mode stays unwrapped: it never exits, so it would
  hold the slot forever.

### Never wait real wall-clock

- **A test never sleeps.** No bare `setTimeout`, no polling loop, no waiting out a production
  timeout in real time. It burns no CPU so it never reads as load, yet it holds a worker — pure
  queue under `### Concurrent test runs`. And a run never beats its slowest file, so one slow test
  floors the whole suite, whatever the core count.
- **Control the clock.** Vitest/Jest `useFakeTimers()` + `advanceTimersByTimeAsync` (modern timers
  only) · Python `freezegun` or an injected clock · Go and Rust an injected clock, never
  `time.Sleep`. Restore it on teardown (`useRealTimers()` in `afterEach`), else the next test
  inherits a frozen clock.
- **Can't fake the timer → inject it.** A fake replaces the JS timer only, so a native deadline
  (`AbortSignal.timeout`) stays real. Take the timer or its duration as a parameter — never assert
  a production number by waiting for it.
- **A raised per-test timeout is usually the tell.** `it(..., 30_000)` says the test waits — fix
  the wait, never the ceiling.

### TDD 

- Follow the cycle: Red → Green → Refactor → Commit.
- Keep to one cycle per commit.
- For bugs, write a failing regression test first, then fix the bug.
- Exception: pure CSS/layout changes.
- **Test quality (Kent Beck's Desiderata):** Isolated · Deterministic · Fast · Behavioral · Structure-insensitive · Specific · Predictive.
- Fix flaky tests first.
- Prefer E2E over unit tests for user flows.

## Dependency Management

- **Preference order, before you write an implementation:** (1) a dependency already in the project, (2) the language/platform standard library, (3) an established, well-maintained third-party library, (4) your own code. This is a bias, not a ranking to obey — take a later option when it is materially simpler, safer, or more reliable, and say why. Between (3) and (4) the default is inverted, see "Small enough to write?" below. An existing dependency never overrides a named prohibition in these rules (e.g. `fetch` over `axios`) or the repo's own conventions.
- **Check capability before you conclude a gap.** Distinct from the availability check in `## Core Guidelines`: once a library is in play, read its docs and its types before deciding it cannot do what you need. "It probably can't do X" is not a finding — grep the types, check the changelog, then decide.
- **Small enough to write? Write it.** Option (3) costs a user round-trip (ask-first, RESTRICTIONS), so propose a new package only when the self-written alternative is non-trivial or correctness-sensitive — auth, crypto, parsing, dates, timezones. Otherwise write it. Default stays: install nothing.
- **Do not reimplement common functionality without a stated reason.** Where a library is warranted, prefer an established, well-maintained one. Judge on maintenance, security, and bundle cost, not on popularity alone. Adding a *new* package is still governed by the ask-first protocol in RESTRICTIONS — propose it, do not install it.
- use local package manager (respect existing lockfile; if none present, prefer pnpm, then yarn, then npm)
- **Install the latest stable version. Resolve it, never recall it.** Let the package manager pick
  the version, or look the version up first. Never write a version string from memory, and never
  copy one from another file or another project. Pre-release, beta, canary, and release-candidate
  builds are not stable — take one only when the user asks.
- **Latest blocked? Take the newest that works, and say so.** A peer-dependency conflict, an engine
  or runtime constraint, a framework that pins the version, or a known breaking change can stop the
  latest version. Install the newest version that does work, then report in chat: (1) the package,
  (2) the version you used, (3) the latest version you could not use, and (4) the reason. Never
  downgrade in silence.
- **This governs the version you add, not the versions already installed.** Do not upgrade an
  existing dependency unless the user asks — that is a separate task with its own risk. When you
  see one that is far behind or no longer maintained, say so in chat and let the user decide.
- Avoid using deprecated, outdated and unsecured libraries
- Never install any dependency outside the project's local package manager — no
  global, `--user`, or one-off installs (e.g. `npm i -g`, `yarn global add`,
  `pnpm add -g`, `brew install`, `pipx install`, `pip install --user`, `cargo install`,
  `gem install`, `go install`, `curl ... | sh`, etc.). See the RESTRICTIONS section
  for the full policy and the ask-first protocol for any required package, library, or binary.

## TypeScript Guidelines

- Use TypeScript for new code (if possible)
- Prefer immutable data (const, readonly)
- Use interfaces for data structures (if possible)
- Use TSX "node --import=tsx ..." to run typescript locally (for production code use tsc build)
- Strict TypeScript types with zero "any"
- Dont use "ts-nocheck" or "ts-ignore"
- Dont allow any types errors - always check your TS (eg. with npx tsc --noEmit), and fix typing if needed

# TOOLS

## Diagrams

- Diagram when a picture beats words on something complex. Do not force one onto simple things.
- Default to inline ASCII / unicode box-drawing: trees, boxes and arrows, flows. Renders in a terminal, a diff, a code comment, and every markdown viewer. No tool, no build step, no asset to keep in sync.
- **Exception, where the target renders it natively.** A fenced ` ```mermaid ` block is correct when the output lands somewhere that renders it with no extra tooling — GitHub markdown, Obsidian — and a skill calls for it. Do NOT convert those to ASCII. The ASCII default governs terminal and chat output, where nothing renders.
- One idea per diagram, roughly 15 nodes maximum. Split rather than cram.
- Label every edge. An unlabelled arrow says things connect, not why.
- What is banned is the toolchain, not the syntax: no standalone `.mmd` files, and never install a renderer or parser to preview or validate a diagram. A fenced block inside a markdown file is not that. If a diagram genuinely needs interactivity or a rendered image, stop and ask first per RESTRICTIONS.

## Browser Automation (bot-walled sites)

- Automating a login or flow on a site that runs bot detection (Reddit, and similar) → drive **real Chrome** (not bundled Chromium) via Playwright, headful, with the anti-automation config, or the site's "network security" / bot check blocks the window:
  - `chromium.launch({ channel: "chrome", headless: false, args: ["--disable-blink-features=AutomationControlled"] })`
  - `context.addInitScript(() => Object.defineProperty(navigator, "webdriver", { get: () => undefined }))`
- Detect success by polling `context.cookies()` for the site's auth/session cookie (e.g. `reddit_session`), not a fixed wait. Do NOT use `page.waitForTimeout` (a redirect detaches the page) → use a plain `setTimeout`.
- A 403 serving a "network policy" / "whoa there" block page is usually transient **IP-level rate-limiting, not a fingerprint wall** (it also blocks a real browser from the same IP). Do not probe-spam to diagnose, and do not reach for `curl-impersonate` or a paid scraper. Stop, wait for the IP block to clear (minutes, up to ~1h), then retry.

# Agent Mode

- ALWAYS read AGENTS.md/CLAUDE.md file first
- dont remove any code, if not asked to (not even "dead code")
- Think carefully and only action the specific task I have given you with the most concise and elegant solution that changes as little code as possible.

## Implementation Verification Protocol

After completing any code changes, perform every verification phase below before considering the task complete:

### Phase 1: Build Verification

- Run the project's build command (e.g., pnpm build, yarn build, npm run build)
- Ensure zero compile errors and warnings are addressed
- Verify all TypeScript types resolve correctly

### Phase 2: Automated Testing (tests, lint etc)

- Run the full test suite (`pnpm test` or any other test command available) after **every** code change — no exceptions
- Ensure all existing tests pass — zero failures
- If your changes break existing tests, **fix them immediately** before proceeding
- If you modified functionality, verify affected tests still pass or update them accordingly
- If new functionality was added, write tests for it
- Run lint (if present in the project), fix any reported issues (errors and also warnings)

### Phase 3: Code Review

- Run a `code-review` task agent on the changes made in this session
- Triage every finding before you change anything. Relevance decides if you fix a finding. Severity only sets the order of the work
- Fix every relevant finding, at any severity. A low severity is never a reason to leave a real defect
- Reject the rest, and state the reason for each rejection. A finding is not relevant when it is wrong about the code, when it points outside the scope of this change, when it contradicts a convention the project already set, or when it is taste with no defect and no convention behind it. State each rejected finding in the report. Never queue a rejection for the user to clear
- When a relevant finding needs a broad refactor, a new dependency, or a change to a public interface, state it with the fix you propose, and ask first. A review never grows the change on its own
- Never apply a finding that changes what a rule requires, at any severity. Draft the wording, show it to the user, and ask
- Present to the user what review returned and what you did with each finding

CRITICAL: Do not mark implementation as complete until every verification phase passes. If any phase fails, fix the issues and re-run all phases.

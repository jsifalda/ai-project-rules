# Verification Protocol Template

Inject the `## Mandatory Verification After Code Changes` section below into the project's agent
instructions file. **Substitute the `{{...}}` placeholders** with commands detected from the repo
(see the detection table). **Omit any gate whose tool was not detected** — never inject an empty or
guessed command. Keep numbering contiguous after omissions (renumber the remaining gates).

## Stack detection

Detect each gate independently from the repo. A gate with no tool is dropped from the injected
block. Code review and docs alignment (the last two gates) are tool-agnostic and always kept.

| Gate | JS/TS | Python | Go | Rust | Config / IaC |
|------|-------|--------|----|------|--------------|
| Lint `{{LINT_CMD}}` | `<pm> run lint` (lint script) or `<pm> exec eslint .` | `ruff check .` / `flake8` | `go vet ./...` / `golangci-lint run` | `cargo clippy` | `hadolint <Dockerfile>`, `yamllint .`, `shellcheck <scripts>`, `terraform fmt -check` / `tflint` — only if the tool is on PATH |
| Typecheck `{{TYPECHECK_CMD}}` | `<pm> exec tsc --noEmit` (needs `tsconfig.json`) | `mypy .` (if configured) | — | — | — |
| Test `{{TEST_CMD}}` | `<pm> test` / `<pm> exec vitest run` | `pytest` | `go test ./...` | `cargo test` | — |
| Coverage `{{COVERAGE_CMD}}` | `<pm> exec vitest run --coverage` (or `jest --coverage`) with the threshold set in config (`coverage.thresholds` / `coverageThreshold`) — the runner enforces `{{COVERAGE_THRESHOLD}}` | `pytest --cov --cov-fail-under={{COVERAGE_THRESHOLD}}` | `go test -coverprofile=coverage.out ./...` then a threshold check on the total (e.g. `go tool cover -func=coverage.out`, fail if total < `{{COVERAGE_THRESHOLD}}`) | `cargo llvm-cov --fail-under-lines {{COVERAGE_THRESHOLD}}` (or `cargo tarpaulin --fail-under {{COVERAGE_THRESHOLD}}`) | — |

- `<pm>` = detected package manager: `pnpm` (`pnpm-lock.yaml`), `yarn` (`yarn.lock`), `npm`
  (`package-lock.json`). Default `npm` if a `package.json` exists with no lockfile.
- `{{DEFAULT_BRANCH}}` = the repo's default branch (`git symbolic-ref --short refs/remotes/origin/HEAD`
  stripped of `origin/`, or `git branch --show-current`; fall back to `main`).
- `{{COVERAGE_THRESHOLD}}` defaults to `90` and is user-adjustable at setup time. A repo's current
  real coverage may sit below it — the gate is aspirational for future changes, so the user may pick
  a lower starting number and raise it later.
- **No lint/typecheck/test tool at all** (e.g. a config-only repo) → inject only the **Code review**
  and **Docs & instructions alignment** gates plus the "no automated gates found" note at the
  bottom, and tell the user.

---

## Mandatory Verification After Code Changes

After ANY code change, run these checks before presenting the work. All are mandatory unless a step
says otherwise.

> **Exemption:** when changes are **solely** to markdown/docs (`*.md`), skip this protocol — no
> impact on builds, types, or tests.

1. **Lint** — `{{LINT_CMD}}` must pass with zero warnings and zero errors.
2. **Typecheck** — `{{TYPECHECK_CMD}}` must exit with **zero errors total**. "Pre-existing" errors
   do not get a pass: if the typechecker reports errors — even in files you did not touch — fix them
   before proceeding. A green typecheck is a gate, not a suggestion.
3. **Tests** — `{{TEST_CMD}}` must show zero failures.
4. **Test coverage for new code** — every new production module gets a co-located test file. Tests
   must cover (1) the main business goal, (2) the main user flow, and (3) error/edge cases (failure
   paths, empty/invalid inputs). Updating existing mocks is necessary but **not** sufficient — new
   logic needs dedicated tests. Exempt: pure type-only files, generated code, trivial re-exports,
   config. On top of that, overall repository coverage must stay at or above `{{COVERAGE_THRESHOLD}}%`
   — run `{{COVERAGE_CMD}}`, which fails the build itself when the total drops below the threshold.
   New tests for new code are necessary but not sufficient either: if the run reports the overall
   percentage under `{{COVERAGE_THRESHOLD}}%`, the gate fails and more tests are needed before
   proceeding.
5. **Code review** — run **all three** in parallel on this session's changes:
   - **5a. Harness-native code review** — invoke your harness's `code-review` agent (Claude Code:
     `Task` tool with `subagent_type: "code-review"`; Copilot CLI: the `code-review` skill). Cover
     bugs, security, logic errors, race conditions, unhandled edge cases, and the project's own
     conventions.
   - **5b. CodeRabbit CLI** — `cr review --agent --base {{DEFAULT_BRANCH}} --type all`. Collect every
     `type: "finding"` event; wait for `type: "complete"`.
     - **Prerequisites** — `cr` on `PATH` (`which cr`) and authenticated (`cr auth status`). If either
       fails, **tell the user and skip 5b** — label it `skipped (CodeRabbit unavailable)`; never skip
       silently.
     - **Triage** — `critical`/`major` → auto-apply the fix, then re-run gates 1–3. `minor`/`trivial`/
       `info` → do **not** auto-apply; list them for the user (file:line + suggested fix).
     - **Re-review budget** — at most one extra `cr review` after auto-fixes; further loops need user
       approval (each costs credits).
   - **5c. Nuclear structural review** — if the `code-review-nuclear` skill is available, spawn a
     subagent that runs it on this session's diff (Claude Code: `Task`/`Agent` tool → a subagent
     whose prompt invokes the skill against `{{DEFAULT_BRANCH}}...HEAD`). Structural /
     maintainability "code judo" only — NOT correctness, security, tests, or lint (5a and gates 1–4
     cover those). Surface its findings for the user; never auto-apply. If the skill isn't
     available, **tell the user and skip 5c** — label it `skipped (nuclear review unavailable)`;
     never skip silently.
   - **Merge** — wait for all three (5a, 5b, 5c) to finish — a `skipped` 5b or 5c still counts as
     done — then deduplicate findings across them and present one combined "Code review findings"
     section.
6. **Docs & instructions alignment** — before marking the task done, check whether this session's
   changes made any documentation stale:
   - **Project docs** (`README.md`, `docs/`, `ARCHITECTURE.md`, other human-facing docs) — stale
     docs are part of the change, like a failing test: update them now and list what was updated.
   - **Agent instructions** (`AGENTS.md` / `CLAUDE.md` and any rule files they link) — draft the
     updated wording and **ask the user** before applying. Never silently edit instruction files.
   - Nothing stale → say so explicitly in one line; do not invent updates.

If any check fails, fix and re-run. These gates are mandatory for every code change — no exceptions.

---

**Note for skill user**: Substitute `{{LINT_CMD}}`, `{{TYPECHECK_CMD}}`, `{{TEST_CMD}}`,
`{{COVERAGE_CMD}}`, `{{COVERAGE_THRESHOLD}}`, `{{DEFAULT_BRANCH}}` from detection. Drop any gate whose
tool is absent and renumber. The quantitative coverage requirement in gate 4 is dropped alongside the
test gate when no test framework/coverage tool exists — a repo with no tests has no coverage number
to gate on. If the project has no lint/typecheck/test tooling, keep only gates 5–6 (code review, docs
& instructions alignment; renumbered 1–2) and append: *"No automated lint/typecheck/test gates were
detected for this repo. Add them here when build tooling lands."* If a source repo has a test
framework but no coverage tooling, the skill wires `{{COVERAGE_THRESHOLD}}` once coverage tooling is
chosen — see `references/test-setup.md`.

**Version / drift.** This block's version is recorded by the versioned provenance note the skill
stamps (SKILL.md Step 5.4), not by a marker inside the block. On re-run upgrade mode (SKILL.md Step
1), when the stamped version is older than the current **Skill version**
(`references/baseline-checklist.md`), refresh a drifted injected block by diffing it against this
current template — diff-and-ask, preserve local edits, never clobber.

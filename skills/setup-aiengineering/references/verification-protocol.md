# Verification Protocol Template

Inject the `## Mandatory Verification After Code Changes` section below into the project's agent
instructions file. **Substitute the `{{...}}` placeholders** with commands detected from the repo
(see the detection table). **Omit any gate whose tool was not detected** — never inject an empty or
guessed command. Keep numbering contiguous after omissions (renumber the remaining gates).

## Stack detection

Detect each gate independently from the repo. A gate with no tool is dropped from the injected
block. Code review (last gate) is tool-agnostic and always kept.

| Gate | JS/TS | Python | Go | Rust | Config / IaC |
|------|-------|--------|----|------|--------------|
| Lint `{{LINT_CMD}}` | `<pm> run lint` (lint script) or `<pm> exec eslint .` | `ruff check .` / `flake8` | `go vet ./...` / `golangci-lint run` | `cargo clippy` | `hadolint <Dockerfile>`, `yamllint .`, `shellcheck <scripts>`, `terraform fmt -check` / `tflint` — only if the tool is on PATH |
| Typecheck `{{TYPECHECK_CMD}}` | `<pm> exec tsc --noEmit` (needs `tsconfig.json`) | `mypy .` (if configured) | — | — | — |
| Test `{{TEST_CMD}}` | `<pm> test` / `<pm> exec vitest run` | `pytest` | `go test ./...` | `cargo test` | — |

- `<pm>` = detected package manager: `pnpm` (`pnpm-lock.yaml`), `yarn` (`yarn.lock`), `npm`
  (`package-lock.json`). Default `npm` if a `package.json` exists with no lockfile.
- `{{DEFAULT_BRANCH}}` = the repo's default branch (`git symbolic-ref --short refs/remotes/origin/HEAD`
  stripped of `origin/`, or `git branch --show-current`; fall back to `main`).
- **No lint/typecheck/test tool at all** (e.g. a config-only repo) → inject only the **Code review**
  gate plus the "no automated gates found" note at the bottom, and tell the user.

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
   config.
5. **Code review** — run **both** in parallel on this session's changes:
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
   - **Merge** — deduplicate findings across 5a and 5b, present one combined "Code review findings"
     section.

If any check fails, fix and re-run. These gates are mandatory for every code change — no exceptions.

---

**Note for skill user**: Substitute `{{LINT_CMD}}`, `{{TYPECHECK_CMD}}`, `{{TEST_CMD}}`,
`{{DEFAULT_BRANCH}}` from detection. Drop any gate whose tool is absent and renumber. If the project
has no lint/typecheck/test tooling, keep only gate 5 (code review) and append: *"No automated lint/
typecheck/test gates were detected for this repo. Add them here when build tooling lands."*

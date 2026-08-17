# Verification Protocol Template

Inject the `## Mandatory Verification After Code Changes` section below into the project's agent
instructions file. **Substitute the `{{...}}` placeholders** with commands detected from the repo
(see the detection table). **Omit any gate whose tool was not detected** — never inject an empty or
guessed command.

## Stack detection

Detect each gate independently from the repo. A gate with no tool is dropped from the injected
block. The **Code review** and **Docs & instructions alignment** gates are tool-agnostic and always
kept.

The **regression test for bug fixes** gate has no command of its own. Unlike a gate that is only
kept or dropped, it also has a dormant state:

- **Source repo with a test framework** → gate is **enforced** as written.
- **Source repo without a test framework** → gate is **kept as prose, dormant and unenforced**. It
  sets the intent for when tests land, and pairs with the `references/test-setup.md` offer. It has no
  command to substitute, so nothing here is empty or guessed — same class as the tool-agnostic code
  review and docs gates, which are always kept.
- **Config / no-source repo** (nothing to fix a bug in) → gate is **dropped**, exactly alongside the
  test and coverage gates it already drops.

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
- **No lint/typecheck/test tool at all** → inject the **Code review** and **Docs & instructions
  alignment** gates plus the "no automated gates found" note at the bottom, and tell the user. Note
  the split: whether the **regression gate** also survives here turns on *source code*, not *tooling*.
  A source repo with no tooling still keeps it as dormant prose; only a config / no-source repo drops
  it.
- **The tail gates (User scenarios in sync, Backlog sweep) have no stack signal at all** —
  nothing here detects them from lint, typecheck, or test tooling. Each one is stack-independent,
  and selection alone earns none of them: each points at a doc or policy section that only its own
  delegated skill installs — the user-scenarios gate at the BDD scenario doc
  (`setup-user-scenarios`), the backlog sweep at the `## TODO / Known issues` policy
  (`setup-todo-backlog`). Each ships **only after its own delegation actually succeeded** (SKILL.md
  Step 6b), which is why they are appended there rather than injected here with the other gates.
  Append them last, in the order written below — user-scenarios sync, then backlog sweep. A repo
  appends only the tail gates that qualify. A repo that appends none ends at the docs & instructions
  alignment gate.
  **No tail gate body below carries meta-guidance** — every condition governing whether they ship
  lives here and in the note at the bottom, so Step 6b can copy each gate verbatim into a repo
  without leaking skill-authoring instructions into that repo's agent instructions.

---

## Mandatory Verification After Code Changes

After ANY code change, run these checks before presenting the work. All are mandatory unless a step
says otherwise.

> **Exemption:** when changes are **solely** to markdown/docs (`*.md`), skip this protocol — no
> impact on builds, types, or tests.

- **Lint** — `{{LINT_CMD}}` must pass with zero warnings and zero errors.
- **Typecheck** — `{{TYPECHECK_CMD}}` must exit with **zero errors total**. "Pre-existing" errors
  do not get a pass: if the typechecker reports errors — even in files you did not touch — fix them
  before proceeding. A green typecheck is a gate, not a suggestion.
- **Tests** — `{{TEST_CMD}}` must show zero failures.
- **Test coverage for new code** — every new production module or feature gets a co-located test
  file. A feature added inside an existing module counts: new behavior needs new tests, wherever it
  lands. Tests must cover (1) the main business goal, (2) the main user flow, and (3) error/edge
  cases (failure paths, empty/invalid inputs). Updating existing mocks is necessary but **not**
  sufficient — new logic needs dedicated tests. Exempt: pure type-only files, generated code,
  trivial re-exports, config. On top of that, overall repository coverage must stay at or above
  `{{COVERAGE_THRESHOLD}}%` — run `{{COVERAGE_CMD}}`, which fails the build itself when the total
  drops below the threshold. New tests for new code are necessary but not sufficient either: if the
  run reports the overall percentage under `{{COVERAGE_THRESHOLD}}%`, the gate fails and more tests
  are needed before proceeding.
- **Regression test for bug fixes** — every bug fix ships a test that **fails before the fix and
  passes after**. Test-first: write the failing test, watch it fail for the right reason, then fix
  the bug and watch it pass. No test, no fix — a fix without a reproducing test does not clear this
  gate. Exempt, and only these: typos in copy, build/CI config, dependency bumps, pure formatting.
  This gate is not covered by the **Test coverage for new code** percentage — a bug fixed on an
  already-covered line does not move the coverage number, so `{{COVERAGE_CMD}}` cannot detect a
  missing regression test. Coverage measures executed lines, not asserted behavior.
- **Code review** — **Exempt:** an integration-only session — a merge, rebase, cherry-pick, or
  revert of already-reviewed work that authored no new lines — skips this gate and only this gate;
  every other gate still runs. Writing one line neither side had voids it. Report the skip with the
  diff proving nothing was authored (`git show --cc --format="" <integration-sha>` for a merge,
  `git range-diff` for a rebase or cherry-pick) **plus** `git diff <integration-sha>..HEAD`, where
  `<integration-sha>` is the merge commit or the replayed tip — that pairing is what proves nothing
  landed after the integration commit, which neither command before it can see. Never skip silently.
  Otherwise run **every lens below** in parallel on this session's changes:
  - **Harness-native code review** — invoke your harness's `code-review` agent (Claude Code:
    `Task` tool with `subagent_type: "code-review"`; Copilot CLI: the `code-review` skill). Cover
    bugs, security, logic errors, race conditions, unhandled edge cases, and the project's own
    conventions.
  - **CodeRabbit CLI** — `cr review --agent --base {{DEFAULT_BRANCH}}`. Collect every
    `type: "finding"` event; wait for `type: "complete"`.
    - **Prerequisites** — `cr` on `PATH` (`which cr`) and authenticated (`cr auth status`). If either
      fails, **tell the user and skip the CodeRabbit CLI lens** — label it `skipped (CodeRabbit
      unavailable)`; never skip silently.
  - **Nuclear structural review** — if the `code-review-nuclear` skill is available, spawn a
    subagent that runs it on this session's diff (Claude Code: `Task`/`Agent` tool → a subagent
    whose prompt invokes the skill against `{{DEFAULT_BRANCH}}...HEAD`). Structural /
    maintainability "code judo" only — NOT correctness, security, tests, or lint (the
    **Harness-native code review** lens and the **Lint**, **Typecheck**, **Tests**, **Test coverage
    for new code**, and **Regression test for bug fixes** gates cover those). This lens is exempt
    from the triage step below, because it proposes structural rewrites and not defects. Each finding
    is a proposal, and each one is larger than the change under review. Surface its findings for the
    user; never apply one on your own. If the skill isn't available, **tell the user and skip the
    nuclear structural review lens** — label it `skipped (nuclear review unavailable)`; never skip
    silently.
  - **Security review** — if your harness provides a security-review capability (Claude Code:
    the built-in `/security-review` skill; Copilot CLI: its built-in security review), spawn a
    subagent that runs it against `{{DEFAULT_BRANCH}}...HEAD`. Vulnerability classes only —
    injection, XSS, SSRF, hardcoded secrets, IDOR, auth bypass, unsafe deserialization, and path
    traversal. Structural and correctness concerns belong to the **Harness-native code review** and
    **Nuclear structural review** lenses, not here.
    - If your harness provides no security-review capability, **tell the user and skip the security
      review lens** — label it `skipped (security review unavailable)`; never skip silently.
  - **Merge** — wait for **every lens** to finish — a `skipped` lens still counts as done — then
    deduplicate findings across them and present one combined "Code review findings" section.
  - **Triage before you fix — relevance decides, not severity.** Judge every merged finding on its
    own before you change anything. Relevance is the gate. Severity sets the order of the work; it
    never decides whether a finding gets fixed.
    - **Relevant** → fix it, whatever its severity. A finding its lens rated low — `minor`,
      `trivial`, or below — that is correct and in scope gets fixed like any other. **A low severity
      is never a reason to leave a real defect.**
    - **Not relevant** → reject it, and state the reason. A finding is not relevant when it is wrong
      about the code or the tooling, when it points at code this session did not change and the
      change did not make it wrong, when it contradicts a documented project convention or a
      decision the user already made, or when it is taste with no defect and no convention behind
      it. Verify a finding that contradicts a command you have actually run — a `--help` output or a
      successful run beats a reviewer's recollection of a tool. Never turn a working command into a
      broken one. Rejecting is your call; do not queue rejections for the user to clear.
    - **Changes what a rule requires** → never apply it on its own, at any severity. Draft the
      wording, show it, ask. This covers a policy number — a threshold, a budget, a retry limit, a
      coverage percentage — and any finding that adds, removes, weakens, or re-scopes a rule. A
      factual defect is different and gets fixed: a broken command or flag, a dead link, a reference
      to something absent, a typo.
    - **Bigger than the change under review** → state the finding with the fix you propose, and ask.
      A relevant finding never grows into a broad refactor, a new dependency, or a change to a
      public interface without approval.
    - **Ambiguous** → ask. A rejection needs a reason you can state. With no reason either way, the
      finding is not rejected.
    - Fix in severity order, highest first. Then re-run the lint, typecheck, and test gates this repo
      has.
    - Report every finding with its verdict — `fixed`, `rejected (reason)`, or `waiting on you`.
      State a rejected or deferred finding as a plain finding in the report. Never collect one into a
      queue, and never offer to file it as a tracked entry.
  - **Re-review budget** — at most one extra `cr review` after the fixes; further loops need user
    approval (each costs credits).
- **Docs & instructions alignment** — before marking the task done, check whether this session's
  changes made any documentation stale:
  - **Project docs** (`README.md`, `docs/`, `ARCHITECTURE.md`, other human-facing docs) — stale
    docs are part of the change, like a failing test: update them now and list what was updated.
  - **Agent instructions** (`AGENTS.md` / `CLAUDE.md` and any rule files they link) — draft the
    updated wording and **ask the user** before applying. Never silently edit instruction files.
  - Nothing stale → say so explicitly in one line; do not invent updates.
- **User scenarios in sync** — every user-visible change ships a matching scenario in the BDD
  scenario doc named by the `## User Scenarios` section of these instructions. A change is
  user-visible when it alters a page, an endpoint's response, a flow, a business rule, an
  entitlement, an email, or an error a user can see. Add or update the scenario, point its
  `Verified by:` line at a real test file, and sync its row in the Coverage Matrix. **This gate
  binds exactly like the test gate: an unsynced scenario doc means the task is not done.** Never
  present the work as complete while the doc is stale, and never defer the scenario to a follow-up.
  Report it every time — `passed`, `failed (what is missing)`, or `n/a (not user-visible)`. There
  is no silent skip. Unsure whether a change is user-visible → treat it as user-visible; a
  redundant scenario costs less than a coverage hole.
- **Backlog sweep** — run the close-only sweep described in the `## TODO / Known issues`
  section of the agent instructions: close the entries this session solved. **This gate overrides
  the markdown-only exemption above — it is the one gate that survives it.** A docs-only change can
  close a docs-only entry, so the sweep runs on every substantive session, whether or not the
  session touched code. **Closing an entry requires evidence the defect no longer reproduces** — a
  re-run, a passing check, a confirmed absence — never close on "looks fixed". Closing is not
  approval-gated. The evidence is the check. Report one line either way: which entries you closed,
  or that you closed none.

If any check fails, fix and re-run. These gates are mandatory for every code change — no exceptions.

---

**Note for skill user**: Substitute `{{LINT_CMD}}`, `{{TYPECHECK_CMD}}`, `{{TEST_CMD}}`,
`{{COVERAGE_CMD}}`, `{{COVERAGE_THRESHOLD}}`, `{{DEFAULT_BRANCH}}` from detection. Drop any gate whose
tool is absent. The quantitative coverage requirement in the **Test coverage for new code** gate is
dropped alongside the test gate when no test framework/coverage tool exists — a repo with no tests
has no coverage number to gate on. The **Regression test for bug fixes** gate degrades on its own
path, not with the test gate: **enforced** in a source repo with a test framework; **kept
as dormant, unenforced prose** in a source repo without one (it sets the intent and pairs with the
`references/test-setup.md` offer, and since it carries no command there is nothing empty or guessed
to inject — same class as the tool-agnostic code review and docs gates); **dropped** only in a
config / no-source repo, alongside the test and coverage gates. If the project has no
lint/typecheck/test tooling, keep code review and docs & instructions alignment, plus the regression
gate as dormant prose **when the repo has source code** — that path keys off source, not tooling. A
source repo with no tooling keeps code review, docs & instructions alignment, and the dormant
regression gate. A config / no-source repo keeps code review and docs & instructions alignment only.
Append to whatever remains: *"No automated lint/typecheck/test gates were detected for this repo.
Add them here when build tooling lands."* If a source repo has a test framework but no coverage
tooling, the skill wires `{{COVERAGE_THRESHOLD}}` once coverage tooling is chosen — see
`references/test-setup.md`. The
**Security review** lens ships only when the security review module is selected in Step 4; when it is
not, omit that lens bullet. The **integration-only exemption** on the **Code review** gate ships
with that gate and is dropped with it — a repo that does not get the code review gate does not get
the exemption either. The **User scenarios in sync** and **Backlog sweep** gates are similar but
strictly stronger: no tail gate carries a `{{...}}` placeholder either, but selection alone is not
enough to ship one. Each references something only its delegated skill installs — the BDD scenario
doc from `setup-user-scenarios`, the `## TODO / Known issues` policy from `setup-todo-backlog` — so
each is **appended in SKILL.md Step 6b after its own delegation succeeds**. Do not inject a tail gate
here with the other gates, or a repo whose delegation was skipped ends up with a mandatory gate
pointing at something that does not exist. Append them last, in the order written above, so a repo
appends only the tail gates that qualify.

**Version / drift.** This block's version is recorded by the versioned provenance note the skill
stamps (SKILL.md Step 5.6), not by a marker inside the block. On re-run upgrade mode (SKILL.md Step
1), when the stamped version is older than the current **Skill version**
(`references/baseline-checklist.md`), refresh a drifted injected block by diffing it against this
current template — diff-and-ask, preserve local edits, never clobber.

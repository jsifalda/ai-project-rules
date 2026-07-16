# Baseline Checklist

The canonical list of AI-engineering baseline concerns this skill installs. It is the target of the
Step 8b coverage self-audit, and it defines what each skill version contains, so re-run upgrade mode
(Step 1) can tell an older setup what it is missing.

**Skill version: v3**

Bump this number whenever a concern is added below (see the maintainer loop at the bottom). The
version stamped into a repo's provenance note is compared against this number on every re-run.

## Concerns

Each row is one baseline concern, its delivery type, the step that installs it, and the version it
first shipped in. `Since` lets re-run mode compute the delta for a repo stamped with an older version.

| Concern | Delivery | Step | Since |
|---------|----------|------|-------|
| Agent instructions file (`AGENTS.md` + `CLAUDE.md` symlink) | scaffold | 1 | v1 |
| Stack detection (package manager, lint/typecheck/test, default branch) | detect | 2 | v1 |
| Backfill grounded body for working repos (opt-in) | scaffold | 3 | v1 |
| Verification protocol (lint, typecheck, test, coverage) | inject | 5 | v1 |
| Coverage threshold gate (overall ≥90%, adjustable) + test-framework setup prompt | inject | 5 | v2 |
| Code review lens 5a — harness-native | inject | 5 | v1 |
| Code review lens 5b — CodeRabbit CLI | inject | 5 | v1 |
| Code review lens 5c — nuclear structural (optional) | inject | 5 | v1 |
| Docs & instructions alignment gate | inject | 5 | v1 |
| Git policy | inject | 5 | v1 |
| File organization | inject | 5 | v1 |
| PRD gate (opt-in, default off) | inject | 5 | v1 |
| Provenance note (versioned) | inject | 5 | v1 |
| ADRs | delegate → `setup-adrs` | 6 | v1 |
| ADR read-before-plan rule | delegate → `setup-adrs` | 6 | v3 |
| Changelog | delegate → `setup-changelog` | 6 | v1 |
| User scenarios (BDD) | delegate → `setup-user-scenarios` | 6 | v1 |
| Worktree auto-bootstrap (hook + `.worktreeinclude` + `.mcp.json` carry) | scaffold | 7 | v1 |
| MCP-config reminder (when no `.mcp.json`) | inject | 7b | v1 |
| GitHub App offer (Claude Code + GitHub only) | suggest | 9 | v1 |

## How the self-audit uses this (Step 8b)

After the Step 8 report, read this file and classify every concern above against the target repo:

- **installed** — the section, delegated doc system, scaffold, or reminder is present.
- **skipped (reason)** — the user opted out, or a guard fired (tool absent, wrong host, skill
  unavailable). Name the reason.
- **not covered** — the concern belongs in this repo but is neither installed nor deliberately
  skipped. This is a real gap. Surface it to the user. Never omit it silently.

The point of the audit is that a missing concern shows up as skill output, not as a future PR.

## How re-run upgrade mode uses this (Step 1)

When a provenance note already exists, read its stamped version. If it is older than the version
above, the repo is missing every concern whose `Since` is newer than the stamp. Offer to inject
those, and to refresh any injected block that drifted from its current template. Diff and ask, never
clobber local edits.

## Maintainer loop

When a new baseline gap is found, do not patch it as a one-off in a target repo. Instead:

1. Add the concern as a row here with `Since: v<next>`.
2. Bump **Skill version** above.
3. Wire it into the matching step (inject → Step 5, delegate → Step 6, scaffold → Step 7).
4. Re-running the skill on any older repo now detects the version gap and offers the new concern.

That is the loop this checklist exists to close: gaps propagate through re-runs, not through a PR
per repo.

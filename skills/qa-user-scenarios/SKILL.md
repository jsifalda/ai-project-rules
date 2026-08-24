---
name: qa-user-scenarios
description: Drive a project's documented user scenarios through a real browser with Playwright MCP, then report what actually broke. Reads whatever scenario inventory the repo keeps, sorts each scenario into browser-reachable or out of scope, writes a falsifiable test plan, resets and seeds the local database, drives each scenario serially against a dev server it starts itself, and judges every one as pass, fail, gap, drift or blocked with a screenshot as evidence. Reports the findings, then decides with the user what to do about each. Never auto-fixes, never files a backlog entry. Use when the user types /qa-user-scenarios, or asks to QA the documented scenarios, verify user scenarios in a browser, or hunt for bugs against the scenario inventory. Do NOT use for writing new end-to-end test files, a one-off browser check of a single change, creating or editing the scenario inventory itself, or running an existing test suite.
disable-model-invocation: true
---

# QA User Scenarios — drive the documented scenarios through a real browser

Take the scenarios a project already documents, drive each one through a real browser, and report
which ones the application does not actually honour. The output is a verdict per scenario with
screenshot evidence, then a decision with the user on each finding.

## Why this exists

A scenario inventory records intent. A unit suite records intent too, in a second notation. Neither
observes the running application.

A test that mounts a component into a simulated DOM proves the component renders when its
dependencies are mocks. It does not prove the page loads, the client code hydrates, the route
resolves, the query returns rows, or the button does anything when a person clicks it. A whole
application can be inert while its unit suite is green, because the two facts are unrelated. Every
gate that runs without a browser shares this blind spot.

So the inventory reads as coverage while nothing in it has been observed. This skill closes that gap
by treating the browser as the only evidence.

## Phase 1 — Discover

Learn the project. Assume nothing.

**The scenario inventory.** Try these paths in order, and stop at the first that exists.

1. `docs/user-scenarios.md`
2. `docs/scenarios.md`
3. `docs/user-stories.md`
4. A glob for `*scenario*.md` and `*stories*.md` under `docs/`

Zero matches, or more than one plausible match, means ask the user for the path and stop. Do not
guess, and do not invent scenarios from the code.

**The doc's own format.** Read the inventory's Conventions section, when it has one, and derive the
format from what it says rather than from what you expect. Establish four things before parsing.

- The scenario ID scheme, and the heading shape that carries it.
- The step shape. Given / When / Then bullets are common, but the notation belongs to the project.
- Whether each scenario names the test that verifies it, and under what label.
- Whether a coverage table exists at the bottom, and whether it agrees with the body.

**The project's commands.** Read the manifest, such as `package.json`, `Makefile`, or `justfile`.
Record the development-server command, the database reset command, and the seed command, each as the
project spells it. A project with no reset command changes Phase 4, so find out now.

**The evidence directory.** Prefer a directory the repository already ignores, such as
`.playwright-mcp/`. Confirm the choice against `.gitignore` before writing into it.

Report all four discoveries before the run starts. A wrong one poisons every later phase.

## Phase 2 — Select

Parse every scenario in the inventory. Sort each one.

**Browser-reachable** means a person can produce the Given, perform the When, and observe the Then in
a browser against a local development environment.

**Out of scope** means they cannot, and the reason is stated. These are the standing categories.

- Needs a third-party provider that is not configured locally, such as mail delivery or payment
  capture.
- Needs object storage or a bucket that the local environment does not have.
- Asserts a database constraint or a data-integrity rule with no user-visible surface.
- Describes a background or scheduled job with no path a user can trigger.

Apply the scope argument `$ARGUMENTS`. It is one of these.

| Argument | Meaning |
| --- | --- |
| A domain prefix, such as `AUTH` | Every scenario in that domain |
| An explicit list of scenario IDs | Exactly those |
| `all` | Every browser-reachable scenario |
| Empty | Propose a named slice, and state its size |

An empty argument does not start an interview. Propose a slice, name the scenarios in it, and say how
many there are. Ask the user exactly once, and only when the slice is genuinely ambiguous.

Print three counts before continuing — selected, out of scope grouped by reason, and the total in the
inventory. A run that silently drops scenarios reads as coverage it does not have.

## Phase 3 — Plan

Write the test plan before the browser opens. This is what makes the run falsifiable instead of
improvised — a plan written afterwards rationalises whatever the browser happened to show.

Record five fields per selected scenario — the scenario ID, the route to load, the preconditions
(signed out, signed in as which account type, or which seeded fixture is needed), the interaction to
drive, and the single observable that decides the verdict.

Present the plan. Do not start the browser until it exists.

## Phase 4 — Prepare

Run these five steps in this order. Each one aborts the run on failure.

**0. Check the environment first.** Where the project ships an environment preflight, run it and
report what it says. Do not abort on a failure — record which variables are missing and carry that
list into Phase 6. A missing variable disables a feature silently while the interface still reports
success, so an unchecked environment turns configuration gaps into false `fail` verdicts and burns
the run on debugging the wrong layer. Where no preflight exists, say so.

**1. Guard the database.** Resolve the database URL the application will actually use, the same way
the application resolves it. Abort unless it resolves to localhost or a local container. Name the
resolved host in the abort message. This run destroys data, and it is the only irreversible thing the
skill does, so the guard is not optional and has no override.

**2. Reset and seed.** Say plainly, before running anything, that the run destroys the local
development database. Then run the project's reset and seed commands. A project with no reset command
runs against whatever is present — say so, because a pass on leftover data proves less.

Ask before resetting when anything else is using that database — another development server, another
checkout, a colleague's session. A reset takes their data with it. Where the user declines the reset,
run without it and record the choice in the report. Then, before Phase 5, count the fixtures the
selected scenarios depend on and state what you found. A scenario whose fixture is absent is
`blocked`, never `fail` — that distinction is the whole reason to look first.

**3. Start the development server.** Start it yourself, in the background, and read the bound port
from the framework's startup banner. Never assume a default port — a server auto-shifts when the
first is busy, and a hardcoded port verifies somebody else's application. Never adopt a server this
session did not start. Where one is already running and is not yours, stop and ask the user. Do not
kill it.

**4. Confirm Playwright MCP.** Where it is absent, report `skipped (Playwright MCP unavailable)` and
stop. Never fall back to fetching pages with a command-line client, and never read the source and
call a scenario verified. Both produce a verdict with no evidence behind it, which is worse than no
verdict.

## Phase 5 — Execute

Run the scenarios serially, one at a time. Playwright MCP drives a single shared browser instance, so
parallel execution is impossible, not merely slow. Do not try to optimise it into subagents — they
contend for the one browser and corrupt each other's session state.

**Drive the interaction, not the paint.** A filter that renders is not a filter that filters. Load the
route, perform the When, and then read what changed. A screenshot of a page that was never used is not
evidence about a scenario.

**Reach the signed-in scenarios.** Seeded fixtures often carry no credentials at all, so signing in as
a seeded account can be impossible. Register a fresh account through the user interface instead. In
development, unsent mail is usually written to the server's own output, so harvest the verification
link from the development server's stdout and open it. An administrator scenario may also need a
grant command the project provides, run against the local database.

**Save evidence.** One screenshot per scenario, into the Phase 1 evidence directory, named by
scenario ID. Take it when the observable is visible, not before the interaction.

**Write the evidence path in full, every time.** A screenshot filename with no directory is written
relative to the working directory, which puts it in the repository root and dirties the tree. Pass
the evidence directory as part of the filename, not as an assumed default.

**Judge what is rendered, not what is in the document.** A collapsed disclosure, a closed dialog and
an inactive tab all keep their content in the document, so counting elements over-counts what the
visitor can see. Measure the rendered box, and where a scenario names a limit, confirm the limit by
opening the control rather than by counting nodes. Read a role from the accessibility tree, never
from a `role` attribute — an element with an implicit role carries no such attribute, and querying
for one silently finds nothing.

**A text match is a lead, not a finding.** Searching served markup for a name, an address or a
telephone number will match advertising copy, other people's records and unrelated prose. Before
reporting a leak, print the surrounding text and confirm whose data it is. A privacy finding reported
from a bare match count is usually wrong, and it is the most expensive kind of wrong.

Report progress as you go. A long serial run that reports only at the end is indistinguishable from
one that hung.

## Phase 6 — Judge

Give every scenario exactly one verdict.

| Verdict | Decision test |
| --- | --- |
| `pass` | The observable matched what the scenario says |
| `fail` | The behaviour is implemented, and it is wrong |
| `gap` | The scenario is documented, and the behaviour is absent |
| `drift` | The behaviour is correct, and the scenario describes something else |
| `blocked` | The scenario could not be reached, and the reason is named |

Two rules decide the hard cases.

- A scenario you could not reach is `blocked`. It is never `pass`. An unreachable scenario has no
  evidence, and no evidence is not agreement.
- "The code looks right" is never evidence. The verdict comes from what the browser did. Reading the
  implementation to explain a failure is fine. Reading it to award a pass is not.

The full rubric, with worked examples of the `fail` against `gap` boundary and the `drift` against
`fail` boundary, is in [references/verdicts.md](references/verdicts.md).

## Phase 7 — Report

Three parts, in this order.

1. **The verdict table.** One row per scenario — ID, domain, verdict, and a one-line note.
2. **A detail block per non-pass**, carrying what was expected, what was observed, the path to the
   evidence file, and a severity.
3. **The coverage line** — how many scenarios ran, how many were out of scope, and the reason for
   each group. A report that omits this reads as a full sweep.

Write the report to the chat, and the same report to a receipt file in the evidence directory. The
chat is what the user reads. The file is what survives the session.

The exact shape is in [references/report-template.md](references/report-template.md).

## Phase 8 — Decide

Put the findings to the user. Offer four options for each.

- **Fix now.** The fix becomes ordinary work after this phase, under the project's own verification
  gates.
- **Record it.** The user decides where. This skill does not choose the destination.
- **Amend the scenario.** The right answer for `drift`, where the application is correct.
- **Drop it.** Not every defect deserves a fix.

Group the findings where there are many, and ask about a group rather than asking once per finding.
Then act on the answers. A finding the user did not decide on stays open in the report.

## Hard rules (never violate)

- **Never edit application code during a run.** A run that changes the thing it measures measures
  nothing.
- **Never edit the scenario inventory.** A wrong verification pointer is a `drift` finding, not an
  edit. A tool that judges a document and rewrites it is trusted on neither.
- **Never file a backlog or issue entry, and never offer to.** Findings go in the report, and the
  user decides unprompted. Some projects forbid even the offer.
- **Never auto-fix.** Fixes happen after Phase 8, as ordinary work. A QA run is not a substitute for
  the project's own gates, and a fix applied mid-run has been reviewed by nothing.
- **Never run against a database the skill did not itself resolve to a local container.**
- **Never adopt a development server this session did not start, and never assume its port.**
- **Close the browser and stop the development server** on the failure path as well as the success
  path.
- **Never mark a phase silently skipped.** Report `passed`, `failed (what broke)`, or
  `skipped (reason)` for each phase. A gate that reads as enforced and is not is worse than no gate.
- **Never report a verdict without evidence.** A screenshot is falsifiable. A claim is not.

## Failure modes (abort with a one-line reason)

| Condition | Message |
| --- | --- |
| No scenario inventory found | `no scenario inventory found — name the path` |
| More than one plausible inventory | `several scenario documents — name the one to use` |
| Database URL is not local | `refusing to run against <host> — the run destroys data` |
| Reset or seed command failed | surface the command's error verbatim and stop |
| Another development server holds the directory | `a development server is already running — stop it, or confirm it is yours` |
| Development server never bound a port | `development server did not start — <last line of output>` |
| Playwright MCP unavailable | `skipped (Playwright MCP unavailable)` |
| Evidence directory is not gitignored | `<dir> is tracked — choose an ignored directory` |
| Scope argument names an unknown domain | `unknown domain <name> — known domains are <list>` |
| Scope argument names an unknown scenario ID | `unknown scenario <id>` |
| Every selected scenario is out of scope | `nothing browser-reachable in this scope — <reasons>` |
| Registration could not complete | `cannot reach the signed-in scenarios — <what failed>` |
| Verification link not found in server output | `no verification link in the server output — signed-in scenarios are blocked` |

## References

- [Verdicts](references/verdicts.md) — the five-verdict rubric, with a decision test and worked
  examples for each, and the boundaries between them.
- [Report template](references/report-template.md) — the run-report shape, with `{{VERDICT_ROWS}}`,
  `{{FINDING_BLOCKS}}` and `{{COVERAGE_LINE}}` placeholders.

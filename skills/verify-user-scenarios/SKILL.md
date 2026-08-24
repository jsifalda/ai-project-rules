---
name: verify-user-scenarios
description: Drive a project's documented user scenarios through a real browser with Playwright MCP, then report what actually broke. Reads whatever scenario inventory the repo keeps, sorts each scenario into browser-reachable or out of scope, writes a falsifiable test plan, resets and seeds the local database, drives each scenario serially against a dev server it starts itself, and judges every one as pass, fail, gap, drift or blocked with a screenshot as evidence. Reports the findings, then decides with the user what to do about each. Never auto-fixes, never files a backlog entry. Use when the user types /verify-user-scenarios, or asks to QA the documented scenarios, verify user scenarios in a browser, or hunt for bugs against the scenario inventory. Do NOT use for writing new end-to-end test files, a one-off browser check of a single change, creating or editing the scenario inventory itself, or running an existing test suite.
disable-model-invocation: true
---

# Verify User Scenarios — drive the documented scenarios through a real browser

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

**The environment.** Where the project ships an environment preflight, run it **here**, and record
the name of every missing required variable. Where none exists, say so, and say that configuration
gaps will therefore surface mid-run rather than up front.

This is a discovery, not a preparation step, because a missing variable decides what can be tested
at all — and Phase 2 needs that answer before it fixes a slice. A missing variable disables a
feature silently while the interface still reports success, so an environment checked late turns a
configuration gap into a false `fail` and spends the browser debugging the wrong layer. One run
found its two missing variables ten minutes into Phase 5, as forensics on a flow that had quietly
done nothing.

Report all five discoveries before the run starts. A wrong one poisons every later phase.

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

**A missing variable is a scope decision, not a mid-run surprise.** Take the list Phase 1 recorded,
map each variable onto the scenarios that depend on it, and mark those `blocked` now, naming the
variable. They still appear in the report; they are simply not driven. A run that meets the same
gap in Phase 5 has already spent the browser on it, and its verdicts for that surface are about
configuration rather than about the product.

Apply the scope argument `$ARGUMENTS`. It is one of these.

| Argument | Meaning |
| --- | --- |
| A domain prefix, such as `AUTH` | Every scenario in that domain |
| An explicit list of scenario IDs | Exactly those |
| `all` | Every browser-reachable scenario |
| Empty | Propose a named slice, and state its size |

An empty argument does not start an interview. Propose a slice, name the scenarios in it, and say how
many there are. Ask the user exactly once, and only when the slice is genuinely ambiguous.

**This phase derives the slice. It never inherits one.** A list of IDs reaching you from anywhere
other than `$ARGUMENTS` — a plan file, an earlier session, a menu answer, your own notes — is an
input to the ranking below, never its output. A run once took twenty IDs from a plan file that
itself said the Select phase would re-derive them; it did not, and the one scenario naming the
defect that run was about was dropped along with eighty-eight others, silently.

**Build the proposed slice by risk, not by spread.** An even sample across domains looks like
coverage and is the least informative slice available, because it re-tests what is already best
tested. Rank the browser-reachable scenarios and take from the top.

1. The verification pointer is `TODO`. Nothing anywhere asserts this scenario, so the browser is
   its only possible evidence.
2. The pointer names a test that runs without a browser — a component mounted into a simulated DOM,
   a unit test over mocks. Open it and read what it asserts. A pointer resolving to assertions loose
   enough to pass on a wrong value is coverage in name only, and it is the cheapest thing to check
   after a `TODO`. Reading a test to **rank** it is not awarding a verdict from code; the hard rule
   below governs verdicts, and nothing here awards one.
3. The scenario crosses a boundary a mocked test cannot reach — a redirect, a generated link, a
   mail, a payment, a role change, a page a crawler sees.
4. Everything else.

Print the counts before continuing — selected and total **per domain**, then the inventory total.
Name every domain with nothing selected. Every scenario left out carries its own stated reason, and
`not selected` is not a reason. A run that silently drops scenarios reads as coverage it does not
have.

## Phase 3 — Plan

Write the test plan before the browser opens. This is what makes the run falsifiable instead of
improvised — a plan written afterwards rationalises whatever the browser happened to show.

Record five fields per selected scenario — the scenario ID, the route to load, the preconditions
(signed out, signed in as which account type, or which seeded fixture is needed), the interaction to
drive, and the single observable that decides the verdict.

**The plan is an artefact, not an assertion.** Print all five fields for all selected scenarios,
in full, and do not open the browser until that text exists in the transcript. "Test plan built" is
not a test plan, and a run that says it improvises instead — which is the exact failure this phase
was written to prevent, because an improvised run then rationalises whatever the browser happened to
show. One run's entire Phase 3 was that sentence; nine seconds later the browser opened, and nothing
had written down the interaction to drive for a single scenario. The report carries this text
verbatim, so a phase skipped here is visible there.

## Phase 4 — Prepare

Run these five steps in this order. Step 0 records its failures and continues. Steps 1 to 4 abort
the run on failure.

**0. The environment was already checked.** Phase 1 ran the preflight and Phase 2 blocked the
scenarios the missing variables reach. Re-run it only if something has touched the environment
since — a checkout, an install, an edited env file. Carry the list into the report either way, and
where Phase 1 found no preflight, say so again here.

**1. Guard the database.** Resolve the database URL the application will actually use, the same way
the application resolves it. Abort unless it resolves to localhost or a local container. Name the
resolved host in the abort message. This run destroys data, and it is the only irreversible thing the
skill does, so the guard is not optional and has no override.

**2. Reset and seed.** Say plainly, before running anything, that the run destroys the local
development database. That warning is not consent. Ask the user for an explicit yes immediately
before the reset command runs, every time. On a yes, run the project's reset and seed commands. On
anything else, run without the reset and record the choice in the report — a decline never stops
the run. A project with no reset command runs against whatever is present — say so, because a pass
on leftover data proves less.

Warn again when anything else is using that database — another development server, another
checkout, a colleague's session. A reset takes their data with it, so name that consequence before
you ask. Then, before Phase 5, count the fixtures the selected scenarios depend on and state what
you found. A scenario whose fixture is absent is
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

**Presence is not function.** A control the Then step says **does** something is operated, never
merely observed. `pass` on "the control is there" is available only when the Then step says
*there*. Nothing about a rendered control tells you it has a handler attached, and one wired to
nothing looks exactly like one that works. Count your own clicks against the scenarios whose Then
step describes an action before judging any of them — a run whose whole record holds one click has
driven nothing. One run saw a resend button, screenshotted it, and scored a pass on its presence.
The button had no handler at all.

**Reach the signed-in scenarios.** Seeded fixtures often carry no credentials at all, so signing in as
a seeded account can be impossible. Register a fresh account through the user interface instead. In
development, unsent mail is usually written to the server's own output, so harvest the verification
link from the development server's stdout and open it. An administrator scenario may also need a
grant command the project provides, run against the local database.

**Every workaround is recorded, and it blocks what it bypassed.** Reaching a scenario sometimes
needs a step the product does not offer — marking an account verified straight in the database,
granting a role, seeding a row by hand. That stays allowed; it is often the only reason those
scenarios are reachable. What is forbidden is letting the workaround disappear. Record four things
before continuing: what was bypassed, what was done instead, which surface therefore went
unobserved, and **which interface branches the change closed.**

The fourth is the one runs forget. A workaround that alters account or fixture state does not merely
leave a surface untested — it can make a control structurally unrenderable for the rest of the run,
so the control is not weakly covered, it is absent, and nothing on screen says so. Mark every
selected scenario depending on that surface `blocked`, naming the workaround: no evidence is not
agreement.

It has happened. A run whose local mail was unconfigured marked its account verified directly in the
database, which flipped the very condition guarding the branch holding the defect the run existed to
find. Twenty scenarios, sixteen passes, and nothing in the report said the surface had been walked
around.

**Save evidence.** One screenshot per scenario, into the Phase 1 evidence directory. The basename
is the scenario ID reduced to a filesystem-safe slug — path separators and `..` removed, not
escaped, because an ID the project spells with a separator writes outside the evidence directory.
Where two reduced names collide, extend the second until it is unique, because every scenario
keeps its own screenshot. Take the screenshot when the observable is visible, not before the
interaction.

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
reporting a leak, confirm ownership from stable DOM context — which record or which section the
match sits in — and mask the matched value itself. The mask applies to the chat, to the report
and to the receipt file, and only the minimum evidence needed to identify the leak is recorded.
A privacy finding reported from a bare match count is usually wrong, and it is the most expensive
kind of wrong.

**Follow every URL the application itself hands a user.** An inventory records what a person sets
out to do, never where the application sends them afterwards — so a link the product generates is
asserted by nothing, and one that leads nowhere is invisible to every scenario and to every mocked
test of the client that produced it. Collect these as the run proceeds, then follow each once at the
end, in the same browser session:

- the destination of every navigation control on a page the run loaded;
- the target of every redirect observed, including the one after a form submission;
- every link harvested from the server's output or a local mail capture, **and the callback each one
  carries**;
- any URL the run had to construct to reach a scenario, before it constructed it.

A destination that renders the project's not-found page is a finding. Report these **outside** the
verdict table — they belong to no scenario, and forcing one in invents a scenario the inventory does
not have.

Two traps. A generated link is not the control that triggered it: a confirmation mail's callback and
the button that requested it can disagree, and only the button is on screen, so read the callback out
of the URL actually generated. And same-origin is not the same as resolvable: a framework will
happily redirect to a path of its own with no page behind it, and the origin check passes because
the path is relative. Load it.

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

## Phase 7 — Self-audit

Before the report is written, walk the hard rules against this run's own record and mark each one
honoured, violated or not applicable, with the proof beside it. The checklist and what counts as
proof for each rule are in [references/self-audit.md](references/self-audit.md).

A violated rule is **reported**, never quietly corrected. Rewriting the run to hide the violation
destroys the only evidence that the rule needs strengthening, and a run that quietly repairs itself
is a run nobody can audit.

This phase exists because the rules were never the missing part. Every gate in this skill is prose,
and prose that is skipped leaves no trace — one run skipped Select and Plan outright, drove one
control across twenty scenarios, and still produced a report that read clean. The audit is what
turns a skipped rule into a line somebody can see.

## Phase 8 — Report

Eight parts, in the order the template lists them.

1. **The run-preparation block.** What each Phase 4 step produced, a status line per phase, and the
   Phase 3 test plan in full — or `not written`, which is itself the finding.
2. **The coverage line** — selected and total per domain, the inventory total, and a stated reason
   against every scenario left out. A report that omits this reads as a full sweep.
3. **The verdict summary** — one count per verdict.
4. **The verdict table.** One row per scenario — ID, domain, verdict, a one-line note, and the
   evidence path or `none`.
5. **A detail block per non-pass**, carrying what was expected, what was observed, the path to the
   evidence file, and a severity.
6. **Workarounds and surfaces not observed** — one block per workaround, or `none`.
7. **Links the application emitted** — what was followed and what rendered.
8. **The hard-rule self-audit** from Phase 7.

Parts 2, 4, 6, 7 and 8 are the checkable half of this skill. Each one has a field that a skipped
phase cannot fill, which is the only reason a skipped phase becomes visible at all. Leave a field
empty and say why; never omit the part.

The template's own `Decisions` section stays empty here. Phase 9 fills it.

Write the report to the chat, and the same report to a receipt file in the evidence directory. The
chat is what the user reads. The file is what survives the session.

The exact shape is in [references/report-template.md](references/report-template.md).

## Phase 9 — Decide

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
- **Never auto-fix.** Fixes happen after Phase 9, as ordinary work. A QA run is not a substitute for
  the project's own gates, and a fix applied mid-run has been reviewed by nothing.
- **Never run against a database the skill did not itself resolve to localhost or a local container.**
- **Never adopt a development server this session did not start, and never assume its port.**
- **Close the browser and stop the development server** on the failure path as well as the success
  path.
- **Never mark a phase silently skipped.** Report `passed`, `failed (what broke)`, or
  `skipped (reason)` for each phase. A gate that reads as enforced and is not is worse than no gate.
- **Never report a verdict without evidence.** A screenshot is falsifiable. A claim is not. The
  verdict table carries the evidence path per row, so a verdict with nothing behind it shows as an
  empty cell rather than as a pass.
- **Never inherit a slice.** Phase 2 derives what runs, from the inventory, every time. A list of
  IDs arriving from anywhere else is an input to ranking, never a substitute for it.
- **Never leave a workaround unrecorded**, and never leave the surface it bypassed unblocked. Name
  the interface branches it closed, because a closed branch is not weak coverage, it is an absent
  control.
- **Never award a `pass` from a control's presence** when its Then step describes what the control
  does. Operate it.
- **Never end a run without following the URLs the application itself emitted.** They belong to no
  scenario, so nothing else in this skill will ever look at them.

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
- [Report template](references/report-template.md) — the run-report shape, with the run-preparation
  placeholders, one `{{PHASE_N_STATUS}}` per phase, and the `{{TEST_PLAN}}`, `{{VERDICT_ROWS}}`,
  `{{FINDING_BLOCKS}}`, `{{COVERAGE_LINE}}`, `{{WORKAROUND_BLOCKS}}`, `{{EMITTED_LINK_ROWS}}` and
  `{{SELF_AUDIT_ROWS}}` placeholders.
- [Self-audit](references/self-audit.md) — one checklist row per hard rule, each with the question
  that decides it and what counts as proof from the run's own record.

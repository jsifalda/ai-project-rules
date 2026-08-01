---
name: loop-todos
disable-model-invocation: true
description: MANUAL-INVOCATION-ONLY skill — do NOT auto-trigger. Only invoke when the user explicitly types the literal slash command `/loop-todos`. Natural-language phrasing such as 'work through the backlog', 'fix the todos', 'process the TODO list', 'start working on known issues', 'clear the backlog', or any paraphrase are ANTI-TRIGGERS — they MUST NOT load this skill; handle with ordinary tools and, if helpful, ask whether to run `/loop-todos`. When invoked — starts a recurring, self-cancelling loop in the project. Each firing claims one open backlog entry, implements it, verifies it against the project's own gates, closes it, updates stale docs, and commits to a local branch, never pushing and never opening a PR. Optional interval argument, default 10 minutes, e.g. `/loop-todos 30m`. Do NOT use for creating or formatting a backlog (that's `setup-todo-backlog`), filing or closing one entry by hand, a one-off task with no backlog, or anything touching a remote.
---

# Loop TODOs

## What this does, and how to run it

```
/loop-todos          # fires every 10 minutes
/loop-todos 30m      # fires every 30 minutes
```

An autonomous backlog worker. The user types it once, in the project directory. The optional argument
is the interval, default `10m`, handed straight to the `loop` skill. On every firing it picks up
exactly one open backlog entry and drives it to a verified, committed, documented finish, then stops
until the next firing. Every later firing re-enters this same skill, detects the run already going,
and goes straight to the work. The loop cancels itself once the run's backlog empties, and until then
the user cancels it. One loop, sequential firings, one checkout, one filesystem. Never two entries at
once, never a second loop.

## Portability

- **Assume nothing.** No language, layout, package manager, test runner, or CI. Detect and use.
- **The host project outranks this skill on every conflict it covers**, per Step 2. Its defaults
  apply where the host is silent, and a host rule scoped to one case is silent about the rest.
- **Degrade cleanly, never guess.**
  - No backlog file: report it, suggest the `setup-todo-backlog` skill, stop without starting a loop.
  - No git repository: ledger in `.claude/loop-todos/`, skip branch creation and commits entirely,
    say plainly after every item that the work is uncommitted.
  - No detectable gates: say so in that item's report, name what you looked for, never claim the
    change was verified. No host instructions file: use this skill's defaults and report that.

## The run ledger

One JSON file doing four jobs: the re-entrancy guard, the claim record, the run record, and the
source of the final summary. **It is the authority on every piece of run state.** Where a step and
the ledger disagree, the ledger is right.

**Location**, first match wins:

1. In a git repo, `<common>/loop-todos/run-<key>.json`, where
   - `<common>` is `git rev-parse --path-format=absolute --git-common-dir`. **Ask for the absolute
     form explicitly.** The bare flag returns a path relative to the current directory (`.git` from a
     repo root, `../.git` one level down), so a path resolved in one shell call and used in another
     lands somewhere else.
   - `<key>` is `git rev-parse --show-toplevel | shasum | cut -c1-12`, giving **one ledger per
     working tree**. Linked worktrees share a common dir but not a checkout, each having its own
     backlog file, branch, and uncommitted work. A shared ledger would let one tree's firing join
     another's run, append to its `closed`, and try to check out a branch git refuses to hand out
     twice.
2. `.claude/loop-todos/run.json` otherwise.

Either path sits outside the working tree, so no `git add` can sweep the ledger into a commit.
**Schema**, every field once. Later steps name a field rather than redescribing it.

```json
{
  "startedAt":       "2026-08-01T14:32:11Z",
  "lastFiredAt":     "2026-08-01T15:12:04Z",
  "interval":        "10m",
  "worktree":        "/abs/path/to/checkout",
  "branch":          "backlog/auto-2026-08-01",
  "snapshot":        ["TODO-2026-07-30-foo", "TODO-2026-08-01-bar"],
  "closed":          ["TODO-2026-07-30-foo"],
  "inFlight":        { "since": "2026-08-01T15:12:04Z", "session": "a1b2c3d4" },
  "claim":           { "todo": "TODO-...-bar", "since": "...", "session": "a1b2c3d4",
                       "step": 9, "lastFailure": null },
  "pendingQuestion": { "todo": "TODO-...-bar", "question": "<text>", "askedAt": "...",
                       "answer": null },
  "attempts":        { "TODO-2026-08-01-bar": 2 },
  "baselines":       { "lint repo/": "40 errors, 0 warnings" },
  "credits":         { "cr review": 3 },
  "finished":        null
}
```

Self-evident from the shape: `interval` as passed, `worktree` from `git rev-parse --show-toplevel`
(a mismatch against the current tree is a stop, not a warning), `branch` null until the first commit,
`closed` in order, `attempts` per todo id, `baselines` per gate label from Step 7, `credits` per
metered gate. The rest earn their keep:

- `startedAt`, first run, UTC. Identity only. **Never a liveness signal**, because it never moves.
- `lastFiredAt`, rewritten by every firing that decides it is an iteration, before any other work.
  **The only liveness signal.**
- `snapshot`, every id whose status line read exactly `**Status:** open` at `startedAt`, in file
  order. **The run's work list, never appended to.** Entries filed later belong to the next run.
  Without it a run cannot end, because a host that mandates filing during verification refills the
  file faster than one item per firing empties it.
- `inFlight`, `null` or the firing currently executing. Set as the first act of an iteration, cleared
  on every exit path. Nothing else stops two firings overlapping in Steps 1 to 4, before a claim
  exists.
- `claim`, `null` or the entry being worked. **The authoritative claim record.** `step` is the step
  number reached, so a firing that stops anywhere between Step 10 and Step 13 stays visible.
  `lastFailure` is the raw tail of the last failing gate.
- `pendingQuestion.answer` starts `null` and is filled by whichever session receives the user's reply.
- `finished`, `null` or the UTC timestamp Step 14 wrote. **A finished ledger is inert**: it records
  no work, blocks no work, and never starts a loop.

## Startup: the re-entrancy guard

Because `/loop-todos` starts its own loop and every firing re-enters this same skill, a firing must
never create a second loop, and two firings must never work one checkout at once.

The ledger is the primary signal and `CronList` only confirms. `CronList` is documented as listing
jobs "scheduled via CronCreate in this session", and whether interval-mode `loop` registers there is
an assumption rather than a verified fact, so **an empty `CronList` is never proof that no loop is
running** and never a reason to start one. Read this working tree's ledger and take the first case
that matches:

1. **`finished` is set.** A previous run ended and could not confirm its own cancel, so it left the
   ledger deliberately. Report that run's summary, say the loop may still be firing, and give the
   two steps to clear it: cancel the job, then delete the ledger. **Start nothing and work nothing.**
   A finished ledger is not a missing one, and treating it as a first run turns an unconfirmed
   cancel into two loops.
2. **`inFlight` set, `session` not this session.** Another firing is mid-iteration. **Write
   `lastFiredAt` and nothing else**, report one line naming `inFlight.since` and `claim.todo` if there
   is one, end. Standing down is still evidence the loop is alive, and skipping the heartbeat here
   would send the firing after a long iteration to case 5 as a false orphan. If `inFlight.since` is
   older than four times the interval the firing that set it died: report it with the full `claim`,
   ask whether to resume or clear the marker, wait. **Never take a stale marker over automatically.**
   An iteration on a slow host outlives several intervals, and a wrong takeover is the
   two-workers-one-tree failure this guard exists to prevent.
3. **No ledger.** First run. Run Step 1 before anything else, because a project with no backlog must
   not get a loop at all. Then write the ledger — `startedAt`, `lastFiredAt`, `interval`, `worktree`,
   `snapshot`, `inFlight` — invoke the `loop` skill with the interval and `/loop-todos` as its
   command, and immediately run iteration 1 in this same session from Step 2.
4. **`lastFiredAt` within four times the interval.** A live run. Set `inFlight`, write `lastFiredAt`,
   go to Step 1. An empty `CronList` changes nothing here.
5. **`lastFiredAt` older than four times the interval.** The firings stopped. Report `startedAt`,
   `lastFiredAt`, `branch`, `closed`, `claim`, `pendingQuestion`, and how much of `snapshot` is left,
   then ask whether to resume, restart, or clear. Do nothing until they answer.

Cases 4 and 5 test `lastFiredAt`, never `startedAt`. A healthy run outlives four intervals inside the
first hour on any project whose gates take real time, so testing the start time would send every such
run to case 5 while it was working perfectly.

## Per-iteration workflow

Update `claim.step` as each step is entered, from Step 5 on. That one number is what lets a later
firing tell a half-implemented item from a closed-but-uncommitted one.

**Clear `inFlight` on every exit, without exception** — closed, held, blocked, stopped, finished. A
step that says "stop" without saying "clear `inFlight`" still means it. An uncleared marker makes the
next firing stand down under guard case 2, silently turning a held question into a dead loop.

### Step 1: Discover the backlog

First match wins: `docs/TODO.md`, `TODO.md`, `BACKLOG.md`, `docs/todo/`. Record which one, and use
only that file for the rest of the run.

If none exists, report that, suggest the `setup-todo-backlog` skill, and **stop without starting a
loop**. A recurring job against a project with nothing to work on is noise on a timer.

### Step 2: Read the host's rules

First match wins: `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`. Read the whole file, plus any rule
file it links that covers verification, git, or documentation.

**Hard rule: the host file overrides every default in this skill.** Its verification gates, git
policy, docs policy, and entry-closing convention win outright, **where it speaks to the case in
hand, not merely where it names the topic.** A host rule governing one branch, one file type, or one
situation says nothing about the others, and this skill's default still fills that silence. Read the
scope of the rule, not its heading. Where the host contradicts this skill on a case it actually
covers, follow the host and say so in the report.

### Step 3: Resume or hold

The ledger decides this, not the backlog file. Take the first case that matches:

1. **`pendingQuestion.answer` is set.** The user answered. Clear `pendingQuestion`, carry the answer
   into the work, and **resume the held entry at `claim.step`**, except a claim still at Step 6,
   which resumes at Step 7 so the answered question is not re-asked. Without this branch an answered
   question holds the claim forever, because `pendingQuestion` is cleared nowhere else Step 3 reaches.
2. **`pendingQuestion` set, `answer` null.** Re-surface the question verbatim with its todo id and
   `askedAt`, say the claim is still held, and **name the ledger's path and the `answer` field**, so
   the reply can be recorded by hand if no session picks it up. Stop.
3. **`claim` set, `attempts[claim.todo]` at 3.** Verification is exhausted. Re-surface `claim.todo`,
   the count, and `claim.lastFailure`. Stop. Never spend a fresh ceiling on it.
4. **`claim` set, `claim.step` 10 or higher.** The entry already reads `resolved` in the working tree
   and nothing is committed. **Resume at `claim.step`.** No in-progress line exists in this state, so
   only the ledger can detect it.
5. **`claim` set, `claim.step` below 10.** An earlier firing stopped mid-implementation. Report
   `claim.todo`, `claim.step`, `attempts[claim.todo]` and `claim.lastFailure`, **saying plainly when
   either is absent** rather than reporting a count nobody took. Resume at `claim.step`.
6. **Nothing held.** Go to Step 4.

Cases 1 to 5 select no new work. A second entry on top of an unfinished one mixes two changes into
one working tree, and the next commit cannot be split apart.

### Step 4: Select exactly one entry

Candidates are the ids in `snapshot` absent from `closed` whose status line still reads exactly
`**Status:** open`. `decided, deferred` never enters `snapshot`, the deferral being a decision
already made.

**Filter first, on dependencies.** Scan the body for every bullet naming another entry id. A
candidate is ineligible while any named id is still open or deferred, **unless the verb is one of
these**: `Blocks`, `Related:`, `See also`, `Supersedes`. Everything else reads as a dependency,
including bare mentions and prose forms like `prerequisite for` or `after`. Then:

- **A safe verb is a reason to look, not a reason to clear.** Read the referenced entry and state
  which way the work runs. Real backlogs bury hard dependencies under `Related:`, where one entry
  cannot start until the other's binary, config, or migration exists.
- **Over-exclusion is the intended failure mode.** A skipped candidate costs one firing. A missed
  dependency costs a change that cannot work.
- **A `YYYY-MM-DD-slug` with no `TODO-` prefix is an ADR or doc stem**, not an entry. Ignore it here.

**Then rank what survives:**

1. Entries whose body carries **both** a locked decision and concrete evidence: a decision already
   taken, a measured number, a command's output, a reproduction. Those can be finished without
   inventing requirements. A one-line wish cannot.
2. Within a tier, an entry that **blocks** another still-open entry outranks one that does not.
   `Blocks` points the opposite way to a dependency and earns a rank here rather than sitting as an
   unscored aside.
3. Oldest date component in the id, then first appearance in the file, top to bottom. Those two
   together are a total order, because no two entries occupy one position. The date alone is not:
   real backlogs file many entries on one day, and a tie-break that leaves the pick undefined lets
   two firings choose differently from identical input.

**Drained is not the same as blocked.** `snapshot` minus `closed` empty means the run is done, go to
Step 14. Entries remaining but every one filtered out means the run is blocked, not finished: report
which ids are blocked and on what, stop the iteration, **do not go to Step 14**. Cancelling over a
temporarily blocked set ends a run with work still in it, and widening the filter is what makes that
set non-empty more often.

### Step 5: Claim the entry

Write `claim` to the ledger **first**: `todo`, `since` from `date -u +%Y-%m-%dT%H:%M:%SZ`, `session`,
`step`, `lastFailure` null. The session handle is the first 8 characters of the harness session id
when one is exposed, otherwise `uuidgen | cut -c1-8`. Then rewrite that entry's status line, in the
working tree only, to:

```
**Status:** in progress, since 2026-08-01T14:32:11Z (session a1b2c3d4)
```

**This is a deliberate fourth value in a three-value vocabulary, and it is a breadcrumb, not the
record.** `setup-todo-backlog` defines three states only, so a reader who knows that rule would
otherwise read this line as a bug and delete it. It exists so a human reading `git diff` sees what a
worker is holding. The ledger's `claim` is what this skill reads, and no step recovers state from the
line, so a commit carrying it by accident is untidy rather than a lost claim. It is still transient
and uncommitted: Step 10 replaces it with `resolved`, and the only transition git should record is
`open` to `resolved`.

**Offer, once per project, to document the transient state in the host's policy**, unless its
`## TODO / Known issues` section already mentions it. Propose exactly one line, wait for a yes, and
**never edit the host's policy file without asking**. If the user declines, drop it for this run.

```
- A worker may set `**Status:** in progress, since <ISO8601> (session <id>)` while an entry is being
  worked. It is a working-tree-only state and never reaches a commit.
```

### Step 6: Stop if the entry is underspecified

Before writing any code, decide whether the entry contains enough to finish it correctly. It does not
when:

- The fix has two defensible shapes and the entry picks neither. A "decision locked" bullet that then
  lists candidates has locked the direction, not the shape.
- A value, threshold, or name is needed and appears nowhere, or the right behaviour depends on intent
  nobody wrote down.
- **The body contradicts its own status line.** A bullet reading `Deferred because ...`,
  `Decision locked ... rather than ...`, or `Workaround in place` under a `**Status:** open` heading
  means the entry records a decision its status does not carry. Ask which is current. Never resolve
  that contradiction yourself, and never let the status line win just because Step 4 read it first.

Then, in this order:

1. Write `pendingQuestion` with the todo id, the question, `askedAt`, and `answer` null.
2. Ask the user, naming the entry and the specific choice you need made. **Tell them the answer is
   picked up on the next firing**, and that whichever session receives their reply must write it into
   `pendingQuestion.answer` before acting on it. Firings do not share the interactive session's
   context, so an answer nobody writes down never arrives.
3. **Hold the claim.** Leave `claim` and the status line in place, clear `inFlight`, stop.

**Never guess, and never start a second entry to fill the time.** A loop that guesses produces
confident wrong work at machine speed, and nobody reads it until the run is over. An idle firing
costs nothing. Step 3 case 1 brings the answer back into the work.

### Step 7: Prepare the ground

Before touching any code, twice over. **Run the host's prerequisites** first. Its gates often depend
on a step documented somewhere other than the gate list: a build the typecheck needs, an install, a
generated file. Read its commands and setup sections, not only the numbered gates. **A failed
prerequisite is a stop, not a verification round.** Report it, hold the claim, clear `inFlight`, and
never spend the Step 9 ceiling diagnosing a toolchain the host documents as needing setup.

**Record the baseline.** Run the gates once now, against untouched code, and write each result into
`baselines` under that gate's label. Where the host states its own known-failure numbers, record both
its figure and yours, and say so when they disagree. Without this, a gate the host already documents
as red is indistinguishable from one this iteration broke.

### Step 8: Implement

Follow the host project's own conventions rather than generic ones: its file layout, naming, error
handling, and the patterns already in the files you are touching. Read the surrounding code before
changing it. Keep the change scoped to the entry. Anything you notice outside that scope is a
candidate for a new backlog entry, not a second change in this commit.

### Step 9: Verify it landed

**When the host defines gates, run them verbatim, in its order, with its commands.** Never substitute
an equivalent. Four qualifications, all about reading a result rather than changing a command:

- **Baseline.** A gate whose `baselines` entry already failed passes when the result matches that
  baseline, fails when it is worse, and passes with a note when it is better. **Never make such a
  gate green by relaxing a rule or widening a config.** A host that both demands zero errors and
  documents a standing failure count has defined the baseline as the bar, whatever its first
  sentence says.
- **Committed-range gates.** A gate defined over a committed range — `main...HEAD`, `origin/main..`,
  a PR diff — cannot see uncommitted work and reports clean on an empty diff. Run those **after Step
  12**, then re-run the fast gates if they produce fixes. **Never commit early to give one something
  to read.** That is the one realistic way the breadcrumb status line reaches history.
- **A host's own backlog sweep.** If a host gate both files and closes entries, run only its filing
  half here. Closing is Step 10's job and is **scoped to the claimed entry**: one entry per iteration
  holds even when a host gate invites a second. Anything filed here goes into the file and **not**
  into `snapshot`.
- **Metered gates.** A gate the host describes as costing money or credits runs at most once per
  item and 6 times per run. Count each run in `credits`, and at the cap skip it, say so, name the cap.
  A per-session budget written for a human becomes a per-interval budget under a loop, and a metered
  gate that auto-applies its own fixes still respects the ceiling below.

When the host defines none, detect what exists and run only that:

- Package manifest scripts named `lint`, `format`, `typecheck`, `types`, `check`, `test`, or
  `Makefile` targets `lint`, `check`, `test`
- Language-native commands where the manifest shows the toolchain configured: `cargo clippy` /
  `cargo test`, `go vet ./...` / `go test ./...`, configured `ruff` / `mypy` / `pytest`
- CI workflow files as the tiebreaker. What CI runs is what this project considers passing.
- Never install a tool, never add a script, never invent a gate. If nothing is detectable, say so in
  the report and never describe the change as verified.

**Failure ceiling: up to 3 fix-and-reverify rounds.** Each round is one diagnosis, one fix, one full
re-run of the gates. Increment `attempts` and write `claim.lastFailure` on every failure.

Still failing after the third round, stop the iteration, keep the changes uncommitted exactly as they
are, keep the claim held, clear `inFlight`, and put the raw failing output in front of the user
rather than a paraphrase of it. **Never revert the work, never commit it, never mark the entry
resolved.** Reverting throws away three rounds of diagnosis the user is about to need, and committing
puts a broken change on the branch under a message claiming it works.

### Step 10: Close the entry

Set `claim.step` to 10 first. From here the working tree shows no in-progress line for this entry, so
the ledger is the only thing that knows the item is unfinished. Then follow the host's convention
when it defines one. For a `setup-todo-backlog`-shaped backlog:

1. Move the whole entry to the `## Resolved` section at the bottom of the same file, keeping its id.
2. Replace the status line with exactly `**Status:** resolved YYYY-MM-DD`. No trailing period, no
   appended sentence. The line stays machine-readable.
3. Put what landed in the first bullet under it, not on the status line.
4. Collapse the body to the problem and what fixed it. Drop the evidence bullets and the traps.
5. **Update, without closing, any other entry whose evidence this change invalidated.** A count or a
   reproduction in a sibling entry that is now wrong is stale documentation sitting inside the
   backlog. Narrow it, never drop its number, and never close it as a second item.

**Only close on evidence**: the gates in Step 9 passed against their baseline, or the defect provably
no longer reproduces. Never close on "looks fixed".

### Step 11: Update what the change made stale

Per the host's docs policy. Where it is silent, check at minimum four things. The README, when a
command, script, port, prerequisite, or limitation changed. Architecture or ADR docs, when the change
altered a cross-cutting decision. Any scenario or behaviour doc the host names, when user-visible
behaviour changed. Any changelog or session log the host requires per change. Nothing stale means
saying so in one line, not inventing an update.

**An instruction file is the case that stalls.** Hosts routinely require their agent-instructions
file to be updated by hand and asked about first, and closing an entry those instructions name by id
triggers exactly that. When this step needs an answer, write `pendingQuestion`, ask, hold the claim
with `claim.step` at 11, clear `inFlight`, stop, in the same shape as Step 6. Step 3 case 4 brings the
iteration back here. Without the ledger's `claim` this is the state that silently loses an entry:
closed in the tree, uncommitted, invisible to anything reading the backlog file.

### Step 12: Commit

The host's git policy wins wherever it speaks to this case. Where it is silent:

- **One feature branch per run**, named `backlog/auto-YYYY-MM-DD`, created on the first item and
  recorded in `branch`. Later items commit onto it. If the name is taken, append `-2`, `-3`. A host
  rule that only says what to do on its default branch has not spoken about the others, so this
  default still applies there rather than piling backlog commits onto an unrelated branch.
- **One conventional commit per closed item.** Subject describes the fix. The body names the todo id
  on its own line, so `git log --grep` finds it later.
- Stage by explicit path. Never `git add -A`. **Before staging the backlog file, confirm its status
  line reads `resolved` and not the breadcrumb.**
- **Never push, never open a PR, never touch a remote.** The user reviews the branch. No git
  repository at all: skip this step and report the change as uncommitted.

Then run any committed-range gate deferred from Step 9 and treat its findings as one more
verification round, ceiling included. Fixes it produces get their own commit on the same branch, not
an amend. **This step is re-entered whenever a firing dies inside it**, so check `git log --grep` for
the todo id first and skip whatever already landed rather than committing it twice.

### Step 13: Record and end the iteration

Append the id to `closed`, drop its `attempts` entry, clear `claim`, clear `pendingQuestion` if it
belonged to this entry, and clear `inFlight`. Report one line: the id, what landed, the commit's
short sha, and how much of `snapshot` is left. Then end the iteration. Do not pick up a second entry.

### Step 14: Finish the run

When Step 4 finds nothing left in `snapshot`:

1. Print the run summary: `startedAt`, `branch`, every id in `closed`, and anything still held.
2. **Write `finished` with the current UTC timestamp, before attempting the cancel.** The ledger is
   inert from that moment, so a firing racing the cancel reads guard case 1 and does nothing instead
   of mistaking a live run for an orphan.
3. Cancel the loop with `CronDelete` on the job id from `CronList`.
4. **Cancel confirmed** — archive the ledger by renaming it `run-<startedAt>.json` beside itself. The
   run is over and a later `/loop-todos` starts clean.
5. **Cancel not confirmed**, no job id or the delete failed — **leave the ledger exactly where it
   is.** Tell the user the job could not be found, that they cancel the loop themselves, and that
   deleting the ledger is the last step. Every firing until then hits guard case 1, does nothing, and
   repeats those two instructions.

Archiving while the loop may still be firing is the one mistake that produces two loops: the next
firing finds no ledger, reads it as a first run, starts a second. `finished` is what makes leaving
the file behind harmless rather than a permanent orphan.

## Claim release

Every exit path releases or holds the claim deliberately, and the ledger records which. **A claim
must never persist with nothing recorded.**

| Exit | Claim | Ledger |
|---|---|---|
| Item closed, Steps 10 to 13 | released | `claim` cleared, `closed` appended, commit records `open` to `resolved` |
| Question outstanding, Step 6 or 11 | **held**, so the next firing resumes rather than restarts | `pendingQuestion` set, `answer` null, `claim.step` records how far it got |
| User answers | resumes at `claim.step` | the receiving session writes `pendingQuestion.answer`, Step 3 case 1 picks it up |
| Prerequisite failed, Step 7 | **held** | `claim.lastFailure` set, `attempts` untouched, because a broken toolchain is not a failed verification |
| Verification failed 3 times, Step 9 | **held**, uncommitted changes sit in the tree | `attempts` at 3, `claim.lastFailure` set, raw output shown. Step 3 case 3 refuses a second ceiling |
| Interrupted, or the session died | **held** wherever it stopped, **including after Step 10**, where the backlog file shows nothing amiss | `claim.step` survives and is what Step 3 reads |
| User abandons | released by hand, restore `**Status:** open` | clear `claim`, `pendingQuestion`, `attempts`. Leave the id in `snapshot`. Settle the uncommitted changes with the user, never discard them unasked |

## Backlog entry format (quick reference)

Inlined so this skill works where `setup-todo-backlog` was never run. That skill is the source.

- **Id**: `## TODO-YYYY-MM-DD-slug: <declarative claim>`, the date filed plus a 2-5 word kebab-case
  slug. The heading is the id. Ids are immutable, never reused, and are how entries cross-reference.
- **Status**, on its own line under the heading, one of three in a committed file: `**Status:** open`,
  `**Status:** decided, deferred` (free text after the comma), `**Status:** resolved YYYY-MM-DD`, plus
  the transient fourth value of Step 5.
- **Body**: 5-8 bullets covering the problem, the evidence, the decisions already locked, and the
  traps. No subsections, no tables, no prose paragraphs. **Closing**: per Step 10, never by deletion.

## Rules

The invariants. Each has a mechanism above, and the mechanism is what makes it true. They are here so
a firing that has drifted can check itself.

- **Exactly one entry per iteration**, and the run's backlog is `snapshot`, not the file.
- **The ledger is the authority on run state**, not the backlog file and not `CronList`. Never
  committed, never off the machine.
- **The host outranks this skill on every conflict it actually covers**, and a host rule scoped to
  one case is silent about the rest.
- **Never guess a requirement.** Guessing at loop speed produces wrong work faster than anyone reads
  it. **Never edit the host's policy file without asking**, either.
- **Never mark an entry resolved without its gates passing against their recorded baseline**, never
  make a red gate green by relaxing it, never close on "looks fixed". A baseline is a list of known
  defects, and widening a rule deletes the list rather than the defects.
- **Never commit an entry before Step 10 has closed it**, including to feed a committed-range review.
  Step 12 commits with the claim still held, and Step 13 is what releases it. **Never revert failed
  work and never commit it.** Never push, open a PR, or touch a remote.
- **Never start a second loop.** A missing ledger is the only signal that justifies creating one, and
  a `finished` ledger is not a missing one. **Never archive one while the loop may still be firing.**
- **A held claim is always recorded and always reported.** Silence plus unfinished work is the one
  state this skill must never produce.

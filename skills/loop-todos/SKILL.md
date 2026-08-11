---
name: loop-todos
disable-model-invocation: true
description: MANUAL-INVOCATION-ONLY skill — do NOT auto-trigger. Only invoke when the user explicitly types the literal slash command `/loop-todos`. Natural-language phrasing such as 'work through the backlog', 'fix the todos', 'clear the backlog', or any paraphrase are ANTI-TRIGGERS — they MUST NOT load this skill; handle with ordinary tools and, if helpful, ask whether to run `/loop-todos`. When invoked — starts a recurring, self-cancelling loop in the project. Each firing claims one open backlog entry, writes a plan for it, implements that plan, verifies it against the project's own gates, closes the entry, updates stale docs, and opens one pull request per entry via the `ship-pr` skill. Optional interval argument, default 10 minutes, e.g. `/loop-todos 30m`. Do NOT use for creating or formatting a backlog (that's `setup-todo-backlog`), filing or closing one entry by hand, or a one-off task with no backlog involved.
---

# Loop TODOs

## What this does, and how to run it

```
/loop-todos          # fires every 10 minutes
/loop-todos 30m      # fires every 30 minutes
```

An autonomous backlog worker. The user types it once, in the project directory. The optional argument
is the interval, default `10m`, handed straight to the `loop` skill. Every firing picks up exactly one
open backlog entry, plans it, and drives it to a verified, documented finish in its own pull request,
then stops. Later firings re-enter this skill, detect the run already going, and go straight to the
work. It cancels itself once the backlog empties, and until then the user cancels it. One loop,
sequential firings, one checkout. Never two entries at once, never a second loop.

## Portability

- **Assume nothing.** No language, layout, package manager, test runner, or CI. Detect and use.
- **The host project outranks this skill on every conflict it covers**, per Step 2. Its defaults
  apply where the host is silent, and a host rule scoped to one case is silent about the rest.
- **Degrade cleanly, never guess.**
  - No backlog file: report it, suggest the `setup-todo-backlog` skill, stop without starting a loop.
  - No git repository, or a repository with no `origin`: ledger in `.claude/loop-todos/`, skip the
    branch in Step 5 and the ship in Step 12 entirely, say plainly after every item that the work is
    uncommitted and unshipped. Both degrade the same way, because both leave nothing to push to.
  - No detectable gates: say so in that item's report, name what you looked for, never claim the
    change was verified. No host instructions file: use this skill's defaults and report that.

## The run ledger

One JSON file doing four jobs: the re-entrancy guard, the claim record, the run record, and the
source of the final summary. **It is the authority on every piece of run state.** Where a step and
the ledger disagree, the ledger is right.

**Location**, first match wins:

1. In a git repo, `<common>/loop-todos/run-<key>.json`, where
   - `<common>` is `git rev-parse --path-format=absolute --git-common-dir`. **Ask for the absolute
     form explicitly**: the bare flag returns a path relative to the current directory, so one
     resolved in a shell call and used in another lands somewhere else.
   - `<key>` is `git rev-parse --show-toplevel | shasum | cut -c1-12`, giving **one ledger per
     working tree**, a shared one letting a firing join another tree's run and append to its `closed`.
     Local state divides that way cleanly. `origin`'s branch namespace does not, which is why Step 5
     checks the remote for `backlog/` branches this ledger cannot account for.
2. `.claude/loop-todos/run.json` otherwise.

Either path sits outside the working tree, so no `git add` can sweep the ledger into a commit.
**Schema**, every field once. Later steps name a field rather than redescribing it.

```json
{
  "startedAt":       "2026-08-01T14:32:11Z",
  "lastFiredAt":     "2026-08-01T15:12:04Z",
  "interval":        "10m",
  "worktree":        "/abs/path/to/checkout",
  "startBranch":     "worktree-inherited-popping-stardust",
  "prs":             [{ "todo": "TODO-2026-07-30-foo", "branch": "backlog/TODO-2026-07-30-foo",
                        "base": "main", "url": "https://github.com/o/r/pull/12" }],
  "snapshot":        ["TODO-2026-07-30-foo", "TODO-2026-08-01-bar"],
  "closed":          ["TODO-2026-07-30-foo"],
  "inFlight":        { "since": "2026-08-01T15:12:04Z", "session": "a1b2c3d4" },
  "claim":           { "todo": "TODO-...-bar", "since": "...", "session": "a1b2c3d4", "step": 9,
                       "plan": "plans/TODO-...-bar.md", "lastFailure": null },
  "pendingQuestion": { "todo": "TODO-...-bar", "question": "<text>", "askedAt": "...",
                       "answer": null },
  "attempts":        { "TODO-2026-08-01-bar": 2 },
  "baselines":       { "lint repo/": "40 errors, 0 warnings" },
  "credits":         { "cr review": 3 },
  "finished":        null
}
```

Self-evident from the shape: `interval` as passed, `worktree` from `git rev-parse --show-toplevel`
(a mismatch against the current tree is a stop, not a warning), `startBranch` the branch HEAD sat on
before Step 5 first moved it and the one Step 14 puts back, `closed` in order, `attempts` per todo
id, `baselines` per gate label from Step 7, `credits` per metered gate. The rest earn their keep:

- `startedAt`, first run, UTC. Identity only. **Never a liveness signal**, because it never moves.
- `lastFiredAt`, rewritten by every firing that decides it is an iteration, before any other work.
  **The only liveness signal.**
- `snapshot`, every id whose status line read exactly `**Status:** open` at `startedAt`, in file
  order, **read from `origin/<default-branch>` and never from the working tree**. The run's work list,
  never appended to: entries filed later belong to the next run, and without that a host mandating
  filing during verification refills the file faster than one item per firing empties it. The read
  source matters because Step 5 branches off the remote's default — a checkout behind it yields ids
  the run can never see, one ahead yields ids Step 10 cannot find to close.
- `inFlight`, `null` or the firing currently executing. Set as the first act of an iteration, cleared
  on every exit. Nothing else stops two firings overlapping in Steps 1 to 4, before a claim exists.
- `prs`, one record per item Step 12 shipped, empty until the first, appended never rewritten. **The
  last record's `branch` is the next item's base**, per Step 5, so the array is the stack in merge
  order and an unwritten record restarts it at the default. `base` is what Step 12 retargeted onto.
- `claim`, `null` or the entry being worked. **The authoritative claim record.** `step` is the step
  number reached, so a firing that stops anywhere between Step 10 and Step 13 stays visible. `plan` is
  that entry's plan file from Step 7, re-read on resume rather than re-derived. `lastFailure` is the
  raw tail of the last failing gate, or of a `ship-pr` abort.
- `pendingQuestion.answer` starts `null` and is filled by whichever session receives the user's reply.
- `finished`, `null` or the UTC timestamp Step 14 wrote. **A finished ledger is inert**: it records
  no work, blocks no work, and never starts a loop.

## Startup: the re-entrancy guard

Because `/loop-todos` starts its own loop and every firing re-enters this same skill, a firing must
never create a second loop, and two firings must never work one checkout at once.

The ledger is the primary signal and `CronList` only confirms. It lists jobs "scheduled via CronCreate
in this session", and whether interval-mode `loop` registers there is an assumption, so **an empty
`CronList` is never proof that no loop is running**. Take the first case that matches:

1. **`finished` is set.** A previous run ended and could not confirm its own cancel, so it left the
   ledger deliberately. Report that run's summary, say the loop may still be firing, and give the
   steps to clear it: cancel the job, then delete the ledger. **Start nothing and work nothing.**
   A finished ledger is not a missing one, and reading it as a first run turns an unconfirmed cancel
   into two loops.
2. **`inFlight` set, `session` not this session.** Another firing is mid-iteration. **Write
   `lastFiredAt` and nothing else**, report one line naming `inFlight.since` and `claim.todo` if there
   is one, end. Standing down is still evidence the loop is alive, and skipping the heartbeat would
   send the firing after a long iteration to case 5 as a false orphan. If `inFlight.since` is older
   than four times the interval the firing that set it died: report it with the full `claim`, ask
   whether to resume or clear the marker, wait. **Never take a stale marker over automatically** — an
   iteration on a slow host outlives several intervals, and a wrong takeover is the
   two-workers-one-tree failure this guard exists to prevent.
3. **No ledger.** First run. Run Steps 1 and 2 before anything else: a project with no backlog must
   not get a loop at all, and Step 2 is where the default branch is settled. Then `git fetch origin`
   and build `snapshot` from `git show origin/<default-branch>:<backlog-path>`, per its schema entry
   above, falling back to the working tree only where Portability says there is no repo and no
   `origin`. Write the ledger — `startedAt`, `lastFiredAt`, `interval`, `worktree`, `startBranch`
   from `git rev-parse --abbrev-ref HEAD`, `snapshot`, `inFlight` — invoke the `loop` skill with the
   interval and `/loop-todos` as its command, and run iteration 1 in this session from Step 2.
4. **`lastFiredAt` within four times the interval.** A live run. Set `inFlight`, write `lastFiredAt`,
   go to Step 1. An empty `CronList` changes nothing here.
5. **`lastFiredAt` older than four times the interval.** The firings stopped. Report `startedAt`,
   `lastFiredAt`, `prs`, `closed`, `claim`, `pendingQuestion`, and how much of `snapshot` is left,
   then ask whether to resume, restart, or clear. Do nothing until they answer.

Cases 4 and 5 test `lastFiredAt`, never `startedAt`: a healthy run outlives four intervals inside the
first hour wherever gates take real time, and the start time would read it as a case-5 orphan.

## Per-iteration workflow

Update `claim.step` as each step is entered, from Step 5 on. That one number is what lets a later
firing tell a half-implemented item from a closed-but-unshipped one.

**Clear `inFlight` on every exit, without exception** — closed, held, blocked, stopped, finished. A
step that says "stop" without saying "clear `inFlight`" still means it. An uncleared marker makes the
next firing stand down under guard case 2, silently turning a held question into a dead loop.

### Step 1: Discover the backlog

First match wins: `docs/TODO.md`, `TODO.md`, `BACKLOG.md`, `docs/todo/`. Record which one, and use only
that path for the rest of the run. The **path** is found in the working tree, its **content** read
from the item's base, per Step 4.

If none exists, report that, suggest the `setup-todo-backlog` skill, and **stop without starting a
loop**. A recurring job against a project with nothing to work on is noise on a timer.

### Step 2: Read the host's rules

First match wins: `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`. Read the whole file, plus any rule
file it links that covers verification, git, or documentation.

**Hard rule: the host file overrides every default in this skill.** Its verification gates, git
policy, docs policy, and entry-closing convention win outright, **where it speaks to the case in
hand, not merely where it names the topic.** A host rule governing one branch, one file type, or one
situation says nothing about the others, and this skill's default still fills that silence. Read the
scope, not the heading. Where the host contradicts this skill on a case it covers, follow the host
and say so in the report. Step 12's push carve-out is the single stated exception.

### Step 3: Resume or hold

The ledger decides this, not the backlog file. Take the first case that matches:

1. **`pendingQuestion.answer` is set.** The user answered. Clear `pendingQuestion`, carry the answer
   into the work, and **resume the held entry at `claim.step`**, except a claim still at Step 6,
   which resumes at Step 7 so the answered question is not re-asked. Without this branch an answered
   question holds the claim forever, because `pendingQuestion` is cleared nowhere else Step 3 reaches.
2. **`pendingQuestion` set, `answer` null.** Re-surface the question verbatim with its todo id and
   `askedAt`, say the claim is still held, and **name the ledger's path and the `answer` field**, so
   the reply can be recorded by hand if no session picks it up. Stop.
3. **`claim` set, `attempts[claim.todo]` at 3.** The ceiling is spent, on verification or on shipping.
   Re-surface `claim.todo`, the count, and `claim.lastFailure`. Stop. Never spend a fresh ceiling on
   it. Step 12's aborts share this counter deliberately: a permanent one — no `origin`, no provider
   CLI, an unsupported host — reproduces every firing, and uncounted it holds the loop forever.
4. **`claim` set, `claim.step` 10 or higher.** The entry already reads `resolved` in the working tree
   and nothing is shipped. **Resume at `claim.step`.** No in-progress line survives here, so only the
   ledger can detect it.
5. **`claim` set, `claim.step` below 10.** An earlier firing stopped mid-implementation. Report
   `claim.todo`, `claim.step`, `attempts[claim.todo]` and `claim.lastFailure`, **saying plainly when
   either is absent** rather than reporting a count nobody took. Resume at `claim.step`.
6. **Nothing held.** Go to Step 4.

Cases 1 to 5 select no new work. A second entry on top of an unfinished one mixes two changes into
one working tree, and one PR cannot be split back into two.

**Resuming at `claim.step` 6 or higher checks the branch first.** `git rev-parse --abbrev-ref HEAD`
must read `backlog/<claim.todo>`. Nothing else enforces it: the plan file is untracked and the backlog
edit uncommitted, so both survive a branch switch and the tree looks correct on the wrong branch.
`ship-pr` then stays wherever HEAD is and Step 12 records a `branch` git does not have. A mismatch is
a stop — report both names and ask, never check out silently.

### Step 4: Select exactly one entry

Candidates are the ids in `snapshot` absent from `closed` whose status line still reads exactly
`**Status:** open` **in this item's base** — `origin/<default-branch>` for the run's first item,
`prs[-1].branch` after that, and the working tree where Portability leaves no base to read. Use
`git show <base>:<backlog-path>`, not HEAD, for the reason `snapshot` gives. `decided, deferred` never
enters `snapshot`, that deferral being a decision made.

**Filter first, on dependencies.** Scan the body for every bullet naming another entry id. A
candidate is ineligible while any named id is still open or deferred, **unless the verb is one of
these**: `Blocks`, `Related:`, `See also`, `Supersedes`. Everything else reads as a dependency,
including bare mentions and prose forms like `prerequisite for` or `after`. Then:

- **A safe verb is a reason to look, not a reason to clear.** Read the referenced entry and state
  which way the work runs. Real backlogs bury hard dependencies under `Related:`, where one entry
  cannot start until the other's binary, config, or migration exists.
- **Over-exclusion is the intended failure mode.** A skipped candidate costs one firing, a missed
  dependency costs a change that cannot work.
- **A `YYYY-MM-DD-slug` with no `TODO-` prefix is an ADR or doc stem**, not an entry. Ignore it here.

**There is deliberately no file-overlap filter, and re-adding one would be a regression.** Items
stack, per Step 5, so item N's branch already contains items 1 to N-1 and two items touching one file
cannot conflict. The filter this replaced matched paths named in an entry's prose against paths a
shipped PR touched, and was blind by construction: it never saw the backlog file or a lockfile, which
every item changes and no entry names, and it could not know a candidate's files before Step 7.

**Then rank what survives:**

1. Entries whose body carries **both** a locked decision and concrete evidence: a decision already
   taken, a measured number, a command's output, a reproduction. Those can be finished without
   inventing requirements. A one-line wish cannot.
2. Within a tier, an entry that **blocks** another still-open entry outranks one that does not.
   `Blocks` points the opposite way to a dependency, and earns a rank here rather than an aside.
3. Oldest date component in the id, then first appearance in the file. Together a total order, since
   no two entries occupy one position. The date alone is not, and an undefined pick lets two firings
   choose differently.

**Drained is not the same as blocked.** `snapshot` minus `closed` empty means the run is done, go to
Step 14. Entries remaining but every one filtered out on a dependency means the run is blocked, not
finished: report which ids are blocked and on what, stop the iteration, **do not go to Step 14**.
Cancelling over a temporarily blocked set ends a run with work still in it.

### Step 5: Claim the entry and branch

The acts, and the order is the point:

1. **Write `claim` to the ledger.** `todo`, `since` from `date -u +%Y-%m-%dT%H:%M:%SZ`, `session`,
   `step`, `plan` null, `lastFailure` null. The session handle is the first 8 characters of the
   harness session id when one is exposed, otherwise `uuidgen | cut -c1-8`.
2. **`git fetch origin`**, so the branch point is current and so is
   `git ls-remote origin 'refs/heads/backlog/*'`. **A `backlog/` branch on the remote that this
   ledger's `prs` does not account for belongs to another tree's run.** Stop and report it. Ledgers
   are per working tree, `origin`'s branch namespace is not, so two trees can claim one entry blind.
3. **Create `backlog/<todo-id>` from this item's base**, e.g.
   `git checkout -b backlog/TODO-2026-08-01-bar origin/main`. The base is `origin/<default-branch>`
   for the run's first item and `prs[-1].branch`, the last shipped item's branch, for every item
   after. Take the default branch from the host's git policy, otherwise from
   `git symbolic-ref --short refs/remotes/origin/HEAD`. On the first move off it, record the outgoing
   branch in `startBranch` so Step 14 can put the tree back.
4. **Then** rewrite the status line, below.

**Items stack. Item N sits on item N-1's branch, never on the default alongside it.** One PR per entry
still holds and each shows only its own diff, but the stack removes the conflict an
independent-off-default layout guarantees: every item rewrites the backlog file, most touch a
lockfile, and no two branches cut from one commit both append to the same `## Resolved` tail cleanly.
**The accepted cost is a forced merge order** — oldest PR first, and rejecting one rebases every item
above it. That trade was made knowingly.

**A branch of that name already existing means an earlier firing made it: check it out instead of
appending a suffix, one branch per entry being what makes one PR per entry. Verify it before reusing
it.** `git merge-base --is-ancestor <base> backlog/<todo-id>` must hold, and its commits must be this
item's. A branch left by an abandoned run carries that run's commits, and the new item stacks on top
of them inside one PR. Step 12's guard reads the working tree, never the branch's history, so nothing
downstream catches it. A failed check is a stop, not a repair job.

**Branch from the base ref, never by checking out the base branch itself.** `git checkout main` fails
inside a linked worktree when another worktree already holds it — `fatal: 'main' is already used by
worktree at ...` — and that topology is exactly where this skill runs. Nobody should "simplify" this
into a checkout followed by a branch. **Branch before the working-tree edit**, so a switch never has
to carry a modified backlog file across, which it does cleanly only while that file matches between
HEAD and the base. No git repository, or no `origin`: skip acts 2 and 3 and the ship in Step 12.

The status line, rewritten in the working tree only, reads:

```
**Status:** in progress, since 2026-08-01T14:32:11Z (session a1b2c3d4)
```

**This is a deliberate value outside `setup-todo-backlog`'s closed status vocabulary, and it is a
breadcrumb, not the record.** A reader who knows that vocabulary is closed would otherwise
read this line as a bug and delete it. It exists so a human reading `git diff` sees what a worker is
holding. No step recovers state from it, the ledger's `claim` being what this skill reads, so a PR
carrying it is untidy rather than a lost claim. Step 10 replaces it with `resolved`, and the only
transition git should record is `open` to `resolved`.

**Offer, once per project, to document the transient state in the host's policy**, unless its
`## TODO / Known issues` section already mentions it. Propose exactly one line, wait for a yes, and
**never edit the host's policy file without asking**. If the user declines, drop it for this run.

```
- A worker may set `**Status:** in progress, since <ISO8601> (session <id>)` while an entry is being
  worked. It is a working-tree-only state and never reaches a commit.
```

### Step 6: Stop if the entry is underspecified, or the work needs an approval

Before the plan or the code, decide whether this firing can finish the entry unaided. It cannot when:

- The fix has two defensible shapes and the entry picks neither. A "decision locked" bullet that then
  lists candidates has locked the direction, not the shape.
- **The work needs an approval this firing cannot obtain.** Installing a package, touching a
  credential, spending on a paid service, editing the host's own instruction file. Step 2 reads the
  project's rules, and the rule forbidding the action often lives in the environment's. Ask first.
- A value, threshold, or name is needed and appears nowhere, or behaviour turns on unwritten intent.
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

**Never guess, and never start a second entry to fill the time.** Guessing at loop speed produces
confident wrong work nobody reads until the run is over, and an idle firing costs nothing. Step 3
case 1 brings the answer back into the work.

### Step 7: Prepare the ground and plan the work

Everything here happens before any code.

**Run the host's prerequisites** first. Its gates often depend on a step documented somewhere other
than the gate list: a build the typecheck needs, an install, a generated file. Read its commands and
setup sections, not only the numbered gates. **A failed prerequisite is a stop, not a verification
round.** Report it, hold the claim, clear `inFlight`, and never spend the Step 9 ceiling diagnosing a
toolchain the host documents as needing setup. **Re-run them after every Step 5 branch switch, not
once per run.** Build output is gitignored, so a checkout leaves it exactly as the previous item built
it, and a baseline measured against a stale artifact is not a baseline.

**Record the baseline.** Run the gates once now, against untouched code, and write each result into
`baselines` under that gate's label. Where the host states its own known-failure numbers, record both
its figure and yours, and say so when they disagree. Without this, a gate the host already documents
as red is indistinguishable from one this iteration broke.

**Write the plan.** One file per entry at `plans/<todo-id>.md`, or in the host's own planning directory
where its instructions name one. Put its path in `claim.plan`. The sections, in this order:

- **Goal** — the outcome the entry is asking for, in a sentence or two.
- **Locked decisions** — carried across from the entry's decision bullets, so implementation cannot
  quietly re-open one that was already settled.
- **Steps** — ordered, each small enough to check off on its own.
- **Files to touch** — the paths, so Step 8 can tell drift from surprise. Nothing downstream reads
  this list, so it is a plan and never a record of what shipped.
- **Gates that must pass** — the host's gates from Step 9, each with its baseline from above.
- **Out of scope** — what this item deliberately skips, so Step 8 tells a gap from a new entry.

**A resuming firing reads the existing plan rather than deriving a new one.** `claim.plan` pointing at
a file that exists means the plan is written, and re-deriving it throws away reasoning an earlier
firing committed to. The plan is committed with the item and lands in the PR beside the diff,
deliberately: nothing gates implementation on the user's approval, so the PR is where they read the
reasoning and the change together.

### Step 8: Implement

**Work the Step 7 plan, step by step, in its order.** A step that turns out to be wrong **updates the
plan file first, saying why, then proceeds.** Silent drift defeats the point of having written it,
because the PR reviewer reads the plan as the account of what was intended.

Follow the host's own conventions, not generic ones: file layout, naming, error handling, and the
patterns already in the files you touch, read before changing. Keep the change scoped to the entry.
Anything noticed outside it is a candidate for a new backlog entry, not a second change.

### Step 9: Verify it landed

**When the host defines gates, run them verbatim, in its order, with its commands.** Never substitute
an equivalent. Qualifications: most are about reading a result rather than changing a command,
and the one that does change a command says so and is bounded to that:

- **Baseline.** A gate whose `baselines` entry already failed passes when the result matches that
  baseline, fails when it is worse, and passes with a note when it is better. **Never make such a
  gate green by relaxing a rule or widening a config.** A host that both demands zero errors and
  documents a standing failure count has defined the baseline as the bar, whatever it says first.
- **Committed-range gates.** A gate defined over a committed range — `main...HEAD`, `origin/main..`,
  a PR diff — is pointed **here, at this item's full change set**, which before shipping is the
  working tree diffed against the item's base from Step 5. Substituting that base for the range's own
  is the one command edit this step permits: the host wrote its range assuming a single branch off
  the default, and the stack makes that base wrong. **Never commit early to give one something to
  read**, the one realistic way the breadcrumb reaches history, and **never defer one past Step 12**,
  which puts a review or security finding on an already-pushed PR. One that genuinely cannot read an
  uncommitted tree gets no commit made for it — report it as a gate that could not run, never as one
  that passed.
- **A host's own backlog sweep.** If a host gate both files and closes entries, run only its filing
  half here. Closing is Step 10's job and is **scoped to the claimed entry**: one entry per iteration
  holds even where a host gate invites a second. What is filed here goes in the file, not `snapshot`.
- **Metered gates.** A gate the host describes as costing money or credits runs **as often per item
  as the host's own budget allows, and 6 times per run**. A host granting a re-review after auto-fixes
  has budgeted for it, and this skill does not cancel it by capping the item at one. Count each run in
  `credits`, and at the run cap skip it, say so, name the cap. A per-session budget written for a
  human becomes a per-interval budget under a loop.

When the host defines none, detect what exists and run only that:

- Package manifest scripts named `lint`, `format`, `typecheck`, `types`, `check`, `test`, or
  `Makefile` targets `lint`, `check`, `test`
- Language-native commands where the manifest shows the toolchain configured: `cargo clippy` /
  `cargo test`, `go vet ./...` / `go test ./...`, configured `ruff` / `mypy` / `pytest`
- CI workflow files as the tiebreaker. What CI runs is what this project considers passing.
- Never install a tool, add a script, or invent a gate. Nothing detectable means saying so in the
  report and never describing the change as verified.

**Failure ceiling: up to 3 fix-and-reverify rounds.** Each round is one diagnosis, one fix, one full
re-run of the gates. Increment `attempts` and write `claim.lastFailure` on every failure.

Still failing after the third, stop the iteration, keep the changes uncommitted, keep the claim held,
clear `inFlight`, and put the raw failing output in front of the user. **Never revert the work, never
ship it, never mark the entry resolved.** Reverting throws away the diagnosis the user is about to
need, and shipping opens a PR on a change that does not work.

### Step 10: Close the entry

Set `claim.step` to 10 first. From here the working tree shows no in-progress line for this entry, so
the ledger is the only thing that knows the item is unfinished. Then follow the host's convention
when it defines one. For a `setup-todo-backlog`-shaped backlog:

1. Move the whole entry to the `## Resolved` section at the bottom of the same file, keeping its id.
2. Replace the status line with exactly `**Status:** resolved YYYY-MM-DD`. No trailing period, no
   appended sentence. The line stays machine-readable.
3. Put what landed in the first bullet under it, not on the status line, then collapse the body to
   the problem and what fixed it. Drop the evidence bullets and the traps.
4. **Update, without closing, any other entry whose evidence this change invalidated.** A count or a
   reproduction in a sibling entry that is now wrong is stale documentation sitting inside the
   backlog. Narrow it, never drop its number, and never close it as a second item. Because items
   stack, that narrowing and this close are visible to every later item, so a host gate that sweeps
   the backlog reads a file the run kept true rather than one that forgot what it already fixed.

**Only close on evidence**: the gates in Step 9 passed against their baseline, or the defect provably
no longer reproduces. Never close on "looks fixed".

### Step 11: Update what the change made stale

Per the host's docs policy. Where it is silent, check each of the following at minimum. The README, when a
command, script, port, prerequisite, or limitation changed. Architecture or ADR docs, when a
cross-cutting decision moved. Any scenario doc the host names, when user-visible behaviour changed.
Any changelog it requires per change. Nothing stale means saying so in one line, not inventing one.

**Steps 10 and 11 edit files after Step 9's gates ran.** Re-run any fast gate that reads what they
touched, and say plainly when a review lens saw the code change but not the close or the docs.
Stating that gap beats implying a coverage nobody had.

**An instruction file is the case that stalls.** Hosts routinely require their agent-instructions
file to be updated by hand and asked about first, and closing an entry those instructions name by id
triggers exactly that. When this step needs an answer, write `pendingQuestion`, ask, hold the claim
with `claim.step` at 11, clear `inFlight`, stop, in the same shape as Step 6. Step 3 case 4 brings
the iteration back here. Without the ledger's `claim` this is the state that silently loses an entry:
closed in the tree, unshipped, invisible to anything reading the backlog file.

### Step 12: Ship

One pull request per closed item, off the `backlog/<todo-id>` branch Step 5 created. **This skill
commits nothing itself.** The host's git policy wins here, but for the one carve-out below.

- **Check for an existing PR before invoking anything.** `gh pr view <branch> --json url`, or the
  provider's equivalent, settles whether an earlier firing shipped this item and died before writing
  `prs`. In that window `prs` is empty and the tree is clean, so a url here means skip `ship-pr` and
  **resume at the retarget below**, which a firing dying between the two never reached. Without the
  check `ship-pr` aborts on the clean tree with `no changes to commit`, Step 3 case 4 resumes here,
  and the loop reproduces that abort once per interval. Its own existing-PR recovery cannot save
  this: that lives in its last phase, the clean-tree abort in its first.
- **Confirm the working tree is dirty and holds only this item's work**, that HEAD is
  `backlog/<todo-id>`, and that the backlog file's status line reads `resolved` and not the Step 5
  breadcrumb. Anything left from an abandoned iteration belongs to its own entry, not this PR.
- **Invoke the `ship-pr` skill.** It branches where needed, commits, pushes, and opens the PR in one
  pass. **Do not commit first**: it aborts on a clean tree, so a commit here breaks this step rather
  than preparing it. Because the worker already sits on `backlog/<todo-id>`, it stays there rather
  than deriving a branch: one PR, one entry.
- **Retarget the PR's base.** `ship-pr` opens every PR against the default branch, so for every item
  after the run's first, `gh pr edit <url> --base <prs[-1].branch>` — or `glab mr update
  --target-branch` on GitLab — points it at the item below it in the stack. **The symptom of a missed
  retarget is a PR showing every earlier item's diff**, which is what to suspect when a review lens
  reports findings this item did not cause. When an earlier PR
  merges and its branch goes, the provider retargets whatever sat on it onto that branch's own base.
  That is the stack unwinding correctly, not something to repair.
- **Append `todo`, `branch`, `base` and `url` to `prs`.** Step 5 branches the next item from
  `prs[-1].branch`, so an unwritten record restarts the stack at the default branch and reintroduces
  the conflict stacking exists to remove.
- **Pushing is authorised here, as consent given at invocation.** The host forbids pushing without an
  explicit instruction from the user. Typing `/loop-todos` is that instruction, given for this run and
  not generalising past it. **Say what it covers**: the first firing reports the branch prefix it will
  push under and how many PRs `snapshot` implies, so the scope consented to is visible before the
  second PR opens. Everything else in the host's policy still wins.
- **Accepted consequence**: the commit subject and the PR title are `ship-pr`'s own derivation from
  the diff, not this skill's. The todo id still reaches the diff, because Step 10 closed that entry
  by editing the backlog file under it.
- **Anything `ship-pr` would ask a question about becomes a `pendingQuestion`**, in the same shape as
  Step 6, never a prompt fired into an unattended firing. It asks when it cannot detect a default
  branch, and when a staged file looks like a secret. When one of its secret patterns matches a file
  that is *not* the only change it drops that file silently rather than asking, so diff what the
  commit actually contains against what Step 8 touched and report the gap instead of trusting the PR
  to be complete.
- **A `ship-pr` abort holds the claim at `claim.step` 12** and surfaces its reason verbatim, in the
  same shape as the Step 11 stall: write `claim.lastFailure`, **increment `attempts`**, clear
  `inFlight`, stop. That counter is what Step 3 case 3 reads, and it is the only thing standing
  between a permanent abort and a loop held forever. **Never retry it with a bypass flag**, and
  **stop if it reports taking its fork fallback** — the carve-out authorises pushing to `origin`, not
  creating a repository. No git repository, or no `origin`: skip the step, report the work unshipped.

Review findings arriving after the PR is open — a re-run lens, a human reviewer, CI — are one more
verification round, ceiling included. Fixes get their own `ship-pr` run onto the same branch and PR,
never an amend. **This step is re-entered whenever a firing dies inside it**, and the existing-PR
check above is what makes that re-entry safe.

### Step 13: Record and end the iteration

Append the id to `closed`, drop its `attempts` entry, clear `claim`, clear `pendingQuestion` if it
belonged to this entry, and clear `inFlight`. Report one line: the id, what landed, the PR url and
the base it was retargeted onto, and how much of `snapshot` is left. Then end the iteration. Do not
pick up a second entry.

### Step 14: Finish the run

When Step 4 finds nothing left in `snapshot`:

1. Print the run summary: `startedAt`, every id in `closed` with its `prs` url in stack order,
   **the merge order the stack forces** (oldest PR first, and rejecting one rebases everything above
   it), and anything held.
2. **Return HEAD to `startBranch`.** The worktree belongs to the harness, not to this skill, and
   leaving it parked on the last item's branch is a side effect nobody asked for. The tree is clean
   at this point, so the checkout is safe.
3. **Write `finished` with the current UTC timestamp, before attempting the cancel.** The ledger is
   inert from that moment, so a firing racing the cancel reads guard case 1 and does nothing instead
   of mistaking a live run for an orphan.
4. Cancel the loop with `CronDelete` on the job id from `CronList`.
5. **Cancel confirmed** — archive the ledger by renaming it `run-<startedAt>.json` beside itself, so
   a later `/loop-todos` starts clean.
6. **Cancel not confirmed**, no job id or the delete failed — **leave the ledger exactly where it
   is.** Tell the user the job could not be found, that they cancel the loop themselves, and that
   deleting the ledger is the last step. Every firing until then hits guard case 1, does nothing, and
   repeats those instructions.

Archiving while the loop may still be firing is the one mistake that produces two loops: the next
firing finds no ledger, reads a first run, starts a second.

## Claim release

Every exit path releases or holds the claim deliberately, and the ledger records which. **A claim
must never persist with nothing recorded.**

| Exit | Claim | Ledger |
|---|---|---|
| Item closed, Steps 10 to 13 | released | `claim` cleared, `closed` and `prs` appended, the PR records `open` to `resolved` |
| Question outstanding, Step 6 or 11 | **held**, so the next firing resumes rather than restarts | `pendingQuestion` set, `answer` null, `claim.step` records how far it got. The session receiving the reply writes `answer`, Step 3 case 1 picks it up |
| Prerequisite failed, Step 7 | **held** | `claim.lastFailure` set, `attempts` untouched, a broken toolchain not being a failed verification |
| Verification failed 3 times, Step 9 | **held**, uncommitted changes sit in the tree | `attempts` at 3, `claim.lastFailure` set, raw output shown. Step 3 case 3 refuses a second ceiling |
| `ship-pr` aborted, Step 12 | **held** at `claim.step` 12, the work still uncommitted on `backlog/<todo-id>` | `claim.lastFailure` verbatim, `prs` untouched, **`attempts` incremented** so a permanent abort reaches Step 3 case 3 |
| Interrupted, or the session died | **held** wherever it stopped, **including after Step 10**, where the backlog file shows nothing amiss | `claim.step` survives and is what Step 3 reads |
| User abandons | released by hand, restore `**Status:** open` | clear `claim`, `pendingQuestion`, `attempts`. Leave the id in `snapshot`. Settle the uncommitted changes with the user, never discard them unasked |

## Backlog entry format (quick reference)

Inlined so this skill works where `setup-todo-backlog` was never run. That skill is the source.

- **Id**: `## TODO-YYYY-MM-DD-slug: <declarative claim>`, the date filed plus a 2-5 word kebab-case
  slug. The heading is the id, immutable, never reused, and how entries cross-reference.
- **Status**, its own line under the heading, one of three in a committed file: `**Status:** open`,
  `**Status:** decided, deferred` (free text after the comma), `**Status:** resolved YYYY-MM-DD`, plus
  Step 5's transient fourth. **Body**: 5-8 bullets — problem, evidence, locked decisions, traps. No
  subsections, no tables, no prose. **Closing**: per Step 10, never deletion.

## Rules

The invariants, each with a mechanism above that makes it true, here so a drifted firing checks itself.

- **Exactly one entry per iteration**, the run's backlog being `snapshot`, read from
  `origin/<default>` rather than the checkout. **One branch and one pull request per entry, stacked**:
  the first off `origin/<default>`, every one after off the previous item's branch. Never a shared run
  branch, never a fan of independent ones. **No implementation before its plan is written.**
- **The ledger is the authority on run state**, not the backlog file and not `CronList`. Never
  committed, never off the machine.
- **The host outranks this skill on every conflict it actually covers**, a rule scoped to one case
  being silent about the rest. **Never edit its policy file without asking. Never guess a
  requirement**, because guessing at loop speed outruns anyone reading the result.
- **Never mark an entry resolved without its gates passing against their recorded baseline**, never
  make a red gate green by relaxing it, never close on "looks fixed". A baseline is a list of known
  defects, and widening a rule deletes the list rather than the defects.
- **Never commit to give a gate something to read, and never defer a gate past the ship.** Every gate
  is pointed at this item's uncommitted change set, per Step 9. **Never ship before Step 10 has closed
  the entry. Never revert failed work, or ship it.**
- **Pushing is authorised, per Step 12, as consent given at invocation and bounded to this run.
  Everything around it is not.** Never force-push, never merge its own PR, never touch a branch it
  did not create, never push outside `backlog/`, never let a fork stand in for a push it was refused.
- **Never start a second loop.** A missing ledger is the only signal that justifies creating one, and
  a `finished` ledger is not a missing one. **Never archive one while the loop may still be firing.**
- **A held claim is always recorded and always reported.** Silence plus unfinished work is the one
  state this skill must never leave behind.

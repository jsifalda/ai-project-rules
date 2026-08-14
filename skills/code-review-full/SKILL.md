---
name: code-review-full
disable-model-invocation: true
description: >-
  RESTRICTED-INVOCATION skill, do NOT auto-trigger. One entry point only, the user typing
  the literal slash command `/code-review-full`. Phrasing like "review this", "review my
  changes", "quick review", "look at this diff", "deep review" or any paraphrase are
  ANTI-TRIGGERS, they MUST NOT load this skill, review directly instead and offer
  `/code-review-full`. When invoked, runs independent reviews concurrently against one
  pinned diff (correctness, structure, a direct read, Jira spec conformance and security),
  verifies every claim against real code and drops false ones, triages survivors through a
  council of AI advisors, verifies the council's own output, reports every finding that
  survives, grouped by verdict, plus paste-ready comments and one offline HTML report. Offers
  to post those comments to the MR or PR one at a time, each only if you approve. Never edits,
  commits or pushes. Roughly 15 agent invocations, wrong for a small change, review a typo
  directly.
---

# Code Review Full

Independent reviews, one pinned diff, every claim verified, a council to rank and rule. The
output is every finding that is real and that matters, in rank order, and nothing else.

**The point is noise reduction.** A single review pass gives one model's opinion, stated with
uniform confidence whether it is right or wrong. This pipeline separates *generating*
candidate findings from *verifying* them and from *triaging* them, so each stage catches the
previous stage's errors. Noise is what is false, or what does not matter. Noise is not what
ranks sixth.

**Never re-introduce a numeric cap.** A count is a proxy for relevance, not relevance. A
finding that is verified, that clears the bar and that the council did not DROP is worth the
author's time whether it ranks second or twelfth. Hiding it because five other findings ranked
above it is arbitrary. Noise is removed by disproving false claims at Stage 6 and by the bar
at Stage 7, never by a headcount.

## How it works

One pass, from the slash command to a posted comment.

```
/code-review-full  (slash only, never auto-triggers)
      │ the only entry point
      ▼
Stage 0   preflight ──probes for──▶ which delegates exist on this machine
      │ the mode of each stage is recorded
      ▼
Stage 1   pin the diff ──extract-anchors.py──▶ anchors.json, the only legal anchors
Stage 1b  resolve the Jira parent ──writes──▶ ticket-context.md
      │ one diff, one anchor set, one ticket context
      ├──────────┬──────────┬──────────┬──────────┐  launched in ONE message
      ▼          ▼          ▼          ▼          ▼
   Stage 2    Stage 3    Stage 4    Stage 4b   Stage 4c
  correctness structure  self-read    spec      security
      │          │          │          │          │
      └──────────┴─────┬────┴──────────┴──────────┘
                       │ every result set
                       ▼
              Stage 5   merge, dedupe on root cause
                       │ one row per finding
                       ▼
              Stage 6   verify claim AND anchor ──disproven──▶ dropped, with the disproof
                       │ verified only
                       ▼
              Stage 7   council ranks and rules ──DROP──▶ out
                       │ everything else, in rank order
                       ▼
              Stage 8   re-read what the chairman named
                       │ a correction is published beside the claim
                       ▼
              Stage 9   verdict + comments + render-report.py ──▶ review-<slug>-<ts>.html, opened
                       │ the gates pass
                       ▼
              Stage 10  post-comment.py ──one per approval──▶ MR or PR
```

### What it calls, and when

| Callee | Kind | Stage | How it is called | If it is absent |
|---|---|---|---|---|
| `code-review` | agent | 2 | Dispatched with a self-contained prompt, concurrently with the other reviews | The role is mandatory. Run it inline when dispatch is unavailable |
| `code-review-nuclear` | skill | 3 | Delegated | Inline per `references/structural-review.md` |
| (none) | none | 4 | The pipeline agent reads the pinned diff and the surrounding files itself | Not applicable. It never delegates |
| (none) | none | 4b | Inline per `references/spec-conformance.md`. It writes `$RUN/spec-ledger.json` | Not applicable |
| `security-review` | skill | 4c | Delegated. The prompt must override its default branch scope in the first line | Inline per `references/security-review.md` |
| `council` | skill | 7 | Delegated with the framed brief. Advisors run in parallel, get anonymized, distinct peer probes run in parallel, then a chairman rules. See `references/council-protocol.md` | Inline per the same file. An inline council counts as WEAKER evidence |
| `extract-anchors.py` | script | 1 | `$SKILL_DIR`-relative | The run has no legal anchor set |
| `render-report.py` | script | 9 | Reads `$RUN/report.json` and nothing else | The deliverable is lost |
| `post-comment.py` | script | 10 | One call per approved comment | Nothing can be posted |

A missing delegate degrades the run. It never aborts it, and the final verdict states which
mode each stage ran in. The bundled scripts resolve against `$SKILL_DIR`, never against cwd,
because cwd is the repo under review and holds no `scripts/` directory.

### Caps

| Cap | Value | Enforced in |
|---|---|---|
| Cost | Roughly 15 agent invocations | `## Invocation` |
| Whole-file reads | Under 8000 bytes | Stage 1 |
| Total read budget | 120000 bytes, largest first | Stage 1 |
| `ticket-context.md` | 60 lines | Stage 1b |
| Jira keys resolved | 6 | `references/spec-conformance.md` |
| Criteria ledger | 60 criteria | `references/spec-conformance.md` |
| Paste-ready comment | 4 lines, roughly 50 words | `references/output-contract.md` |

The finding count is absent from this table on purpose, because there is no cap on it.

### Gates and refusals

| Gate | What happens | Owner |
|---|---|---|
| Slash-only entry | Any paraphrase must not load the skill | `## Invocation` |
| Never edits, commits or pushes | The run produces a verdict, a comment set and a report, nothing else | `## Hard constraints` |
| Working tree never moves | No `checkout`, `stash` or `worktree`. History is read with `git show` | `## Hard constraints` |
| Anchor must be an added line | The anchor moves to the line that carries the mechanism, and the finding survives | Stage 6 |
| No legal anchor anywhere | The finding is marked not postable and still reaches the verdict | Stage 6 |
| Unverified claim | Never reaches the council or the verdict. This is the claim check, not the anchor check | Stage 6 |
| Spec ledger `implemented` row | Goes through the same two-part check. A row that fails is demoted and enters the ledger as a finding | Stage 6 |
| Finding count | No cap. Every verified finding the council did not `DROP` reaches chat | Stage 7 |
| Missing delegate | The run degrades to inline. It never aborts | Stage 0 |
| Parent ticket unreadable | Spec-finding confidence is capped at medium | Stage 4b |
| Files skipped by the read budget | Every affected finding is capped at low confidence | Stage 1 |
| Posting gates | The source was an MR or PR, the run can ask, and a comment survived | Stage 10 |
| Per-comment approval | Nothing posts without an individual yes. A batched approval breaches the rule | Stage 10 |

## Invocation

One entry point, the literal `/code-review-full`. Nothing else loads this skill. It is
expensive, roughly 15 agent invocations, so accidental firing on a two-line fix is the
failure this restriction prevents.

## Hard constraints (never relaxed)

- **Read-only means the code under review, not the filesystem.** No edits to repository files,
  no commits, no pushes. Nothing reaches an MR or PR except through Stage 10, one comment at
  a time, each one approved by the user in the turn it is posted. If the user wants fixes,
  that is a separate request after they read the verdict.

  **Two writes are required and never breach this rule:** the scratch dir `$RUN` and the HTML
  report. The report is the deliverable, so a run that suppresses it to "stay read-only" has
  misread this rule and failed. Write it into the user's cwd even when that cwd is the repo
  under review, then name the path and suggest a gitignore line. Never silently skip it.
- **Never move the user's working tree.** No `checkout`, no `stash`, no `worktree`. Read
  history with `git show <ref>:<path>` only. On a shared machine a checkout silently destroys
  uncommitted work. Confirm the branch and clean state before finishing.
- **Host CLIs are read-only apart from a comment the user approved.** Viewing MRs, PRs,
  diffs and pipelines is fine. Posting is confined to Stage 10 and its per-comment gate.
  Never close, merge, delete or approve anything, at any point.
- **Ask before installing anything.** Name what and why, propose the command, wait.
- **Never post a comment the user has not individually approved.** The invariant is that
  the human decides what reaches the MR, one comment at a time. Printing was only ever
  the mechanism. Stage 10 keeps the decision and automates the paste. A batched approval,
  an implied yes, or posting in a run that cannot ask all breach this.

## Stage 0 - Preflight

**Resolve `$SKILL_DIR` first.** It is the directory you loaded this `SKILL.md` from, wherever
your agent installs skills, which differs between agents and may also be a path inside a repo
that vendors it. Your cwd is the repo under review and does not contain `scripts/` or
`references/`, so every bundled path in this file resolves against `$SKILL_DIR`, never cwd.
Get it wrong and Stage 9 fails with `No such file or directory`.

Probe for the delegate skills that install as a directory, and record which mode the run is in.
They live outside this repo and may be absent on any given machine. Probe, do not assume.

```bash
for d in code-review-nuclear council; do
  ls -d ~/.agents/skills/$d ~/.claude/skills/$d 2>/dev/null | head -1
done
```

**`security-review` is a harness built-in, so this probe cannot see it.** It has no directory
under `~/.claude/skills/`, `~/.claude-pro/skills/` or `~/.agents/skills/`, and adding it to the
loop above only makes the probe report it absent on every machine. Judge it by observation
instead, whether the host lists `security-review` among the skills you can invoke.

| Delegate | Used for | If absent |
|---|---|---|
| `code-review` agent | Stage 2, correctness | Role is mandatory. Run inline when dispatch is unavailable |
| `code-review-nuclear` skill | Stage 3, structure | Run inline per `references/structural-review.md` |
| `security-review` skill | Stage 4c, security | Run inline per `references/security-review.md` |
| `council` skill | Stage 7, triage | Run inline per `references/council-protocol.md` |

A missing delegate degrades the run, it never aborts it. State in the final verdict which
mode each stage ran in.

Create the run dir `/tmp/code-review-full-<YYYY-MM-DD-HHMMSS>/`, referred to below as `$RUN`.
If you cannot write there, for any reason, including a sandbox where `/tmp` is read-only and a
harness that forbids agent writes to `/tmp` even though the path itself is writable, fall back
to `<cwd>/.code-review-full-<YYYY-MM-DD-HHMMSS>/` and delete it at the end of the run. Say
which one you used.

**`$RUN` is internal scratch, not output.** The pinned diff, per-reviewer results, the findings
ledger and `report.json` all live there and stay there. Only the published artifact in
Stage 9, the HTML report, is written to the user's cwd. These are two different locations on
purpose and they never merge.

**Creating and deleting `$RUN` does not breach the read-only rule.** That rule protects the
code under review, meaning tracked repository files, git state and anything on the MR or PR.
`$RUN` is scratch this run created itself, so cleaning it up is required, not forbidden. When
the fallback put it inside the repo, delete it after Stage 9 has finished writing the report,
never before. If deletion fails, say where it is so the user can remove it.

Derive `<source-slug>` once here and reuse it for the artifact filename. `$SOURCE` is the
raw change identifier exactly as the user gave it, before Stage 1 resolves it: an MR or PR URL,
`MR !1234`, `branch feat/x`, a commit range like `076f001~1..076f001`, or `working tree`.
Slugify it, because a raw source contains spaces and characters like `!` and `/` that break
shell quoting and filenames:

```bash
SOURCE="<the change identifier the user gave>"
SOURCE_SLUG=$(printf '%s' "$SOURCE" | tr -cs '[:alnum:]._-' '-' | sed 's/^-*//;s/-*$//')
```

`MR !1234` becomes `MR-1234`, `branch feat/x` becomes `branch-feat-x`, and
`076f001~1..076f001` becomes `076f001-1..076f001`.

Derive the timestamp once here too, as `$TS`, and reuse it for the run dir and the artifact
filename. Recomputing it scatters one run across several timestamps.

## Stage 1 - Pin the fixed point

Resolve what the change is measured against BEFORE reading any code, then capture it once to
a file. Every later stage reads that file, so all reviewers judge identical bytes.

Four accepted sources. For a hosted MR or PR, resolve the branch and merge base from the host
CLI. For a branch or commit range, use it directly. For uncommitted work, diff the working
tree.

```bash
git diff <merge-base-ref>...<head-ref> > "$RUN/diff.patch"
git log <merge-base-ref>..<head-ref> --oneline > "$RUN/commits.txt"
```

**Three-dot form only.** Two dots compares against the tip of the target branch, so unrelated
commits landing there pollute the diff. Three dots compares against the merge base.

Confirm the ref resolves (`git rev-parse`) and the diff is non-empty before continuing. A bad
ref fails loudly here, never later as a confusingly empty review.

Now derive the legal anchor set from that same patch.

```bash
python3 "$SKILL_DIR/scripts/extract-anchors.py" --diff "$RUN/diff.patch" --out "$RUN/anchors.json"
```

**`$RUN/anchors.json` is the sole source of legal anchors for the whole run.** It is keyed by
new-side path, and for each file it carries `hunks`, the added lines with their text, and the
removed lines. **Only the `added` lines are legal anchors.** A context line, a removed line,
and any line outside every hunk are all illegal, because a comment there points at code this
change did not write.

This exists because reviewers used to count line numbers by eye inside a 300-line
`git show` blob. On one recorded run that put a comment about `setToolbarHidden` on
`SearchScreen.swift:196`, which is a continuation of an array literal, and another on
`DashboardViewController.swift:122`, which sits in the opposite branch of the
if/else the finding was about. Looking an anchor up in `anchors.json` is cheaper than
counting, and it cannot drift.

The allowlist is the first of two defences and it does not catch everything. Both wrong
anchors above happen to be added lines, so they pass the allowlist. What catches them is the
text check in Stage 6, which reads the one line and confirms it carries the mechanism the
claim turns on. The allowlist rules out off-diff anchors. The text check rules out the rest.

Build `$RUN/diff_index.json` so later stages can budget reads without loading the whole patch.
An array, one entry per changed path, sorted by `bytes` descending:

```json
[{"path": "src/A.kt", "old_path": null, "bytes": 4210, "new_file": false,
  "renamed": false, "deleted": false, "ext": "kt"}]
```

Read files under 8000 bytes in full, then largest-first to a total of 120000 bytes. Anything
skipped is listed in the verdict and caps every affected finding's confidence at low.

## Stage 1b - Resolve the ticket hierarchy

This stage runs at the end of Stage 1, BEFORE the reviews are dispatched, because the
next stage launches every reviewer in one message and a reviewer cannot be handed context
that has not been fetched yet.

Resolve the ticket key and fetch the hierarchy exactly as `references/spec-conformance.md`
sections 2 and 3 specify. **Fetching the parent is unconditional for a sub-task**, whatever
the child's description contains. Then state the hierarchy invariant line from section 3.3
before continuing. A run that cannot state it has not resolved the hierarchy.

Write `$RUN/ticket-context.md`, at most 60 lines, in this shape:

```
# Ticket context (read-only)
primary: <KEY> (<issuetype>) - <summary>
parent:  <KEY> (<issuetype>) - <summary>

## In scope (from parent)
## Out of scope (from parent)     <- verbatim, this is the scope boundary
## Acceptance criteria            <- parent first, then child
## Sibling sub-tasks              <- key, summary, platform label
```

Stage 4b reuses this same fetch for the criteria ledger it writes to `$RUN/spec-ledger.json`. Do
not fetch twice.

**When there is no ticket** the file is not written, and the reviewer prompts in the next
stage omit the context paragraph rather than pointing at a missing file.

## Stages 2, 3, 4, 4b, 4c - The reviews, concurrently

**Launch every review in one message.** Do not wait for one before starting the next.

If the runtime cannot spawn sub-agents, which is the case when this skill is itself running
inside a sub-agent, run every pass inline and sequentially instead. Say so in the verdict
header. The mandates stay separate even when one agent performs them. Do not let them
collapse into a single undifferentiated read, the separation is what produces independent
corroboration in Stage 5.

| Stage | Who | Looks for |
|---|---|---|
| 2 | `code-review` agent | Correctness. Logic errors, bugs, contract violations, repo rule breaches |
| 3 | `code-review-nuclear`, or inline per `references/structural-review.md` | Structure. Architecture, abstraction quality, complexity growth |
| 4 | The agent itself | Reads the pinned diff and the surrounding files directly |
| 4b | Inline, per `references/spec-conformance.md` | Spec conformance. Gaps and extras against the Jira ticket AND its parent. The parent is fetched on every run, never only when the child looks empty. Writes `$RUN/spec-ledger.json`, one row per criterion, which Stage 6 verifies and Stage 9 publishes |
| 4c | `security-review` skill, or inline per `references/security-review.md` | Security. Exploitable defects in the pinned diff, injection, authorization gaps, secret handling, unsafe deserialization, crypto misuse |

**Stage 4 is not optional and not redundant.** On the recorded run the agent found the
headline blocker on its own while both reviewers were still working. When their results
arrived that finding had three independent sources instead of one, which settled its severity
immediately.

Give each delegated reviewer: the path to `$RUN/diff.patch`, the path to `$RUN/anchors.json`,
the path to `$RUN/ticket-context.md` when Stage 1b wrote one, the repo's binding convention
documents (`AGENTS.md`, `CLAUDE.md`, or equivalent), the
`git show` recipe for reading branch state without mutating the working tree, and an
instruction to report `file:line` for every claim. **A finding without a line anchor cannot be
verified and must not proceed, and neither can a finding whose anchor is absent from the
`added` list in `anchors.json`.** An anchor off the diff is as disqualifying as no anchor at
all, because a comment posted there lands on code the author did not write in this change.

**Every reviewer reads the ticket context. Only Stage 4b scores against it.** Attach this
paragraph verbatim to the Stage 2, 3, 4 and 4c prompts whenever `$RUN/ticket-context.md`
exists:

> Read `$RUN/ticket-context.md` first. It states what this change was asked to do, and the
> scope boundary the parent ticket drew, including which platform or layer the work was
> supposed to land in. Use it to judge whether a construct is justified, and to tell a
> deliberate decision apart from an accident. Do NOT report spec gaps, missing acceptance
> criteria, or out-of-scope work. Another reviewer owns that mandate and a duplicate from you
> is dropped. The context changes how you weigh what you find, never what you are looking for.

The reason is on the record. On one recorded run the structural reviewer independently proposed
letting the backend supply the default, which the parent ticket had in fact assigned to the
backend while marking frontend changes out of scope. Blind to the ticket, the reviewer filed
it as taste and the council dropped it. The context block is what turns that into evidence.

**Tell reviewers to pick the anchor by grepping `anchors.json`, not by counting lines.** The
construct a claim is about is in the `text` of some added line. Search for it, take that
`line`, and use it verbatim. Counting lines inside a `git show` read is what produced the
wrong anchors on the recorded run above.

**Stage 2 is a sub-agent dispatch when sub-agents are available.** Spawn the `code-review`
agent type with a prompt. It is stateless and sees nothing of this session, so the prompt must
carry everything. Use this shape, so two runs of the pipeline give it the same mandate:

> Review the diff at `$RUN/diff.patch` for CORRECTNESS only. Logic errors, bugs, contract
> violations, breaches of the repo's own rules in `<convention docs>`. Not style, not
> architecture, not performance. Read surrounding files with `git show <ref>:<path>`, never
> `checkout`. Report every claim as `file:line` plus what is wrong and why. A claim you cannot
> anchor to a line, do not report.
>
> The only legal anchors are the added lines listed in `$RUN/anchors.json`, which is keyed by
> file path and lists each added line with its text. Find your anchor by searching that file
> for the construct you are describing and taking its `line` value. Do not count lines by eye
> in a file read, that is how previous runs landed comments on unrelated code. A context line,
> a removed line, or any line outside the hunks is not a legal anchor.
>
> When the thing you are reporting lives on a line this change did not touch, anchor the claim
> to the added line that causes the problem and name the untouched location in the body of the
> claim instead. Never drop the finding, and never anchor it off the diff.

**When sub-agents are unavailable, run Stage 2 inline against that same mandate.** The Stage 0
table calls the `code-review` agent "always available" because the reviewer role is always
performed, not because dispatch always works. The role is mandatory, the dispatch is not.
Read the prompt above as your own instructions and keep the correctness pass separate from
the other passes.

**Stage 4c delegates to the `security-review` skill when the host provides one.** That skill
defaults to reviewing the pending changes on the current branch, which is NOT what this
pipeline reviews, so the prompt has to override its scope in the first line. Use this shape:

> Review the diff at `$RUN/diff.patch` for SECURITY only. That file is the authoritative and
> only target of this review. Review nothing outside it. Do not resolve your own scope from the
> checked-out branch or from the working tree, whatever either one holds, because the pinned
> diff was captured for you already. Look for exploitable defects the pinned diff introduces,
> injection, authorization gaps, unsafe secret handling, unsafe deserialization and crypto
> misuse. Read surrounding files with `git show <ref>:<path>`, never `checkout`. Report every
> claim as `file:line` plus the attack path and the impact.
>
> The only legal anchors are the added lines listed in `$RUN/anchors.json`, which is keyed by
> file path and lists each added line with its text. Find your anchor by searching that file
> for the construct you are describing and taking its `line` value. Do not count lines by eye
> in a file read, that is how previous runs landed comments on unrelated code. A context line,
> a removed line, or any line outside the hunks is not a legal anchor.
>
> When the thing you are reporting lives on a line this change did not touch, anchor the claim
> to the added line that causes the problem and name the untouched location in the body of the
> claim instead. A guard this change DELETED is the case that matters most to you. A removed
> line is not a legal anchor, so anchor to the added line that now runs unguarded and name the
> deleted guard in the body. Never drop the finding, and never anchor it off the diff.
>
> When the change deletes a guard and adds no line in that file, prefer an added line elsewhere
> in the diff whose behaviour the deletion changes. When the diff holds no such line anywhere,
> keep the finding, mark it not postable, and name the deleted guard and its old location in
> the body. Say plainly that it has no legal anchor.
>
> Correctness, structure and spec conformance belong to other reviewers. A finding of theirs
> raised here is dropped as a duplicate at Stage 5.
>
> Report a finding only when you can state the path from attacker-controlled input to the
> dangerous sink. A construct that only looks unsafe is not a finding.

**When the host provides no `security-review` skill, run Stage 4c inline against
`references/security-review.md`.** The security role is mandatory, the delegation is not.

**On a DELEGATED run whose pinned source is not the checked-out branch, say so in the verdict as
a degradation warning.** The delegate's default scope and the pinned diff disagree, so the reader
has to know this lens was steered off its default. An inline run has no default scope to steer,
so this warning does not apply to it. `references/output-contract.md` holds the warning wording.
Take it from there rather than writing a second copy of it.

Stage 4b is skipped when no Jira key is found and the user supplied no MR or PR link. Ask once
whether to supply one, allow the skip, then run four reviewers and say so loudly in the
verdict header. A thin review must never masquerade as a full one. **When the run is
non-interactive** and there is no channel to ask, take the skip without asking and record that
the question could not be put.

**A key that was found but whose parent could not be read is NOT a skip.** Stage 4b still
runs on the child criteria. Carry the `method.warnings` entry from section 3.2 into the verdict
header, cap spec-finding confidence at medium, and never emit a scope-inversion finding
without the parent in hand.

## Stage 5 - Merge and dedupe

Collapse every result set into one ledger. The session database works well.

| Column | Purpose |
|---|---|
| `id` | Short stable handle, `F1` |
| `severity` | Initial assessment, revised after verification |
| `origin` | Which reviewers raised it |
| `file` | Exactly one path. The canonical anchor's file |
| `lines` | Exactly one added line number, or one contiguous range within a single hunk |
| `occurrences` | The other sites of the same root cause, `path:line` each, empty when there is one site |
| `claim` | What is allegedly wrong |
| `status` | `unverified`, `verified`, `disproven` |
| `evidence` | Filled by Stage 6 |

**A `file` value holding two paths is malformed.** On the recorded run a row carried
`file: "SearchScreen.swift, DashboardViewController.swift"` and
`lines: "196-197, 122"`. Nothing downstream can use that. `scripts/post-comment.py` takes one
`--file` and one `--line`, so the row can only be posted by picking one at random. Fix it
before it leaves this stage: either the two sites are separate root causes and become separate
findings, or they are one root cause and collapse to one canonical anchor.

**Dedupe on the root cause, not on the site.** One mechanism appearing at five places is one
finding with five occurrences, never five findings and never a parent with `F1b` style
siblings. On the recorded run the same defect, a toolbar shown and never torn down, was split into
`F1` and `F1b` because it shows up in two files. That posts the author two comments for one
fix. The sibling pattern is banned.

**The canonical anchor is the first site in diff order.** Diff order means the order the files
appear in `diff.patch`, then ascending line number within a file. This beat "prefer the shared
or lowest-level site" because it needs no judgement call, so two runs over the same diff pick
the same anchor. The tradeoff is real and you have to cover for it. First in diff order will
sometimes be the mirror rather than the source, so the comment body has to name the other
sites plainly enough that the author fixes the right one.

Every other site goes in the body as an "also at" line. Never a second comment and never a
second finding ID.

**Two findings landing on the same anchor is a signal to re-check the dedupe.** Stage 6 moves
an anchor when the original was illegal, so two findings that started apart can converge on
one line. When that happens, ask whether they are really one mechanism described from two
angles. Usually they are, and they merge, with the second finding's detail folded into the
body. When they genuinely are two mechanisms that share a causing line, keep both and say in
each comment what the other one covers, so the author does not read the second as a repeat of
the first.

This dedupe axis is separate from cross-reviewer dedupe below. One collapses sites of a
mechanism, the other collapses reviewers who spotted the same thing. Run both.

**Record every origin.** Two reviewers with different mandates raising the same thing without
seeing each other's work is strong evidence and raises severity. On the recorded run that
corroboration nearly got lost during the merge.

Track dropped findings with their reason. The dropped list is what makes the kept list
credible.

## Stage 6 - The hard verification gate

**No finding proceeds to the council or the verdict unverified.** This gate is the difference
between a review worth acting on and a list of plausible-sounding guesses.

For each finding, open the real code at the anchor and confirm the claim.

**The claim and the anchor are two separate checks.** Verifying the claim tells you the defect
is real. It tells you nothing about whether the line number is right. Run both, and record
both.

The anchor check has two parts, and it passes only when both hold.

1. The line is in the `added` list for that file in `$RUN/anchors.json`.
2. The text at that line carries the mechanism the claim turns on.

Part 2 is about the mechanism, not about matching a name out of the claim's prose. A claim
usually names the symptom, and the anchor belongs on the added code that causes it. Those are
often different identifiers. A finding about `setHidden()` failing to tear the toolbar down
anchors to the added `setToolbarHidden(false, ...)` call, because that added line is the
mechanism, and `setHidden` appears nowhere on it. Ask whether an author reading that one line
would see the thing the finding is about. Do not grep the claim for a symbol and demand it
appear.

```bash
python3 -c "import json; d=json.load(open('$RUN/anchors.json'));\
 print([a for a in d['files']['<path>']['added'] if a['line']==<n>])"
git show <head-ref>:<path> | sed -n '<n>p'   # the true text of that line
```

The recorded run is the case that shows why part 2 is not optional. A finding said the toolbar
is shown and never hidden, and anchored to `DashboardViewController.swift:122`. Line 122
is in the diff and it is an added line, so part 1 passed. Its text is
`search.searchBar.barTintColor = .brandNavy`, which sits in the `else` branch, the older-OS
path. The comment contradicted its own anchor. Reading a twenty-line window around 122 still
shows the `if #available` block a few lines up, so the claim read as confirmed while the
anchor was wrong. A window is not a check. Read the one line.

The correct anchor was 120, `navigationController?.setToolbarHidden(...)`, which is the line
whose text carries the construct.

**A failed anchor check corrects the anchor. It never drops the finding.** Move the anchor to
the added line whose text holds the construct the claim is about. When the subject of the
finding is not a changed line at all, anchor to the added line that causes the problem and put
the untouched location in the comment body, named as somewhere the author needs to look. On
the recorded run a finding about `SearchScreen.setHidden()` at line 70 was anchored there, and
this change never touches line 70. What the change does is add toolbar setup at 191 to 199 with no
matching teardown. So the anchor becomes 199 and `setHidden()` at line 70 moves into the body.
The finding survives with a legal anchor, which is the only outcome that both tells the truth
and can be posted.

**One case has no legal anchor at all.** A change that deletes a guard and adds no line
anywhere the deletion reaches leaves nothing in the `added` list to carry the claim. Do not
drop it and do not invent an anchor. Mark the finding not postable, name the deleted code and
its old location in the body, and let it through to the chat verdict and the report. Stage 10
skips it, because there is no diff line to attach a comment to. This is the only finding that
reaches the verdict without an anchor, so say why in the finding itself.

- Trace the callers before believing any claim about how something is invoked.
- Check history before believing any claim that something is pre-existing or newly introduced.
- If a finding claims a parity break with another implementation, open that implementation and
  compare. On the recorded run a naming inconsistency looked like a clear defect until the
  other platform's code showed the two forms matched exactly. It was deliberate parity.

**Tooling can lie about file contents.** Before reporting that a literal secret, placeholder or
mask is hardcoded in a file, confirm it at the byte level. Output filters redact secrets in
tool results, so a correct `Authorization: ${TOKEN}` can be DISPLAYED as `Authorization: ******`
in every read you do. This produced a false BLOCK MERGE on a verification run.

```bash
git show <ref>:<path> | sed -n '<line>p' | xxd | head   # what the bytes actually are
```

The tell: your own finding text renders the "wrong" value and the "correct" value identically.
If the before and after of your proposed fix look the same, you are reading a redaction, not a
bug. Applies to any all-asterisk, all-x or `REDACTED` run in a credential position.

```bash
git show <ref>:<path>                    # whole file at that ref
git show <ref>:<path> | sed -n '80,120p' # a range
```

Outcomes. **Verified** proceeds with evidence attached. **Disproven** is dropped with the
disproof recorded, never silently deleted, so the same false finding is not re-raised next
run. **Refined** proceeds with corrected severity or scope.

### The spec ledger goes through this gate too

**No `implemented` row reaches the verdict unverified either.** Everything above this line
protects the reader from a finding that is wrong. This part protects them from a pass that is
wrong, which is the more expensive error, because a false finding wastes an author's afternoon
while a false all-clear ships the gap.

On the recorded run the spec pass declared all eight criteria implemented. That claim never
became a finding, so nothing verified it, the council never saw it, Stage 8 never re-read it, and
it reached the report as one sentence with no per-criterion anchor anywhere in `$RUN`. The reader
could not tell whether a given acceptance criterion had been scored at all.

Read `$RUN/spec-ledger.json` and check every row whose `status` is `implemented`. Use the same
two-part check defined above, not a second mechanism:

- `anchor_kind` of `added` -> the line is in the `added` list for that file in `anchors.json`,
  AND the text at that line carries the mechanism the criterion turns on.
- `anchor_kind` of `preexisting` -> `git show <ref>:<path> | sed -n '<n>p'` and confirm that one
  line carries the mechanism. It is legitimately off the diff, so the allowlist does not apply,
  but the text check does.

Then walk `chain[]` the same way. One hop that does not resolve to real code means the chain was
asserted, not traced.

A row that fails any part is demoted, to `partial` when part of the criterion still holds and to
`missing` when none of it does, and it **then** enters the Stage 5 ledger as a finding with
`origin` of `spec-conformance`. From there it flows through the council and Stage 8 like any
other finding. Record the demotion in `corrections`, because it is the pipeline catching its own
error and the user should see that.

Reading a row without checking it is the failure this section exists to prevent. `implemented` is
a claim until this gate confirms it.

## Stage 7 - Council triage

Only verified findings reach the council. Its job is not to find problems, it is to decide
which verified problems are worth the author's time and to resolve severity disagreements.

The council **always convenes**, however few findings survive.

Delegate to the `council` skill, or run the identical method inline. Either way the protocol,
the five advisor prompts, the five distinct peer probes, the mandatory dissenter, the fixed
verdict vocabulary and the chat gate are defined in `references/council-protocol.md`. Read it.

**An inline council is weaker than a delegated one, say so in the verdict.** Run inline, all
ten seats are one model reasoning sequentially. The content still differs, because each seat
has a different probe, but the responses are not independent the way separately dispatched
advisors are. The error-correction argument rests on that independence. Inline runs should
treat a unanimous council as weaker evidence, not stronger, and lean harder on Stage 6's
evidence than on the council's agreement.

Verdict vocabulary, fixed: `BLOCK MERGE`, `FIX BEFORE MERGE`, `FOLLOW-UP TICKET`, `DROP`.

**Every verified finding the council did not DROP reaches the chat verdict.** There is no
numeric cap. The council ranks and rules, it does not cut to a number. The ranking survives as
the order the findings are presented in, highest first. A finding must clear the bar to reach
chat at all: it changes runtime behaviour, breaks a contract, loses or corrupts data, or
violates a binding repo convention. Taste, naming, style, hypotheticals and "consider
extracting this" never reach chat at any severity, because the council rules DROP on them.

## Stage 8 - Verify the chairman

**The synthesis is the most confident text in the pipeline and it is not automatically
correct.**

Re-read every file and symbol the chairman names before passing its recommendation on. On the
recorded run the chairman's single headline instruction was to delete two methods. Both also
managed coroutine scopes and cancelled collectors, so following it would have broken the
application. The correct action was removing two lines from inside those methods.

Where the synthesis is wrong, publish the correction next to it rather than silently
rewriting. The user should see that the pipeline caught its own error.

## Stage 9 - Output

Three artifacts, all defined in `references/output-contract.md`. Read it before emitting
anything.

1. The chat verdict. Opens with the actionable headline and any degradation warning, never
   with reviewer provenance. The findings grouped by verdict, then the acceptance-criteria
   table whenever the spec lens ran, then the dropped table, the report path, and one concrete
   closing next action.
2. Paste-ready comments, one fenced block each, scrubbed of every internal term. Anchor,
   one-sentence problem, one-sentence ask, and nothing else. **Four lines and roughly fifty
   words is a hard cap.** Verified evidence is stated flatly, the ask is an imperative unless
   it turns on a judgement the pipeline cannot make, and no comment carries an effort
   estimate. A comment that runs long has failed the contract and goes back to be cut.
3. The HTML report, built by `scripts/render-report.py`, never assembled by hand. It is the
   only file this pipeline writes and it carries the full audit record. It opens on screen at
   the end of this stage.

Both the verdict and the comments follow the writing and shaping rules in
`references/output-contract.md`. Those rules are inlined there in full, deliberately, so this
skill has no dependency on any writing-style skill being installed. Do not substitute your
own house style for them.

**Assemble `$RUN/report.json` first.** The renderer reads that ONE file and nothing else, so
every advisor response, peer review, dropped finding and criteria row must be embedded in it
before the script runs. Its exact schema is the module docstring of
`scripts/render-report.py`. Read that docstring, then build the file to match.

**Copy the criteria ledger into `report.json` under `spec`.** Take it from
`$RUN/spec-ledger.json` after Stage 6's demotions, so the published table reflects the verified
statuses and not the reviewer's first pass. The renderer draws a per-criterion section from it,
and without that key the spec pass has no published record at all, whatever it found. When the
spec reviewer was skipped, omit the key.

**There is no separate transcript file.** The whole audit record lives in `report.json` under
`record`, and it is verbatim. That means `record.original_request` holds the user's request as
received, `record.advisors` and `record.peer_reviews` hold every response unedited,
`record.anonymization_mapping` reveals the letters, and `record.ranked_list` holds the full
ranking. Summarizing any of these loses the audit trail the report exists to carry.

**Fill in `meta.pipeline` from what the run actually did.** The script draws the report's ASCII
chart from it, so never hand-draw the chart and never pass a pre-drawn string. Record each
source you fetched and where it came from, one row per review pass with its delegate, model,
mode, tool-call count, duration and finding count, the merge and verification counts, the
council numbers, and the outcome line. Those counts are what make the chart worth reading,
so leave a field out only when the run genuinely does not know it.

**`tool_calls` on the spec-conformance row must be a real integer.** A lens that scored eight
criteria and reports `null` read nothing, and on the recorded run that null was the only visible
tell that the spec pass had produced a claim rather than a result. A spec row reporting no tool
calls is recorded as degraded, and the warning goes in the verdict opening block.

**A degraded reviewer is a reviewer that ran.** It belongs in `meta.reviewers_run`, and its row
in `meta.pipeline.reviewers` carries the mode it really ran in, `delegated` or `inline`. A lens
can be degraded and still delegated, so never write `inline` to mean degraded. Never put it in
`meta.reviewers_skipped`. The renderer prints "some reviewers were skipped" for every entry
in that list, which is the one word `references/output-contract.md` forbids for a lens that
ran. `meta.reviewers_skipped` is for a lens that produced nothing at all.

```bash
python3 "$SKILL_DIR/scripts/render-report.py" --run-dir "$RUN" \
  --out "$PWD/review-<source-slug>-<ts>.html"
```

`$SKILL_DIR` is the directory this `SKILL.md` was loaded from, not your cwd. Your cwd is the
repo under review, and it does not contain `scripts/`. Resolve `$SKILL_DIR` once at Stage 0
from the path you read this file from, and use it for every bundled script and reference.
Every path in the "Bundled files" list below is relative to it.

The report lands in the user's cwd, which may be the repo under review. Name the file in the
closing message and suggest a gitignore line rather than staying silent about dirtying the
tree.

**Open the report the moment it is written.** The report is the deliverable, so the user must
not have to open it by hand. Every run that wrote a report attempts the open. It is not
optional and it does not depend on the run being interactive. Try `open`, then `xdg-open`, then
`wslview`, and use the first one that exists on `PATH`.

```bash
REPORT="$PWD/review-<source-slug>-<ts>.html"
opened=0
for opener in open xdg-open wslview; do
  if command -v "$opener" >/dev/null 2>&1; then
    "$opener" "$REPORT" </dev/null >/dev/null 2>&1 &
    opened=1
    break
  fi
done
[ "$opened" -eq 1 ] || printf 'Could not open automatically - open %s\n' "$REPORT"
```

**Detach the opener from stdin and run it in the background.** `xdg-open` with `$BROWSER` set
to a terminal browser starts that browser attached to your stdin and never returns, which
stalls the stage until the harness times out. `</dev/null` and the trailing `&` are what stop
that. The cost is that the loop reports the opener it started, not that a window appeared.

**A failed open never fails the run.** No opener on `PATH`, or an opener that errors, produces
that one printed line and nothing else. Swallow the error, do not retry, and do not report the
run as failed.

The path and the gitignore suggestion print either way. The open is in addition to that closing
note, never a replacement for it. Do the open at the end of this stage, immediately after the
report is written and BEFORE Stage 10 offers to post, so the report is on screen while the user
decides what to post.

## Stage 10 - Offer to post

The user has now read the verdict, the comments and the report. Offer to put the comments
on the MR or PR, walking them one at a time. Full mechanics in `references/posting.md`,
read it before offering anything.

Three gates, all of which must pass. The source was an MR or PR URL or number, the run can
ask the user, and at least one comment survived. A failed gate is stated in one line and
the stage ends. **Never resolve a target the user did not name.** A branch review does not
go hunting for that branch's open MR, because a silently resolved target is the one way
this stage puts a comment on the wrong merge request.

When the gates pass, the offer replaces the closing next action rather than following it,
so the run still ends on exactly one concrete action.

Per comment the user picks Post, Skip, Edit or Stop. **Approval is per comment and it is
the entire safety mechanism.** Never batch the prompts, never present a multi-select,
never read one yes as covering the rest. An edited comment posts verbatim as the user
wrote it.

Posting goes through `scripts/post-comment.py`, never a hand-built CLI call. Comment
bodies are multi-line prose with backticks that the shell will execute, and GitLab's
inline API needs a nested `position` object that `glab api --field` silently flattens
into a general note while reporting success.

```bash
python3 "$SKILL_DIR/scripts/post-comment.py" --host gitlab --target <iid> \
  --file <path> --line <n> --body-file "$RUN/comment-F1.md" --diff "$RUN/diff.patch"
```

Inline on the diff line, falling back to a general comment when the line is not in a hunk
or the host rejects the position. A fallback is not a failure. A failed post does not abort
the queue.

Close with a compact summary naming what was posted, skipped and not offered, with URLs.
The report is not re-rendered, so this summary is the only record.

## Anti-goals

- **Not a code-review rubric.** This orchestrates review, verification and triage. What makes
  code good belongs to the reviewers it delegates to and to the repo's own conventions.
- **Not a fixer.** It produces a verdict and comments, it does not edit code.
- **Not a bot commenter.** It posts only what the user approved, one comment at a time,
  in the turn they approved it. It never posts on its own judgement and never in bulk.
- **Not for small changes.** For a typo, review it directly.
- **Not a summarizer.** Every stage must decide. The most common failure is balanced
  discussion with no verdict. If the output does not tell the author what to change, the
  pipeline failed regardless of how good the analysis reads.

## Bundled files

Paths are relative to this skill's directory.

- `references/spec-conformance.md` - Stages 1b and 4b. Jira key resolution, the mandatory
  parent walk and the hierarchy invariant, the criteria ledger and the criteria invariant that
  forbids a blanket pass, `$RUN/spec-ledger.json`, scope-inversion detection, the
  anti-false-clear, anti-false-gap and anti-false-extra protocols, all against the pinned diff.
- `references/structural-review.md` - Stage 3 inline fallback, used only when
  `code-review-nuclear` is absent.
- `references/security-review.md` - Stage 4c inline fallback, used only when the host provides
  no `security-review` skill.
- `references/council-protocol.md` - Stage 7. Advisors, anonymization, the distinct peer
  probes, chairman ruling rules, the chat gate.
- `references/output-contract.md` - Stage 9. The verdict block, the terse paste-ready comment
  contract and its four-line cap, the certainty rule, the inlined writing and shaping rules,
  worked examples, and the report contract including the verbatim record and the pipeline
  chart.
- `references/posting.md` - Stage 10. The three gates, the per-comment picker, placement and
  fallback, duplicate detection, failure handling, the summary block.
- `scripts/extract-anchors.py` - Stage 1. Derives `anchors.json`, the allowlist of legal
  anchors, from the pinned diff. Only its `added` lines may anchor a finding.
- `scripts/render-report.py` - builds the self-contained offline HTML report, including the
  ASCII pipeline chart it draws from `meta.pipeline`.
- `scripts/post-comment.py` - posts one approved comment, inline where the diff allows it.
  `--dry-run` makes zero network calls and is mandatory for any verification run.

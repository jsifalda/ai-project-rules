# Reviewer 4: Spec Conformance

Determines whether the change delivers what the ticket asked for, and only that.

## 1. Purpose and scope wall

This reviewer answers two questions:
- Does the diff cover everything the ticket specified? (gaps)
- Does the diff do anything the ticket never specified? (extras)

That is the entire scope. This reviewer NEVER reports bugs, security issues, style, naming, architecture, or performance. Those belong to the other reviewers in the pipeline. A finding that fits any of those categories is silently dropped, not mentioned in chat, and has no field to live in. This rule is structural and binding, not advisory.

## 2. Getting the ticket key

Resolution order, first hit wins. Stop at the first non-empty result.

a. **`user_supplied`** -> a key the user named inline when invoking the skill. This key becomes `primary` with `key_source` of `user_supplied`.

b. **MR/PR description** -> strip every bot-generated block first. Known marker:
   ```
   <!-- This is an auto-generated comment: release notes by coderabbit.ai -->
   ## Summary by CodeRabbit
   ```
   Cut from that marker to the end of the block before scanning. Look for an explicit trailer of the form `Closes|Fixes|Resolves|Implements <KEY>`. A hit sets `key_source` of `description_trailer`.

c. **Branch name** -> scan the branch for the key regex `[A-Z][A-Z0-9]+-[0-9]+`. A hit sets `key_source` of `branch`.

d. **Non-merge commit title** -> scan commit titles from `$RUN/commits.txt`, which Stage 1 wrote with `git log <merge-base>..<head> --oneline`. Identify merge commits by a title matching `^Merge (branch|remote-tracking)`. Drop any key seen ONLY in merge-commit titles. A hit sets `key_source` of `commit_title`.

Validate every candidate against `^[A-Z][A-Z0-9]+-[0-9]+$` before using it. Dedupe. Cap at 6 keys. Designate one key as `primary` (the first hit by precedence above). All others are `secondary`.

**If no key is found AND the user did not supply an MR/PR link**, this reviewer is SKIPPED. Return zero findings. Write a single `method.warnings` entry: `"spec-conformance skipped: no ticket key found and no MR/PR link supplied"`. A run with no spec has nothing to compare against.

## 3. Fetching the tickets

### 3.1 Fetch each in-scope key

For each surviving key, call:

```
getJiraIssue(
  cloudId  = <cloud-id>,
  issueIdOrKey = <KEY>,
  fields   = ["summary","status","issuetype","description","parent",
               "subtasks","labels","comment"],
  responseContentFormat = "markdown",
)
```

`<cloud-id>` identifies the reader's own Atlassian site and is never hardcoded here. Resolve it
once at run time by listing the accessible Atlassian resources through the same integration that
provides `getJiraIssue`, then reuse that value for every call in this run. When the lookup returns
more than one site, ask the user which one holds the ticket rather than guessing.

The `fields` array is a checklist, not a suggestion. Reproduce it exactly. `parent` and
`subtasks` are REQUIRED and are the two most often dropped when the call is written from
memory. A call that omits `parent` cannot see the hierarchy at all, and every downstream
step then reads as if the ticket were standalone. Verify the array before sending.

Parse defensively: the response is sometimes a flat `{key, fields, ...}` and sometimes wrapped as `{issues:{nodes:[{...}]}}`. Always resolve with `.issues.nodes[0] // .`.

A large response can exceed the tool output limit and land in a temp file. Such a file is
often not valid JSON end to end. Parse it with `json.JSONDecoder().raw_decode(raw)`, not
`json.load`, which fails with `Extra data: line <n>`.

### 3.2 Walk to the parent. Always.

**This step is unconditional.** Run it whenever `fields.issuetype.subtask` is true, no
matter what the child's `description` contains. Do NOT gate it on the child description
being null, short, or apparently complete. A sub-task usually carries a one-line restatement
of its own slice, which reads like a finished spec while the product specification, the
scope boundary and the acceptance criteria all live one level up. Treating a thin child
description as the whole spec is the single most common way this reviewer returns a
confident, well-evidenced, and wrong verdict.

For each ticket with a `fields.parent`, fetch each DISTINCT parent key once with the same
`fields` array, role `parent`. The parent's `fields.subtasks[]` gives sibling keys and
summaries, which feeds the parent-ownership rule in the forward pass.

**Escalate one more level only when the parent is itself spec-free.** If the parent's
`description` is null, or contains no acceptance criteria, tech spec, scope section, or
normative `must`/`should` sentence, fetch ITS parent once, role `grandparent`. Stop there.
Never walk further. Epic and initiative prose is aspirational and manufactures false gaps.

**No parent is normal and silent.** A standalone Story with no `fields.parent` is not a
defect. Record it and move on without a warning.

**An unreadable parent warns loudly and never aborts.** If a sub-task names a parent that
cannot be fetched (permissions, outage, deleted), add a `method.warnings` entry
`"parent <KEY> unreadable: <reason>"`, surface it in the verdict header, and cap
`confidence` at `medium` on every finding this reviewer emits. Continue the run.

### 3.3 Hierarchy invariant

Before building the criteria ledger, state the resolved hierarchy on one line:

```
hierarchy: <PRIMARY-KEY> (<issuetype>) -> parent: <KEY> fetched | no parent | unreadable: <reason>
```

A run that cannot state this line has not resolved the hierarchy and is incomplete. This
gate is structural and binding, exactly like the two invariants in section 7.

### 3.4 Comments

`fields.comment.comments[]` is dominated by "Jira Automation" bot comments echoing commits. Filter on `author.displayName` before reading comments for scope changes. If `comment.total` exceeds what came back, paginate via `getJiraIssue` or the REST comment endpoint at `startAt=<n>`.

## 4. Building the criteria ledger

Decompose ticket text in this fixed order, so IDs are stable across runs:

```
acceptance_criteria -> tech_spec -> non_goals -> description
```

Apply the platform filter BEFORE creating any criterion.

**Platform filter.** Derive platform from `$RUN/diff_index.json`'s dominant extensions, then the project path, then a branch prefix such as `feature/ios/`. A `--platform=<p>` flag overrides. Tech Spec bullets labelled for another platform (`FE:`, `BE:`, `Mobile:`, `iOS:`, `Android:`, `Web:`) go to `excluded_criteria[]` with `reason` of `other_platform:<P>` and are never scored.

**Platform is usually implied, not labelled.** Most real tickets carry no `BE:` prefix at all.
Infer the owning platform from the vocabulary of the criterion, and record how you decided in
the `reason`. Named server-side machinery (a migration, a queue or cron task, an ORM model, a
server event handler, a management command, a database column) implies backend. Named
client-side machinery (a screen, a component, a route, a form, a rendered label) implies
frontend. Use `other_platform:<P>` with an `inferred` marker so a reader can challenge the
call. **Ambiguity resolves toward INCLUSION.** A criterion you cannot confidently assign is
scored, not excluded. Excluding a criterion by a weak guess is how a real gap disappears
silently, and a false gap at least gets argued about in the verification gate.

**Criterion IDs.** Ticket-scoped, source order, never renumbered.

| section | ID form |
|---|---|
| Acceptance Criteria | `<KEY>/AC-n` |
| Tech Spec | `<KEY>/TS-n` |
| Non-goals | `<KEY>/NG-n` |
| Description normative sentence | `<KEY>/DS-n` |

**Splitting.** One criterion equals one independently failable assertion. Split a compound bullet on `and` only when both halves can fail separately. BDD: one criterion per `Then` clause, with `Given` and `When` folded into `text`.

**Description prose.** Background, links, and screenshots are never criteria. Exception: a normative sentence using `must` or `should` that no acceptance criterion already covers becomes a `DS-n` criterion, with `confidence` capped at `medium`.

**Non-goals.** These become negative criteria with `polarity` of `negative` and IDs of `NG-n`. A respected Non-goal is `implemented`. A violated Non-goal is `contradicted`, and `contradicted` is always blocking.

**Parent criteria.** Decompose the parent exactly like any other ticket, under
`<PARENT-KEY>/AC-n` and so on. The platform filter still applies, so on a frontend diff the
parent's backend criteria go to `excluded_criteria[]` and are never scored as gaps. That is
correct and expected. Their value is not the forward pass, it is the scope-inversion check in
section 5.

**A parent Out-of-scope section is a source of negative criteria.** Every bullet under
`Out of scope`, `Not in scope`, or `Non-goals` on the parent becomes an `NG-n` criterion with
`polarity` of `negative`, owned by the parent key. This is the highest-value thing the parent
carries, and it is frequently the only place the boundary between platforms is written down.
Do not skip a parent Out-of-scope section because its bullets are labelled for another
platform. Platform labels exclude criteria from SCORING, never from the scope boundary.

**Budget.** Cap at 60 criteria total. Divide the cap evenly across in-scope tickets and redistribute unused remainder. On overflow, merge the finest-grained sibling criteria and record a `method.warnings` entry.

## 5. Forward pass

Score every criterion against `$RUN/diff.patch`. Use `$RUN/diff_index.json` to locate files before reading hunks.

Statuses (the ones below, no others). `not_scored` is the one addition, and section 9 is the
only place that allows it:

| status | meaning |
|---|---|
| `implemented` | evidence of kind `code`, `config`, or `preexisting` covers the whole criterion |
| `partial` | one clause evidenced, another not; `note` MUST name the unevidenced clause |
| `missing` | anti-false-gap protocol ran and found nothing; requires `absent` evidence with `searched[]` |
| `contradicted` | the diff does the opposite; always blocking |
| `not_verifiable` | a diff cannot prove it; requires `unprovable_reason` and `suggested_check`; NEVER a gap |
| `not_scored` | degraded runs only, per section 9; the criterion was never reached and `note` carries the reason |

A test alone never yields `implemented`. A criterion evidenced only by `kind` of `test` is `partial`, with the note `"test present, implementation not located"`.

**Anti-false-clear protocol.** Run BEFORE emitting any `implemented`. This is the mirror of the
anti-false-gap protocol below and it is not optional. Emitting `missing` used to cost four
recorded steps while `implemented` cost nothing, and a status nothing checks is the one way a
real gap leaves the run as a clean pass.

All three must hold, and all three are recorded on the criterion's row.

1. **An anchor.** Exactly one `file:line`, either from the `added` list for that file in
   `$RUN/anchors.json` with `anchor_kind` of `added`, or an untouched location with
   `anchor_kind` of `preexisting`. A criterion with no anchor is never `implemented`. Route it
   to `partial`, or to `not_verifiable` when a diff genuinely cannot prove it.

2. **A traced chain.** Record `chain[]`, one real `file:line` per hop, from the entry point the
   criterion's `Given` names to the mechanism its `Then` asserts. A criterion evidenced only by
   a flag or a Bool threaded one level deep is `partial`, with the untraced hop named in `note`.
   Threading a value is not the same as delivering the behaviour it is supposed to switch on.

3. **Clause coverage.** Every clause of the criterion evidenced, not only the one that was easy
   to find. One unevidenced clause makes the criterion `partial` and `note` names that clause.
   The rule for tests above is the precedent: partial evidence never rounds up to a pass.

**An `implemented` whose chain runs through untouched code is `implemented (preexisting)` and is
reported as such.** Set `anchor_kind` to `preexisting`, name the untouched `file:line`, and put
one sentence in `note` saying this change did not deliver it. A criterion the change inherits
rather than implements is not a defect and not a gap. Silently folding it into a plain pass is
what makes the verdict unreadable, because the reader cannot tell what the change actually did.

**Anti-false-gap protocol.** Run in this order BEFORE emitting any `missing`. Most false gaps come from skipping step 1.

1. Grep `$RUN/diff.patch` for the criterion's key identifiers and domain nouns. A hit means coverage exists somewhere not yet read. Locate the file, read the hunk, reclassify to `implemented` or `partial`.

2. Grep the working tree only when `cwd` is the same repo as the change. Verify by comparing the git remote URL against the project path. Same repo -> grep the tree. A criterion already satisfied by pre-existing code is `implemented` with evidence of kind `preexisting`. Different repo or not a repo -> skip this step and add a `method.warnings` entry.

3. Scan commit titles and the description for a sibling ticket key or a reference of the form `done in !NNNN` or `done in #NNNN`. A hit still means `missing`, but set `owner_ticket` and exclude the criterion from `blocking_gaps[]`.

4. Only now emit `missing`, with an `absent` evidence item whose `searched[]` records exactly the commands run in steps 1 to 3.

**Criteria a diff cannot prove.** Route to `not_verifiable`, never to `missing`.

| ticket language | `unprovable_reason` | `suggested_check` shape |
|---|---|---|
| "full regression pass", "run acceptance plans", exploratory QA | `manual_qa` | "Run <suite> on <platform> before merge" |
| "works against the real backend", staging verification | `external_system` | "Smoke <endpoint> against staging" |
| "no regressions", "existing flows unaffected" | `runtime_behaviour` | "Exercise <flow> manually" |
| "matches Figma", pixel or design parity | `design_parity` | "Design review on <screen>" |
| latency or memory budgets with no benchmark in the diff | `perf_target` | "Measure <metric> on device" |
| feature-flag rollout %, App Store submission, release steps | `release_process` | "Confirm <step> at rollout" |
| "existing records migrated", production data state | `data_state` | "Verify migration count in production" |

If a benchmark or automated test IS in the diff and asserts the target, that is `implemented` with evidence of kind `test`. The `perf_target` trigger covers unbacked targets only.

### Scope inversion (parent boundary check)

Run this check once, after the forward pass, using the parent criteria from section 4. It
detects work done on the wrong side of a boundary the parent drew. It is the main reason the
parent is fetched at all.

Two triggers, either one is sufficient:

1. **The diff's platform is named out of scope by the parent.** Take the platform derived by
   the platform filter. If a parent `NG-n` criterion excludes that platform (`FE changes`,
   `No backend work`, `Mobile out of scope`), and the diff changes product behaviour on that
   platform, the criterion is `contradicted`.

2. **The diff implements a criterion the parent assigns to another platform.** A parent
   acceptance criterion labelled or clearly scoped for platform X is satisfied by code in the
   diff on platform Y. The behaviour is being built twice, in the wrong layer, or in a layer
   that will conflict with the owning one.

`contradicted` is already defined as always blocking, so no new severity is needed. Emit it
through the normal ledger with `criterion_id` set to the parent criterion and `ticket_key` set
to the PARENT key, not the primary.

**Anti-false-positive.** Before emitting, confirm all three. Skip the finding if any fails.
- The out-of-scope bullet is about THIS work, not a named follow-up story.
- The diff genuinely changes behaviour, not only tests, types, or copy.
- No comment or description sentence on either ticket re-admits the platform to scope.

A scope inversion is a spec finding and nothing more. Do not restate it as a design or
architecture opinion. Those belong to other reviewers and are barred by the scope wall in
section 1.

## 6. Reverse pass

Walk EVERY path in `$RUN/diff_index.json` and classify it. First match wins.

1. **Auto-ignored.** Straight to `ignored_files[]`, never an extra.
   - `lockfile` -> `*.lock`, `package-lock.json`, `yarn.lock`, `Podfile.lock`, `*.resolved`, `go.sum`
   - `generated` -> `__generated__/**`, `*.generated.*`, `*.pb.*`, `*.g.dart`, `__snapshots__/**`, `*.snap`
   - `vendored` -> `vendor/**`, `Pods/**`, `node_modules/**`

2. **Pure formatting.** Every changed line differs only in whitespace, quote style, or import order -> `ignored_files[]` with `classification` of `formatting`.

3. **Merge churn.** A file changed only under merge-commit titles -> `ignored_files[]` with `classification` of `merge_churn`. Add a `method.warnings` entry with the count.

4. **Test for a covered criterion.** A test file whose content clearly targets a criterion that is already `implemented` or `partial` -> attach as evidence of kind `test` on that criterion. Not an extra.

5. **Sibling-key ownership.** A key other than the primary appears in the commit that touched this file -> extra with `category` of `other_ticket_work`, `possible_owner_ticket` set, severity `info`.

6. **Surviving paths are real extras.** Assign a category from: `out_of_scope_feature`, `other_ticket_work`, `refactor_drive_by`, `dependency_bump`, `tooling_or_config`, `test_only`, `docs_only`. Apply severity:
   - `concern` if the change alters product behaviour AND no in-scope ticket plausibly owns it.
   - `info` if `possible_owner_ticket` is set, or category is `test_only` or `docs_only`.
   - `review` otherwise.

Extra IDs: `EX-1`, `EX-2`, `EX-3`, in the order found. Use that exact prefix.

## 7. Invariants

Two of them, both structural and binding, both stated before any finding is emitted. They close
different holes. The first proves every changed FILE was looked at. The second proves every
CRITERION was scored. A run can close the first while having scored nothing at all, which is why
the second exists.

### 7.1 File coverage invariant

Every path in `$RUN/diff_index.json` must land in exactly one of:
- a criterion's `evidence[].file`
- `ignored_files[].path`
- an extra's `files[]`

Not zero places, not two. State the ledger counts:
```
paths total: <N>  accounted: <N>  (criteria evidence: <n>, ignored: <n>, extras: <n>)
```

### 7.2 Criteria invariant

State the counts, then one row per criterion. The counts alone are not the record.

```
criteria total: <N>  scored: <N>  (implemented: <n>, partial: <n>, missing: <n>,
                                   contradicted: <n>, not_verifiable: <n>, excluded: <n>)

PROJ-1234/AC-1  implemented       SearchScreen.swift:120  flag ON -> multi element
PROJ-1234/AC-2  implemented(pre)  SearchScreen.swift:112  untouched, main already gates
PROJ-1234/NG-1  implemented       DashboardViewController.swift:92   bypass needs files.count > 1
```

Every criterion gets a row, including every `excluded_criteria[]` entry, which prints its
`reason` in place of an anchor. A criterion excluded by a weak platform guess is the other way a
real gap disappears without argument, and section 4 already warns about it. The row is what makes
that call challengeable by a reader.

**A summary sentence is banned as the record.** "All eight criteria are implemented", "the change
matches its spec", "all four acceptance criteria are covered" and every variant are prose, not
evidence. They may appear in the verdict only AFTER the rows exist, and only as a restatement of
them. On the recorded run the entire spec pass reached the report as one such sentence, buried in
process notes, with no per-criterion anchor anywhere in the run directory. Nothing downstream
could check it, and the reader could not tell whether a given criterion had been scored at all.

**A run that cannot print the counts line and every row has not run this reviewer.** Say so in
the verdict as a degradation. Do not report it as a clean spec result.

Both invariants must close. A run that closes neither, or only one, is incomplete.

### 7.3 The ledger file

Write the rows to `$RUN/spec-ledger.json` as soon as they are complete, before emitting any
finding. Stage 6 reads this file to verify the `implemented` rows and Stage 9 reads it to publish
them, so a ledger held only in this reviewer's head reaches neither. It is the same contract as
`$RUN/ticket-context.md`: a named file the rest of the pipeline can open.

```json
{
  "invariant": "criteria total: 8  scored: 8  (implemented: 8, partial: 0, ...)",
  "criteria": [
    {"criterion_id": "PROJ-1234/AC-1", "ticket_key": "PROJ-1234", "polarity": "positive",
     "text": "Given the user creates an entry and the multi_select flag is on, when selecting files, then the user can select more than one file.",
     "status": "implemented", "anchor": "path/to/File.swift:120", "anchor_kind": "added",
     "chain": ["Entry.swift:161", "Provider.swift:20", "Provider.swift:120"],
     "note": "", "searched": []}
  ],
  "excluded_criteria": [
    {"criterion_id": "PROJ-1234/TS-3", "text": "...", "reason": "other_platform:BE (inferred)"}
  ],
  "warnings": []
}
```

`searched[]` carries the commands from the anti-false-gap protocol on a `missing` row and is
empty otherwise. `note` is required on every `partial` and every `preexisting` row and empty
elsewhere.

## 8. Emitting into the pipeline ledger

After both invariants in section 7 are satisfied, emit pipeline findings. Only gaps and extras become findings. Matches and `not_verifiable` are recorded in the run's spec section for the final report only.

Each finding row:

| field | value |
|---|---|
| `origin` | `spec-conformance` |
| `file` | the primary changed file for this gap or extra |
| `lines` | a real `file:line` anchor from the diff. A finding with NO anchor is dropped by the pipeline unverifiable |
| `claim` | one sentence describing what is missing or what was added out of scope |
| `severity` | initial severity: `concern` for blocking gaps and `contradicted`; `review` for `partial` and non-`concern` extras; `info` for `owner_ticket` gaps and `info`-severity extras |
| `evidence` | the evidence array from the criterion or extra |
| `criterion_id` | the `<KEY>/AC-n` or `EX-n` identifier |
| `ticket_key` | the primary ticket this criterion came from |

Criteria with status `implemented` or `not_verifiable` do NOT become pipeline findings.

**Not becoming a finding is not the same as not being checked.** Stage 6 verifies every
`implemented` row in `$RUN/spec-ledger.json` against the branch bytes, and a row that fails there
is demoted and enters the pipeline as a finding at that point. This reviewer's `implemented`
verdicts are a claim awaiting verification, not a result.

For a gap with no changed file to anchor against, use the closest file in the diff that is semantically related to the feature. If no file can be found, the criterion is `not_verifiable` with `unprovable_reason` of `runtime_behaviour` and it does not enter the pipeline.

## 9. Degraded modes

**No acceptance-criteria section anywhere.** Fall back in order: Tech Spec bullets, then Description `must`/`should` sentences. Set `verdict.conformance` to `insufficient_evidence`. Add a `method.warnings` entry. Lead the pipeline's report section with why.

**Primary ticket carries thin criteria relative to its parent.** This trigger is NOT limited to
a null description. It fires whenever the primary is a sub-task and the parent holds
acceptance criteria, a scope section, or a tech spec that the child does not restate. A
two-sentence sub-task description under a fully specified parent is the normal case, not an
exception, and it looks like a complete spec until the parent is read. Score the parent
criteria and report them in a separate parent section. Set `verdict.conformance` to
`insufficient_evidence` only when the child contributed no scorable criteria of its own.
NEVER return a clean `conforms` verdict over zero criteria. Name the ticket the criteria
actually came from. A clean verdict over zero criteria is a false all-clear.

**Parent unreadable on a sub-task.** Add the `method.warnings` entry from section 3.2, lead the
report section with it, and cap `confidence` at `medium` on every finding. Never emit a
scope-inversion finding from section 5 without the parent in hand. Do not abort the run.

**Working-tree check unavailable** (different repo or not a repo). Skip step 2 of the anti-false-gap protocol. Add a `method.warnings` entry. Do not guess the answer that step would have given.

**`diff.patch` absent or empty.** This reviewer is SKIPPED. Emit one `method.warnings` entry: `"spec-conformance skipped: $RUN/diff.patch missing or empty"`.

**Criteria invariant cannot be closed.** Criteria were decomposed but some could not be scored,
for example because the read budget ran out before their files were reached. Print the rows you
have, mark the rest `not_scored` with the reason, and add a `method.warnings` entry naming the
count. Then lead the report section with it and cap `confidence` at `medium`. Never round the
unscored rows up to `implemented`, and never drop them from the table to make the counts close.

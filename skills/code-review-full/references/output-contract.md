# Output Contract: code-review-full

Defines every artifact the pipeline emits. The chat verdict, the paste-ready comments, one
HTML report, and a closing note.

---

## 1. Chat Verdict

### Opening lines (required, in this order)

**The first line is the answer, not the setup.** State what the reader has to do and how much
was cut, in one line. Reviewer names and mode are provenance, and provenance belongs below the
answer.

```
<N> findings to fix before merge. <M> dropped.
<any degradation warning, one line each>

Reviewers: <roles that actually ran, from: correctness, structural, direct-read, spec-conformance>
Mode: <any reviewer that ran inline because its skill was absent, or "all delegates available">
```

Match the headline to the strongest verdict present. `<N> findings block merge` when anything
is `BLOCK MERGE`, `<N> findings to fix before merge` when the strongest is `FIX BEFORE MERGE`,
`Nothing blocks merge. <N> follow-ups` when only `FOLLOW-UP TICKET` survives, and
`Nothing to fix. <M> candidates dropped` when everything was cut. That last one is a real
result, not a failure, and it must never be padded to look like a finding.

`<N>` counts the findings carrying that verdict, not every kept finding. Drop the plural when
`<N>` is 1, so it reads `1 finding blocks merge`. When blockers and lower-severity findings
coexist, the headline reports the blockers, and the rest are visible in the findings below.

**Degradation warnings sit in the opening block, above the provenance.** A warning the reader
scrolls past is a warning that failed. These are the warnings that qualify: a skipped
spec-conformance reviewer, a diff that was not read in full, and any reviewer that could not
run at all.

When the spec-conformance reviewer ran, say so. When it was skipped, say so loudly. A thin
review must never look like a full one.

**The skip has three distinct causes and the warning must name the right one.** They are not
interchangeable, because each tells the reader something different about how much to trust the
result.

```
Spec-conformance reviewer: SKIPPED -- no Jira ticket was found.
                           This review covers code quality only, not ticket requirements.
```

```
Spec-conformance reviewer: SKIPPED -- you chose to run without a ticket.
                           This review covers code quality only, not ticket requirements.
```

```
Spec-conformance reviewer: SKIPPED -- the run was non-interactive, so no ticket key
                           could be requested. A ticket may well exist. This review
                           covers code quality only, not ticket requirements.
```

The third case is the one that most needs stating. A ticket probably exists and simply could
not be asked for, so the gap is in the pipeline, not in the change.

### Per finding (one block each, max 5)

- **Anchor.** `file:line`. Exactly one file and exactly one added line from the diff. Other
  sites of the same finding belong in the body, not in the anchor.
- **What is wrong.** One or two plain sentences. No jargon.
- **Why it matters.** The practical consequence if left unfixed.
- **Fix direction.** What to change, not how to write the patch.

### Self-correction disclosure

Any correction the pipeline made during Stage 8 (council synthesis) must appear inline, next
to the original council claim. Format:

```
Council claimed: <original claim>
Pipeline correction: <what was wrong and what the correct reading is>
```

Never fold a correction silently into the final text. The user should see the pipeline caught
its own error.

### Dropped-findings table (required)

| Finding | Dropped at stage | Reason |
|---------|-----------------|--------|
| ... | Verification gate | No reproducible path found |
| ... | Council cut | Duplicate of F2 |
| ... | Cap | Ranked below the top 5 |

This table is not filler. It is what tells the reader the pipeline discriminated rather than
pattern-matched. Its presence is what makes the kept findings credible. Omitting it is not
allowed.

### Artifact paths

```
Report: <cwd>/review-<source-slug>-<YYYY-MM-DD-HHMMSS>.html
```

### Closing next action (required)

The last line names ONE thing the reader can do in under two minutes. Starting is the hardest
step, so make the first move small and specific enough that no decision is needed to begin.

```
Next: open SearchScreenViewModel.kt:84 and check what calls bindSearch().
```

One action, not a list. When several findings are kept, point at the highest-ranked one only.
When nothing was kept, the action is still concrete:

```
Next: nothing to fix. Skim the dropped table if you want to sanity-check the cuts.
```

Never close with an offer of further help, a recap of what the pipeline just did, or a
question like "want me to dig deeper". End on the action.

**One exception, Stage 10.** When the review was pinned to an MR or PR and comments were
kept, the posting offer in `posting.md` becomes this closing line instead of following it.
It qualifies because it is one concrete action, not an open-ended offer of help:

```
Next: post these 3 comments to MR !1234? I'll go one at a time.
```

Still one action. Do not emit both a closing action and a posting offer.

### Worked layout

```
3 findings to fix before merge. 8 dropped.
Spec-conformance reviewer: SKIPPED -- no Jira ticket was found.
                           This review covers code quality only, not ticket requirements.

Reviewers: correctness, structural, direct-read
Mode: all delegates available

---

F1  SearchScreenViewModel.kt:84
    What is wrong: global_search_entered fires during view setup, not on user action.
    Why it matters: search funnel counts screen renders as searches. Numbers will not
                    match iOS.
    Fix direction: move the event to the point where the query changes from empty to
                   non-empty.

F2  PaymentRepository.kt:201
    What is wrong: network call on the main thread inside a suspend function that is
                   launched with Dispatchers.Main.
    Why it matters: ANR on slow connections.
    Fix direction: switch to Dispatchers.IO for the retrofit call.

F3  build.gradle:14
    What is wrong: minSdkVersion 19 but code calls API 21 without a version guard.
    Why it matters: crash on Android 4.4 devices still in the field for this app.
    Fix direction: add a Build.VERSION.SDK_INT guard or raise minSdkVersion to 21.

Council claimed: F3 affects fewer than 1% of sessions.
Pipeline correction: that claim was based on global Play Store data. The app targets a
                     region where Android 4.4 share is higher. The finding stands.

---

Dropped findings

| Finding                               | Dropped at stage   | Reason                          |
|---------------------------------------|--------------------|---------------------------------|
| Nullable receiver in ExtUtils.kt:55   | Verification gate  | Compiler null-checks the site   |
| Magic number in Config.kt:9           | Council cut        | Existing constant one line up   |
| Import order in 6 files               | Council cut        | Style-only, no behaviour risk   |
| Missing kdoc on internal fun          | Cap                | Ranked below top 5              |
| ...                                   | ...                | ...                             |

---

Report: <cwd>/review-myrepo-2024-11-15-143022.html

Next: open SearchScreenViewModel.kt:84 and check what calls onSearchOpened().
```

---

## 2. Paste-Ready Review Comments

The most important section. Every kept finding gets one comment block.

**Terse is the contract, not a preference.** The author reads these on a merge request, between
other tasks. A comment that takes thirty seconds to read gets skimmed, and a skimmed comment
does not get fixed. Every word has to earn its place.

### Structure (fixed order)

1. **Anchor.** `file:line`, on its own line. One file, one added line, nothing else on that
   line. Two anchors on one comment means the finding was not deduped, go back to Stage 5.
2. **Problem.** One sentence. What is wrong, and the mechanism that makes it wrong.
3. **Ask.** One sentence. What to change.

That is the whole comment. Two optional lines may be added, and only when they carry
information the two sentences above cannot:

- An **also-at** line, when the same defect sits at other sites.
- A **code snippet**, when showing beats describing. Under five lines.

### Hard length cap

**Four lines maximum, roughly fifty words.** Anchor, problem, ask, and at most one optional
line. A comment over the cap is not "thorough", it failed the contract and goes back to be cut.

The cap counts non-blank lines. Keep a blank line after the anchor and between the remaining
lines, the way the worked example does, so the comment breathes on the merge request. Those
blanks are free, the words are not.

Two exceptions, both narrow:

- A snippet may push it to five lines. The prose still holds at three.
- A subtle mechanism that stops being checkable when compressed may take a second sentence in
  the problem line. Use this rarely. Most findings that feel like they need it are just
  padded.

The cap is what forces the finding to be understood before it is written. A verbose comment is
usually a sign the pipeline is describing its own reasoning instead of naming the defect.

### What to cut

Cut these on sight. They are what make a comment read as machine-written.

- **The consequence line.** Fold it into the problem sentence, or drop it. "Fires on every
  render" already tells an engineer the funnel is wrong. Spelling that out patronises.
- **Restating the code.** The reader is looking at the line. Do not narrate it back.
- **Reasoning trail.** Not how the defect was found, not what was checked, not what was ruled
  out. Only the defect.
- **Scene-setting.** "This function is responsible for..." Start at the problem.
- **Both halves of a pair.** "It fires during setup, not on user action" says one thing twice.
  Keep the half that carries more.
- **Every intensifier and hedge.** "Actually", "simply", "just", "quite", "it appears",
  "it seems", "perhaps", "somewhat", "could possibly".

### Certainty: state facts flatly, ask only on judgement calls

- **The evidence passed the Stage 6 verification gate.** It is a fact. Write it flat and
  declarative. Not "this might be firing too often", but "this fires on every render".
- **The ask is an imperative when the fix is unambiguous.** "Move it to the query change."
  Not "could we consider moving it". A question mark on a settled fix is padding.
- **The ask is a question only when it turns on a judgement the pipeline cannot make**, such
  as a product decision or a constraint the author may know about. That question is honest and
  it stays.

Keep a hedge that carries real uncertainty. Deleting that one manufactures confidence the
pipeline did not earn.

### Rules

- One fenced `text` block per finding. Copies cleanly with no surrounding markup.
- **Scrubbed of all internal vocabulary.** No finding IDs, no severity labels, no mention of
  a council, advisors, verification stages, or the pipeline. The author never saw any of that.
  Leaking it confuses.
- **One finding per comment.** Never append a second issue, however small. A comment that
  raises three things gets none of them fixed. Other findings have their own blocks.
- **One comment per finding, and one anchor per comment.** The inverse of the rule above, and
  it breaks just as often. When the same defect shows up at three places, that is still one
  comment on one line. The other two go in the body as an "also at" line, right before the
  ask:

  ```
  Also at `DashboardViewController.swift:120`, same pattern.
  ```

  Two comments for one fix wastes the author's attention and splits the conversation across
  threads. Posting is one file and one line per comment anyway, so a comment carrying two
  anchors cannot be placed and one of them gets picked at random.
- **No preamble, no closer.** Never open with "Great work on this" or "I noticed that". Never
  close with "let me know what you think", "hope this helps", or "happy to discuss". Open on
  the anchor, end on the ask.
- **Number the steps when the fix genuinely takes more than one.** A numbered list beats a
  sentence with two "and then"s in it. Cap at three steps, and each step is a fragment, not a
  sentence. Most fixes are one step, so reaching for a list is usually a sign the finding
  should have been split or cut.
- **No effort or time estimates.** Never say how long a fix will take or call it quick. The
  pipeline has not built the code, does not know the test surface, and cannot see what the
  author already tried. An estimate that is wrong reads as dismissive.
- Written to a peer. State the problem and the request. No praise padding, no blame,
  no lecturing.
- Matter-of-fact about defects. Never "uh oh", never "there seems to be a problem". Name the
  cause and the fix.
- Include a code snippet only when showing beats describing. Under five lines.

### Language

**These rules bind every word the pipeline emits, the chat verdict as well as the comments.**
Both are prose a human reads. Check output against this list before sending it.

- Active voice. "`bindSearch()` calls this during setup", not "this is called by `bindSearch()`".
- Address the author as "you", or use "we" for a shared decision. Not "the developer" or
  "one should".
- Simple words. "fix", "use", "move", not "address", "utilise", "leverage".
- Short sentences. In the chat verdict one longer sentence may carry a mechanism. In a comment
  it may not, the cap does not allow it.
- No semicolons, no em-dashes, no asterisks for emphasis, no emoji. Periods and commas do the
  work. This one leaks most often. An em-dash in a verdict is as much a breach as one in a
  comment, and a proposed snippet is not an exemption.
- No marketing or hype words: "robust", "seamless", "critical", "game-changer", "best
  practice".
- No cliches or idioms: "circle back", "low-hanging fruit", "moving the needle", "on the same
  page". Say the literal thing.
- Cut any sentence the previous sentence already said.

### Worked example

Internal form (never posted):

> **F1 - headline events measure lifecycle, not user intent.** `SearchScreenViewModel.kt:84-104`.
> Event fires from `onSearchOpened()`, whose only caller is a view-setup function.
> Verdict: FIX BEFORE MERGE. Corroborated by both reviewers plus independent read.

Paste-ready form:

```text
`SearchScreenViewModel.kt:84`

`global_search_entered` fires from `bindSearch()` during view setup, so it counts renders,
not searches.

Move it to where the query goes from empty to non-empty.

Also at `PanelFragment.kt:262`, same call path. One fix covers both.
```

Four lines, 44 words. The anchor, the defect with its mechanism, the ask, the also-at.

What disappeared: the finding ID, the severity label, the corroboration count, every reference
to the council and pipeline stages. Also the consequence paragraph about the funnel not
matching iOS, because "counts renders, not searches" already carries it. Also the second event
`global_search_closed`, which is a different defect and gets its own comment or gets cut.

Note the anchor. `PanelFragment.kt:262` is the same defect, not a second one, so it does not
get its own comment and it does not sit beside the anchor. `SearchScreenViewModel.kt` comes
first in diff order, so it wins, and the body names the other site so the author knows the full
blast radius before choosing where to fix it.

Note the certainty. The problem line is flat, because Stage 6 verified it. The ask is an
imperative, because the fix is unambiguous. Nothing here turns on a product judgement, so
nothing is phrased as a question.

### The same finding, over the cap

This is what the pipeline writes when nobody holds it to the contract. It is the same defect
and the same fix.

```text
`SearchScreenViewModel.kt:84`

`global_search_entered` needs to move off `onSearchOpened()`. It currently fires when the
dashboard renders, not when anyone searches.

`bindSearch()` is the only caller, and it runs during view setup. The search bar is always
visible and the view model is scoped to the activity, so the event fires on every render.

So the search funnel counts renders as searches, and the numbers will not line up with iOS,
which triggers on the first character typed.

Could we move it to the point where the query goes from empty to non-empty? That matches what
iOS measures.
```

Eleven lines, 106 words, and it says nothing the four-line version did not. What went wrong:
the ask is stated twice, once at the top and once at the bottom. The mechanism takes three
clauses where one does. The consequence gets its own paragraph. The fix is unambiguous but is
phrased as a question. This version reads as machine-written because it is padded, and padding
is the tell.

### Hard rule

**The agent NEVER posts a comment the user has not individually approved.** Print them all.
Anything that reaches the MR goes through Stage 10, one comment at a time, in the turn it was
approved. See `posting.md`.

A batched approval, an implied yes, or posting in a run with no channel to ask all breach this.
When Stage 10 does not run, or the user skips it, the printed comments are the deliverable and
the human pastes what they want.

---

## 3. HTML Report

**The only file the pipeline writes.** It is the deliverable and the full audit record at once,
so a run that produces no report produced nothing.

**Written to the user's current working directory.** Not the run dir under `/tmp`, which holds
internal scratch only. Not the skill dir.

Filename pattern: `review-<source-slug>-<YYYY-MM-DD-HHMMSS>.html`

`<source-slug>` is the slugified source computed once in Stage 1. Never interpolate a raw
source into a filename, `MR !1234` contains a space and a `!`.

Repeat runs produce new files. Nothing is overwritten.

**There is no companion markdown file.** Earlier versions wrote a `-transcript.md` beside the
report. That artifact is gone. Everything it held now lives in the report's collapsed record
section, and the rule below is what keeps the audit trail intact after the merge.

### Generation

Produced by `scripts/render-report.py` (path relative to the skill directory). Never assembled
by hand in the agent's reasoning.

**Its only input is `$RUN/report.json`.** The script reads that one file and nothing else, so
everything the report shows has to be inside it first: the pipeline chart data, the verdict,
findings, overflow, dropped, corrections, and the whole council record. The authoritative
schema is the module docstring at the top of `scripts/render-report.py`. Read it, then build
`report.json` to match. The script validates its own output and exits non-zero with a reason if
anything is malformed.

### The record is verbatim

`report.json` carries the complete audit record, and every field in it is reproduced word for
word. Nothing is summarized, trimmed, or elided.

| Field | Holds |
|---|---|
| `record.original_request` | The user's request exactly as received |
| `record.framed_question` | The question sent to advisors |
| `record.advisors[]` | Every advisor response, unedited |
| `record.peer_reviews[]` | Every peer review, unedited |
| `record.anonymization_mapping` | Which advisor letter maps to which role |
| `record.ranked_list` | The full ranked list before the cap was applied |
| `record.synthesis` | The chairman synthesis and the final output |
| `record.process_notes` | Stage timings and model versions |

Summarizing any of these to save space defeats the point. The record exists so a reader can
check the pipeline's work, and a summary is the pipeline checking itself.

### The pipeline chart

`meta.pipeline` carries the structured run data and the script draws the ASCII chart from it.
**Never hand-draw the chart and never pass a pre-drawn string.** Same rule as the report
itself, for the same reason: a hand-drawn chart is a claim about the run rather than a record
of it.

Fill in what the run actually did, and leave out what it did not. Every field is optional and
the chart degrades cleanly.

- `sources` - each thing fetched, where it came from, and one detail. The MR or PR, the pinned
  diff, the Jira ticket, anything else read from outside the repo.
- `reviewers` - one row per review pass, carrying the role, the delegate, the model, whether
  it was delegated or inline, and its tool-call count, duration and finding count when those
  are known.
- `stages` - the steps between the reviews and the verdict, such as the merge and the
  verification gate, with their counts. **Only steps that have no key of their own.** Sources,
  reviewers, the council and the verdict each have a dedicated key, so repeating one here
  draws that branch on the chart twice.
- `council` - mode, model, advisor and peer counts, kept and overflow.
- `outcome` - the verdict line.

The counts are what make the chart worth reading. "34 calls, 6m40s, 5 findings" tells the
reader how much work went into a pass. A chart of bare role names does not.

### Requirements

- Self-contained. Opens from disk with no network.
- Inline CSS only. No external fonts, scripts, or images.
- White background, system font stack, single readable column.

### Structure (top to bottom)

1. **Pipeline chart.** The ASCII run map. First thing on the page, so the reader sees what was
   reviewed and by what before reading any conclusion.
2. **Verdict block.** Reviewer list, skipped-reviewer notice if applicable, kept / total count.
3. **Per-finding table.** Anchor, what, why, fix direction, self-correction notice if one exists.
4. **Paste-ready comments.** Each in a styled block with a copy-to-clipboard button.
5. **Collapsed details.** Inside `<details>` elements, collapsed by default:
   - The original request.
   - The framed question sent to advisors.
   - Each advisor response.
   - Each peer review.
   - The ranked list before the cap.
   - The synthesis.
   - Overflow findings cut by the cap.
   - Process notes (stage timings, model versions used).

The report is NOT auto-opened. The skill prints the path and the human opens it.

---

## 4. Closing Note

The skill must print this note after writing the report, because it lands in the user's
current working directory, which may be the repository being reviewed:

```
Wrote:
  review-<source-slug>-<YYYY-MM-DD-HHMMSS>.html

The file is in your working directory. If you do not want it committed, add this line to
.gitignore:

  review-*.html
```

The skill does not add the gitignore line itself. It suggests. The human decides.

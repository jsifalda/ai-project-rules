# Stage 7: Council Triage Protocol

Findings from Stage 6 are real and verified. The council does not find problems.
It ranks, drops noise, and assigns verdicts.

Decisions required: assign a verdict to every finding, resolve severity disagreements,
and rank all survivors.

## Delegation vs. inline execution

If the `council` skill is available, delegate to it and pass the framed brief as the
question. Override its chairman prompt with the one in this file.

If `council` is not available, run every step below. The inline path is complete.

---

## Step 1: Frame the brief

Advisors are stateless. They see nothing except what the brief contains.

Required sections, in this order:
1. **Change summary.** One to three sentences on what the diff accomplishes.
2. **Diff shape.** Files touched, rough line count, type (refactor / feature / fix / migration).
3. **Verified findings ledger.** One row per finding.

Finding row format:
```
[ID] file:line | severity | origin count (N/4 raised this) | summary | evidence | reviewers
```

Origin count is mandatory. Two reviewers independently raising the same finding is strong
evidence and must survive into every advisor's view.

4. **Questions for the council.**
   - Which findings block the merge?
   - Which can be a follow-up ticket?
   - Where do reviewers disagree on severity?
   - Which findings are noise?

---

## Step 2: Five advisors, run in parallel

Spawn all five simultaneously with the framed brief. Each returns a per-finding verdict
table, not an essay. Verdict vocabulary: `BLOCK MERGE / FIX BEFORE MERGE / FOLLOW-UP TICKET / DROP`.

| Advisor | Prompt focus |
|---|---|
| **The Contrarian** | Find the finding most likely to be underweighted. Assume at least one severity is too low. Return a per-finding table, then one paragraph on your top concern. |
| **The First Principles Thinker** | For each finding, ask what contract it violates. Are two findings the same cause in disguise? Return verdicts plus a root-cause map if clusters exist. |
| **The Expansionist** | Identify findings whose blast radius is larger than the evidence suggests. A bug in a utility called from ten places is ten bugs. Return verdict and real blast radius per finding. Do not invent findings. |
| **The Outsider** | You have no project history. Catch findings that reviewers normalised. Flag any finding where the evidence alone does not make the bug self-evident. Return verdict and a fresh-perspective sentence. |
| **The Executor** | For each finding, ask whether the author can act on it today. If you cannot state the required action in one sentence, rate it FOLLOW-UP TICKET or DROP. |

---

## Step 3: Anonymize before peer review

Collect all five responses. Assign letters A through E using a randomized mapping.
Record and reveal the mapping in the report record. Peers judge arguments, not personas.

---

## Step 4: Five peer reviewers in parallel, each with a distinct probe

All five see the anonymized advisor responses and the framed brief.

Why distinct probes: identical prompts produce five versions of one review. Distinct probes
force coverage of blind spots. The dissenter seat is mandatory and may never be dropped,
even for cost reasons. No dissenter means no error-correction path.

| Reviewer | Probe |
|---|---|
| **1. Factual accuracy** | Hunt factual errors. Focus on provenance claims ("pre-existing" or "newly introduced"). Any such claim must be checked against the pinned diff and git history before it is allowed to change a severity. Flag every unsupported claim by advisor letter. |
| **2. Smallest correct fix** | For each finding, propose the smallest correct fix. Correctness first, then minimality. A fix that silences a warning but leaves the root cause is not correct. One sentence per finding. |
| **3. Mandatory dissenter** | Argue against the emerging consensus. Make the strongest possible case that the majority is wrong. You must take a position. "Both sides have merit" is not a position. Reference specific advisor letters. |
| **4. Actionability judge** | For each finding: ACTIONABLE TODAY or NEEDS MORE WORK, plus one sentence. Criteria: clear fix path, bounded scope, author has context without a design meeting. NEEDS MORE WORK -> FOLLOW-UP TICKET at most. |
| **5. Root-cause tracer** | Look for shared causes across findings. A cluster with one root cause should be one item, not several. Return a root-cause map: for each cluster, name the cause and list the finding IDs it explains. |

---

## Step 5: Chairman synthesis

The chairman receives the framed brief, all five de-anonymized advisor responses, and all
five peer reviews. It rules. It does not summarize.

Chairman instructions:

1. Assign every finding exactly one verdict: `BLOCK MERGE`, `FIX BEFORE MERGE`,
   `FOLLOW-UP TICKET`, or `DROP`.

2. Where Reviewer 1 caught a factual error, correct that advisor by name. State what they
   claimed, what the diff shows, and what the corrected verdict is.

3. **Never settle a verdict by counting seats.** The Contrarian and the dissenting peer
   reviewer were assigned to disagree, so a four-to-one split is the protocol working, not a
   majority. Weigh the evidence each seat cites, and prefer the seat that names a specific
   `file:line` over the seat that reasons in general terms. A cited dissenter beats an uncited
   majority. When the dissenter is overruled, say why in one sentence and record it in the
   report record.

4. Rank all surviving findings by severity and confidence. Preserve that full ranked list, it
   goes into the report as `record.ranked_list`. The list is the ordering evidence behind the
   verdict, so a reader can check how you weighed severity against confidence. It is no longer
   an audit of a cut, because there is no cut.

5. Every finding you did not rule `DROP` reaches the chat verdict. There is no cap. Never cut
   to a number. Rank order decides the order the findings are presented in, nothing more.

   **Runaway guard.** When more than 10 findings survive to chat, re-run the root-cause map
   from Reviewer 5 before you finalise. A count that high is more often a dedupe miss than ten
   separate mechanisms. Merge what shares a cause. Never drop a finding to hit a number, and
   record in the synthesis that you ran this re-check.

   This guard is a diagnostic, not a cap. It must never remove a finding. It can only merge
   findings that share one root cause.

6. Bar for reaching chat. A finding must do at least one of:
   - change runtime behaviour
   - break a contract (interface, protocol, API guarantee)
   - lose or corrupt data
   - violate a binding repo convention

   Taste, naming, style, hypotheticals, and "consider extracting this" never reach chat.
   DROP them. The whole point of this pipeline is noise reduction. Handing back twelve
   follow-up tickets is the failure mode it was built to prevent.

7. Required output structure:

   ```
   ## Verified findings by verdict
   [table: rank | ID | file:line | verdict | one-sentence reason]

   ## Severity corrections
   [advisors corrected by name, claim vs. what the diff shows]

   ## Root-cause clusters
   [Reviewer 5 output: cause name -> finding IDs]

   ## Chat-facing findings
   [group under verdict headers with a count: BLOCK MERGE (n), FIX BEFORE MERGE (n),
    FOLLOW-UP TICKET (n), in that order. Omit an empty group. Keep rank order inside a
    group. Per finding: file:line and the required action]

   ## Dropped findings
   [one-sentence reason each]
   ```

---

## Provenance hard rule

Advisors hallucinate history. Any claim that a finding is "pre-existing" or "newly
introduced" must be verified against the pinned diff and git history before it is allowed
to change a severity. This check is not optional.

Real incident: an advisor downgraded a double-counting bug to FOLLOW-UP TICKET because it
called the bug pre-existing. The surrounding function was pre-existing. The specific line
causing the bug was added by the diff. Reviewer 1 caught it. The chairman corrected the
advisor by name and restored the original severity.

If the diff and git history are not available at council time, treat every provenance claim
as unverified and ignore it for severity purposes.

---

## The council always convenes

Even with one verified finding. No minimum threshold to skip Stage 7. One finding still
needs a verdict, a rank, and a decision on whether it reaches chat.

---

## Stage 8 handoff warning

The chairman's synthesis is the most confident text this pipeline produces. It is not
automatically correct.

Before acting on any chairman instruction, re-read every file and symbol it names.

Real incident: a chairman instructed deleting two methods. Both methods also managed
coroutine scopes and cancelled collectors. Following the instruction would have broken the
application. The correct action was removing two lines from inside those methods, not the
methods themselves.

The chairman sees summaries. It does not run the code. Treat its output as a well-reasoned
recommendation, not a patch to apply blindly.

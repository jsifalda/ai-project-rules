# Hard-rule self-audit

> Phase 7. One row per hard rule. Answer the question from the run's **own record** — the tool calls
> it made, the files it wrote, the counts it printed — never from memory of what it meant to do.
> Fill the audit table in the report from these answers.

Each rule gets exactly one mark.

| Mark | Meaning |
| --- | --- |
| `honoured` | The proof exists, and the audit names it |
| `violated` | The proof is absent, or contradicts the rule |
| `n.a.` | The rule's precondition never arose in this run |

`n.a.` needs the precondition named. "No workaround was used" is `n.a.` for the workaround rule.
"I do not think I did that" is not `n.a.`, it is `violated` — an unproven rule is a failed one,
because a rule whose proof nobody can find is exactly the rule that gets skipped.

## The checklist

### Never edit application code during a run

**Question.** Did any write reach a file outside the evidence directory?
**Proof.** The list of paths written this run. Only the evidence directory and the receipt file may
appear.

### Never edit the scenario inventory

**Question.** Was the inventory file opened for anything other than reading?
**Proof.** No write to the inventory path. A wrong verification pointer recorded as a `drift`
finding rather than corrected in place.

### Never file a backlog or issue entry, and never offer to

**Question.** Did the run write to an issue tracker or a backlog file, or say the words that offer
to?
**Proof.** No such write, and no such offer in the chat.

### Never auto-fix

**Question.** Did anything get repaired mid-run, including a fix that looked too small to count?
**Proof.** Findings carried into the report unrepaired.

### Never run against a database the skill did not itself resolve to localhost or a local container

**Question.** Which host did the database URL resolve to, and who resolved it?
**Proof.** The resolved host, named in the run-preparation block. A host the run never resolved for
itself is `violated`, even where it happens to be local.

### Never adopt a development server this session did not start, and never assume its port

**Question.** Which command started the server, and where did the port come from?
**Proof.** The start command from this run's own record, and the port read out of the startup
banner. A port that matches the framework default is not proof it was read.

### Close the browser and stop the development server

**Question.** Did both stop, including on the path where the run failed?
**Proof.** The close and stop calls. This one is audited before the report is written, so a run
that ends early still answers it.

### Never mark a phase silently skipped

**Question.** Does every phase carry a status?
**Proof.** One status line per phase in the run-preparation block, none of them blank.

### Never report a verdict without evidence

**Question.** How many verdicts, and how many evidence files?
**Proof.** The two counts, side by side. They match, or every mismatch is an explicit `none` in the
verdict table. A count of screenshots far below the count of verdicts is the signature of a run
that throttled itself on an imagined budget — check the actual remaining budget before accepting
that trade, because runs get this wrong in the pessimistic direction.

### Never inherit a slice

**Question.** Where did the selected IDs come from?
**Proof.** The Phase 2 ranking, applied to the parsed inventory. A list that arrived from a plan
file, an earlier session or a menu answer and went unranked is `violated`, however sensible the
list was.

### Never leave a workaround unrecorded

**Question.** What did the run do that a user could not have done through the interface?
**Proof.** One workaround block per such step, each naming the surface left unobserved **and the
interface branches closed**, plus the scenarios marked `blocked` because of it. Direct database
writes, role grants and hand-seeded fixtures all count. So does a step that felt like setup.

### Never award a `pass` from a control's presence

**Question.** How many controls were operated, and how many scenarios have a Then step describing
what a control does?
**Proof.** The two counts. Where the first is lower, name each scenario judged without operating
its control — every one of them is `blocked`, not `pass`.

### Never end a run without following the URLs the application itself emitted

**Question.** How many URLs did the application generate, and how many were loaded?
**Proof.** The emitted-links table, with a rendered result against every row. An empty table is
`violated` unless the run genuinely loaded no page carrying a link, which is close to impossible.

## Reporting the audit

A violated rule is **reported**, never quietly corrected. Rewriting the run to hide the violation
destroys the only evidence that the rule needs strengthening, and a run that repairs itself is a run
nobody can audit.

A violation does not invalidate the verdicts it did not touch. Say which verdicts it does touch, and
downgrade those — usually to `blocked`, because a rule broken around a scenario means that scenario
has no evidence, and no evidence is not agreement.

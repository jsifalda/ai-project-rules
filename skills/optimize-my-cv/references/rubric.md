# CV Audit Rubric

The judgement layer of the audit. `best-practices.md` holds the craft rules (bullet formula, metric families, ATS constraints, section order, projects). This file says what a reviewer scores against, how each dimension calibrates for two career tracks, and where the line between a blocker and a nitpick falls. Reference the craft rules rather than re-teaching them. One deliberate exception: dimension 1 quotes the IC bullet formula, because the leadership variant is only legible when defined against it.

## Part 1 — Severity

The buckets are `blocker`, `major`, `minor`. Every classification is a judgement call, not a measurement. Two competent reviewers will disagree on the margin, and that is expected.

**No numeric scores.** The audit never emits "7/10", "82% ATS match", or a per-dimension rating out of five. A fabricated number reads as precision the method does not have, and it invites the candidate to optimise the number instead of the CV. Findings carry a severity label and a reason. Nothing else.

### blocker

Bar: a recruiter or hiring manager scanning for 30 seconds would set the CV down. The defect loses the screen on its own, regardless of how good the rest is.

- Experience section is a duty list with no result anywhere. Every bullet ends at what was done.
- Leadership-track CV never states team size or reporting structure at any point.
- The file does not survive parsing: two-column layout, experience inside a table, contact details only in the page header, or a PDF exported as an image.

### major

Bar: survives the screen, then loses to a comparable candidate. The CV is viable and materially weaker than it should be.

- Metrics appear in older roles but the current role is the thin one. The reader's most recent evidence is the weakest.
- Bullets lead with the mechanism instead of the outcome, so the payoff sits at the end of a four-line sentence.
- Skills section lists forty technologies flat, giving no signal of which three the person is actually deep in.
- A job description was supplied and a stated requirement the candidate genuinely meets appears nowhere in the CV.

### minor

Bar: worth fixing when convenient. Polish, not survival. Nobody rejects on these alone.

- Tense drift between bullets inside one role.
- Date formats inconsistent across roles (`03/2021` in one, `March 2021` in another).
- Skills listed alphabetically rather than by relevance to the target.
- One bullet runs three lines where two would do.

### Breaking ties

A borderline case, worked: bullets carry numbers, but every number counts activity rather than effect ("owned 12 services", "wrote 200 integration tests", "ran 40 interviews"). Metrics are present, so it is not a bare duty list. Blocker or major?

Rule: **can the reader still form a judgement of the person's level?** If activity numbers at least establish scope and the reader can rank the candidate against others, it is `major`. If the numbers leave the reader unable to tell what level this person operates at, it is a `blocker`. Same defect, two severities, decided by whether the screen can still function.

Modifiers, applied after the initial classification:

- **Recency escalates.** A defect in the current role, or in the top third of page one, moves up one level. A defect confined to a role older than roughly seven years moves down one.
- **Repetition escalates.** The same defect in one bullet is minor. In every bullet of every role it is structural, and structural defects are at least `major`.
- **Defects do not stack.** One bullet failing three dimensions produces one finding at the worst severity, not three findings. Report the dimension that best explains the fix.

## Part 2 — The dimensions

Each dimension: what it measures, IC calibration, leadership calibration, and the failure signals to scan for.

### 1. Impact evidence

**Measures:** does each claim carry a result, or only an activity.

- **IC track.** The upstream bullet formula applies unchanged: `[Action Verb] + [Technical What] + [Scale/Impact] + [Technology Used]`, drawing on the four metric families (scale, performance, efficiency, business). Bar: every bullet in the two most recent roles carries at least one metric family. Older roles, at least half.
- **Leadership track.** Same shape, last slot swapped: `[Action Verb] + [Org/System What] + [Outcome] + [Mechanism Changed]`. The mechanism is the process, structure, or practice the person altered. It is a manager's equivalent of naming the technology, and it is what separates a person who was present for an outcome from the person who caused it. Evidence types, in rough order of how much they carry: team size and shape, scope owned, hiring and retention, delivery and quality metrics, cross-functional influence, people grown and promoted. Bar: at least three distinct evidence types across the CV, and the current role names a mechanism rather than only an outcome.

**Failure signals:**

- Bullets that end at the "what" with no result clause.
- Verbs of presence: "worked on", "participated in", "was part of", "contributed to".
- Numbers that count effort, not effect: tickets closed, meetings run, documents written, lines of code.
- Outcome with no mechanism: "improved team morale", "raised engineering quality". No reader can tell what the person did.
- Mechanism with no outcome: "introduced weekly retrospectives", "rolled out a new on-call rota". Something changed, and nothing is claimed for it.
- Company results claimed without a personal link (see dimension 6, over-claiming).

### 2. Specificity

**Measures:** vague verbs, hedges, and claims nobody could dispute.

- **IC track.** Vagueness usually hides scale. "Optimised the ingestion pipeline" is missing a number, not a word. The fix is always a question: what moved, from what, to what.
- **Leadership track.** Vagueness usually hides the lever. The fix question is different: what did this person change that a different manager in the same seat would not have.

**Failure signals (both tracks):**

- Hedged verbs: "helped", "assisted", "supported", "involved in", "contributed towards".
- Uncounted plurals: "various", "several", "multiple", "a number of", "numerous stakeholders".
- Intensifiers doing a metric's job: "significantly", "dramatically", "substantially", "successfully".
- Marketing adjectives: "world-class", "cutting-edge", "best-in-class", "passionate about".
- "Cross-functional teams" used instead of naming which functions.

**Manager-specific passive ownership.** These describe a job description rather than an act, and they are the leadership track's most common specificity failure:

- "Responsible for", "accountable for", "oversaw", "provided leadership for", "managed the process of", "helped drive", "played a key role in".
- Each one should be replaced by a verb naming what the person actually did. "Responsible for hiring" becomes "rebuilt the interview loop", or it becomes nothing.

**Unfalsifiable-claim test:** could a peer who was in the room dispute this sentence? If nobody could disagree with it, it carries no information and costs a line.

### 3. Scope signalling

**Measures:** can a reader tell how big the job was.

- **IC track.** System scale (traffic, data volume, users served, services owned), blast radius (what breaks when this person is wrong), autonomy (who set the direction, who chose the approach), and which technical decisions were owned end to end rather than executed.
- **Leadership track.** Headcount with the direct-versus-indirect split, reporting depth (individual contributors, or managers of managers), number of teams, budget or spend owned, org surface (which other functions this person negotiates with), and how long they held that scope. A leadership CV that never states team size forces the reader to guess, and readers guess low.

**Blocker rule (leadership only):** no team size stated anywhere in the CV is a `blocker`, not a `major`. It is the single number the reader needs and cannot infer.

**Failure signals:**

- "Led the team" or "managed engineers" with no count.
- "Large-scale", "high-traffic", "enterprise-grade" with no scale attached.
- The title carrying the weight a number should. A senior-sounding title says nothing about size and varies wildly between organisations.
- Scope stated once, in the oldest role, and never again.
- Direct and indirect reports collapsed into one figure to make it larger.
- No indication of who set the direction, so the reader cannot tell owner from executor.

### 4. Structure and scannability

**Measures:** section order, bullet density, length, front-loading. The expected section order lives in `best-practices.md`. This dimension judges whether the layout puts the best evidence where it gets read, and the density and length limits below are its own.

**Practical reality:** the top third of page one carries most of the decision. Whatever sits there is what the reader sees, and everything below it is confirmation for a judgement already forming.

- **IC track.** The two strongest technical bullets belong first in the current role. A skills block should be reachable in the first scan, but never above experience for anyone past their first job.
- **Leadership track.** Scope comes before outcomes: team size and org surface, then what the org delivered. A leadership CV opening with a technology list reads as an IC CV with a manager's title bolted on, which is dimension 6's under-claiming failure expressed as layout.

**Failure signals:**

- Current role pushed below education, certifications, or a long summary.
- Bullets ordered chronologically inside a role instead of strongest-first.
- More than roughly six bullets in any one role, so nothing stands out.
- Walls of four-plus-line bullets.
- A summary longer than three lines, or a summary that could sit on anyone's CV.
- Two pages of thin content, or a senior leader's fifteen years crushed into one.

### 5. ATS readiness

**Measures:** keyword coverage against the target, standard section headers, and parse hazards.

**Parse hazards to scan for:** tables, multi-column layouts, text inside headers or footers (contact details there can vanish entirely), icons and graphics, skill-bar or star ratings, text boxes, decorative glyphs, and any PDF that is really an image.

**Standard headers:** "Experience", "Education", "Skills". Creative section names are both a parse risk and a signal risk.

**With a job description supplied,** this dimension becomes a requirement-by-requirement match. List each stated requirement, mark it `present` / `partial` / `absent`, and quote the CV line that satisfies it. Requirements the candidate genuinely meets but never wrote down are the highest-value fix in the entire audit, because the remedy is free.

**Without a job description,** score against the role family's common vocabulary and flag terms the CV uses that the market does not: internal tool names, internal level names, unexpanded internal acronyms.

- **IC track.** Gaps are usually naming mismatches. The CV names one library, the market searches for the ecosystem around it.
- **Leadership track.** Gaps are usually competencies never named at all. Hiring, performance management, roadmap ownership, stakeholder management, budget ownership, incident and reliability governance. Managers skip these because they feel too obvious to state, and the filter does not agree.

**Failure signals:** skill bars, two-column PDF, contact block only in a header, no skills section at all, first-use acronyms with no expansion, and any job-description requirement with zero corresponding line.

### 6. Seniority calibration

**Measures:** does the CV read at the level being targeted. Both directions are failures.

**Under-claiming.** The most common leadership-track failure by a wide margin. A manager writes IC bullets, listing what they personally built rather than what the org shipped. Tells:

- Bullets name code the person wrote, in a role where they had reports.
- The technology list is longer than the org evidence.
- "Hands-on" appears defensively, as if the reader needs reassuring.
- Achievements framed as tasks completed rather than outcomes delivered.
- No bullet describes a decision only a manager could make: headcount, team structure, priority trade-off, hiring bar, a performance call.

**Over-claiming.** The second most common. Credit taken for org outcomes with no evidence of the person's own lever. Tells:

- A large business number with no mechanism attached to it.
- Company achievements restated in the first person.
- Scope claimed at a size the reporting line does not support.
- "Drove", "owned", "spearheaded" attached to outcomes several layers away from the person's actual seat.
- A title that outruns everything the bullets underneath it describe.

**IC calibration.** Under-claiming is a senior engineer listing work a mid-level engineer also does. Over-claiming is a mid-level engineer using architecture-ownership verbs for work they contributed one part of.

**The level test.** Take the three strongest bullets and ask what someone one level below would have written for the same work. If the answer is "the same sentence", the bullet is not signalling level and needs the scope, decision, or ambiguity added back.

### 7. Consistency and verifiability

**Measures:** whether the document holds together, and whether the candidate can defend it in a room.

- **Dates.** Unexplained gaps over roughly four months. Overlapping roles with no note. Month precision in some entries and year-only in others, which reads as hiding rather than tidying.
- **Titles.** A title that does not match what the bullets underneath describe. Retroactive upgrades to old roles. Senior-sounding titles over two-person scope.
- **Drift.** Tense (present for current, past for prior), bullet-end punctuation, date formats, capitalisation of technology names, first-person pronouns appearing in some bullets only.

**The interview-defence test.** Any claim the candidate could not discuss at depth for five minutes is a liability, not an asset. It converts a strong CV into a weak interview.

- Every metric needs a story: where the number came from, what it was before, who else contributed.
- Every listed technology needs real use, not a tutorial.
- Every outcome needs decomposing into what this person specifically did.

**Rule when provenance is unknown:** the audit does not delete an unverifiable number. It flags it as "prepare the story or cut it" and leaves the choice with the candidate, who is the only one who knows.

## Part 3 — Track selection

Pick one track before scoring. State the pick in one line at the top of the audit with its reason, then move on. Do not ask the user. If the pick is wrong they will say so, and re-running is cheaper than a question.

**Default heuristic:**

1. A stated target role wins over history. Someone with an IC history targeting a management role is scored on the leadership track, and the resulting gap is the audit's main finding, not a scoring error.
2. No stated target: use the most recent role. Bullets mostly about systems, code, and architecture point to IC. Bullets mostly about people, delivery, and structure point to leadership.
3. Still split: follow where the candidate spent the most recent two years, not where they spent the most years overall.

**Ambiguous cases, with rules:**

- **Tech lead.** IC track. Apply the leadership calibrations of dimensions 3 and 6 as a secondary lens. Tech leads are hired on technical depth first, and leadership evidence is the differentiator on top, not the basis.
- **Staff-plus IC.** IC track, always, regardless of how much influence work appears. Scope signalling calibrates to org-wide reach rather than headcount: do not ask for team size, ask how many teams a decision moved.
- **Player-coach.** Leadership track if the target role includes any performance management or hiring. Otherwise IC. Rationale: the manager parts of the job are exactly the parts a reader cannot infer from technical bullets, so they need the leadership bar applied.
- **Manager returning to IC.** IC track. Count the management history as scope evidence, but hold the CV to the IC bar for recent, specific technical work. The classic failure is a manager's CV applying for an engineer's job, and naming that is the point of the audit.
- **Founder or solo operator.** Whichever track the target role names. These CVs fail both bars the same way, by choosing breadth over depth, and the fix is to cut everything the target role does not need.
- **Genuinely dual target.** Pick the track for the role the candidate named first, note the other track in one line, and produce one audit. Two parallel audits halve the attention each gets and neither ships.

**Terminal tiebreaker.** If the default heuristic and every case above leave the pick genuinely even, take the leadership track. Rationale: the leadership bar asks for evidence the IC bar does not (scope, headcount, mechanism), so a leadership audit surfaces the IC gaps as well, while the reverse silently drops them. State that the tie was broken this way, in the same line that announces the track, so the user can redirect in one word.

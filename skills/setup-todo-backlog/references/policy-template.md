# TODO Backlog Policy Template

Inject the section below into the project's agent instructions file (AGENTS.md or CLAUDE.md).
Copy it verbatim, with one substitution: replace the `{{PROJECT_TRIGGERS}}` line with the
project-specific triggers gathered during setup. If the project keeps its backlog somewhere
other than `docs/TODO.md`, substitute the chosen path everywhere before injecting.

---

## TODO / Known issues

`docs/TODO.md` is the backlog of known weaknesses. It exists so a defect found mid-task outlives
the session that found it. Maintain it from both ends: propose an entry when you notice a weakness,
close one when you fix it. Skipping the closing half is worse than skipping the opening half,
because a stale entry gets trusted.

### When to create an entry

Note it the moment you notice it and keep working. Do not write it to `docs/TODO.md` — no entry is
filed without the user's approval, per **Approval gate** below. Mid-task counts. So does a defect
you will never fix yourself, and one nowhere near what you were asked to do.

- A bug or limitation you found and are not fixing now.
- A workaround chosen over the real fix.
- A fix skipped because it needs something you do not have: access, data, a migration, a release
  window, a decision from someone else.
- The same rule or value implemented in two places.
- A requirement you guessed at, where the guess is written down nowhere.
- Behavior documented in one place but not in another a reader would check.

{{PROJECT_TRIGGERS}}

### When NOT to create an entry

- You fixed it in this session. Fix beats file.
- An existing entry already covers it. Strengthen that entry with the new evidence instead of
  opening a competing one.
- Style, naming, or formatting preference.
- A speculative worry with no evidence behind it.

When in doubt, skip the noise. Never skip a defect a reader can actually hit.

### Approval gate

An agent never files a backlog entry on its own. The backlog is the user's record of what is wrong
with their project, so the user decides what goes in it.

- **Collect, do not write.** A trigger firing mid-task means note the candidate and carry on.
  Nothing touches `docs/TODO.md` until the sweep, so a trigger never interrupts the work in flight.
- **Present the full draft, not a summary.** Show every candidate exactly as it would be written:
  the `## TODO-YYYY-MM-DD-slug: <claim>` heading, the status line, and every bullet. "Found a flaky
  test, file it?" is not a draft. Nobody can approve wording they have not seen.
- **One decision per candidate.** Three candidates get three answers, not one blanket yes. They are
  independent findings, and the user may want one in the backlog and the other two forgotten.
- **Write only what was approved**, verbatim or with the edits the user asked for. A declined
  candidate is never written, never softened into a code comment or a note somewhere else, and never
  re-proposed later in the same session. A decline is a decision, not a delay.
- **Report the declines.** Say what you proposed and what the user turned down, so the finding
  survives in the session transcript even though it never reached the backlog.
- **Closing is not gated.** Moving a resolved entry to `## Resolved` needs evidence, not approval.
  Closing retires a claim the user is already carrying, so the evidence rule is the check that
  matters there. Never conflate the two halves: creating asks, closing proves.

**The one exception, and it is narrow.** When a top-level session has no interactive channel at
all — a headless run, a scheduled or cron job — there is nobody to ask, and a lost finding is
worse than an entry the user deletes later. File it, and make this its last bullet, verbatim:

`- _Filed without approval in an unattended session._`

The marker is a bullet, not a status. The vocabulary stays `open`, `decided, deferred`, and
`resolved YYYY-MM-DD`.

**A subagent never files an entry.** It returns its candidates to whoever spawned it, and the
parent session runs the sweep, because the parent holds the user channel. Only a top-level session
decides whether a channel exists. A subagent having no way to reach the user says nothing about
whether the user is reachable, because the parent can ask.

The exception is about capability, not convenience. It does NOT fire because the user seems busy,
because asking would break the flow, because the session has run long, because you are running as
a subagent, because the finding is obviously worth filing, or because the user is slow to reply. If
a question can reach the user at all, ask it.

### Backlog sweep before you finish

Run this on every substantive session, read-only investigation included. Both halves are
mandatory.

- **Propose what you found.** Draft every candidate from the triggers above and present it per the
  **Approval gate**. File the approved ones. Drop the declined ones.
- **Close what you solved.** Re-read `docs/TODO.md` and ask of every open entry whether this
  session resolved it. A session that fixes something rarely remembers an entry described it,
  which is how a backlog rots into a list of work already done.
- Close only on evidence. Point at what proves it no longer reproduces: a test, a command's
  output, a code path that now exists. Never close on "looks fixed".
- Partial resolution is not resolution. Leave the entry open and narrow its problem statement to
  what remains.
- A change that makes an entry moot also closes it. Say which it was, fixed or obsolete.
- Say one line either way: what you proposed, what the user approved and you filed, what was
  declined, what you closed, or that none of it happened. Never skip this silently.

### How an entry is closed

Resolved entries are never deleted. The entry is the record that the defect existed.

- Move it to the `## Resolved` section at the bottom of `docs/TODO.md`, keeping its id.
- Replace the status line with exactly `**Status:** resolved YYYY-MM-DD` — no trailing period, no
  appended sentence. The status line stays machine-readable.
- Put what landed in the first bullet under it, not on the status line.
- Collapse the body to the problem and what fixed it. Drop the evidence and the traps.
- References from other entries keep working, because ids are stable and the heading moves with
  the entry.

### How to write one

- **One home.** `docs/TODO.md` is the only list of known issues. Never copy an entry into
  `README.md` or anywhere else. A second copy is a hand-maintained sync that loses, and the
  reader who finds the stale one trusts it.
- **Bullets, not prose.** A status line, then bullets. No `###` subsections, no tables, no
  paragraphs. Aim for 5-8 bullets. Past roughly 12 it is a plan, not a backlog entry.
- **Shorten the wording, never drop a number.** An entry nobody can defend with evidence is not
  worth keeping. Evidence is the last thing to cut, not the first.
- **Content** is the problem, the evidence, the decisions already locked, and the traps. Not the
  implementation. No line numbers, no function names, no code excerpts, because those rot and
  mislead the session that trusts them.
- **Ids.** `## TODO-YYYY-MM-DD-slug: <declarative claim>`, using the date the entry was filed
  and a 2-5 word kebab-case slug. Ids are immutable and never reused. Cross-reference other
  entries by id, never by position. "The entry above" breaks as soon as an entry is inserted or
  resolved.
- **Status is a closed vocabulary**: `open`, `decided, deferred`, `resolved YYYY-MM-DD`. The
  qualifier after the comma is free text. The states are not.

### Read the backlog before you plan

Before planning work in an area, read `docs/TODO.md` for entries touching it. A plan that trips
over a known limitation without acknowledging it is a bug.

---

**Note for skill user**: Replace the `{{PROJECT_TRIGGERS}}` line with 2-4 bullets naming the
weaknesses this codebase actually produces, written in the same voice as the six generic
triggers above. If the project has none worth naming, delete the line rather than leaving the
placeholder. If the backlog file is not `docs/TODO.md`, substitute the chosen path in every
reference above, including the `## Resolved` section pointer.

# TODO Backlog Policy Template

Inject the section below into the project's agent instructions file (AGENTS.md or CLAUDE.md).
Copy it verbatim. If the project keeps its backlog somewhere other than `docs/TODO.md`,
substitute the chosen path everywhere before injecting.

---

## TODO / Known issues

`docs/TODO.md` is the backlog of known weaknesses. It exists so a defect found mid-task outlives
the session that found it, when the user decides to keep it. An entry is filed only when the user
asks for one. An entry is closed as soon as the evidence shows the defect is gone. Filing waits for
a request. Closing waits for nothing. A stale entry gets trusted, so closing is the half you must
never skip.

### File an entry only when asked

Never raise the backlog yourself. The user asks for an entry, or no entry exists. The backlog is
the user's record of what is wrong with their project, so the user decides what enters it and when.

These are forbidden, at every point in a session:

- Offering to file an entry.
- Suggesting that something belongs in the backlog.
- Drafting a candidate entry, in the backlog file or anywhere else.
- Asking whether to file something, in any wording.
- Framing a finding as a backlog candidate, or collecting findings into a queue to triage.

A defect you found and did not fix is still stated. Put it in your ordinary session report, as a
plain finding in the same voice as any other observation about the work: what is wrong, what proves
it, and what you did instead. No id, no heading, no status line, no question attached. The user
reads it and decides, unprompted, whether it becomes a todo. When the user asks for an entry, write
it in the format below.

Closing works the other way, and it is not gated on a request. Moving a resolved entry to
`## Resolved` needs evidence, not permission. Closing retires a claim the user is already carrying,
so the evidence rule is the check that matters there. Never conflate the two halves: filing waits
to be asked, closing proves.

### What does not belong

When the user asks for an entry, write it. Push back once, in one line, and only when one of these
is true:

- You fixed it in this session. Fix beats file.
- An existing entry already covers it. The new evidence belongs in that entry, not in a competing
  one.
- It is a style, naming, or formatting preference.
- It is a speculative worry with no evidence behind it.
- **It is a decision, not a defect** — one you or the user just took deliberately. A decision
  belongs where decisions live: an ADR, a code comment, the PR body. An entry implies unfinished
  work, and a decision is finished work. A `decided, deferred` status on something nobody intends
  to revisit is the tell.
- **Its own body has to explain why nobody will act on it** — an architectural constraint, a
  permanent trade-off, a fix ruled out on purpose. That is a design property, not a defect.
  Document it at the code and stop.
- **A code comment and a test already record it.** A third copy is the drift the one-home rule
  exists to prevent, and the backlog is the copy that goes stale first.

The test that catches the last three: **would somebody pick this up and do it?** If the entry has to
argue that nobody will, it is not a backlog entry.

Then honor the answer. The user's call is final, and a second objection is noise.

### Backlog sweep before you finish

Run this on every substantive session, read-only investigation included. The sweep closes entries.
It never opens one, and it never proposes one.

- **Close what you solved.** Re-read `docs/TODO.md` and ask of every open entry whether this
  session resolved it. A session that fixes something rarely remembers an entry described it,
  which is how a backlog rots into a list of work already done.
- Close only on evidence. Point at what proves it no longer reproduces: a test, a command's
  output, a code path that now exists. Never close on "looks fixed".
- Partial resolution is not resolution. Leave the entry open and narrow its problem statement to
  what remains.
- A change that makes an entry moot also closes it. Say which it was, fixed or obsolete.
- Say one line either way: which entries you closed, or that you closed none. Never skip this
  silently.

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
  paragraphs. Aim for 5-8 bullets, hard cap 120 words total. Past roughly 12 it is a plan, not a
  backlog entry.
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

**Note for skill user**: If the backlog file is not `docs/TODO.md`, substitute the chosen path in
every reference above, including the `## Resolved` section pointer.

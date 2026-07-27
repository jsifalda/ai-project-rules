---
name: setup-todo-backlog
disable-model-invocation: true
description: Bootstrap a known-issues backlog in any project. Creates docs/TODO.md from a template, offers to convert an existing flat checklist or id-bearing TODO list into dated immutable ids, and injects a file-it-when-you-find-it policy into AGENTS.md or CLAUDE.md. Use when setting up a TODO backlog, adding known-issues tracking, scaffolding a defect or tech-debt list, initializing deferred-work tracking, or the user mentions "setup todo backlog". Do NOT use to file or resolve one specific backlog entry (just edit the backlog), to set up changelogs, ADRs, or PRDs, or to manage sprint tickets, roadmap items, or feature requests.
---

# Setup TODO Backlog

Set up a known-issues backlog in any project. Every weakness found mid-task gets a dated,
immutable id in `docs/TODO.md`, and a policy in the agent-instructions file makes future
sessions maintain it from both ends. Open an entry when you notice a defect, close it when you
fix it. The point is that a defect outlives the session that found it.

## When to use

- User asks to "set up a TODO backlog", "add known-issues tracking", or "scaffold a tech-debt list"
- User wants the backlog pattern (dated ids + policy + end-of-session sweep) replicated in a new repo
- User mentions "setup todo backlog" or "initialize the known-issues list"
- A setup or bootstrap flow delegates backlog provisioning to this skill

## Workflow

### Step 1: Assess current state

Check the project for:

1. **An existing backlog file.** Look for `docs/TODO.md`, `TODO.md` at root, a `docs/todo/`
   directory, and `TODOS.md`. Reuse the first one found. Otherwise default to `docs/TODO.md`.
2. **The shape of any existing backlog.** Classify it as one of three:
   - **Flat checklist**, lines like `- [ ] do thing` or `* TODO: thing`.
   - **Id-bearing entries**, headings or lines carrying a handle such as `TODO-01` or `#12`.
   - **Freeform prose**, neither of the above.
   Only the first two convert cleanly in Step 3. For freeform prose, tell the user what you
   found and ask how they want it handled before touching anything.
3. **The agent-instructions file.** First match wins, root files first so a project that already
   uses `CLAUDE.md` is honored:
   1. `AGENTS.md` at project root
   2. `CLAUDE.md` at project root
   3. `.claude/CLAUDE.md`

### Step 2: Create the backlog file

If no backlog exists, copy `assets/todo-template.md` to `docs/TODO.md`.

```bash
mkdir -p docs
```

The template carries the shape rules, one worked example, and an empty `## Resolved` section.
Tell the user the example entry is there to be deleted or overwritten by their first real entry.

**If a backlog already exists, do not overwrite it.** Skip to Step 3.

### Step 3: Convert an existing backlog

Offer the conversion. Explain what it buys: dated ids that never collide across parallel
branches, and a stable handle other entries can reference. Then honor the answer.

**Decline path.** If the user declines, keep the repo's existing scheme exactly as it is.
Inject the policy only, and adjust the id and status wording in the injected `### How to write
one` subsection to describe the scheme the repo actually uses. Say so explicitly in the final
report, so nobody later assumes the ids are dated when they are not.

**Accept path.** Mirror this order, and do not deviate from it. Build the whole old-to-new
mapping first, apply renames and reference rewrites together, then verify.

1. **Choose the search text, then quote it safely.** One choice per item drives both the dating
   and the reference rewriting, so settle it before running anything.
   - **Flat checklist**: the item's prose with the marker stripped. Drop `- [ ]`, `- [x]`, or
     `* TODO:` and search only the words that follow. Keeping the marker dates the checkbox flip
     instead of the item.
   - **Id-bearing entries**: the heading line only, for example `## TODO-01:`. Never the status
     line, never a body bullet. `**Status:** open` is near-identical across entries, so it matches
     every entry at once and hands one item the dates of all the others.
   - Assign that text to a shell variable and pass the variable double-quoted. Never paste the
     text into the command.

   ```bash
   file='docs/TODO.md'
   line='Improve error messages in CLI validator (don'\''t swallow exceptions)'
   git log -S"$line" --format=%ad --date=short --reverse -- "$file"
   ```

   An apostrophe in the text breaks a literal `-S'<text>'`. The shell raises a parse error, and in
   a multi-statement script the unterminated quote swallows the commands that follow, so the
   damage reads like a search that simply found nothing. Escape an apostrophe as `'\''` inside the
   single quotes. When the text carries both quote characters, assign it with a quoted heredoc.
2. **Derive a date for every item.** Take the earliest date the evidence supports.
   - **Per-line, preferred.** The first line of the search above. That is the commit that
     introduced the item under its current wording.
   - **Hunt earlier wordings.** Run `git log -p -- "$file"` and read the removed lines. A reworded
     item reports the day it was reworded, not the day it was filed. Re-run the search on every
     earlier wording you find and keep the earliest date across all of them.
   - **File-level fallback, only with proof.** When the search returns nothing, read the file as
     it stood in the commit that added it.

     ```bash
     first=$(git log --diff-filter=A --format=%H --reverse -- "$file" | head -1)
     git show "$first:$file" | grep -qF -- "$line"
     ```

     A match means the item was there from the start, so the file's creation date is real evidence
     for it. No match means that date says nothing about this item, so it is not evidence and you
     may not use it.
   - **Otherwise ask the user for the date.** An untracked item, a file with no history, and a
     failed proof all land here. Never guess and never substitute today's date silently.
   - **A checked item carries two dates.** The id date is the day the item was filed, found by
     searching the prose, because an id records when the problem was written down and a resolved
     entry has to sort beside the open entries filed alongside it. The `resolved YYYY-MM-DD` on
     the status line is the day the box was checked, found by searching `- [x] ` plus the prose.
     Ask the user when that second search returns nothing.
3. **Build the mapping.** One row per item: old handle or original line, new id, derived date,
   derived slug, target section. Show it to the user before writing anything.
   - **Flat checklist**, unchecked (`- [ ]`): the item becomes a thin entry. Heading
     `## TODO-YYYY-MM-DD-slug: <declarative claim>`, then `**Status:** open`, then the item's
     prose as its first bullet. Carry over the words, not the markup. Strip the `- [ ]` or
     `* TODO:` marker so the bullet reads `- Fix the flaky login test` and never
     `- - [ ] Fix the flaky login test`. Do not invent evidence or decisions that were never
     written down.
   - **Flat checklist**, already checked (`- [x]`): the item goes straight into `## Resolved`
     with `**Status:** resolved <check date>` and the same marker-stripped prose as its bullet.
   - **Id-bearing entries**: keep the body, rename the heading to the new dated id, and record
     the old handle so its inbound references can be rewritten.
   - Slugs are 2-5 words, kebab-case, derived from the claim. Two items on the same date need
     different slugs, because the date plus slug is the identity.
4. **Apply renames and rewrites together.** Write the converted entries, then rewrite every
   inbound reference **across the whole repo**, not just the backlog file. Search source comments,
   docs, the agent-instructions file, and any planning files.
   - **Id-bearing items: rewrite on a word boundary.** A plain substring replace corrupts any
     handle the old one is a prefix of. Replacing `TODO-01` blindly rewrites an unrelated
     `TODO-010` into `TODO-2026-03-14-slug0`. Demand that the old handle sits between boundaries,
     with no digit or letter immediately before or after it.

     ```bash
     perl -pi -e "s/\\b\Q$old\E(?![0-9A-Za-z])/$new/g" "$f"
     ```

   - **Flat items: rewrite the prose references too.** A flat item has no old handle, so the rule
     above never fires and the loose text quotes in docs and comments stay orphaned. Search the
     repo for the same text you dated the item with, earlier wordings included, and edit each hit
     to name the new id. A comment reading `see "Fix the flaky login test" in TODO.md` becomes
     `see TODO-2026-03-14-flaky-login-test in TODO.md`. Skip this and the conversion buys the repo
     nothing outside the backlog file.
5. **Verify. Two checks, both required.**
   - **(a) Every mapped old handle is gone.** Search the repo for each one under the same boundary
     rule the rewrite used, and expect zero hits. A plain substring search passes over a corrupted
     near-miss, because the corrupted text no longer contains the old handle.
   - **(b) No unmapped handle survives.** Search the repo for the backlog's whole id pattern, not
     only the handles in the mapping. Match whole tokens so a new dated id matches as itself and
     cancels cleanly in the subtraction below. A prefix-length pattern such as `TODO-[0-9]+` would
     hit the `TODO-2026` head of every new id and drown the result.

     ```bash
     grep -rhoE 'TODO-[0-9A-Za-z-]+' --exclude-dir=.git . | sort -u | comm -23 - new-ids.txt
     ```

     Everything that survives the subtraction is a reference the conversion cannot account for,
     either a handle the backlog never carried or an unrelated string that merely looks like one.
     Report each one with its file and line and let the user triage it. Never leave one silently.
     This check applies to an id-bearing conversion only, because a flat checklist has no id
     pattern to search.
   - Report the number of entries converted, split into open and resolved.

### Step 4: Inject the policy

Read the full policy from [references/policy-template.md](references/policy-template.md). Do not
paraphrase it. Copy the section between the horizontal rules.

**Target file**, first match wins, using the order from Step 1. If a target exists, append the
`## TODO / Known issues` section to it. If **none** exist, create `AGENTS.md` at root with the
policy, because `AGENTS.md` is the cross-tool canonical file.

**Keep `AGENTS.md` and `CLAUDE.md` resolving to one file.** After choosing or creating the
target, **if `AGENTS.md` is the real policy file at root AND no `CLAUDE.md` exists at root**,
create a relative symlink at the project root so Claude Code, which reads `CLAUDE.md`, sees the
same file:

```bash
ln -s AGENTS.md CLAUDE.md   # run at project root
```

That one condition covers both cases that need it, the none-existed case where you just created
`AGENTS.md`, and the `AGENTS.md`-only case. Guards:

- Only when **no `CLAUDE.md` exists**. Never overwrite a real `CLAUDE.md`, or any existing file,
  with a symlink.
- If a real `CLAUDE.md` exists **separately** from `AGENTS.md`, inject into `AGENTS.md`, leave
  both files as they are, and tell the user `CLAUDE.md` is a separate file they may want to
  reconcile.
- If the project uses `CLAUDE.md` or `.claude/CLAUDE.md` and has **no `AGENTS.md`**, just inject
  there. Do NOT introduce `AGENTS.md` or a symlink.
- If `CLAUDE.md` is already a symlink to `AGENTS.md`, they are the same file. Inject once into
  `AGENTS.md`.
- Symlinks need `core.symlinks=true` on Windows checkouts. macOS and Linux work out of the box.

**Before injecting**: if a `## TODO / Known issues` section already exists in the target, ask the
user whether to replace or skip. Never clobber it silently.

**If the backlog path is not `docs/TODO.md`**, substitute the chosen path everywhere in the
policy before injecting, including the pointer to the `## Resolved` section.

Leave the `{{PROJECT_TRIGGERS}}` line in place for now. Step 5 resolves it.

### Step 5: Gather project-specific triggers

The policy lists six generic triggers, then a `{{PROJECT_TRIGGERS}}` placeholder. Ask the user
for 2-4 triggers specific to this codebase, written in the same voice as the generic ones. Each
should name a weakness this codebase actually produces, not a generic virtue. Offer candidates
drawn from what you saw in the repo, so the user has something to react to rather than a blank
question.

Replace the placeholder line with those bullets. **If the user has none, delete the
`{{PROJECT_TRIGGERS}}` line.** Never leave the raw placeholder text in a shipped file.

### Step 6: Verify

Confirm to the user:

- Backlog file created or reused, with its path
- Conversion done, with the count of entries converted, or declined, or not applicable
- Policy injected into `[target file]`
- `CLAUDE.md` to `AGENTS.md` symlink created, if applicable
- Project-specific triggers added, with how many, or skipped and the placeholder removed

## Entry format (quick reference)

Full rules live in the policy template. The short version:

**Id**: `## TODO-YYYY-MM-DD-slug: <declarative claim>`, using the date the entry was filed and a
2-5 word kebab-case slug. The heading is the id. Ids are immutable and never reused.
Cross-reference other entries by id, never by position.

**Status**: a closed vocabulary of three, on its own line under the heading.

- `**Status:** open`
- `**Status:** decided, deferred` (the qualifier after the comma is free text)
- `**Status:** resolved YYYY-MM-DD`

**Body**: bullets under the status line. No subsections, no tables, no prose paragraphs. Aim for
5-8 bullets, and past roughly 12 it is a plan rather than a backlog entry. Content is the
problem, the evidence, the decisions already locked, and the traps. Not the implementation, so
no line numbers, no function names, no code excerpts, because those rot and mislead.

**Closing**: move the entry to `## Resolved` at the bottom of the same file, keep the id, swap
the status line, and collapse the body to the problem plus what fixed it.

## Rules

- **One home.** The backlog file is the only list of known issues. Never copy an entry into
  `README.md` or anywhere else. A second copy is a hand-maintained sync that loses, and the
  reader who finds the stale one trusts it.
- **Ids are immutable and never reused.** They are the handle other entries reference. Renaming
  one breaks inbound references silently.
- **Resolved entries move to `## Resolved`, never get deleted.** The entry is the record that the
  defect existed.
- **Entries are bullets under a status line.** Never subsections, never tables, never prose.
- **Conversion is offer-then-honor-decline.** Never force a repo off its existing scheme. On a
  decline, inject the policy and adapt its id wording to what the repo uses.
- **Never clobber an existing `## TODO / Known issues` policy section.** Always ask first.
- **Never overwrite an existing backlog file.** Convert it or leave it, do not replace it.
- **Dates come from git or from the user.** Never guess a date, and never quietly stamp today
  onto an item that predates today. Git counts as evidence only for the item being dated. The
  file's own creation date proves nothing about an item that was absent from its first commit,
  and a search on the current wording proves nothing about an item that was reworded.
- **Handles are rewritten on a word boundary.** A substring replace corrupts every longer handle
  the old one prefixes, and the corrupted text then hides from any search for the old handle.
- **Conversion reports what it cannot account for.** Any handle-shaped string the mapping does not
  explain goes to the user with its file and line. Never leave one silently.
- **Idempotent on re-run.** Re-running finds the backlog, finds the policy section, and asks
  before changing either. A second run must not duplicate the policy or reset the backlog.
- **Never ship the `{{PROJECT_TRIGGERS}}` placeholder.** Fill it or delete the line.

## References

- [policy-template.md](references/policy-template.md) is the full `## TODO / Known issues` policy
  to inject into `AGENTS.md` or `CLAUDE.md`, including the `{{PROJECT_TRIGGERS}}` placeholder

## Assets

- `assets/todo-template.md` is copied into the project as `docs/TODO.md`. It holds the shape
  rules, one worked example to delete or overwrite, and an empty `## Resolved` section

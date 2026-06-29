# indie-hacker-wrapup remembers angles across sessions

- Added a persistent ledger at `~/.claude/indie-hacker-wrapup/suggested-angles.md` that the skill loads (new Step 0) and appends to the moment it shows a shortlist (Step 2).
- On later runs it dedups candidates against the ledger — clear repeats drop silently, borderline ones surface with a "you covered this on DATE" flag — so it stops pitching the same X angle session after session.
- Recording happens at shortlist time, not after drafting, so an angle is remembered even when the user walks away without picking one.
- Why: the skill only saw the current conversation, so it kept resurfacing the same ideas across sessions.

# Add setup-todo-backlog skill for known-issues backlog provisioning

- Added new skill `setup-todo-backlog` at `~/instructions/skills/setup-todo-backlog/` with SKILL.md, references/policy-template.md, and assets/todo-template.md. It provisions a known-issues backlog into any repo: a `docs/TODO.md` with dated immutable ids, plus a policy injected into the agent-instructions file.
- The policy carries a two-way end-of-session sweep: file the weaknesses you found, close the entries you solved. Closing requires evidence the defect no longer reproduces.
- Wired the skill into `setup-aiengineering` as an opt-in delegated module (default off, like the PRD gate): Modules table, Step 4 menu, Step 6 delegate list, Step 8 report, Rules, References.
- Added gate 8 (Backlog sweep) to `references/verification-protocol.md`. It overrides the markdown-only exemption and is omitted entirely when the backlog module is not selected. Being last, omitting it renumbers nothing.
- Bumped `references/baseline-checklist.md` to v6 with two new rows, so every repo stamped v5 gets offered the backlog on its next re-run.

**Why:** The pattern came from one repo where it caught real defects, but it lived in that repo's CLAUDE.md and was written entirely in that project's domain language. Nothing was reusable. Ids are date-prefixed (`TODO-YYYY-MM-DD-slug`) rather than sequential, matching what `setup-adrs` already does. Sequential ids collide when two sessions run against the same tree.

**Notable:** An adversarial dry-run against synthetic git fixtures found seven defects in the conversion algorithm before it shipped. The worst two produced confident silent wrong answers: the "ask the user for a date" branch was unreachable dead code because the file-level fallback always succeeded, and the verify step returned a clean PASS over both a corrupted reference and a dangling one. All seven were fixed and re-verified against the fixtures.

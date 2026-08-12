# TODO / Known issues

The single list of known weaknesses and deferred work for this project.

- **This is the only list.** Never copy an entry into `README.md` or anywhere else. One home, no sync.
- **When an entry is filed, and when one is closed, live in the project's agent instructions** (`AGENTS.md` or `CLAUDE.md`), under `## TODO / Known issues`. That file owns those rules and the closing sweep. This file owns the shape.
- **Shape.** Status line, then bullets. No subsections, no tables, no prose paragraphs. Aim for 5-8 bullets. Past roughly 12 it is a plan, not a backlog entry.
- **Content.** The problem, the evidence, the decisions already locked, the traps. Not the implementation. No line numbers, no function names, no code excerpts, because those rot.
- **Ids.** `## TODO-YYYY-MM-DD-slug: <claim>`, using the date filed and a 2-5 word kebab-case slug. Immutable, never reused. Cross-reference by id, never by position.
- **Status.** One of `open`, `decided, deferred`, `resolved YYYY-MM-DD`. The qualifier after the comma is free text. The states are not.
- **Filing.** An entry is filed only when the user asks for one. An agent never files, offers, or drafts one unprompted. Closing an entry needs evidence, not a request.

---

Example only. Delete before use, or copy the shape below for the first real entry.

## TODO-2026-01-15-pin-old-dependency: A core dependency is pinned to an old major version

**Status:** decided, deferred

- The build pins a dependency below its current major release, because that release breaks a feature this project relies on.
- Evidence: the version pin and a comment linking the upstream issue sit next to each other in the dependency manifest.
- Decision: stay pinned until the upstream issue closes, then upgrade in one step rather than patch around the break locally.
- Trap: a second dependency wants the newer major too. Bumping only one of them will reintroduce the break.
- Recheck the upstream issue on every backlog sweep that touches this area.

## Resolved

Entries move here once fixed. Keep the id and the original problem statement, collapse the body to what fixed it. Never delete, never renumber.

_Nothing yet._

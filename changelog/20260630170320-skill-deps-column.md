# Declare skill dependencies in the README Skills table

- Added a `Depends on` column to the `## Skills` table in `README.md` — every row now states which other repo skills it invokes/requires, or `—` for none.
- Backfilled the 6 real dependency edges: `better-plan`→`grill-me`,`op`; `indie-hacker-wrapup`→`write-like-human`; `landing-page-gap-analyzer`→`defuddle`; `rewrite`→`write-like-human`; `setup-aiengineering`→`setup-adrs`,`setup-changelog`,`setup-user-scenarios`; `team-ship`→`team-code-writer`,`team-tester`,`team-reviewer`.
- Made the rule unskippable: documented the mandatory column in three authoring touchpoints — README table intro, README Contributing add-a-skill bullet, and the repo CLAUDE.md Conventions bullet — plus a pointer from `create-skill`'s "Referencing Other Skills" gate.
- Why: cross-skill coupling was invisible. Renaming or removing a depended-on skill could break a consumer silently. A visible, always-filled column surfaces the coupling for any reader.
- Dependency is defined as runtime invoke/require only. Disambiguation pointers ("use X instead") and sync-provenance are not dependencies.

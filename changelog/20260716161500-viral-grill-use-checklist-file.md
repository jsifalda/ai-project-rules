# landing-page-viral-grill audits against a checklist file

- Replaced the skill's invented 28-criterion rubric with a checklist file it reads at run time. Deleted the rubric.
- The checklist file is now the only source of criteria. The skill parses every bullet in file order, adds nothing, merges nothing, skips nothing.
- Check IDs derive from position rather than being hand-written, so the file stays the single source of truth.
- Rewrote the report template to be checklist-driven. It hardcodes no checks of its own and works with any list of `## ` sections and `- ` bullets.
- Added `checklist_path` as an optional input so a project can audit against its own list.
- Stripped personal vault frontmatter (wikilinks to private notes) from the bundled checklist and moved attribution to a visible credit line with a source link.
- Why: the skill was answering a question nobody asked. Grading against criteria the agent invented is not an audit, it is an opinion. The checklist decides what counts.
- No new dependencies.

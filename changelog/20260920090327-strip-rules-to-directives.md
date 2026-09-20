# Strip the rule files to directives

- Rewrote `authoring.md`, `browser.md`, `git-ship.md`, `testing.md` and `docs-diagrams.md` as
  one line per rule. Removed every prose paragraph, section intro, rationale and worked example.
- Why: the previous change moved content out of the always-loaded layer and then wrote it
  longer than it was. `browser.md` came out 2.6x its source, `git-ship.md` 2.1x. The split was
  right, the compression never happened.
- `authoring.md` gains a `## Move` section. Both failures were the same move: treating a
  relocation as licence to re-explain the rule. It now says carry the directive, drop the
  explanation, and make the new file smaller than the text it replaces.
- `authoring.md` also states that it binds on-demand files, not only always-loaded ones. That
  scope gap is what let the rule files grow unchecked.
- The counts rule and the always-loaded test lost their duplicate statements inside the same
  file.
- Review caught the strip going too far in places. Restored as clauses, not new prose: the whole
  `## Counts` section in `authoring.md` (two files pointed at it), the ban on deleting a
  tautological test, the `go test -p` trap, the never-the-bare-form git-common-dir key, the
  Vitest v3 config-over-CLI note, modern-timers-only, and the rule that a commit body and an
  MR body follow the writing style.
- `git-ship.md` destructive rules read as absolute while an approval path sat below them. They
  now say "without an explicit chat instruction, never", matching the source.
- `CLAUDE.shared.md` no longer bans naming another skill outright. The absolute ban contradicted
  a documented relative-skill pattern; it is back to confirm-each-reference, default deny.

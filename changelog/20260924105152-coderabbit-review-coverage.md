# CodeRabbit lens now reviews untracked files and checks coverage

- The CodeRabbit CLI lens runs with `--include-untracked`, so new files are no longer skipped from review.
- Before the run, list the untracked files, because `--include-untracked` uploads every one that is not gitignored. Gitignore or move anything that must not leave the machine.
- Added a coverage check that compares the `complete` event's `reviewedFiles` against the files actually shipped, and labels the lens `partial (missed: <files>)` when one is missing, instead of reporting a clean pass.
- Added a re-review step for any file added or changed after the lenses ran, so it does not ship unreviewed. Late files get CodeRabbit plus the harness-native lens, with triage limited to those files. Template exemption: a file whose only post-lens change is a triaged fix, or a file a later gate of the protocol writes (docs, scenarios, backlog, changelog).
- This repo's `CLAUDE.md` gets the same coverage check (Step 2) and re-review (Step 5). Its exemption is narrower: a file whose only post-lens change is a Step 4 fix, or the Step 6 changelog entry. The re-run counts against the budget, and a spent budget means asking first.
- The Merge gate now treats a `partial` lens as done too, alongside `skipped` and `n/a`.
- Bumped the skill baseline to v17.
- Why: `cr review --agent --base <default>` skips untracked files, so new files were never reviewed. Agents also treated a partial `reviewedFiles` list as a clean pass, and files edited after the lenses ran were never reviewed. A local review reported 0 findings on a change whose new files it never saw, while the server review found 2.
- CLAUDE.md prompt-audit cleanup — duplicate conventional-commits line and changelog-incident paragraph dropped, pressure caps lowercased.

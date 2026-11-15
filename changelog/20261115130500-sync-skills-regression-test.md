# Regression test for the skills sync hook

- Added `skills/setup-skills-autorefresh/tests/run_tests.sh`. It runs `sync-skills.js` on temp dirs with an absolute `CLAUDE_CONFIG_DIR`.
- It checks that a `commands/` link into `<source>-backup` stays, a link into `<source>/x` goes, and skills land in `<CLAUDE_CONFIG_DIR>/skills`.
- Why: the separator match in the legacy command migration is a bug fix, and a later edit could bring the old prefix match back.

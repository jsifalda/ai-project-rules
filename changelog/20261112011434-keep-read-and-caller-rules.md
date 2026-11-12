# Keep the READING FILES rules as they are

- Dropped the proposed "Never `cat` or `sed` a file you will `Edit`." sentence from `rules/general.md`.
- Why: it fails the always-loaded test in `rules/authoring.md`. One `Read` call recovers the error, and the `Edit` tool already refuses a file that `Read` did not read. It also brought back part of the ban that `20261005175909-drop-bash-read-ban` removed.
- Restored the original caller rule. The rewrite widened its scope to read every call site before every function edit, and that change was not related to the fix.
- Net result: `rules/general.md` is unchanged.

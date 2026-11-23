# Merge the READING FILES read and edit lines

- Merged the two `Read` lines in `rules/general.md` `# READING FILES` into one line, and named `Edit` as the tool to change a file
- Why: three sessions used `sed` to read or edit a file, and permission checks denied each call
- Dropped the `sed` ban that the first commit of this change added. It fails the always-loaded test in `rules/authoring.md`: the permission check already enforces it, and each denial recovered with one retry. `20261005175909-drop-bash-read-ban` and `20261112011434-keep-read-and-caller-rules` made the same call

# Add the investigate skill

- Added `/investigate`, a slash-only read-only mode. It verifies each finding with a command, changes nothing, and reports the answer first with evidence.
- It blocks Edit, Write and NotebookEdit through the `disallowed-tools` frontmatter key. An e2e probe confirmed the block.
- Let `quick_validate.py` and `create-skill` accept `disallowed-tools`.
- Fixed in `create-skill`: the YAML colon claim, a typo, and one dated coaching line removed.
- Why: replace a phrase typed by hand with a versioned, enforced mode.

# Version every skill in its frontmatter

- Added `metadata.version: "1.0"` to every skill, and `metadata.upstream` to every skill vendored from another repo.
- Added an opt-in `--require-version` flag to `quick_validate.py`. The pre-commit hook passes it for every skill not listed in the new `scripts/synced-skills.txt`.
- `init_skill.py` now emits the version block. `create-skill`, `CLAUDE.md` and `README.md` document the bump rule.
- Fixed the `code-review-nuclear` README Origin cell, which named no upstream.
- Applied prompt-audit fixes: `create-skill` gains a negative trigger, conditional packaging, an outline-order rule and plain emphasis; `CLAUDE.md` drops its `## Key Rules` block, a drifted copy of `rules/general.md`.
- Why: a version makes a skill's changes traceable for every consumer, and the validator keeps new and edited skills from dropping it.

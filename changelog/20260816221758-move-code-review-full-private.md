# Move code-review-full to a private tree

- Moved the `code-review-full` skill out to a private, local-only tree that has no git remote. Removed it from this repo and from the README table.
- Why: the skill needs employer-specific detail — an Atlassian tenant id, real merge-request numbers and filenames — that this public repo's universality requirement forbids. Changelog `20260814093000-publish-code-review-full.md` records the sanitization that publishing it cost. A private tree removes that tax.
- The sanitized copy stays in this repo's git history by choice. It was audited as publishable, so no history rewrite was done.
- No dependency change.

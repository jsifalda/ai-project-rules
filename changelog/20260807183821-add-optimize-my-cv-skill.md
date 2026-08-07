# Add `optimize-my-cv` skill

- New skill that audits a CV and returns a severity-ranked gap analysis plus an ordered remediation plan. It never rewrites the CV.
- Two rubric tracks: tech IC, and engineering leadership. The leadership track is native to this repo.
- Craft rules in `references/best-practices.md` are distilled from `tech-resume-optimizer` in `Paramchoudhary/ResumeSkills` (MIT), reframed from rewriter guidance into audit criteria.
- Findings use severity buckets with quoted evidence rather than numeric scores, so users fix the CV instead of optimising a number.
- CV content is personal data, so the skill reports in chat, refuses to write anything inside this public repo, and requires confirmation before any third-party egress.
- No new dependency. PDF intake uses the native file-reading tool.

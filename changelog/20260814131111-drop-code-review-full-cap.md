# Remove hard cap on code-review-full findings

- Removed the five-finding limit that hid extra findings in a collapsed overflow section.
- All verified findings that pass council review now reach the chat verdict.
- Added a runaway guard: above 10 findings, re-run the root-cause map first.
- Updated skill description, three reference documents, report renderer, and README.

Why: a count is a proxy for relevance, not relevance itself. A finding that clears both gates, code
verification and council review, is real and was not rejected. Hiding it because five others ranked
above it is arbitrary. The verdict now groups findings under verdict headers with counts, so a
longer list stays readable. The runaway guard is a diagnostic, not a new cap. A count that high is
more often a missed dedupe than ten separate defects, so the council merges what shares a cause. It
never drops a finding to hit a number.

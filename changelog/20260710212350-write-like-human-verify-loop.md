# write-like-human: bounded verification loop

- Replaced the single-pass "Before returning" check with a bounded iterate-loop (read → flag → rewrite → re-read, cap 3 passes, escalation note).
- Why: output still read as AI after one re-read. One pass lets AI-sounding sentences survive.
- Kept the 17-rule framing intact (no new detection criteria), so no cross-file count edits.

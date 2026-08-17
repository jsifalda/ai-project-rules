# Code-review findings triage by relevance, not severity

- The code-review findings gate no longer decides by severity. Relevance decides if a finding gets
  fixed. Severity only sets the order of the work. A correct, in-scope `minor` or `trivial` finding
  now gets fixed instead of waiting in a queue for the user.
- Triage runs first, over the merged and deduplicated finding set, so nothing gets applied before it
  is judged. A finding that is not relevant gets rejected with a stated reason, not silently dropped.
- Changed in the exported `setup-aiengineering` template and in this repo's own policy together —
  `CLAUDE.md`, `README.md`, and `rules/general.md`. The repo governed itself by the severity gate it
  exported, so a change to only one side would put the two out of step again.
- Why severity was the wrong measure, in both directions: a real small defect went unfixed because
  its rating was low, and a wrong finding got applied because its rating was high. Severity says
  nothing about whether a finding is correct or in scope.
- The exported template gained the normative carve-out it never had. Without it, a gate that fixes at
  every severity lets a reviewer rewrite a target repo's binding policy. A finding that changes what a
  rule requires still gets drafted, shown, and asked — at any severity.
- The rule used to be stated twice, once per lens, and the harness-native lens carried no rule at
  all. One shared step replaced both copies and closed that gap.
- `rules/general.md` said "Fix the findings from the review, if that makes a sense", which contradicted
  the stricter rule in `CLAUDE.md`. It is now a self-contained relevance gate, because that file loads
  in projects that have no verification-protocol section to point at.
- The nuclear structural lens keeps its no-auto-apply exemption and now states why: it proposes
  rewrites rather than defects, and each proposal is larger than the change under review.
- **Forward-only, by design.** No `baseline-checklist.md` row was added and the skill version stays
  at `v11`. That file's maintainer loop forbids a bump for a wording or mechanism change, because a
  bump refreshes the injected half of a setup while leaving the delegated half stale. New setups get
  the new gate; an existing repo picks it up on a hand re-run. The absent bump is deliberate, not an
  oversight.

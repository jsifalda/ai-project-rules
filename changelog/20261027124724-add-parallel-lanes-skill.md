# Add the parallel-lanes skill

- Added `skills/parallel-lanes`, which turns a spec, PRD or list of user scenarios into a plan for running coding agents in parallel without file conflicts.
- It scouts each repo read-only, builds one minimal foundation unit per repo, cuts file-disjoint lanes, checks scenario coverage, and batches units under resource caps.
- It ships `scripts/check_lanes.py`, a stdlib validator with a unittest suite.
- Why: parallel agents that edit the same files cause merge conflicts, and no existing skill planned file-disjoint work.

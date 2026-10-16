# Remove the ship-pr attribution policy

- Removed every attribution rule from ship-pr: the ban, the required-line exception, and the trailing-block rule. Version bumped to 2.0, because harness-default attribution now passes through.
- Dropped "only" from the PR body rule, so it no longer reads as a ban on a line an instruction file requires.
- Narrowed the description from "anything touching tags or changelogs" to "creating tags or changelogs", because committed mode ships a branch that carries a changelog commit.
- Fixed the failure-mode table to match the abort messages the code prints.
- Why: ship-pr is a public, universal skill. Attribution is a per-user or per-org choice, and each reader's own instruction files and harness settings already govern it.

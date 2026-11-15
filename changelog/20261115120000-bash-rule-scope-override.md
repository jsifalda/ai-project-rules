# Keep the one-purpose Bash rule and add an override

- `rules/general.md` `# READING FILES`: the rule again covers every Bash call ("one purpose"). The ban on `&&` and `;` chains now names reads and probes.
- A command that a rule, a skill or a repo spells out overrides the ban, so the presence check in `# SECRETS & ENV FILES` and chained tests in skills stay valid.
- Why: review found that the earlier wording narrowed the rule to reads and probes, and conflicted with commands other rules prescribe.

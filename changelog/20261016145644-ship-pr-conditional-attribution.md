# Make the ship-pr attribution ban conditional

- The ship-pr attribution ban now gives way when an instruction file explicitly requires an attribution line. Built-in harness text does not count. The required line is written once, in its exact form.
- Why: an org-managed instruction now requires a `Co-Authored-By: Claude <model>` trailer on work commits and MRs, to track the share made by Claude Code. The hard ban in ship-pr conflicted with it.

# Drop the session-wide tool block from investigate

- Removed `disallowed-tools: Edit, Write, NotebookEdit` from the investigate skill. Its read-only rules stay as prose, and "Change nothing" now says "with any tool".
- Added rules for stacking with a skill that plans or ships. It stays read-only until the user approves that skill's plan, or approves its first change when it has no plan. Before then, the plan file is the only write beyond the scratch and ignored-artifact writes. After it, that skill's rules govern.
- Why: a stacked `/investigate` removed Write for the whole session and its subagents, so a planning skill in the same stack could not write its plan file.

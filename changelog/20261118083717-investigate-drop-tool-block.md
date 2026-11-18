# Drop the session-wide tool block from investigate

- Removed `disallowed-tools: Edit, Write, NotebookEdit` from the investigate skill. Its read-only rules stay as prose, and "Change nothing" now says "with any tool".
- Added a rule for stacking with a skill that plans or ships. It stays read-only until the user approves that skill's plan, and the plan file is the only allowed write before then.
- Why: a stacked `/investigate` removed Write for the whole session and its subagents, so a planning skill in the same stack could not write its plan file.

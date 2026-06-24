# Add distill-notes-v2 skill

- Added `distill-notes-v2`, a sibling to `distill-notes` for notes that mix reference facts with heuristics.
- It organizes facts losslessly (grouped by inferred category, deadlines flagged, every number/date/condition kept verbatim) and distills heuristics into sharpened maxims. Two sections in chat plus an outputs/ .md file.
- Why: `distill-notes` is lossy and rhetorical by design (drops 40-60%, 8-word maxims), which destroys factual notes like tax, medical, or legal records. The new skill is lossless on facts, lossy only on principles.
- Distill logic is inlined, not delegated to `distill-notes`, to keep the skill self-contained.
- Updated the README skills table.

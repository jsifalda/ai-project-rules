# rephrase answers without a confirmation question

- Changed `rephrase` to give its restatement as a finished answer, with no confirmation question and no next-step offer.
- On thin or ambiguous input it picks the most likely reading and lists its assumptions at the end.
- Why: the confirmation question made the user answer again before getting the restatement they asked for.
- Reworded the `brainstorm` rephrase step to say restate, not confirm. `brainstorm` keeps its own confirmation step.

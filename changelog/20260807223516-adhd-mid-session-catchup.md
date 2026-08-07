# i-have-adhd catches the reader up when invoked mid-session

- Added an `## On invocation` section to `i-have-adhd` — a four-case branch on what the skill emits the moment it turns on.
- Bare invocation with work in flight now opens with a merged catch-up block (what is done, the steps from the last answer, one next action, a time estimate). Bare invocation with nothing open reshapes the last answer instead. An invocation carrying a request skips the catch-up and just answers.
- Why: the skill only shaped future replies, so turning it on after a long session did nothing visible. That is when a state restatement is worth most, because the reader has already lost everything not on screen.
- Updated the frontmatter `description` and the README summary row to scope the claim to the one case that actually produces a catch-up.

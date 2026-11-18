# Add a sibling repo sync prompt

- Added `## Sibling repo sync`: a change to a shared section asks the user whether to port it to a private sibling repo.
- The Step 5 late-file rule now also re-runs the prompt-audit lens when it fires.
- Why: the two files drifted silently. A prompt at change time keeps them in step.

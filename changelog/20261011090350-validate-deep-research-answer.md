# Add a validate step to deep-research-answer

- Added Step 7. Validate, with a stdlib script that checks the answer before it is shown: the ANSWER line first, both labelled blocks, the main question, 5 or more sources with 1 or more primary, and the assumptions, conflicts and added-queries fields.
- Fixed the output labels in Step 6 so the script can find them. Added a manual checklist for hosts with no shell.
- Why: the answer format had no automated check, so a missing field or a thin source list could reach the reader.

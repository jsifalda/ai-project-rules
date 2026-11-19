# Cut always-loaded instruction tokens

- Moved low-frequency rule sections to load-on-trigger files and shortened skill descriptions over 600 chars to 500 or less.
- Why: OTel data showed each headless session starts at ~78k tokens, about 51k written fresh to the 1h cache. Instruction files were ~18k of that.
- Experiment PR, labelled `no-automerge`.

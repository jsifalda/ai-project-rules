# Read long output from a file, re-run only after a fix

- `rules/general.md` now tells agents to save long output to a file and read that, instead of piping a live command through `tail`.
- Why: agents piped a slow gate through `tail`, then ran it again to see the failure. The new line allows a re-run only after a fix, which matches the verification protocol.

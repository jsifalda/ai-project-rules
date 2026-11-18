# Stop processes without killing the agent's own shell

- `rules/coding.md` now bans `pkill -f` and `pgrep -f` on a pattern that matches the agent's own command line, and names a fallback for a process with no PID and no port: bracket one letter of a pattern unique to the target.
- `rules/general.md` now loads `rules/coding.md` when an agent starts or stops a process, server or background job.
- Why: `pkill -f` matches the calling Bash tool shell, whose command line holds the pattern, so the call kills itself (exit 144). `pgrep -f … | xargs kill` does the same. The rule did not load in the sessions where agents stop processes.

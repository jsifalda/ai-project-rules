# indie-hacker-wrapup runs directly without the upfront ask

- Removed the blocking "Want to draft a learning from this session for X?" yes/no gate from the skill.
- On invocation it now goes straight to scanning the session and surfacing angles; steps renumbered 1-3.
- Why: by the time the skill runs the user has already opted in (typed the command or asked to wrap up), so the question was a redundant round-trip. The decline-when-nothing-clears behavior stays as the real safety valve.

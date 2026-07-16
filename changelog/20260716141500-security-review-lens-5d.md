# Add security review lens 5d to setup-aiengineering

- Added a fourth parallel code-review lens (5d) to the injected verification protocol's gate 5, invoking the harness's built-in security review (Claude Code: `/security-review`). Defaults ON in the Step 4 module menu, deselectable, self-gating on host availability.
- Why: gate 5 covered correctness (5a), general review (5b), and structure (5c), but nothing owned vulnerability classes specifically. Injection, XSS, SSRF, hardcoded secrets, IDOR, auth bypass, unsafe deserialization, and path traversal now have a named lens.
- Triage mirrors 5b: `critical`/`major` auto-apply then re-run gates 1-3, `minor`/`info` get listed for the user.
- Made gate 5 count-agnostic ("every lens below" instead of "all three"), so a deselected 5d needs no conditional rewrite and a future 5e needs no edit here at all.
- Added Step 9b, a suggestion-only nudge for the `security-guidance` plugin. Fires only on Claude Code, only when 5d was selected, and only when the plugin is absent. The plugin is hooks-only (pattern warnings, LLM diff review on stop, agentic review on commit) and is a separate always-on layer, not the source of `/security-review`. The skill never installs it.
- Bumped baseline **Skill version v3 to v4** and added the two matching checklist rows, so re-runs offer both concerns to repos already stamped v3.
- No new dependency. `/security-review` is a Claude Code built-in and needs no plugin.

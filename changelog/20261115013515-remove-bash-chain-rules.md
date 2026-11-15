# Remove the Bash chaining rules from the core rules

- `rules/general.md` `# READING FILES`: removed the rule "One Bash call, one purpose" and the rule "Run one git command per Bash call".
- Why: the rules forced many small tool calls, which cost time, tokens and permission prompts. Agents can chain related commands again. The trailing-command failure from PR #253 is accepted.
- The removal is deliberate. It reverses `20261115020500-one-bash-call-per-probe.md` and `20261115120000-bash-rule-scope-override.md` (PR #253), and the git rule from `20261012170629-add-scope-git-dotfile-rules.md`.

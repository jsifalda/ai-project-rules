# Add find-skills skill

- New `find-skills` skill finds a skill in the public skills.sh registry and copies an approved skill into the current project.
- Deliberate fork of the upstream skill in `vercel-labs/skills`. The upstream drives the `npx skills` CLI and installs at user level with `npx skills add -g -y`.
- Transport changed to plain HTTP reads with `curl`, because this repo forbids installs. `npx skills add` is banned. A registry outage can fall back to `npx -y skills find` for SEARCH only, and only after the user approves it, because that command downloads a package.
- Copied skills land in the project, not in the user-level skill folder. Each skill is versioned with the repository that uses it and reaches teammates and CI.
- Checks what the agent can already reach before it searches. Any hit ends the flow, so the same skill does not get copied twice.
- Reads every file of a candidate for security problems before anything lands. Checks include scripts, install commands, secret reads, unexpected network calls, destructive commands, and prompt-injection text. The verdict is pass, warn, or block.
- Auto-invocation narrowed to explicit skill-seeking phrasings. The upstream fired on any "how do I do X" question, which would intercept ordinary how-to turns.
- Offers to add a mention of a copied skill to `AGENTS.md` or `CLAUDE.md`, so the skill actually gets used.
- No new dependency.

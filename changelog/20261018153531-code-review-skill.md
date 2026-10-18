# Replace the code-review agent with a synced code-review skill

- Added the `code-review` skill, vendored from addyosmani/agent-skills `code-review-and-quality` (MIT). It runs as a forked read-only Sonnet subagent and replaces the bundled `/code-review`.
- Removed the dangling cross-references and the file-editing mutation step from the vendored text, and added a target section and a fixed output format.
- Cut the upstream parts a forked read-only reviewer cannot act on: asking before deletes, running tests or builds, review-speed and multi-model guidance.
- The injected verification protocol now scopes the review to every change since the default branch, and `CLAUDE.md` maps the new labels onto CodeRabbit severities.
- Rewired `rules/general.md`, `CLAUDE.md` and the `setup-aiengineering` verification protocol from the `code-review` agent type to the skill.
- Allowed the `context`, `agent` and `model` frontmatter keys in the skill validator.
- Why: Claude Code has no built-in `code-review` agent type. The old agent was a local file that did not sync to other machines, so the review gate failed there.

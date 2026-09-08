# Remove the four team-* agent-team skills

- Deleted `skills/team-ship/`, `skills/team-code-writer/`, `skills/team-tester/`, and
  `skills/team-reviewer/`, plus their `README.md` rows and the upstream attribution line.
- They shipped an agent dev team adapted from an X post. The workflow was not used, and an
  unused skill is noise in the skill list every session loads.
- No archive copy was kept. The repository history is the recovery path.
- Also dropped the now dead `/team-ship` pointer from the personal global rules outside this
  repo, so no rule routes to a skill that no longer exists.

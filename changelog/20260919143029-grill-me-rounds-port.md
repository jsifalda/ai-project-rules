# Port the upstream grilling rewrite into grill-me

- Replaced the `grill-me` body with the current upstream `mattpocock/skills`
  `productivity/grilling` body, verbatim. Local frontmatter kept, as the fork contract in
  `README.md` and `scripts/sync-mattpocock-skills.sh` requires.
- Behavior changed: the skill no longer asks one question per turn. It works a design tree
  in rounds, asking every question whose prerequisites are already settled, and finds facts
  through a sub-agent instead of asking the user.
- Why: the fork was last refreshed on 2026-07-16 and upstream has since rewritten the skill.
  Rounds cut the round-trips and state the dependency rule the old body only implied.
- Updated the `grill-me` description, the README row, `better-plan` Stage 2, and
  `landing-page-viral-grill` step 6, which all still stated the old one-at-a-time cadence.
- Also corrected `better-plan`, which claimed `grill-me` asks through `AskUserQuestion`. The
  new body asks in chat text, and a round can exceed the four questions that tool accepts.
- Known narrowing: the new body requires a sub-agent for fact finding and states no
  fallback. Consumers without sub-agents lose that step.

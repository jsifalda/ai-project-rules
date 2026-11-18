# Fix review findings on the landing copy mechanism rules

- Put the audit pass item list and its exact cost (minus 1 per section, floor 0) in the whole-page check, so the blind scorer sees them. Matched the cost in `SKILL.md`.
- Renumbered the aftertaste check to 6.
- Renamed the Features template slots from `feature_N_mechanism` to `feature_N_how_it_helps`.
- Exempted technical-ICP feature specs from the viral grill "No mechanism copy" check.
- Why: the blind scorer could not run the audit pass, scores could drift, template drafts failed the new rule, and correct technical-ICP pages failed the grill.

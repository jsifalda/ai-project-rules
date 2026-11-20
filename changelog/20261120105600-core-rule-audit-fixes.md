# Apply prompt-audit fixes to core rules

- Allowed a short reason clause in `rules/authoring.md` when a rule is not self-evident.
- Reworded the BLOCKERS denial line in `rules/general.md`. It now separates a denial from a target block, says to find a way around the denial, and to report it when none exists.
- Removed the "Follow every rule in this file" booster.
- Changed "FORCE" to plain case.
- Why: a prompt audit for current models found these lines dated or ambiguous for a literal model.

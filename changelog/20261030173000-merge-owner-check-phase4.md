# Merge the owner check into Phase 4

- Moved the "check as its owner would" core rule into Phase 4, which already checks as the user would. One term, no duplicate rule.
- Gated the fix step on the ask-first rules, so a fix that needs approval is flagged, not applied.
- Why: review of #226 found the rule grew the always-loaded layer with no offset and conflicted with the ask-first gates.

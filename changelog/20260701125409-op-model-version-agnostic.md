# Make op skill model references version-agnostic

- `skills/op/SKILL.md`: replaced the hardcoded "verified" example (`claude-haiku-4-5`, `claude-sonnet-4-6`, `claude-opus-4-8`) with a description of the actual invariant — `model` is a tier alias, not a dated ID, and the Agent tool always resolves it to Anthropic's current highest release for that tier.
- Added a dispatch rule forbidding a hardcoded dated model ID in `model`, so routing can never regress to a superseded version.
- `skills/op/references/model-routing.md`: dropped the hardcoded `claude-fable-5` version from the `fable` callout.
- Why: the old prose was already stale (Sonnet 5 replaced the named `claude-sonnet-4-6`) and would need editing again on every future model release. Same fix mirrored into the sibling `opusplan` skill (ai-prompts repo).

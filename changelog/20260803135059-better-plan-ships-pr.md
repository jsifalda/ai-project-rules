# better-plan ships the work as a PR by default

- Added Stage 5 to `better-plan`. Once execution finishes it invokes `ship-pr` as the last
  thing in the flow, gated on the run being verified with nothing left awaiting the user.
  A blocked gate names the condition instead of shipping, and is not a failed run.
- Removed `disable-model-invocation` from `ship-pr`. That flag is a hard harness block, not
  a hint. It removes a skill from the Skill tool entirely, so no dependent skill could ever
  reach `ship-pr` regardless of wording. Its guard is now the description's anti-triggers
  plus a new `## Invocation` section.
- Side effect: this also unblocks `loop-todos`, whose documented per-entry ship step had the
  same latent problem and could never have fired.
- Tradeoff accepted knowingly: a skill that opens real PRs is now guarded by prompt text
  rather than by the harness, which runs against the guidance in `create-skill`.

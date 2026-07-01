# Simplify verify-models.py, drop its test suite

- `skills/op/scripts/verify-models.py`: the skill only ever calls it bare (no flags), but it shipped `--session`/`--all`/`--json` modes plus a token-usage percentage engine none of that call site uses. Cut all three flags and simplified usage reporting to a flat per-model token tally.
- Deleted `test_verify_models.py` and its fixture: no other skill script in this repo carries tests, nothing runs them in CI, and the surviving ~270-line script is simple enough to hand-verify.
- Same simplification mirrored into the sibling `opusplan` skill (ai-prompts repo).

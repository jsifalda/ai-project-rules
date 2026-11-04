# Port pstack skills from cursor/plugins

- Ported `why`, `how`, `unslop` and `in-your-own-words` (renamed `rephrase`) from cursor/plugins pstack at commit ae5650f, MIT.
- Why: give agents these investigation and writing skills, callable only on purpose.
- Restricted invocation through the description and an Invocation section instead of `disable-model-invocation`, so agents and dependent skills can still call them.
- Cursor model routing removed from `why` and `how`, so poteto-mode, setup-pstack and the pstack-models rule were not ported.
- Added GitLab support to `why`: `glab mr view` and `!1234` merge request numbers beside `gh`.

# Add opusplan skill

- New skill `opusplan`: takes an implementation plan, routes each task to the cheapest capable Claude model (Haiku/Sonnet/Opus), presents the annotated plan, then executes by dispatching each task as a subagent on its assigned model.
- Why: Claude Code runs one model per session, so on Opus every task pays Opus cost even mechanical ones. Per-task routing keeps deep-reasoning work on Opus while sending mechanical and mid-complexity tasks to smaller, faster, cheaper models.
- Mechanism verified: the Agent tool `model` param runs a subagent on a different model than the session default (haiku/sonnet/opus subagents report distinct model ids). End-to-end run dispatched two independent tasks in parallel on Haiku + Sonnet and verified correct output.
- Added row to README skills table.

# Add council-v2 skill

- New `skills/council-v2/` — a variant of `council` whose advisor roster is built from existing reasoning skills instead of ad-hoc personas.
- Two v1 seats were replaced where the jobs overlapped — the First Principles Thinker now delegates to `first-principles-mode`, and the Executor is superseded by `founder-thinking-mode`. The Contrarian, Outsider, and Expansionist survive because no new voice covers their job.
- Added two domain seats, `persona-stanier` and `persona-levelsio`, seated only when the question is a leadership or an indie/bootstrap call. Routing mirrors the reasoning-mode routing already in use, so seats that have nothing to say stay benched instead of adding filler.
- Ships slash-only so it cannot collide with `council`, which keeps the natural-language triggers.
- Peer-review anonymisation dropped — the persona voices are unmistakable, so the letters bought nothing. The chairman now dedups repeated claims so echoes are not mistaken for consensus.

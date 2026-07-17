# ADR: Record architecture decisions

- Status: Accepted
- Date: YYYY-MM-DD

## Context

We need to record the meaningful architectural decisions made on this project, so the
reasoning behind them is preserved and future contributors — human or AI — can stay true to
past choices instead of re-deriving them.

## Decision

We will use Architecture Decision Records (ADRs), as described in the project's ADR policy.
Each meaningful technical decision gets a dated record in `docs/adr/`, copied from
`docs/adr/0000-template.md`. A companion `ARCHITECTURE.md` recap doc keeps the current-state
overview derived from these ADRs.

## Options considered

- **ADRs (chosen)** — lightweight, version-controlled, live next to the code, greppable.
- **No formal record** — decisions live only in commit messages or memory; rejected, the
  reasoning gets lost.
- **An external wiki or doc** — drifts from the code and is easy to forget; rejected.

## Consequences

A growing, greppable history of decisions and the reasoning behind them. Small per-decision
overhead. New decisions that reverse old ones must supersede them rather than delete them.

## Supersedes / Superseded by

—

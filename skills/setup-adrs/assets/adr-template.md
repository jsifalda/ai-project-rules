# ADR: <short decision title>

<!-- BUDGET — delete this whole block when you fill the template in.

Hard cap: 250 words for the entire file. A cap, not a target.
More than three options: add 20 words per extra option.
Context 50 · Decision 70 · Options 20 each · Consequences 40 · Supersedes 15.
Replace the example text under each heading. Keep it the same length as the example.

Cut this:
  - narrative recap of how the problem was discovered
  - anything the code already says
  - a "the lesson is ..." moral at the end
  - a Consequences section that re-argues the Decision instead of naming its cost
  - an option bullet longer than one line
  - a Supersedes section that says it supersedes nothing and takes 230 words to say it;
    write "Nothing." and stop
-->

- Status: Proposed | Accepted | Superseded by YYYY-MM-DD-slug | Deprecated
- Date: YYYY-MM-DD
- Deciders: <who decided> (optional)

## Context

Photos arrive from phones at 8 MB. Uploads time out and storage cost grows with every
listing. The client wants a limit before launch.

## Decision

We will reject any photo over 1 MB in the browser, five per listing, and do no
server-side processing at all.

## Options considered

- **Browser-side 1 MB reject — chosen** — no server cost, client accepted the trade.
- **Server-side resize — discarded** — needs a worker and a queue v1 does not have.
- **10 MB cap — discarded** — the client reversed it on 2026-08-08.

## Consequences

Photos keep their EXIF, GPS included. The limit holds in the browser only, so a crafted
request still gets past it.

## Supersedes / Superseded by

Supersedes 2026-08-08-photo-size-cap. Nothing supersedes this yet.

# PRD Structure

## Conciseness contract (read first)

Write for a builder skimming on a phone, not a committee reviewing a doc.

- Every line earns its place or gets cut.
- Fragments over sentences. Bullets over paragraphs. Tables where they compress.
- Ban corporate filler: leverage, robust, seamless, synergy, stakeholder, best-in-class, deliverable, utilize, facilitate.
- No em-dashes, semicolons, or emojis. Use periods, commas, or arrows.
- Link details out (a mockup, a doc). Never inline them.

Keep the whole PRD to about one page as a ceiling, not a target. Shorter is better as long as it stays buildable.

## Sections

Keep all 8. Each has a budget. Skip a section only when it truly adds nothing for a small feature.

1. **Summary** → 1 line: "Building [what] for [who] so they can [outcome]." A second line only if unavoidable.
2. **Problem & Context** → max 3 bullets: the pain, why it matters, how people solve it today. No sub-headers, no paragraphs, no solution talk.
3. **Users & Key Use Cases** →
   - 1 line naming who it is for (specific, not "everyone").
   - 3-5 user stories, one line each: "As a [user], [action] so [benefit]." Trim filler.
4. **Goals & Success Signals** →
   - 1 goal line: what "good" looks like after shipping.
   - Up to 2 signal bullets (signups, first paying user, activation). Optional. Skip when obvious.
5. **Scope (In / Out)** → two short bullet lists of fragments.
   - **In**: what this version ships.
   - **Out / Non-goals**: what you are not doing yet.
6. **Solution Outline & Requirements** →
   - **Approach**: 1-2 lines on the core idea. No paragraphs, no pixels.
   - **Functional Requirements**: numbered list. Terse "must" statements, one behavior each. Explicit enough to build from.
   - **Edge cases**: bullets. Only the real ones (limits, failures, invalid input).
   - **Design ref**: link a mockup if you have one. Never inline pixel specs.
   - **Tech notes**: bullets. External services or APIs you rely on (auth, payments), plus any hard constraint.
7. **Risks & Assumptions** → bullets.
   - Assumptions: what you bet is true (people want this, they will pay, an API does X).
   - Risks: what could sink it (no demand, you will not finish, a dependency breaks). Flag the scary one.
8. **Open Questions** → bullets, or "None." Keep updated as you learn. The PRD is a living document.

## Format

- **Default to bullet points for every section so the whole PRD is skimmable at a glance.** Use prose only when a bullet genuinely cannot carry the point.
- Markdown headers (#, ##). Shallow hierarchy.
- Numbered lists for ordered or requirement items. Tables where they compress.

## Worked example (target this density)

```markdown
# PRD: Magic-link login

## Summary
Building passwordless email login for solo SaaS users so they can sign in without remembering a password.

## Problem & Context
- Password resets are the #1 support ticket, and they cost me time I do not have.
- Users abandon signup when forced to invent a password.
- Today: email + password with a clunky reset flow.

## Users & Key Use Cases
For existing free-tier users on the web app.
- As a returning user, I request a login link by email so I skip the password.
- As a new user, I sign up with just an email so onboarding is one step.
- As a user on a new device, I get a fresh link so I do not get locked out.

## Goals & Success Signals
Cut login friction to a single email step.
- Password-reset tickets drop toward zero.
- Login completion rate goes up.

## Scope (In / Out)
**In**
- Email a one-time signed link, 15-min expiry.
- Create the session on click.
**Out / Non-goals**
- Social login.
- SMS or authenticator apps.

## Solution Outline & Requirements
**Approach**: on login, mint a signed token, email a link, create the session when the link is opened.

**Functional Requirements**
1. The system must send a login link to any submitted email.
2. The link must expire after 15 minutes and work once.
3. The system must create a session on a valid click and redirect to the dashboard.
4. An expired or reused link must show a "request a new link" screen.

**Edge cases**
- Unknown email: send the same link (do not reveal if the account exists).
- Rapid re-requests: rate-limit to 3 per email per hour.

**Design ref**: [Figma login flow](link)

**Tech notes**
- Email via the existing transactional provider.
- Signed tokens via the current session library. No new dependency.

## Risks & Assumptions
- Assumption: users check email fast enough for a 15-min window.
- Risk (scary one): email deliverability. A link in spam blocks all logins.

## Open Questions
- Keep password login as a fallback, or remove it?
```

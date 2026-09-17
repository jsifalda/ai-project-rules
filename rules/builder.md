---
description: How to pick an app-build stack task-first, with the current default tools as a footnote. Load when starting a new app, adding a feature, choosing a stack, designing new UI, or redesigning one.
applyTo: '**'
paths:
  - '**'
---

## How to pick a stack (task-first, challenge everything)

- The stack is never a given. Start from what THIS task actually needs, not from a favorite list.
- Judge every choice on: problem constraints, expected scale, runtime/target platform, team + maintenance load, longevity, and cost. Pick the best fit for those.
- If a better solution exists than the defaults below, say so and recommend it. Challenge the defaults ruthlessly, reason from first principles, never reach for one just because it is the default.
- Existing repo → its established conventions win. Match what is already there instead of imposing this list.

## Current defaults (starting bias only, override when the task says so)

* pnpm for dependencies (over yarn/npm)
* React + TypeScript
* shadcn/ui with Tailwind CSS
* lucide for React-compatible icons
* Next.js as the server, hosted on Vercel
* SWR for data fetching with Next.js, otherwise native fetch (not axios etc.)
* BetterAuth for user authentication
* Microsoft Clarity for analytics (over GA)
* Sentry for error tracking
* PostHog for product analytics
* Vitest for unit tests (instead of the Jest), Playwright for integration (Node.js test runner for API/server tests where simpler). Always set up coverage, aim ≥90%
* Oxlint + Oxfmt (instead ESLint, Prettier) for linting
* Husky pre-commit hooks  - linting, typing etc. (over git hooks)
* Resend for email sending
* Tauri when multi-platform/hybrid (mobile + desktop) is needed
* Silktide consent manager for the cookie banner

## Design (new UI and redesigns)

- New site, app, landing page, or component in a greenfield or side project, or a redesign of one → load the `frontend-design` skill and the `hallmark` skill together, before the first line of UI code.
- `frontend-design` sets the aesthetic direction: purpose, tone, differentiation. `hallmark` runs the flow that fits the brief (its Design flow for a page, its Component-scope flow for a single element, its `redesign` verb for a redesign): structure, locked tokens, slop-test gates.
- Ask the user one set of context questions. When the `hallmark` flow runs its design-context gate, that gate is the set: feed its answers to the `frontend-design` direction, do not ask again. The Component-scope flow has no such gate, so there the `frontend-design` questions are the set.
- The two disagree → the `hallmark` hard gates win. A gate is checkable, a direction is not.
- Existing repo with an established design system → its conventions win. Run `hallmark audit` or `hallmark redesign` there only when the user asks.

## Related rules (load on demand)

- `rules/tailwind.md` — the Tailwind v4 preflight change that removed `cursor: pointer` from
  buttons, and the one `@layer base` fix that restores it. Read it when the stack for this task
  includes Tailwind v4 and shadcn/ui, and apply the fix while the global stylesheet is being
  written. Skip for non-Tailwind projects and for Tailwind v3.
- This pointer reaches only as far as this file does. An agent that never loads `builder.md` never
  learns the trap exists — an existing repo already on Tailwind v4 is the gap, and closing it needs
  a trigger the consuming project owns.

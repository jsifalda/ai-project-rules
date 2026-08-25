---
description: How to pick an app-build stack task-first, with the current default tools as a footnote. Load when starting a new app, adding a feature, or choosing a stack.
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

## Tailwind v4 cursor trap (shadcn/ui default stack)

- Tailwind v3's preflight set `button, [role="button"] { cursor: pointer }`. Tailwind v4 removed
  that rule (a documented breaking change). Result: every `<button>` and `[role="button"]` falls
  back to the UA default `cursor: default`, while `<a href>` keeps `cursor: pointer` — links feel
  clickable, buttons do not.
- `<summary>`, `<select>`, and a checkbox or radio `<label>` are not part of that regression —
  Tailwind's preflight never set a pointer on them in v3 either. They read as clickable and are
  not, so fix them in the same place.
- Fix once, in the global stylesheet's `@layer base` — never per-component `cursor-pointer`
  utilities, which just hide the bug in each new component instead of fixing it:
  ```css
  @layer base {
    button:not(:disabled):not([aria-disabled="true"]),
    [role="button"]:not([aria-disabled="true"]),
    summary,
    select:not(:disabled),
    label:has(input:is([type="checkbox"], [type="radio"]):not(:disabled)),
    input[type="checkbox"]:not(:disabled),
    input[type="radio"]:not(:disabled),
    input[type="file"]:not(:disabled),
    input[type="file"]:not(:disabled)::file-selector-button {
      cursor: pointer;
    }
  }
  ```
- Text inputs and textareas are deliberately excluded — they keep the text caret.
- A `<label for>` that does not wrap its input is out of reach — CSS cannot see the target's type
  through `for=`. shadcn/ui's `<Label htmlFor>` + `<Checkbox>` pairs are the common case. That pair
  is the one place a `cursor-pointer` utility on the label is correct.

# Coding standards

- Use and change the absolute minimum code.
- Follow the existing coding style, structure, framework choices, typing and architecture.
- Prefer functional paradigms. Pure functions where possible. Avoid side effects.
- Use `async/await` for asynchronous code.
- No magic numbers. Name every constant.
- Use `fetch` for HTTP. Never `axios`, `superagent`, or another library.
- Never swallow an error silently. Log or propagate it.
- Keep routine success quiet in what you build. Send no ping or alert that needs no action.
- No convention in the repo → camelCase for variables and functions, PascalCase for classes and components.

## Comments

- Default: none. Rename or extract until the code needs no comment. In doubt, do not write it.
- Never: restate the code, narrate the diff, banners, doc blocks that echo the signature, agent chatter, or prose a test title already says.
- Only: a non-obvious why, a cited external constraint, a correctness trap, or an API contract the signature cannot show (side effects, errors, units, threads, ownership). "It is complex" does not qualify. Simplify instead.
- Never add or edit a comment outside your change. Delete one only when your change made it wrong. A comment that contradicts the code is a defect.
- Tooling directives are not comments. Never remove one (`eslint-disable`, `@ts-expect-error`, `# noqa`).

## Enforcement

- Catch a repeated review finding or correction with a lint rule, type, CI check, hook or test. A new tool or package → ask first.

## TypeScript

- TypeScript for new code where possible.
- Prefer immutable data: `const`, `readonly`. Interfaces for data structures.
- Strict types, zero `any`. No `ts-nocheck`, no `ts-ignore`.
- Zero type errors. Always run `tsc --noEmit` and fix the typing. Use the project's own compiler. `npx` is fine for a binary the project already depends on; it is an install when it fetches a package the project does not have, so `general.md` `# RESTRICTIONS` applies.
- Run locally with `node --import=tsx ...`. Build production with `tsc`.

## Dependency management

- Preference order: a dependency already in the project, then the standard library, then an established third-party library, then your own code. A bias, not a ranking. Take a later option when it is materially simpler or safer, and say why. An existing dependency never overrides a named prohibition here or in `general.md` (`fetch` over `axios`) or the repo's conventions.
- Never assume a library or framework is available or appropriate. Verify it in imports, `package.json` or `requirements.txt` first. Read its docs and types before deciding it cannot do the job.
- Small enough to write? Write it. Propose a package only when the self-written alternative is non-trivial or correctness-sensitive: auth, crypto, parsing, dates, timezones.
- Do not reimplement common functionality without a stated reason. Judge a library on maintenance, security and bundle cost, not popularity. Avoid deprecated, outdated or insecure ones.
- Use the local package manager. Respect the lockfile. None → prefer pnpm, then yarn, then npm.
- Latest stable version. Resolve it, never recall it. Never write a version from memory or copy one from another project. Pre-release, beta, canary and RC are not stable.
- Latest blocked → install the newest that works and report package, version used, latest not usable, and reason. Never downgrade in silence.
- Never upgrade an existing dependency unless asked. One far behind or unmaintained → say so.
- Adding a new package goes through the ask-first protocol in `general.md` `# RESTRICTIONS`. Propose, do not install.

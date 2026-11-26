# Coding standards

- Use and change the absolute minimum code.
- Follow the existing coding style, structure, framework choices, typing and architecture.
- Prefer functional paradigms. Pure functions where possible. Avoid side effects.
- Use `async/await` for asynchronous code.
- No magic numbers. Name every constant.
- Use `fetch` for HTTP. Never `axios`, `superagent`, or another library.
- Never swallow an error silently. Log or propagate it.
- Delete a config key, env var or flag to reach its default. Never pin the default value unless another layer overrides it.
- Keep routine success quiet in what you build. Send no ping or alert that needs no action.
- Stop a process by its saved PID or listening port. Never `pkill -f` or `pgrep -f` a pattern that matches your own command line.
- No PID and no port → bracket one letter of a `-f` pattern unique to the target.
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
- Run the project's own `tsc --noEmit`. Fix every type error.
- Run `npx` only for a binary the project already depends on. An `npx` fetch is an install under `general.md` `# RESTRICTIONS`.
- Run locally with `node --import=tsx ...`. Build production with `tsc`.

## Dependency management

- Prefer a dependency already in the project, then the standard library, then an established library, then your own code.
- Take a later option when it is materially simpler or safer. Say why.
- Never let an existing dependency override a named prohibition, such as `fetch` over `axios`, or a repo convention.
- Never assume a library or framework is available or appropriate. Verify it in imports, `package.json` or `requirements.txt` first. Read its docs and types before deciding it cannot do the job.
- Write small code yourself. Propose a package only for non-trivial or correctness-sensitive code: auth, crypto, parsing, dates, timezones.
- Never reimplement common functionality without a stated reason.
- Judge a library on maintenance, security and bundle cost, never popularity. Avoid a deprecated, outdated or insecure one.
- Use the local package manager. Respect the lockfile. None → prefer pnpm, then yarn, then npm.
- Latest stable version. Resolve it, never recall it. Never write a version from memory or copy one from another project. Pre-release, beta, canary and RC are not stable.
- Latest blocked → install the newest that works and report package, version used, latest not usable, and reason. Never downgrade in silence.
- Never upgrade an existing dependency unless asked. One far behind or unmaintained → say so.
- Adding a new package goes through the ask-first protocol in `general.md` `# RESTRICTIONS`. Propose, do not install.

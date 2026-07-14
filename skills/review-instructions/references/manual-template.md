# Manual template — shape, contracts, and worked examples

Read this before drafting. It defines the output skeleton, shows one bad → good pair
per section, and lists the banned adjectives.

Contents:
- Skeleton (L15)
- Section 1 — Conventions (L38)
- Section 2 — Failure modes (L60)
- Section 3 — Quality bar (L96)
- Section 4 — When uncertain (L124)
- Banned adjectives (L157)
- Coverage ledger (L173)

## Skeleton

The manual is the four sections below, in this order, and nothing else. No preamble
about the project's mission, no history, no rationale for the rewrite.

```markdown
# <Project> — operating manual

<One or two lines: what this project is, and what an agent is expected to produce here.>

## Conventions

## Failure modes

## Quality bar

## When uncertain
```

Every line in the manual is addressed to the model doing the work, in imperative
voice. The reader cannot ask follow-up questions, so a sentence that needs
clarification has already failed.

## Section 1 — Conventions

How work is actually done in this project. One bullet per convention. Each names the
rule and the anchor (a path, a pattern, or a command) that demonstrates it.

Cut anything a competent model already does without being told. "Write tests for new
code" is not a convention, it is a default. Keep only what is true *here* and would be
guessed wrong elsewhere.

Bad:

> - Follow the existing code style and keep things consistent.

Nothing to act on. "Existing style" is what the reader cannot see.

Good:

> - Route every DB read through `src/db/query.ts`. Direct `pool.query()` calls exist
>   only in `src/db/` itself. Anything outside that directory calling `pool` is a bug.
> - Handlers return `Result<T, AppError>`, never throw. See `src/api/users.ts` for the
>   pattern every handler copies.

## Section 2 — Failure modes

The mistakes a weaker model will make in this project, named. One block each:

```markdown
### <Name the mistake>

<What the weaker model does, and where it bites.>

**Rule:** <the single directive that prevents it>
```

Three contracts:
- Every failure has exactly **one** rule. Two rules means two failures, split them.
- Every failure names **where** it bites — a path or a pattern, not "in the codebase".
- No rule without a failure. A rule that prevents nothing is a convention, move it.

Name failures so they can be referenced later. "Silent enum drift" beats "Enum issue".

Bad:

> - Be careful with the config loader, it's easy to get wrong.

No name, no mechanism, no rule. The reader learns only that something is dangerous.

Good:

> ### Config read before load
>
> `config.get()` returns `undefined` rather than throwing when called before
> `config.load()` has resolved. Module-level calls in `src/services/*.ts` run before
> the loader finishes, so the value silently becomes `undefined` and the failure
> surfaces later as a null deref somewhere unrelated.
>
> **Rule:** Call `config.get()` inside a function body, never at module top level.

## Section 3 — Quality bar

One block per deliverable type this project actually produces. Discover the types by
reading the project. Do not assume a project ships the same artifacts as any other.

Every criterion resolves by one of exactly three means:
1. **A command** that exits 0 or 1 — `pnpm typecheck` passes.
2. **A countable threshold** — the diff touches at most 2 packages.
3. **A binary question** answerable without judgement — does the migration have a
   `down()`? Yes or no.

If a criterion needs the reader to decide what "enough" means, it is not a criterion.

Bad:

> A good migration is clean, reasonably safe, and well tested.

Three adjectives, zero checks. Two readers will disagree on every word.

Good:

> **A migration is done when:**
> - `pnpm migrate:up && pnpm migrate:down` both exit 0 against a scratch DB.
> - It defines `down()`. (Yes or no.)
> - It adds no `NOT NULL` column without a default. (Grep the diff for `NOT NULL`,
>   confirm each has `DEFAULT`.)
> - It changes at most 1 table. More than 1 means split it.

## Section 4 — When uncertain

Every rule has the form `if <observable trigger> → <action>`.

The trigger must be observable — something the reader can detect, not a feeling.
"If you're unsure" is not observable. "If two instruction files disagree" is.

The action comes from this closed set. Nothing else is an action:
- Stop and ask the user.
- Read `<specific file>`.
- Run `<specific command>`.
- Default to `<specific choice>`.

"Use your judgement", "proceed carefully", and "consider the tradeoffs" are not
actions. If the honest answer is that the model must decide, then pick the default it
should decide on and write that.

Bad:

> If you're not sure whether a change is risky, use your best judgement and escalate
> if needed.

No trigger, no action, no addressee for the escalation.

Good:

> - If two instruction files give conflicting rules → stop and ask the user which wins.
> - If a test fails and the cause is not in the diff → run `git log -p -- <file>` on the
>   failing file before touching it.
> - If a public function has no callers in the repo → default to leaving it. Deleting
>   is a separate change.
> - If a change needs a new dependency → stop and ask the user. Never install.

## Banned adjectives

Never in the quality bar. Each one hides a check the writer did not make. When one
appears in the draft, replace it with the check it stands for, or delete the line.

```
clean        robust       appropriate    reasonable
concise      clear        well-structured  proper
good         solid        sensible       maintainable
readable     idiomatic    thorough       sufficient
minimal      simple       elegant        careful
```

The test: if a criterion can be argued about with no command to settle it, an adjective
is doing the work.

## Coverage ledger

Not part of the manual. Show it to the user alongside the draft.

Every directive in the original file gets exactly one row. A rewrite that silently
drops a live rule is the worst outcome this skill can produce, and the ledger is what
makes a drop visible instead of invisible.

| Original directive | Disposition | Where / why |
| --- | --- | --- |
| "Use conventional commits" | kept | Conventions |
| "Write good tests" | merged | Quality bar → test criteria (was an adjective) |
| "Ask before adding deps" | merged | When uncertain → new-dependency rule |
| "Prefer Yarn" | dropped | Repo uses pnpm, lockfile is `pnpm-lock.yaml` |

Disposition is one of: `kept`, `merged`, `dropped`. A `dropped` row without a reason is
not allowed.

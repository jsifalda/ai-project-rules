---
name: review-instructions
description: Rewrite this project's agent instruction file (CLAUDE.md or AGENTS.md) as the operating manual a less capable model would need to work at the level of the model doing the rewrite. Reads the whole project and every instruction file reaching it, then produces four mandatory sections — the project's real conventions, named failure modes a weaker model will hit here each paired with the one rule that prevents it, a quality bar per deliverable written as checkable criteria with zero adjectives, and exact if-then escalation rules for when uncertain. Refuses to run outside the project root. Writes a draft beside the original, shows a coverage ledger accounting for every directive in the old file, and replaces the original only on explicit approval. Slash-only. Use when you type /review-instructions. Do NOT use to create an instruction file from scratch, to author or edit a skill, to review code, or to rewrite prose for style.
disable-model-invocation: true
---

# Review Instructions — rewrite the manual for a weaker model

Most agent instruction files are written by a strong model, for a strong model. They
record decisions but not the traps, not the bar, and not what to do when the file runs
out of answers. This skill reads the whole project and rewrites its instruction file as
the manual a **less capable model** would need to work at your level.

Run the gate, then five stages, in order. Do not skip any. Stop and surface a blocker
rather than guessing.

## Gate — model, then location

Both checks run before anything is read. Nothing proceeds until both clear.

**Model.** This skill is meant to run on Fable. You know your own model from your own
context, so no command is needed. If this session is on any other model, stop and ask
the user to switch (`/model claude-fable-5`), explaining why it matters — this skill
distills what the model doing the writing knows tacitly, so a weaker writer produces a
weaker manual. This is a prompt, not a refusal. If the user says continue anyway,
continue, and state at the top of the draft which model produced it.

**Location.** This skill takes no argument and runs only at the project root.

1. Run `git rev-parse --show-toplevel`. If it succeeds and does not match the current
   directory, **stop**. Name the correct directory and do not proceed. This is a
   refusal, not a prompt.
2. If it fails (not a git repo), the target file must exist in the current directory,
   and ask the user once to confirm this is the project root. Stop on anything but yes.

## Stage 1 — Locate the target

Find the agent instruction file at the project root: `CLAUDE.md`, else `AGENTS.md`.

- **Resolve symlinks first.** One of these is often a symlink to the other. Target the
  real file. Never write through the link, and never produce two drafts of one file.
- If neither exists, stop. This skill rewrites a manual, it does not invent one.
- If both exist as separate real files, ask the user which one to rewrite.

## Stage 2 — Read the project

Read the entire project and how you work in it. Never draft from the instruction file
alone. The manual describes reality; the instruction file is only a claim about reality.

1. Read the target file in full, first, before anything else.
2. Read the project. Fan out parallel `Explore` agents by area rather than reading a
   large tree serially:
   - Layout, build, test, and lint setup. Which commands actually gate a change.
   - Conventions and repeated patterns. What the code does the same way every time.
   - Every instruction file reaching this project — nested `CLAUDE.md`, imported rules,
     editor or tool config carrying directives.
   - Recent git history. What gets changed, what gets reverted, what keeps breaking.
3. Log the gaps as you go. These are the raw material for the first two sections:
   - Contradictions between instruction files.
   - Rules with no enforcement behind them.
   - Drift between what the instructions claim and what the code does.

## Stage 3 — Draft the four sections

Read [references/manual-template.md](references/manual-template.md) now. It carries the
output skeleton, a bad → good pair per section, and the banned-adjective list.

The manual is exactly these four sections, in this order:

**`## Conventions`** — how work is actually done here. Each states the rule and the
anchor (path, pattern, or command) proving it. Cut anything a competent model does by
default. Only project-specific conventions survive.

**`## Failure modes`** — the mistakes a weaker model will make here, each **named**, with
what it does, where it bites, and **the one rule that prevents it**. Reason these from
what you read in Stage 2. Contracts: one rule per failure, every failure anchored to a
path or pattern, no rule without a failure.

**`## Quality bar`** — one block per deliverable type this project actually produces.
Discover the types in Stage 2; do not assume. Every criterion resolves by a command that
exits 0 or 1, a countable threshold, or a binary question needing no judgement.
**Adjectives are banned.** Replace each with the check it stands for, or delete it.

**`## When uncertain`** — every rule is `if <observable trigger> → <action>`. The trigger
must be detectable, not a feeling. The action comes from a closed set — stop and ask the
user, read a specific file, run a specific command, or default to a specific choice.
"Use judgement" is not an action.

**Build the coverage ledger as you draft.** Every directive in the original gets one row:
`kept`, `merged into <section>`, or `dropped because <reason>`. A rewrite that silently
drops a live rule is the worst outcome this skill can produce, and the ledger is what
makes a drop visible. Show it to the user; never write it into the manual.

## Stage 4 — Self-check the draft

Run every contract back against the draft before the user sees it. A draft that fails
its own bar does not get presented.

- Every failure mode has a name, an anchor, and exactly one preventing rule.
- Every quality criterion carries a command, a threshold, or a binary — and no banned
  adjective.
- Every escalation rule is `if → then`, with an observable trigger and a closed-set
  action.
- The ledger accounts for every directive in the original, and every `dropped` row
  states a reason.

Fix and re-check. Do not present a draft with known violations and a note apologising
for them.

## Stage 5 — Write the draft, then replace on approval

1. Write the manual to `<TARGET>.review.md` beside the original — `CLAUDE.review.md` for
   `CLAUDE.md`. **Never touch the original before approval.**
2. Present to the user:
   - The diff against the original.
   - The coverage ledger, with dropped rules called out first.
   - Each named failure mode and the anchor it came from.
3. On explicit approval, replace the original with the draft and remove the draft. Leave
   any symlink pointing at the file untouched.
4. Do not commit. The host project's own rules decide that.

If the user does not approve, leave both files in place and stop. The draft is theirs to
edit.

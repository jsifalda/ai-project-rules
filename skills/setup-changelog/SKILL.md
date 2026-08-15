---
name: setup-changelog
description: RESTRICTED-INVOCATION — do NOT auto-trigger. The only entry points are the literal `/setup-changelog` command and `setup-aiengineering` Step 6. Every paraphrase is an ANTI-TRIGGER. When invoked through one of those — bootstrap a per-session changelog system in any project. Creates changelog/ directory, adds policy to AGENTS.md or CLAUDE.md, and optionally freezes an existing changelog.md. Do NOT use to write one changelog entry in a project that already has the system.
---

# Changelog Setup

## Invocation (check this first)

These are the only entry points allowed:

1. The user types the literal slash command `/setup-changelog`.
2. `setup-aiengineering` reaches Step 6 and delegates the Changelog module.

Everything else is an anti-trigger. None of these load this skill — "add a changelog", "start
tracking changes", "we should log what we did", or any other paraphrase. This skill creates a
`changelog/` directory and appends a policy section to the project's agent-instructions file, so
a wrong trigger changes files the user did not ask about. Writing one changelog entry is not
this skill.

This rule is prompt-enforced, not harness-enforced. This skill deliberately carries no
`disable-model-invocation` flag, because that flag is a binary block with no per-caller
allowlist — it removes the skill from the Skill tool entirely, so a dependent skill's delegation
step fails with `cannot be used with Skill tool`. Do not re-add it to "tighten" invocation
without first removing every dependent skill's delegation step.

Set up a per-session, file-per-change changelog system in any project. Each agent session records what changed and why in a dedicated file — no automation, no tooling, just documented policy.

## When to use

See `## Invocation` above. Those two entry points are the only ones. A user who describes
wanting a changelog is not one of them — offer `/setup-changelog` and wait for them to run it.

## Workflow

### Step 1: Assess current state

Check the project for:
1. Existing `changelog/` directory
2. Existing `changelog.md` at root
3. Existing `AGENTS.md` or `.claude/CLAUDE.md` (project-level agent instructions)

### Step 2: Create changelog directory

```bash
mkdir -p changelog
touch changelog/.gitkeep
```

If `changelog/` already exists with entries, skip this step.

### Step 3: Freeze existing changelog (if applicable)

If `changelog.md` exists at root:
- Add a freeze notice at the top (after any title):
  ```markdown
  > **Frozen archive** — do not edit. New entries go in `changelog/` as individual files.
  ```
- Do NOT delete or move the file

If no `changelog.md` exists, skip this step.

### Step 4: Inject changelog policy

Read the full policy template from [references/policy-template.md](references/policy-template.md).

Find the target file in this priority order:
1. `AGENTS.md` at project root
2. `.claude/CLAUDE.md` (project-scoped Claude instructions)
3. `CLAUDE.md` at project root

If the target file exists, append the policy section. If none exist, create `AGENTS.md` at root with the policy.

**Before injecting**: Check if a `## Changelog` section already exists in the target — if so, ask the user whether to replace or skip.

### Step 5: Verify

Confirm to the user:
- `changelog/` directory created with `.gitkeep`
- Policy injected into `[target file]`
- Existing `changelog.md` frozen (if applicable)

## Changelog entry format (quick reference)

**When to create one**: only for a change worth a future reader knowing — code/config/behavior changes, structural or dependency changes, or any destructive / hard-to-reverse action (always log those). Skip low-impact work: creating a standalone note or scratch md file, read-only research, trivial no-impact edits. Full criteria live in the policy template.

**Filename**: `changelog/YYYYMMDDHHMMSS-short-slug.md`
- Timestamp: 14-digit format (e.g., `20260412114500`)
- Slug: 2-5 word kebab-case (e.g., `fix-auth-redirect`, `add-token-tracking`)

**Content**:
```markdown
# Short title of the change

- What was done (brief, bullet points)
- Why it was done
- New dependency: `package-name` (if any were added)
```

## Rules

- Only create an entry for real changes or destructive actions — skip trivial/no-impact work like dropping a new note file (full criteria in the policy template)
- Never edit existing changelog files — always create a new one
- One file per agent session (multiple related changes go in same file)
- Focus on **why** over **how** — no technical implementation details
- Keep it concise

## References

- [Policy template](references/policy-template.md) — full text to inject into AGENTS.md/CLAUDE.md

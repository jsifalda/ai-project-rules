---
name: changelog-setup
description: Bootstrap a per-session changelog system in any project. Creates changelog/ directory, adds policy to AGENTS.md or CLAUDE.md, and optionally freezes an existing changelog.md. Use when setting up changelogs, initializing project change tracking, or the user mentions "changelog setup".
---

# Changelog Setup

Set up a per-session, file-per-change changelog system in any project. Each agent session records what changed and why in a dedicated file — no automation, no tooling, just documented policy.

## When to use

- User asks to "set up changelogs" or "add changelog tracking" to a project
- User wants to replicate the per-session changelog pattern in a new repo
- User mentions "changelog setup" or "initialize changelog"

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

- Never edit existing changelog files — always create a new one
- One file per agent session (multiple related changes go in same file)
- Focus on **why** over **how** — no technical implementation details
- Keep it concise

## References

- [Policy template](references/policy-template.md) — full text to inject into AGENTS.md/CLAUDE.md

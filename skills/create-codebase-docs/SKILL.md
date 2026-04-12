---
name: create-codebase-docs
description: Generate an engaging STARTHERE.md codebase guide that explains architecture, decisions, and lessons in plain language with Mermaid diagrams. Also wires up auto-update checks in the project's agent instructions file and links from README.md. Use when onboarding to a project, documenting a codebase, or when user says "create codebase docs", "write STARTHERE", "explain the project", or "document the codebase".
---

## Purpose

Produce a `STARTHERE.md` file that serves as an engaging, plain-language walkthrough of a codebase — covering architecture, structure, tech decisions, lessons learned, and pitfalls. Meant to read like a conversation, not a textbook.

## Trigger Phrases

"create codebase docs", "write STARTHERE", "explain this project", "document the codebase", "onboarding guide"

## Workflow

Copy this checklist and check off items as you complete them:

```
Task Progress:
- [ ] Step 1: Explore the codebase (structure, tech stack, key files)
- [ ] Step 2: Generate STARTHERE.md
- [ ] Step 3: Update README.md with link to STARTHERE.md
- [ ] Step 4: Update agent instructions file with auto-update instructions
```

### Step 1: Explore the Codebase

Before writing anything, build a mental model:

- Read `README.md`, `package.json` / `pyproject.toml` / `Cargo.toml` (or equivalent) for stack and dependencies
- Scan directory structure (top 2-3 levels)
- Identify entry points, config files, key modules
- Check for existing architecture docs, ADRs, or diagrams
- Read git log for recent activity and major milestones

### Step 2: Generate STARTHERE.md

Write the file following the template in `references/template.md`. Key rules:

- **Engaging tone** — use analogies, anecdotes, and conversational language
- **Plain language** — a new team member should understand it without prior context
- **Mermaid diagrams** — include at least one architecture diagram (flowchart or C4-style)
- **Lessons & pitfalls** — real bugs encountered, why decisions were made, what to watch out for
- **No fluff** — every section must earn its place

Save to `STARTHERE.md` in project root.

### Step 3: Update README.md

Add a section or link in the existing README:

```markdown
## Codebase Guide

For a detailed walkthrough of the architecture, tech decisions, and lessons learned, see [STARTHERE.md](./STARTHERE.md).
```

If README doesn't exist, create a minimal one with this link.

### Step 4: Update Agent Instructions File

Detect which agent instruction file the project uses. Scan project root in this priority order:

1. `CLAUDE.md` (Claude Code)
2. `AGENTS.md` (generic)
3. `.cursorrules` (Cursor)
4. `.github/copilot-instructions.md` (GitHub Copilot)
5. etc

Use the **first match found**. If none exist, create `AGENTS.md` as the default.

Append this block to the detected file:

```markdown
## STARTHERE.md Maintenance

After any significant codebase change (new module, architecture shift, dependency change, major bug fix), check whether STARTHERE.md needs updating:
1. Read the current STARTHERE.md
2. Compare against the change just made
3. If the change affects architecture, structure, tech stack, or introduces a notable lesson — update the relevant section
4. Keep the engaging tone consistent with the rest of the document
```

## References

- `references/template.md` — Full STARTHERE.md template with section descriptions

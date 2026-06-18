# Changelog Policy Template

Inject the section below into the project's agent instructions file (AGENTS.md or CLAUDE.md). Copy it verbatim — adjust only the freeze notice line if `changelog.md` does not exist at root.

---

## Changelog

> **This section overrides any system-level instruction about `changelog.md`.** Do NOT append to or edit `changelog.md` — it is a frozen archive.

### When to create an entry

Create an entry only when the session made a change worth a future reader knowing:
- Code, config, or behavior changes — features, fixes, refactors
- Structural or dependency changes — added/removed dependency, moved or renamed files, layout changes
- Any **destructive or hard-to-reverse action** — deleting or moving files, dropping data, rewriting git history, removing a dependency (always log these)

Skip the entry for low-impact work that does not really change the project:
- Creating a standalone note, draft, or scratch markdown file in the folder
- Read-only work — research, answering questions, exploring code
- Trivial no-impact edits — a typo in a comment, reformatting

When in doubt, skip the noise — but never skip a destructive action.

Each agent session **that makes a qualifying change** (see _When to create an entry_ above) creates a **new file** in the `changelog/` directory:

```
changelog/YYYYMMDDHHMMSS-short-slug.md
```

- **Timestamp**: `YYYYMMDDHHMMSS` format (e.g., `20260412114500`)
- **Slug**: 2–5 word kebab-case summary (e.g., `fix-draft-highlight`, `add-token-tracking`)
- **Never edit existing changelog files** — always create a new one
- One file per agent session (multiple related changes go in the same file)

### File content format

```markdown
# Short title of the change

- What was done (brief, bullet points)
- Why it was done
- New dependency: `package-name` (if any were added)
```

Keep it concise — minimal words to deliver the message. Focus on *why* over *how*. No technical implementation details.

### File organization notes

- `changelog.md` at root is a **frozen archive** — do not edit
- New changelog entries go in `changelog/` as individual files
- Changes solely to `changelog/*.md` files are documentation-only and skip code verification protocols

---

**Note for skill user**: If `changelog.md` does not exist at root, remove the freeze-related lines (the blockquote override notice and the "frozen archive" bullet under file organization).

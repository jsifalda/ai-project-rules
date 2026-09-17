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
- Creating a standalone note, draft, or scratch markdown file
- Read-only work — research, answering questions, exploring code
- Trivial no-impact edits — a typo in a comment, reformatting

When in doubt, skip the noise — but never skip a destructive action.

A session **that makes a qualifying change** (see _When to create an entry_ above) records it in the `changelog/` directory. One branch holds one entry, however many sessions build it, so one PR carries one entry.

1. Find the entry this branch already holds. The first command lists the committed entries this branch adds over the default branch, the second lists the uncommitted ones — staged, unstaged, or untracked:

   ```
   BASE="$(git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null || git rev-parse --verify -q --abbrev-ref main || git rev-parse --verify -q --abbrev-ref master)"
   git diff --name-only --diff-filter=A "$BASE...HEAD" -- changelog/
   git status --porcelain -- changelog/
   ```

   `BASE` empty → run `git remote set-head origin -a` once, or name the default branch by hand.

2. One exists → **extend it**. Append bullets for this session's change. Keep the filename. Retitle only when the title no longer covers the whole entry. Condense as you append, so the entry stays short.
3. None exists → create a **new file**:

   ```
   changelog/YYYYMMDDHHMMSS-short-slug.md
   ```

- **Timestamp**: `YYYYMMDDHHMMSS` format (e.g., `20260412114500`)
- **Slug**: 2–5 word kebab-case summary (e.g., `fix-draft-highlight`, `add-token-tracking`)
- **Never edit an entry that is already on the default branch** — a merged entry is history. Only the current branch's own entry is open for edits.
- One file per branch. On the default branch itself, one file per session (multiple related changes go in the same file).

### File content format

```markdown
# Short title of the change

- What was done (brief, bullet points)
- Why it was done
- New dependency: `package-name` (if any were added)
```

80 words maximum per entry. Focus on *why* over *how*. No technical implementation details.

### File organization notes

- `changelog.md` at root is a **frozen archive** — do not edit
- Changelog entries live in `changelog/` as individual files, one per branch
- Changes solely to `changelog/*.md` files are documentation-only and skip code verification protocols

---

**Note for skill user**: If `changelog.md` does not exist at root, remove the freeze-related lines (the blockquote override notice and the "frozen archive" bullet under file organization).

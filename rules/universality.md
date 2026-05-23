---
type: "always_apply"
---

# Universality requirement

This repo is **public and reusable**. Every skill, rule, script, and instruction added here must work for any reader without modification. Treat any new file as if a stranger will read it tomorrow on a different machine, with a different name, at a different company.

**Do not commit personal data, secrets, employer-specific names, or hardcoded identities into this repo.** If you need machine-specific or person-specific context to make something work, take it from an env var, a runtime prompt, or the agent's private memory — not from a file checked into this tree.

## What "non-universal" means

| Category | Forbidden | Use instead |
|---|---|---|
| Filesystem paths | `/Users/<name>/...`, `/home/<name>/...`, `C:\Users\<name>\...` | `~`, `${HOME}`, repo-relative paths, or `$(dirname "$0")`-derived paths |
| People | Real personal names, handles, emails, account/mention IDs | `<your-name>`, `<USER>`, generic placeholders, or "the user" |
| Employer / org | Company names, team names, internal product codenames | `<your-company>`, `<team>`, or omit entirely |
| Internal URLs | `*.internal`, internal Confluence space slugs, intranet hosts | Public docs links, or instruct the reader to set their own |
| Project IDs | Specific JIRA project keys (`ABC-`), Linear slugs, Notion DB IDs | `<PROJECT-KEY>` placeholder + a "configure this" note |
| Secrets | API keys, tokens, OAuth client IDs/secrets, passwords | `$ENV_VAR` references; never literal values, even fake-looking ones |
| Account IDs | Atlassian accountIds, Slack user IDs, GitHub user numeric IDs | "lookup at runtime" or `<account-id>` |
| Personal directories | Obsidian vault paths, dotfile locations specific to one machine | Ask the user at runtime, or read from a config var |
| Personal preferences as universal rules | "We always do X here" without justification | Either justify universally, or move to the user's private global memory |

Generic engineering preferences with universal rationale (e.g. "prefer pnpm because of lockfile speed") are fine — these are advice, not identity.

## Worked examples

**Bad — absolute personal path:**
```bash
bash /Users/alice/instructions/skills/foo/scripts/sync.sh
```
**Good — portable, derived at runtime:**
```bash
bash "$(dirname "$0")/scripts/sync.sh"
```

**Bad — hardcoded org context inside a skill:**
```markdown
Search the `ACME` Confluence space, then post to #acme-eng in Slack.
```
**Good — parametrised:**
```markdown
Search the configured Confluence space (`$CONFLUENCE_SPACE`), then post to the channel the user specifies.
```

**Bad — embedded secret-shaped value:**
```yaml
api_key: "sk-live-abc123def456..."
```
**Good — env var reference:**
```yaml
api_key: "$OPENAI_API_KEY"
```

**Bad — leaked teammate identity:**
```markdown
Ping Bob Smith (accountId `5f8e9c...`) when the ticket is ready.
```
**Good — runtime lookup:**
```markdown
Ping the ticket's reporter (lookup via the issue's `reporter.accountId`).
```

## The scanner

A grep-based scanner enforces this policy:

```bash
# scan the whole repo
bash scripts/check-universality.sh

# scan specific files (used by the pre-commit hook)
bash scripts/check-universality.sh path/to/file1 path/to/file2
```

It flags:
- Absolute paths containing `/Users/<name>/`, `/home/<name>/`, `C:\Users\<name>\`
- Names listed in `scripts/universality-denylist.txt` (clone-local, gitignored — each contributor adds their own name + employer there)
- Common secret shapes: `api_key="..."`, AWS access keys (`AKIA...`), GitHub PATs (`ghp_...`), Slack tokens (`xox[baprs]-`)
- Internal hostname suffixes: `*.internal`, `*.corp`

Exit code 0 means clean. Non-zero means commit blocked (unless `--no-verify` is used as an escape hatch).

## Setup for new clones

After cloning this repo once, run:

```bash
bash scripts/install-hooks.sh
```

This sets `core.hooksPath=.githooks` so the pre-commit scanner runs locally. It's idempotent and uses only `git config` — no dependencies installed.

Then create your local denylist:

```bash
cp scripts/universality-denylist.txt.example scripts/universality-denylist.txt
# edit it to include your own name, employer, internal team names, etc.
```

## When you find a violation

Don't bypass — fix the source. Replace the leaked value with a placeholder, env var, or runtime lookup. If the content genuinely belongs in *some* file, ask whether it belongs in the user's private global memory (e.g. `~/.claude/memory/`) instead of this public repo.

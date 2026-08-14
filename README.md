# instructions

Jiri's personal monorepo of AI-tool instructions: rules, skills, and slash commands consumed by Claude Code, Copilot CLI, Gemini CLI, Cursor, and any other agent that can read markdown.

Everything here is tool-agnostic where possible. Each AI tool picks up what it needs through its own loading mechanism (Claude Code via the sync hook, Cursor via `@file` references, Gemini CLI via its commands directory, etc.).

## Repository layout

| Path | Purpose |
| --- | --- |
| `rules/` | Always-apply rule files (`type: "always_apply"` frontmatter) — coding standards, restrictions, writing style (ASD-STE100) |
| `skills/` | Agent skills following the [agentskills.io](https://agentskills.io/specification) spec. Each subdir has a `SKILL.md` |
| `gemini-cli/commands/` | `.toml` slash commands for Gemini CLI (`description` + `prompt` with `{{args}}`) |
| `create-prd.md`, `generate-tasks.md`, `process-task-list.md`, `feature-request.md` | Standalone PRD workflow prompts (the original "AI Dev Tasks" pipeline) |
| `CLAUDE.md` / `AGENTS.md` | Project instructions for AI tools. `AGENTS.md` is a symlink to `CLAUDE.md` |
| `changelog/` | One entry file per agent session, `YYYYMMDDHHMMSS-short-slug.md` |
| `changelog.md` | **Frozen archive** of pre-`changelog/` entries — do not edit or append |
| `scripts/`, `.githooks/` | Universality scanner, hook installer, the tracked `pre-commit` hook, and the upstream skill-sync scripts (see [Upstream skill sync](#upstream-skill-sync)) |
| `_prds/`, `_tasks/`, `_tickets/` | Generated outputs from the PRD workflow (gitignored) |

## How it gets into Claude Code & Copilot CLI

A `SessionStart` hook symlinks every `skills/*/` folder into `~/.claude/skills/`, so skills appear automatically inside Claude Code at every session start — no manual install step.

The canonical hook script lives in this repo at `skills/setup-skills-autorefresh/scripts/sync-skills.js`. It syncs whatever **source folder is passed to it as an argument** (and prunes symlinks for skills you've removed). Register it on a machine with the bundled `setup-skills-autorefresh` skill, which bakes the folder into the hook command in `~/.claude/settings.json`:

```bash
bash skills/setup-skills-autorefresh/scripts/install.sh ~/instructions/skills
```

- **Copilot CLI** uses a parallel script at `~/.copilot/hooks/sync-skills.js` that copies (not symlinks, [github/copilot-cli#1021](https://github.com/github/copilot-cli/issues/1021)) skills into `~/.copilot/skills/`.

The hook script is the source of truth for the sync behaviour — read it directly if you need to debug.

## How it gets into Claude's chat surfaces

The symlink hook only reaches CLI tools that read the filesystem. To use these skills in Claude on iOS, Desktop, or the web, they have to be served over a remote MCP connector instead.

The companion `skills-mcp` server does that: it clones a repo laid out like this one, parses each `SKILL.md` frontmatter, and exposes **one MCP tool per skill** — the tool description is the skill's `description`, so Claude can pick a skill implicitly rather than you naming it. It polls the tracked branch, so a skill edited and pushed here reaches connected clients without any client-side step. It is read-only and serves nothing outside the skills tree.

You host it yourself — there is no shared instance. Point it at your own fork and connect it with your own domain and credentials.

### Running it on your own server

The shape of a working deployment, if you want to reproduce it:

- A small service speaking **MCP over Streamable HTTP**, bound to **loopback only** and never exposed directly. It keeps a clone of the skills repo on disk and re-reads it when the tracked branch moves.
- Configuration entirely through environment variables: the git URL and branch to track, a bearer token, the credentials for the login gate in front of the OAuth flow, and the `Host` / `Origin` allowlists the MCP transport enforces. Both allowlists must name the public hostname and the client's origin, or every MCP call is rejected (`421` / `403`) while the discovery endpoints keep answering normally — a failure that looks like a working server.
- A **TLS reverse proxy** in front. Leave the discovery and OAuth endpoints reachable, since clients need them to authenticate; the MCP and token endpoints can additionally be restricted to your client's egress range for defence in depth.
- Give the connector the **full endpoint URL, ending in `/mcp`**. With a bare origin, OAuth still completes and the client reports *connected* — then every MCP call `404`s and the tool list is silently empty.
- Keep it **read-only**: register no write tools, and resolve every requested file against the skill's own directory, rejecting `..`, absolute paths, and symlinks that escape the tree.

## Rules

The rule files under `rules/`. The `type` frontmatter is a convention for tools that honor it; in this setup a file loads only because `CLAUDE.md` names it.

- `rules/general.md` — core principles, coding standards, testing (TDD mandatory), restrictions, file-length limits, writing style (ASD-STE100 Simplified Technical English, plus scannability and terseness), the ban on stating how many items a set holds, git commit format.
- `rules/builder.md` — task-first guidance for picking an app stack (selection criteria plus a default-tools footnote), for new-app builds.

`CLAUDE.md`'s First Action loads `rules/general.md` on every session, before anything else. `rules/builder.md` is loaded on demand instead, only when a new-app build or a stack/tooling choice is in play. Frontend design thinking and aesthetics guidelines live in the `frontend-design` skill (see the Skills table).

## Skills

Each skill is a directory under `skills/` containing a `SKILL.md` with `name`, `description`, and (optional) `metadata` frontmatter, followed by the skill body. See the [agentskills.io spec](https://agentskills.io/specification) for the format. The table below lists every skill in the repo — keep it in sync when you add, remove, or rename one. Each skill name links to its `SKILL.md`; new rows should link the name to `skills/<name>/SKILL.md` the same way.

The **Depends on** column lists other skills in this repo that the skill invokes or requires to function (`—` if none). It is mandatory: every row must declare its dependencies. A skill that only points the reader to another skill ("use X instead") or is synced from an upstream repo does not "depend on" it — leave the cell `—`.

The **Origin** column marks skills pulled from an upstream repo — link to that upstream repo's root (e.g. `mattpocock/skills`, `kepano/obsidian-skills`), or `—` for skills native to this repo. It is mandatory: every row must declare it.

| Skill | What it does | Depends on | Origin |
| --- | --- | --- | --- |
| [`apple-mail-query`](skills/apple-mail-query/SKILL.md) | Query the local Apple Mail (Mail.app) SQLite DB on macOS to list, search, count, or extract emails (read-only snapshot). | — | — |
| [`apple-mail-thread-export`](skills/apple-mail-thread-export/SKILL.md) | Export Apple Mail conversation threads from a sender into one markdown file per thread, with an incremental manifest so re-runs only write new or changed threads. | — | — |
| [`audit-instructions`](skills/audit-instructions/SKILL.md) | Audit every instruction loaded in the current session's context and report all contradictions — inventories atomic rules, normalises each to a WHEN/DO/ON/UNLESS form, compares only overlapping triggers, and classifies each clash by type with verbatim evidence, severity, and paste-ready fix wording. Reports only, never rewrites. Slash-only. | — | — |
| [`better-plan`](skills/better-plan/SKILL.md) | Chained planning ritual: enhance the request via prompt-enhancer, build a plan (plan-mode rigor), stress-test it via grill-me, then cost-route tasks via op; runs inside plan mode, so the routed plan lands in the plan file and goes through the native approval gate before it executes, then ships it as a PR via ship-pr once verification is green and nothing is left awaiting you. Slash-only. | `grill-me`, `op`, `prompt-enhancer`, `ship-pr` | — |
| [`brave-submit-site`](skills/brave-submit-site/SKILL.md) | Submit a site URL or bare domain to Brave Search for indexing or re-fetching via the public `search.brave.com/submit-url` form, driven with Playwright; confirms the Success state and explains how to verify indexing later. | — | — |
| [`claude-allow-home`](skills/claude-allow-home/SKILL.md) | Mark a folder as trusted in Claude Code (sets `hasTrustDialogAccepted`), skipping the interactive trust prompt. | — | — |
| [`code-review-full`](skills/code-review-full/SKILL.md) | Runs independent reviews concurrently against one pinned diff (correctness, structure, a direct read, Jira spec conformance, and security), verifies every claim against real code and drops the false ones, triages survivors through a council, then reports at most 5 findings plus paste-ready comments and one offline HTML report that opens automatically — finally offering to post those comments to the MR or PR one at a time, each only if you approve it. The security lens uses the host's `security-review` skill when one is available and runs inline otherwise. Never edits, commits, or pushes. Slash-only. | `code-review-nuclear`, `council` | — |
| [`code-review-nuclear`](skills/code-review-nuclear/SKILL.md) | Strict single-axis structural/architectural review of a diff or branch — hunts "code judo" moves that delete whole branches, layers, or abstractions, scored against Fowler smells and a fixed set of non-negotiable standards. Not a correctness, style, or security review. | — | — |
| [`council`](skills/council/SKILL.md) | Run a question or decision through a council of AI advisors that analyze, peer-review, and synthesize a verdict. | — | — |
| [`council-v2`](skills/council-v2/SKILL.md) | Run a decision through a routed council of reasoning modes and personas that analyze, peer-review, and synthesize a verdict. | `first-principles-mode`, `founder-thinking-mode`, `persona-stanier`, `persona-levelsio` | — |
| [`create-codebase-docs`](skills/create-codebase-docs/SKILL.md) | Generate an engaging `STARTHERE.md` codebase guide (architecture, decisions, Mermaid diagrams) and wire up auto-update checks. | — | — |
| [`create-implementation-plan`](skills/create-implementation-plan/SKILL.md) | Generate a concise, machine-friendly implementation-plan template for engineering work. | — | — |
| [`create-product-vision`](skills/create-product-vision/SKILL.md) | Turn a short product or project description into one tight, motivating vision doc covering motivation, practical, and product angles, with the tagline offered in several wordings (motivational main, practical and product-descriptive alternatives). | `write-like-human` | — |
| [`create-skill`](skills/create-skill/SKILL.md) | Guide for authoring or updating a skill — SKILL.md structure, conventions, and validation. | — | — |
| [`create-svg-image`](skills/create-svg-image/SKILL.md) | Generate production-quality SVG images (banners, cards, OG images, badges) from a text description. | — | — |
| [`create-svg-logo`](skills/create-svg-logo/SKILL.md) | Create professional SVG logos from a description — multiple concepts, layout lockups, colour variations, and a usage-guidelines document. | — | — |
| [`deep-research`](skills/deep-research/SKILL.md) | Conduct multi-source research with synthesis, citation tracking, and claim verification. | — | — |
| [`defuddle`](skills/defuddle/SKILL.md) | Extract clean markdown from web pages with the Defuddle CLI (strips clutter) to save tokens. | — | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) |
| [`distill-notes`](skills/distill-notes/SKILL.md) | Distill raw notes into a sharp set of standalone maxims (drop 40-60% of ideas, compress to <=8 words, sharpen into antithesis/couplets); returns them in chat, then asks whether to also save to a .md file. | — | — |
| [`distill-notes-v2`](skills/distill-notes-v2/SKILL.md) | Process notes that mix facts with heuristics — organize the facts losslessly (grouped by category, deadlines flagged, every value verbatim) and distill the heuristics into sharpened maxims; returns both sections in chat, then asks whether to also save to a .md file. | — | — |
| [`distill-persona`](skills/distill-persona/SKILL.md) | Distill a leader's worldview from interview transcripts into a reusable advisor persona. | — | — |
| [`find-skills`](skills/find-skills/SKILL.md) | Find a skill in the public skills.sh registry and clone an approved one into the current project — checks what you already have first, security-reviews every file before it lands, never installs anything globally. | — | [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| [`first-principles-mode`](skills/first-principles-mode/SKILL.md) | Strip a problem back to fundamental truths and rebuild the answer from only what's verifiable. | — | — |
| [`founder-thinking-mode`](skills/founder-thinking-mode/SKILL.md) | Answer in a blunt founder-operator voice — the specific decision, the trade-off, and the real risk. | — | — |
| [`frontend-design`](skills/frontend-design/SKILL.md) | Create distinctive, production-grade frontend UI that avoids generic AI aesthetics. | — | — |
| [`generate-prd-tasks`](skills/generate-prd-tasks/SKILL.md) | Turn a PRD into a step-by-step developer task list (parent tasks + sub-tasks). | — | — |
| [`goal-breakdown`](skills/goal-breakdown/SKILL.md) | Break a big finite goal into a sharp end state, ordered milestones (riskiest first), and one-day tasks with a single clear next action; re-plans as milestones complete. | — | — |
| [`grill-me`](skills/grill-me/SKILL.md) | Interview the user relentlessly about a plan, design, or decision until reaching shared understanding, one question at a time. | — | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [`handoff`](skills/handoff/SKILL.md) | Compact the current conversation into a handoff document for another agent to pick up. | — | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [`highlight-key-takeaways`](skills/highlight-key-takeaways/SKILL.md) | Highlight the key takeaways in an Obsidian note with `==highlight==` syntax, in place. | — | — |
| [`i-have-adhd`](skills/i-have-adhd/SKILL.md) | Reshape every response for an ADHD reader — action first, numbered steps, restated state, concrete time estimates, no preamble or closers. Invoked bare mid-session with work in flight, it opens by catching you up on where the work stands. Manual-invoke only. | — | [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) |
| [`indie-hacker-wrapup`](skills/indie-hacker-wrapup/SKILL.md) | End-of-session ritual that mines the session across lenses (the product built and the craft behind it), scores angles against a resonance bar, and drafts the strongest build-in-public post (or declines when nothing clears it), tracking past angles to repeat one only on stronger evidence. | `write-like-human` | — |
| [`json-canvas`](skills/json-canvas/SKILL.md) | Create and edit JSON Canvas (`.canvas`) files — nodes, edges, groups, connections. | — | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) |
| [`landing-page-copy`](skills/landing-page-copy/SKILL.md) | Write a landing page from a product description, or improve an existing one (paste, file, or URL) — both driven by a scored loop over a conversion blueprint that rewrites what fails and re-scores until it converges. | `create-product-vision`, `defuddle` | — |
| [`landing-page-viral-grill`](skills/landing-page-viral-grill/SKILL.md) | Audit a landing page against a viral checklist file, one verdict per check, then grill the gaps and plan the fixes. | `grill-me`, `defuddle` | — |
| [`loop-todos`](skills/loop-todos/SKILL.md) | Manual `/loop-todos` only — starts a self-cancelling recurring loop that claims one open backlog entry per firing, writes a plan for it, implements that plan, verifies it against the host project's own gates, closes it, updates stale docs, and opens one stacked pull request per entry. | `loop`, `setup-todo-backlog`, `ship-pr` | — |
| [`markdown`](skills/markdown/SKILL.md) | Create, refine, or convert content into strictly formatted, export-ready Markdown. | — | — |
| [`microsoft-clarity`](skills/microsoft-clarity/SKILL.md) | Add Microsoft Clarity analytics (heatmaps, session recordings) to a Next.js app. | — | — |
| [`nextjs-ga-tracking`](skills/nextjs-ga-tracking/SKILL.md) | Add GA4 tracking with GDPR-compliant Silktide cookie consent to a Next.js project. | — | — |
| [`obsidian-bases`](skills/obsidian-bases/SKILL.md) | Create and edit Obsidian Bases (`.base`) — views, filters, formulas, summaries. | — | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) |
| [`obsidian-cli`](skills/obsidian-cli/SKILL.md) | Interact with Obsidian vaults via the Obsidian CLI (read/create/search notes; plugin/theme dev + debug). | — | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) |
| [`obsidian-markdown`](skills/obsidian-markdown/SKILL.md) | Create and edit Obsidian Flavored Markdown (wikilinks, embeds, callouts, properties). | — | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) |
| [`obsidian-task-extractor`](skills/obsidian-task-extractor/SKILL.md) | Extract atomic tasks from a note and add them to `To Remember.md`. | — | — |
| [`op`](skills/op/SKILL.md) | Route each task in a plan to the cheapest capable Claude model (Haiku/Sonnet/Opus), then execute by dispatching tasks as subagents on their assigned model. | — | — |
| [`optimize-my-cv`](skills/optimize-my-cv/SKILL.md) | Audit a CV against a two-track rubric (tech IC or engineering leadership) and return a severity-ranked gap analysis plus an ordered remediation plan — it never rewrites the CV. | — | — |
| [`pdf`](skills/pdf/SKILL.md) | PDF toolkit — extract text/tables, create, merge/split, and fill forms at scale. | — | — |
| [`pdf-to-md`](skills/pdf-to-md/SKILL.md) | Convert a text-based PDF into one clean, structured Markdown file — layout-aware extraction, auto-strips page furniture, reflows paragraphs, maps structure to headings. | — | — |
| [`persona-levelsio`](skills/persona-levelsio/SKILL.md) | Channel Pieter Levels (levelsio) as a solo bootstrapped indie-hacker advisor, grounded in his frameworks and build-in-public voice. | — | — |
| [`persona-luca`](skills/persona-luca/SKILL.md) | Channel Luca Rossi (Refactoring newsletter) as an engineering-leadership advisor, grounded in his articles and named mental models. | — | — |
| [`persona-stanier`](skills/persona-stanier/SKILL.md) | Channel James Stanier as an engineering-leadership advisor, grounded in his blog posts and frameworks. | — | — |
| [`prd-creator`](skills/prd-creator/SKILL.md) | Generate lean, scannable PRDs in Markdown via a clarifying-questions interview. | `grill-me` (optional) | — |
| [`prompt-enhancer`](skills/prompt-enhancer/SKILL.md) | Transform a simple prompt into a high-quality, structured one for better AI results. | — | — |
| [`prototype`](skills/prototype/SKILL.md) | Build a throwaway prototype to flesh out a design, as a runnable terminal app or several toggleable UI variations. | — | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [`qmd-project`](skills/qmd-project/SKILL.md) | Turn any folder into a folder-local qmd semantic index over its nested `.md` files (isolated from the global index, shared models) and ship a project-local `qmd-ask` skill that answers questions from it. | — | — |
| [`radical-feedback`](skills/radical-feedback/SKILL.md) | Diagnose and improve feedback with Kim Scott's Radical Candor framework, or generate well-structured feedback for a situation. | — | — |
| [`reddit-post`](skills/reddit-post/SKILL.md) | Create high-engagement Reddit posts (title + body) from a guided questionnaire. | — | — |
| [`rewrite`](skills/rewrite/SKILL.md) | Improve, correct, or rephrase text in its own language (DeepL Write style) with Simple/Business/Academic/Casual styles and Enthusiastic/Friendly/Confident/Diplomatic tones. Improve mode loads the write-like-human ruleset first so default output reads human. | `write-like-human` | — |
| [`seo-keyword-generator`](skills/seo-keyword-generator/SKILL.md) | Generate a categorized SEO keyword strategy for a side project via a questionnaire. | — | — |
| [`setup-adrs`](skills/setup-adrs/SKILL.md) | Bootstrap an Architecture Decision Record (ADR) system in any project — ADR dir + template + seed record ADR, `ARCHITECTURE.md` recap, and an ADR policy injected into AGENTS.md/CLAUDE.md. | — | — |
| [`setup-aiengineering`](skills/setup-aiengineering/SKILL.md) | Bootstrap a repo's AI-engineering baseline — inject verification/git/file-org/writing-style policy blocks (plus an opt-in PRD gate) into AGENTS.md/CLAUDE.md, delegate ADRs/changelog/user-scenarios/TODO-backlog to their setup skills, and scaffold a worktree bootstrap hook plus a detected `.worktreeinclude`. Versioned and re-runnable — a coverage self-audit reports uncovered baseline concerns, and re-runs upgrade older setups to the current version. Stack-agnostic. | `setup-adrs`, `setup-changelog`, `setup-user-scenarios`, `setup-todo-backlog`, `find-skills` (optional), `code-review-nuclear` (optional) | — |
| [`setup-changelog`](skills/setup-changelog/SKILL.md) | Bootstrap a per-session changelog system in any project (creates `changelog/`, adds the policy to AGENTS.md/CLAUDE.md). | — | — |
| [`setup-rtk`](skills/setup-rtk/SKILL.md) | Install RTK (Rust Token Killer) on a machine for a single Claude Code profile — binary (Homebrew or official install script) + the `rtk hook claude` PreToolUse hook in settings.json, via RTK's own `rtk init`. | — | — |
| [`setup-skills-autorefresh`](skills/setup-skills-autorefresh/SKILL.md) | Install the SessionStart hook that auto-syncs skills from a chosen folder into `~/.claude/skills/`. | — | — |
| [`setup-todo-backlog`](skills/setup-todo-backlog/SKILL.md) | Bootstrap a known-issues backlog in any project — `docs/TODO.md` with dated immutable ids, optional checklist conversion, and a policy where entries are filed only on request and closed automatically on evidence. | — | — |
| [`setup-user-scenarios`](skills/setup-user-scenarios/SKILL.md) | Bootstrap a BDD user-scenarios inventory (`docs/user-scenarios.md`) + doc-sync policy in a project. | — | — |
| [`ship-pr`](skills/ship-pr/SKILL.md) | `/ship-pr`, or the ship step of a skill that depends on it — go from a dirty working tree to an open PR/MR (self-assigned to you) in one pass. | — | — |
| [`ship-v1`](skills/ship-v1/SKILL.md) | Ship the smallest live version of a side project in one weekend, post it, then let real signal decide whether to continue, pivot, or drop. An anti-roadmap protocol for unvalidated, zero-user products. | — | — |
| [`summarise-text`](skills/summarise-text/SKILL.md) | Summarise pasted text, a local file, or an Obsidian note into main idea, takeaways, and an action plan. | — | — |
| [`summarise-url`](skills/summarise-url/SKILL.md) | Fetch a link's content and return a structured summary, plus a distilled set of maxims from the same content, in one reply. | `defuddle`, `distill-notes` | — |
| [`team-code-writer`](skills/team-code-writer/SKILL.md) | Writer role for an agent dev team — implements features matching existing style and summarizes with file:line refs. Writes code only, no tests and no self-review. | — | — |
| [`team-reviewer`](skills/team-reviewer/SKILL.md) | Reviewer role for an agent dev team — read-only, runs `git diff` and reports Critical/Important/Nitpick findings with file:line, never edits. | — | — |
| [`team-ship`](skills/team-ship/SKILL.md) | Lead orchestrator — `/team-ship <task>` records the agent territories in the project's AGENTS.md/CLAUDE.md, writes a brief, dispatches the writer and tester in parallel then the reviewer on the diff, and collects one summary that produces a PR you approve. | `team-code-writer`, `team-tester`, `team-reviewer` | — |
| [`team-tester`](skills/team-tester/SKILL.md) | Tester role for an agent dev team — writes tests from the spec, blind to the implementation, covering every branch, edge case, and error path. | — | — |
| [`translate-to-czech`](skills/translate-to-czech/SKILL.md) | Translate English text to Czech while preserving accuracy. | — | — |
| [`write-like-human`](skills/write-like-human/SKILL.md) | Apply a strict style guide so prose reads as human, not AI-generated. | — | — |
| [`yt-video-finder`](skills/yt-video-finder/SKILL.md) | Drive a real Chrome browser via Playwright to search YouTube, shortlist and rate candidates by engagement + comments, then pick the single best video for the user's criteria and write it up. | — | — |

_(Inside Claude Code you may also see skills loaded from other sources; this table covers the skills defined in this repo — `ls skills/`.)_

_The four `team-*` skills (an agent dev team — a writer, a reviewer, a tester, and a `team-ship` lead that runs them) are adapted from [@zodchiii's post on X](https://x.com/zodchiii/status/2067552428627484853)._

## Upstream skill sync

Some skills in the table above started life in someone else's repo. One script per upstream pulls them in. They are run by hand from the command line, not through an agent, because the work they do (fetch a tree, diff it against a baseline, write files) is fully deterministic and needs no judgment call. Each one flattens the upstream's nested layout (skills grouped under a plugin, category, or vendor directory) into this repo's flat `skills/<name>/`.

### `scripts/sync-anthropic-skills.sh`

Pulls from `anthropics/knowledge-work-plugins`, upstream a plugin marketplace where each skill lives nested under a plugin directory (`marketing`, `engineering`, and so on) or under `partner-built/<vendor>/`.

Flags:
- `<name> ...`: one or more skill names to sync
- `--list`, `-l`: print the full upstream catalog grouped by plugin, then exit
- `--force`, `-f`: overwrite local edits instead of skipping them
- `--dest <dir>`: sync into `<dir>` instead of this repo's `skills/` (also `--dest=<dir>`)
- `--help`, `-h`: show usage and exit

Run with no names and it re-syncs the previously-synced set recorded in its state file, erroring if that set is empty. A name that exists in more than one plugin needs qualifying as `<plugin>/<name>`. Set `GITHUB_TOKEN` to raise the GitHub API rate limit.

```bash
bash scripts/sync-anthropic-skills.sh --list
bash scripts/sync-anthropic-skills.sh standup incident-response
bash scripts/sync-anthropic-skills.sh marketing/standup --force
```

Before writing a staged skill, this script also runs `scripts/sync-anthropic-contextualize.py` over it: the helper strips links pointing at files that don't exist in this repo and marks unwired connector placeholders. One limitation worth knowing: upstream skills sometimes assume MCP connectors configured at the plugin level, and flattening leaves those behind, so a synced skill that needs external data may need its connector wired up separately.

### `scripts/sync-mattpocock-skills.sh`

Pulls from `mattpocock/skills`, upstream nesting every skill under a category directory (`engineering`, `productivity`, `misc`, `deprecated`, `in-progress`).

Flags:
- `--list`, `-l`: print the upstream catalog grouped by category, then exit
- `--force`, `-f`: overwrite locally-modified skills instead of skipping them
- `--dest <dir>`: sync into `<dir>` instead of this repo's `skills/` (also `--dest=<dir>`)
- `--help`, `-h`: show usage and exit

This repo carries a curated default set, `prototype` (engineering) and `handoff` (productivity). A fresh clone has an empty state file, so name both explicitly the first time.

```bash
bash scripts/sync-mattpocock-skills.sh --list
bash scripts/sync-mattpocock-skills.sh prototype handoff
bash scripts/sync-mattpocock-skills.sh productivity/handoff --force
```

These names are refused outright, exit code 2, and `--force` does not bypass the refusal: `grilling` and `grill-me`. This repo carries the upstream `grilling` skill's body as `skills/grill-me/SKILL.md`, a deliberate fork with a different name. Syncing `grilling` under its own name would add a duplicate directory instead of refreshing the fork. Syncing upstream's own `grill-me` is worse: that name is a stub upstream, and it would overwrite the working fork with a skill that does nothing here. Both `better-plan` and `prd-creator` depend on the `grill-me` name, so this matters beyond the one skill. Pull an upstream change to it by hand instead: copy the upstream body into `skills/grill-me/SKILL.md` and keep the existing frontmatter.

### `scripts/sync-obsidian-skills.sh`

Pulls from `kepano/obsidian-skills`. It takes no skill names, always syncing a fixed set: `defuddle`, `json-canvas`, `obsidian-bases`, `obsidian-cli`, `obsidian-markdown`. Passing a name, or any unknown flag, is an error, exit code 2. Change the set by editing the `SKILLS` array near the top of the script. Set `GITHUB_TOKEN` to raise the GitHub API rate limit.

```bash
bash scripts/sync-obsidian-skills.sh
```

> **Warning:** this script has no safety net. Unlike the other sync scripts, there is no sha256 baseline, no manifest, and no `--force` gate. Every run deletes local files not present upstream and overwrites every remaining file unconditionally. Local edits to any of those skills are lost with no warning and no prompt. Commit or stash changes to them before running it.

### Overwrite safety and registering new skills

The anthropic and mattpocock scripts (not the obsidian one, see the warning above) record every file they write in a sha256 baseline. Once a local edit makes a file diverge from that baseline, the script reports the skill as locally modified and skips it instead of clobbering your changes. `scripts/.sync-state/` is gitignored, so a fresh clone starts with no baseline at all, and everything already on disk reports as locally modified on the first run. That's expected, not a bug. Reach for `--force` once you know the local copy is actually untouched.

The `## Skills` table above is maintained by hand, not generated, so a sync does not register its own output. Every sync script prints a `NEW SKILLS — REGISTER THESE` block naming what landed. After a sync, add a row for each one, linking its `Origin` cell to the upstream repo root.

## Gemini CLI commands

TOML slash commands under `gemini-cli/commands/`. Format:

```toml
description = "One-line description shown in /help"
prompt = """
Your prompt body. Use {{args}} where the user's input should be interpolated.
"""
```

Current commands: `create-prd`, `feature-request`, `generate-changelog`, `process-task-list`, `summarise`.

Gemini CLI reads from its own config path — symlink or copy this directory there to wire them up.

## PRD workflow (legacy)

The original PRD → tasks → process pipeline this repo started as. Still usable as standalone prompts when you want a structured feature-development flow with manual review gates.

1. `create-prd.md` — interview-driven PRD generation. Output: `_prds/prd-[feature-name].md`.
2. `generate-tasks.md` — break the PRD into parent tasks, then sub-tasks (with a confirmation gate between them). Output: `_tasks/tasks-[name].md`.
3. `process-task-list.md` — instructs the AI to work one sub-task at a time, waiting for approval, running tests, committing per parent task.
4. `feature-request.md` — alternative entry point: skip the PRD and go straight from a feature request to a task list.

Usage in Claude Code / Cursor: reference the file with `@create-prd.md` (or your tool's equivalent) and let it drive.

Video demo of the original workflow on [Claire Vo's "How I AI" podcast](https://www.youtube.com/watch?v=fD4ktSkNCw4).

## Contributing

Personal repo, but PRs welcome if something here is genuinely useful elsewhere. To add:

- A **skill**: create `skills/<name>/SKILL.md` following the agentskills.io spec. It will be picked up by the sync hook on next session start. Add a matching row to the [Skills](#skills) table above, linking the name to `skills/<name>/SKILL.md`, **and fill the `Depends on` cell** — list every other repo skill this one invokes or requires, or `—` if it is self-contained.
- A **rule**: add `rules/<name>.md` with `type: "always_apply"` frontmatter.
- A **Gemini command**: add `gemini-cli/commands/<name>.toml`. Add it to the Current commands list above.

**Universality requirement:** anything added here must be reusable by any reader — no personal data, secrets, employer names, internal URLs, or hardcoded identities. Full policy: the [`## Universality requirement`](CLAUDE.md#universality-requirement) section of `CLAUDE.md`. After cloning, activate the pre-commit scanner once: `bash scripts/install-hooks.sh`.

**Verification gate:** every change here runs the repo's verification gate before it is reported done — the universality scanner, the skill validator, then a CodeRabbit review and the harness's built-in code review, with `critical` and `major` *factual* findings (broken commands, dead links, wrong references) fixed automatically and everything else brought to you. Anything that would change what a rule requires always asks first, whatever its severity. Full policy: the [`## Verification Protocol (MANDATORY)`](CLAUDE.md#verification-protocol-mandatory) section of `CLAUDE.md`.

Log notable changes as a new file in `changelog/`, named `YYYYMMDDHHMMSS-short-slug.md`. The root `changelog.md` is a frozen archive — never append to it.


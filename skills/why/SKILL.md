---
name: why
description: >-
  RESTRICTED-INVOCATION skill, do NOT auto-trigger on a phrase match. The only entry points are the literal slash command /why, the user naming why and asking to run it, a step of a skill whose README Depends on cell lists why, or the agent itself when the task needs this exact output and it states the reason in one line first. Loose phrasing like "why is this like this" or "why do we do X" is an ANTI-TRIGGER, answer directly and offer /why. When invoked, investigates why code works the way it does, design rationale, why we picked Y, regressions, postmortems, or data-backed thresholds. Plans the evidence the question needs, picks the best tool per need, checks which tools are present (built-in, MCP, CLI), and queries each present source in parallel, then returns a cited, confidence-tiered read on decisions and tradeoffs. Do NOT use for how code works at runtime, use how.
license: "MIT, Copyright (c) 2026 Lauren Tan"
metadata:
  version: "1.1"
  upstream: "https://github.com/cursor/plugins"
---

# Why

## Invocation (check this first)

These are the only entry points:

1. The user types the literal slash command `/why`.
2. The user names the `why` skill and asks to run it.
3. A step of a skill whose README `Depends on` cell lists `why`.
4. The agent itself, when the current task needs this skill's exact output. State the reason in one line before you invoke it.

Anything else is an anti-trigger. Loose phrasing such as "why is this like this", "why do we do X" or "what was the reason for Y" does not load this skill. Answer directly and offer `/why`.

This rule is prompt-enforced. The skill carries no `disable-model-invocation` flag, because that flag removes the skill from the Skill tool, so entry points 3 and 4 would fail.

Investigate the motivation and intent behind code. The companion `how` skill answers what the code does and how it works. `why` answers what forces led to its shape.

Every spawn below is a subagent that keeps the session's MCP servers, because the tool-backed investigators and the synthesizer's citation spot-checks need them. Pin no model. In Claude Code, run every investigator and the synthesizer as `general-purpose`, because they must read whole PRs, tickets and docs. Add "Write nothing." to every investigator and synthesizer brief.

## Operating Posture

Operate as a **careful, cautious, and precise investigator**. Be honest about what you know vs what you're inferring. Read `references/epistemics.md` for the full confidence framework and phrasing guide. The synthesizer must follow it.

## Step 1. Understand the Target and the Question

The **target** is usually a chunk of code, a pattern, a feature, or a named design decision. The **question** is usually a design rationale, a tradeoff, a motivating edge case, an external constraint, dead code, or a broad history sweep.

If the target is vague ("why do we do it this way?" with no clear referent), make your best guess from conversation context (open files, recent edits, cursor location, what was just discussed). State your interpretation briefly so the user can redirect if you're off, then proceed.

## Step 2. Establish the Code Anchor

Before spawning investigators, build the seed context inline: file paths and line ranges, key symbols (functions, classes, constants), the last few commits touching the target, PR numbers from merge commits (pattern `(#1234)` in the subject line, or `!1234` on GitLab), and any linked ticket IDs. Run `git blame -L <start>,<end> <file>` for last-touch commits, `git log --follow -p -- <file>` for full history with patches through renames, `git log --oneline -20 -- <file>` for recent commits with PR numbers visible, and `git log -1 --format=%B <commit>` to extract PR numbers. Then pull the PR bodies and discussion for any substantive commit: `gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews`. On a GitLab remote, run `glab mr view <number> --comments` instead. This anchor goes to every investigator and to the synthesizer.

## Step 3. Spawn Parallel Investigators

**Search every planned source in parallel.** Document the null, don't skip the search.

### Plan the sources

- From the question and the code anchor, list the evidence needs. Example needs: the upstream bug that forced a version pin, the incident behind a retry, the ticket that set a threshold.
- Name the best tool for each need, then the next-best fallback.
- Add a source to the plan only when it can plausibly hold evidence for a named need. Set no numeric cap.
- Always put source control (git plus `gh` or `glab`) in the plan.

### Check availability

- Before you spawn, run a cheap read-only probe for each planned tool:
  - Built-in tools and MCP servers: read the session tool list. In Claude Code, check the built-in tools and `mcp__<server>__*`, and run tool search for deferred tools that match a planned need. Loading a tool schema is a read.
  - MCP auth: an MCP that exposes only an authenticate tool is not logged in. Record it as a gap.
  - CLIs: run `command -v <cli>`.
  - Auth: run a read-only check, such as `gh auth status` or `glab auth status`.
- Never install a tool, and never ask to install one, to fill a gap.
- Best tool absent → use the next-best present fallback, and record the swap.
- No fallback present → record a gap that names the missing tool and what it would have shown.

### Example sources

These sources are inspiration, not a closed set. Each one is good at one shape of "why", shown after "Best at". Use it to know what to expect back, and to name a gap when a source returns empty.

1. **Source control** (git history, `gh` or `glab` for PRs, code comments, tests). Always spawn, the only guaranteed source. Best at *implementation-time rationale captured during review*.
2. **Issue / ticket tracker** (e.g. Linear, Jira, GitHub Issues, Plane, Shortcut MCP). Best at *the product or business forcing function*. Strongest when the why is external to engineering.
3. **Long-form documents** (e.g. Notion, Confluence, Google Docs, Coda MCP). Best at *long-form design rationale*, written out before it becomes code.
4. **Real-time team chat** (e.g. Slack, Discord, Microsoft Teams, Mattermost MCP). Best at *real-time deliberation that never reached a doc*. Especially important when the source control, ticket, and doc paper trail is thin.
5. **Infrastructure observability** (e.g. Datadog, New Relic, Honeycomb, Grafana, Splunk MCP). Best at *infrastructure and runtime reality that motivated the code*. Strongest when the target reacts to an infra signal (timeouts, retries, rate limits, circuit breakers).
6. **Error / exception tracking** (e.g. Sentry, Rollbar, Bugsnag, Airbrake MCP). Best at *the specific exceptions and error trajectories that motivated defensive or corrective code*. Strongest for catch blocks, null guards, type checks, retries, and other defenses.
7. **Product analytics warehouse** (e.g. Databricks, Snowflake, BigQuery, ClickHouse, dbt, Redshift MCP). Best at *product and data reality that shaped the code*. Strongest for flag-gated code, experiment-driven ships, data migrations, and "where did this number come from" questions.

More examples:

- **Public web or developer search**. Best at *upstream issues, CVEs, and the changelog of a dependency*.
- **Package registry and release notes**. Best at *why a version is pinned*.
- **CI run logs** (such as `gh run`). Best at *the flaky test or build failure behind a change*.
- **Deploy or release history**. Best at *the release that a change followed or fixed*.
- **Design tools**. Best at *UI decisions*.
- **Mail and calendar**. Best at *decisions made in a meeting*.
- **Notes vault or knowledge base**. Best at *notes that never reached a shared doc*.
- **Feature-flag service**. Best at *rollout state*.

### Spawn

- Spawn one investigator per planned source that is present, all in a single message so they run concurrently. Each one owns exactly one source. Never ask one investigator to cover more than one. Source control is one source: git plus `gh` or `glab`.
- Build each investigator's prompt from `references/investigator-prompt.md`, filled in, plus:
  - a fitting playbook `references/sources/<source>.md`, found through the table in `references/source-playbook.md`, if one exists. No playbook fits → the investigator reads the tool's schema and server instructions first.
  - `references/sources/incident-postmortem.md` **if the target code looks defensive** (null checks, retry logic, timeout handling, rate limiting, feature flags, egress guards, OOM handlers)
  - the code anchor and the user's original question
  - the evidence need this source serves, and whether the user approved billable calls for it
- Guard rails:
  - Make read-only calls only. Never call a write, send, post or delete tool, even when the MCP offers one.
  - Give a public tool (web search, scrape) only public identifiers: library name, version, public error string, upstream issue URL. Never send private code or data. The agent's own egress rules apply on top.
  - Run free and included calls freely. A call is billable when the tool's server instructions or docs state a per-call price. Ask the user before you spawn an investigator whose calls are billable, and state the approval in its brief. You cannot ask (a non-interactive run) → do not spawn it, and record a gap.
  - Treat an auth failure as a gap. Never retry with other credentials.

### When to skip a source

Only with an **explicit, written justification** that goes in the final Sources Consulted. The valid reasons:

- **No tool is available for that source** in this environment, and no fallback is present. Flag it as a gap, not a choice: "Team chat → gap. No chat MCP or CLI is available, so the conversational record was not searchable."
- **The source is provably irrelevant**, not just "probably irrelevant." A high bar: "Error tracking skipped. Target is a build-time script with no runtime code path."

If your scope assessment suggests a single-commit trivial target where the PR description already contains the complete answer, you may answer inline **only after** confirming every planned source search would be redundant. Say so explicitly. This should be rare.

## Step 4. Synthesize

Spawn one synthesizer. It gets:
1. The investigator findings, including any null results
2. The source plan: for each planned source, its evidence need, best tool, and the outcome (tool used, fallback swap, gap with its reason, or skip with its reason)
3. The code anchor
4. The user's original question
5. The epistemics framework from `references/epistemics.md`
6. The synthesizer prompt template from `references/synthesizer-prompt.md`

## Step 5. Present

Present the synthesizer's output to the user. You may lightly edit for clarity or add context from the conversation, but **do not rewrite the confidence language**.

## Output Format

The structure is the one in `references/synthesizer-prompt.md`: The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, Confidence Summary. Adapt as needed, but keep the confidence separation intact, and keep Sources Consulted as one line per planned source: the tool used, a fallback swap, a gap, or a written skip reason. Include the sources that returned nothing.

After Sources Consulted, if the user's `why` question is a precursor to changing this code, convert the lineage findings into a Preserve / Change / Avoid / Risk constraint set for planning the change.

## Common Failure Modes to Avoid

- **Recency bias**. Assuming the most recent commit is authoritative. The current shape is often the accretion of many earlier decisions. Trace back.

---
name: deep-research
description: Decision-grade research in claude.ai chat or Claude Code. Answers a hard question with a verdict first, a dated claim table, primary sources, conflicts, and one concrete next action, in one screen. Loads memory and project files first so settled facts and dead ends are not redone. Enforces a freshness limit per question type, and a ground-truth test for local-availability questions. Validates its own report with two stdlib scripts in a shell. Use when the user types /deep-research, or asks for deep research, a verified answer, a comparison that ends in a decision, or research that needs several sources. Do NOT use for a single fact that one search answers, for debugging, or for long report files.
metadata:
  version: "2.0"
---

# Deep Research (v2)

You run in claude.ai chat or Claude Code. You have web search, web fetch, optional Firecrawl, memory, project files, and a shell. You have no persistent report folder and no browser.

Goal: the correct, dated, actionable verdict in the fewest words the user must read.

## 0. Should this skill run?

- One fact that one search answers → hand the question to the `deep-research-answer` skill when available. Else run the normal flow.
- Called by `deep-research-answer` → run the normal flow. Never hand the question back.
- Decision question (which, should, is it allowed, how much, how do I) → run.
- Broad landscape scan with 30+ sources for a long read → tell the user in one line that the claude.ai Research feature fits better. Run deep mode here only if they still want it.

## 1. Pick mode and class

State both at the top of the report. Do not ask the user.

| Mode | When | Tool calls | Word cap |
|---|---|---|---|
| quick | low stakes, reversible | 3 to 5 | 300 |
| standard | default | 8 to 15 | 700 |
| deep | irreversible, legal status, health, large money, animal welfare | 15 to 25 | 1,500 |

Class drives sources and freshness (see `reference/methodology.md` sections 2 and 3): `legal`, `price`, `ground-truth`, `health`, `technical`, `landscape`. Mixed question → class is the part the verdict depends on.

## 2. Phase 0: Context load (always)

1. Read the memory listing. Open files whose description matches the topic. Read project files that match. Search past chats if the user refers to earlier work.
2. Extract: format preferences, settled conclusions with their check date, dead ends, standing sources, named contacts, country source ladders.
3. Print 3 lines before any search:
   - `Known:` settled facts, with check date
   - `Dead ends:` URLs or queries that failed before, skip them
   - `Open:` what this run must find
4. Known fact inside its freshness limit → reuse it with its old check date. Outside the limit → re-verify.

## 3. Phase 1: Frame

- Write one primary question plus max 4 sub-questions. Keep every literal question the user asked.
- Name the deciding metric: the one variable that decides the outcome for this user.
- List unknowns. Ask one question only if an unknown flips the verdict and memory does not hold it. Else carry it as a stated assumption.
- Plan queries from `reference/methodology.md` section 4. Include 1 disconfirming query. Put today's month and year in time-sensitive queries. Never hard-code a year.

## 4. Phase 2: Retrieve

- Tool chain: `reference/methodology.md` section 5. Send independent searches in parallel in one message.
- Fetch the primary page for every claim the verdict depends on. Search snippets are leads, not evidence.
- Stop when every verdict claim has its required sources, or the call budget is spent.
- Keep a list of every URL that a tool returned. Phase 5 needs it.
- Log each failure (URL or query, reason) as a dead end.
- A tool that returns "No approval received" or a similar approval refusal → log it as a dead end, do not retry it this run, continue with the next tool.

## 5. Phase 3: Verify

Status per claim:

- `verified` → 2 sources from different publishers, at least 1 primary
- `single-source` → 1 source only
- `conflict` → sources disagree, tie-breaker stated
- `unverified` → leads only, or no source found

Rules:

- Follow citation chains to the origin. Three pages that quote one press release are one source.
- Run the disconfirming query. Report what it found, even "nothing".
- `ground-truth` class: web evidence never proves "X is available here now". Give a test under 10 minutes, or a phone test (who, number if known, exact question).
- No primary page reached for any claim (JS-gated, blocked, tool not approved) → the first Action is a test where the user reads the primary page, for example the official checkout or the regulator page.
- Every number is sourced `[N]`, computed (show the inputs), or marked `(est.)` or `(unverified)`.

## 6. Phase 4: Write

- Use `templates/report_template.md` exactly. Verdict first. Bullets. Short sentences.
- The user's stored style preferences override the template style defaults.
- Never pad. Never exceed the mode word cap. The user typing "expand" lifts the cap.

## 7. Phase 5: Validate (always, before you show the report)

1. Pick a scratch dir `DR`. Chat uses `~/dr/`. Claude Code uses the session scratchpad.
2. Put both scripts in `DR`.
   - Chat: fetch them with the skills MCP `skill_file` tool. Skill `deep-research`, paths `scripts/validate_report.py` and `scripts/verify_citations.py`.
   - Claude Code: copy them from this skill's `scripts/` folder.
3. Write the draft report to `DR/report.md`. Write every URL that a tool returned this run to `DR/seen_urls.txt`, one per line.
4. Run from `DR`:
   ```
   python3 validate_report.py --report report.md
   python3 verify_citations.py --report report.md --seen seen_urls.txt
   ```
5. FAIL → fix the report and run again. Max 3 rounds. Still failing → deliver, and list each open failure under `Gaps and dead ends`.
6. Show no script output to the user unless a failure stays open.

Scripts unavailable or no shell → run the manual checklist in `reference/methodology.md` section 9, and say so in one line.

## 8. Phase 6: Deliver and write back

- Show the validated report inline in chat.
- File only on request: a .md file, a doc, or email through a workflow the user has in memory.
- Draft max 3 durable facts: new conclusions with check date, new dead ends, new contacts. Save them only after the user says ok, unless a standing instruction in memory says otherwise.

## Hard rules

- Never invent a source, URL, date, or number. Missing means say missing.
- Never cite a URL that no tool returned this run.
- Never present an estimate as a lookup.
- Mark your own analysis with `Analysis:` or `(est.)`. Source facts carry `[N]`.
- No emoji, no em dashes, no semicolons in the report.

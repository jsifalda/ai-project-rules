# Adopt a writing standard and ban stated counts

## Writing standard

- `rules/general.md` `# WRITING STYLE` now names ASD-STE100 Simplified Technical English. It replaces
  loose bullets that named no standard. Its subsections are `## STE Core Rules`,
  `## STE Bans and Exceptions`, `## STE Precedence`, and `## Scannable and Terse`.
- The standard covers chat replies, documents, plans, summaries, commit bodies, and PR bodies. It
  does not cover code, structured config such as JSON and YAML, terse CLI output, the commit subject
  line, or the PR title.
- The commit subject line keeps the conventional-commit format. That format and the STE full-sentence
  rule cannot both hold, so the subject format wins. `## GIT Commit Guidelines` gained a bullet that
  says so.
- `## Scannable and Terse` came last. The sentence caps limit how long one sentence runs. Nothing
  limited the shape or the volume of a whole answer. Completeness wins over brevity, and terseness
  applies inside that limit.
- This change makes deliberate exceptions to the source standard. Em-dashes stay allowed, because the
  existing repo text uses them everywhere. A ban would leave every current file non-compliant with no
  fix planned.
- The block that ships to other repos names no skill. Most target repos have no style skill
  installed. A rule that points at a missing skill is a defect.

## Stated counts

- `rules/general.md` `# COUNTS IN INSTRUCTIONS` now bans a statement of how many items a set holds.
  Such a number is a second copy of the set's length. One added item invalidates every copy, and the
  copies sit in files the author never opens.
- The rule is not specific to this repo. Any instruction file in any project becomes inconsistent the
  same way. The rule therefore lives in `rules/general.md`, which loads in every session in every
  repo, and not in `CLAUDE.md`, which loads only here.
- One count was already wrong. `seo-keyword-generator` claimed six categories in two files while its
  reference file defined eight. Nothing caught the error. The sweep fixed the claim and removed the
  count, so the same error cannot return.
- The sweep covered 23 skills, plus `README.md`, `CLAUDE.md`, and `rules/general.md`. It removed
  phrases such as "Present the eleven modules", "a strict 17-rule style guide", and "a 14-section
  conversion blueprint".
- Most sites lost the number and now name the set, for example "the modules below" and "every tail
  gate". The sweep rewrote the sites where the number was the subject or was load-bearing. "Spawn 5
  advisors in PARALLEL" became "Spawn one agent per advisor", so the instruction still says how many
  agents to run.
- The rule exempts numbers that enumerate nothing. The exemptions cover thresholds and limits,
  ordinals for a step, phase, or stage, versions, dates, and exit codes. They also cover distributive
  phrasing, verbatim quotes, and named frameworks whose number is part of the concept.
- The sweep repaired two cross-skill references. `council-v2` named "the four passes" of
  `first-principles-mode`, and `better-plan` required "all four" ship conditions. Both now name the
  set instead.

## Delivery to other repos

- The `setup-aiengineering` skill gained a writing-style inject module at
  `references/writing-style.md`. Every repo that runs the skill now receives the standard. The module
  defaults to on, and a user can turn it off per project.
- The skill version moved from v9 to v10, so an older repo detects the gap on a re-run. The version
  stays at v10 after the later corrections, because those corrections add no concern to the baseline
  checklist.
- That skill's `description` and its `README.md` row described the old module set. Both now name the
  writing-style block. The same sentence had never named `setup-todo-backlog`. The skill gained that
  delegate in v6. The sentence now names every delegate target.
- The `description` was 985 characters against a 1024 limit and a 950 target. The additions alone
  raise it to 1020. That leaves no room for a later edit, and the Copilot CLI parser rejects a skill
  above the limit. This change therefore removed the word "genericized" and two of the four trigger
  phrases. The field is now 937 characters.
- The removed phrases change nothing for a user. The skill sets `disable-model-invocation: true`, so
  no phrase in that field starts it. A user starts it with `/setup-aiengineering`.

## Structure

- Both rules live in `rules/general.md`. `CLAUDE.md` points at each and restates neither. A second
  full copy would drift from the first, which is the failure the counts rule forbids.
- `CLAUDE.md` keeps its `## Counts` pointer next to `## Identifiers`, because both rules ban a value
  that goes stale for the same reason.
- The rule text in `rules/general.md` omits the `seo-keyword-generator` example on purpose. That file
  loads in every repo, so a story about one skill here does not belong in it. The example lives in
  this entry, and `CLAUDE.md` points at it.
- `README.md` names the standard in its layout table and in its `## Rules` bullet.
- The `# WRITING STYLE` subsections first used sentence case. Every other H2 in that file uses Title
  Case. They now match. No file links to them by anchor, so the rename changed no link.

## Scope and housekeeping

- This change rewrote no existing repo prose. Both rules govern new and edited text.
- It added no dependency.
- This session first wrote four separate changelog entries. `CLAUDE.md` requires one file per
  session. This change deleted those four and merged them into this file. Git history keeps the
  originals. The deleted names were `20260809232650-ste-writing-standard.md`,
  `20260810081839-clear-ste-findings.md`, `20260810085949-drop-brittle-counts.md`, and
  `20260810092838-counts-rule-global.md`.

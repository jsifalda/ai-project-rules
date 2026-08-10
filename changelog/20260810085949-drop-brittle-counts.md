# Drop brittle counts from the instructions

- Instruction files across the repo stated how many items a set holds. Examples: "Present the eleven
  modules", "a strict 17-rule style guide", "a 14-section conversion blueprint". Each number is a
  second copy of the set's length. One added item invalidates every copy, and the copies sit in files
  the author never opens.
- One count was already wrong. `seo-keyword-generator` claimed six categories in two files. The
  reference file defines eight. Nothing caught the error. This change fixes it and removes the count,
  so the same error cannot return.
- The sweep covers 23 skills, plus `README.md`, `CLAUDE.md`, and `rules/general.md`.
  Most sites lost the number and now name the set, for example "the modules below" and "every tail
  gate". Sites where the number was the subject or was load-bearing were rewritten, not deleted. The
  council skills are one example. "Spawn 5 advisors in PARALLEL" became "Spawn one agent per advisor",
  so the instruction still says how many agents to run.
- `CLAUDE.md` gained a `## Counts` section. It states the rule, the delete-versus-rewrite
  distinction, and the exemption list. The section sits next to `## Identifiers`, because both rules
  ban a value that goes stale for the same reason.
- Numbers that do not enumerate a set were left alone. The exemption list covers thresholds and
  limits, step and phase ordinals, version numbers, dates, distributive phrasing, verbatim quotes,
  and named frameworks whose number is part of the concept.
- Two cross-skill references were repaired in the same pass. `council-v2` named "the four passes" of
  `first-principles-mode`, and `better-plan` required "all four" ship conditions. Both now name the
  set instead.

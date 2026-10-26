---
name: generate-user-scenarios
description: Derive BDD user scenarios in Given, When, Then form from a PRD, or from any source that states a user problem and its solution, and write them into that PRD as a User Scenarios section. Covers each user story, real edge case and failure path, maps every functional requirement to a scenario, builds dated domain IDs, and sets every Verified by line to TODO. Reads the project's scenario inventory docs/user-scenarios.md for domains, IDs and overlaps, and never edits it. Use when the user types /generate-user-scenarios, or says "generate user scenarios from this PRD", "write BDD scenarios for this feature" or "turn this PRD into scenarios", or when a setup skill delegates scenario generation. Do NOT use to bootstrap a scenario inventory, to verify scenarios in a browser, to write test code, or to break a PRD into tasks.
metadata:
  version: "1.0"
---

# Generate User Scenarios

## Workflow

### 1. Resolve the source

- Argument is a file path → read the file.
- Pasted text, or a ticket you can already read with your own tools → use it as the source.
- No argument → list `docs/prds/*.md`. One file → use it. Several → ask which. None → ask for a source.
- A calling skill passes a list of PRD paths → process each path in turn.

### 2. Extract

- Extract the users, the user problem, the solution, the functional requirements, the edge cases, the failure paths and the out-of-scope items.
- No clear user problem or no clear solution → write nothing for that source, and ask. With a list of paths, go on to the next one.
- Never invent behavior the source does not state.

### 3. Read the inventory

- Read the scenario inventory `docs/user-scenarios.md` when it exists. Never edit it.
- Note its frozen domain prefixes, its ID scheme, its existing IDs, and the scenarios that overlap the source.

### 4. Pick the domain

- No inventory and the source already has a `## User Scenarios` section → reuse the prefix that section uses.
- Inventory exists → use its frozen domain prefixes.
- A behavior fits no frozen domain → ask the user. Never add a domain.
- No inventory → derive one all-caps prefix that matches `^[A-Z]+$` from the feature. Do not ask.

### 5. Generate

- Write one happy-path scenario per user story or use case.
- Write one scenario per real edge case and per failure path.
- Merge variants that differ only in data.
- Write no scenario for an out-of-scope item.
- Follow [references/scenario-format.md](references/scenario-format.md) for the block shape, the IDs and the voice.

### 6. Check coverage

- Map every functional requirement to scenario IDs in working memory. Never write the map into the source.
- A requirement maps to no scenario → add one. The source is too thin for one → name the gap in the report.

### 7. Write

- Source file without `## User Scenarios` → insert the section at the end of `## Solution Outline & Requirements`, before the next `##` heading.
- `## Solution Outline & Requirements` absent → insert the section before `## Risks & Assumptions`. Both absent → append it at the end of the file.
- Write a new section without asking.
- Source file with `## User Scenarios` → keep the IDs of unchanged scenarios, show the diff, and ask before you replace the section.
- Never add a second `## User Scenarios` section.
- Non-file source → print the section in chat. Write a file only when the user names one.

### 8. Report

- Report per target:
  - The path, or `chat`.
  - The reason, when you wrote nothing for that source.
  - The scenarios written.
  - The functional requirements with no scenario.
  - The inventory IDs that overlap a new scenario. Flag them. Never reuse or edit them.
  - The domain used, and whether you derived it.
  - Any ID-scheme mismatch with the inventory.
  - Inventory exists → a one-line reminder that the scenarios move into it when the code ships.

## Rules

- Change nothing in the source file outside its `## User Scenarios` section.

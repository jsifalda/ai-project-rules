# Correct the setup-aiengineering summaries and the STE heading case

- The `setup-aiengineering` skill gained a writing-style module in the previous change. Two summaries
  still described the old module set. The `description` frontmatter and the `README.md` skill row now
  name the writing-style block.
- The same `description` sentence also omitted `setup-todo-backlog`. The skill has delegated to that
  skill. The skill gained that delegation in v6. The sentence now names all four delegate targets.
- The `description` was 985 characters. The repo permits 1024 characters and targets 950. The two
  additions alone raise the field to 1020 characters. A later edit of that field then pushes it over
  the limit. The Copilot CLI parser rejects a skill above the limit. This change therefore removed
  other text. It removed the word "genericized" and two of the four trigger phrases. The field is now
  937 characters.
- The removal of the two trigger phrases has no effect on how a user starts the skill. The skill sets
  `disable-model-invocation: true`, so no phrase in that field starts the skill. A user starts it with
  `/setup-aiengineering`.
- The three new subsections under `# WRITING STYLE` in `rules/general.md` used sentence case. Every
  other H2 in that file uses Title Case. The three headings now match the other headings. No file
  links to these headings by anchor, so the rename changed no link.
- The skill version stays at v10. This change corrects two summaries. It adds no concern to the
  baseline checklist.

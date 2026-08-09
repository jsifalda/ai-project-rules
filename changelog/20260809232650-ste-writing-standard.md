# Repo adopts ASD-STE100 as its writing standard

- `rules/general.md` now names ASD-STE100 Simplified Technical English as the writing standard. The new `# WRITING STYLE` section states the rules, the scope, the exclusions, and a ban list. It replaces four old bullets. Those bullets named no standard.
- The section adds three subsections. `## STE core rules` states the grammar rules. `## STE bans and exceptions` lists banned items and allowed exceptions. `## STE precedence` states which rule wins in a conflict.
- `## GIT Commit Guidelines` gained one new bullet. The commit subject line keeps the conventional-commit format. The commit body and the PR body follow the new standard.
- `CLAUDE.md` gained a new `## Writing Style` section. This section points to `rules/general.md` as the single source of the rules. It restates no rule. The two files cannot drift apart.
- The `setup-aiengineering` skill gained a new inject module. The module lives in `references/writing-style.md`. The module ships the same standard to every repo that runs the skill. The skill version moved from v9 to v10. `README.md` gained two lines that name the standard. The module defaults to on. A user can turn the module off per project.
- This change makes two deliberate exceptions to the source standard. Em-dashes stay allowed. The source standard bans em-dashes. The existing repo text uses em-dashes everywhere. A ban would leave every current file non-compliant, with no fix planned. The injected block also names no skill. Most target repos have no style skill installed. A rule that points at a missing skill is a defect.
- This change did not rewrite any existing repo text. The new rule governs only new and edited text. The change added no new dependency.

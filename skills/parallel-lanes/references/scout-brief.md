# Scout brief

- Fill one copy per repo. Replace each `<...>` placeholder.
- Dispatch every copy as a read-only exploration subagent (`Explore` in Claude Code), all in one message.

```text
Scout <repo-path> read-only for a parallel execution plan. Never edit a file. Never run a git write operation.

Feature: <feature-summary>

Capabilities in this repo, one per line as id and description:
<capability-list>

For each capability, report:
- Existing files to edit, as exact paths, with line ranges where useful.
- New files, each with its owning directory.
- Registration points it touches.
- Single-head files it touches: migration head, lockfile, generated files, project files, ordered lists.
- The access, permission and data-state checks it relies on.
- Host instruction files inside this repo that apply to it by path glob.

Across all capabilities, report:
- Each file that two or more capabilities edit, labelled append-only, structural or single-head.
- The repo's module convention, such as one manager per entity.
- The test levels the repo allows.
- Machine-global resources needed to build or test: simulator or emulator, ports, local database. Say for each whether the build or run needs it, or only the tests.
- Each capability or repo the feature needs that the list above misses.
- A recommended foundation and lane split.

<host scout questions and report fields, or nothing>

Report conclusions with paths. Never paste file contents.
```

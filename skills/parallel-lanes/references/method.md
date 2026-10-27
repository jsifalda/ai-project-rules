# Parallel lanes method

## Contents

- Hotspot classes
- Foundation checklist
- New module pattern
- Lane partition
- Repo areas
- Scenario mapping
- Contracts
- Resources
- Batching
- Plan JSON
- Validator

## Hotspot classes

| class | examples | rule |
|---|---|---|
| append-only registry | route or blueprint tuple, event-type enum, error classes, typed-dict files, messages or i18n files, flag enums | the foundation pre-adds every entry, or pre-wires each registration to a stub file that one lane later fills |
| structural | a shared manager or service class that several capabilities add methods to, a shared page | the foundation makes each edit that two or more capabilities share, then split the shared class or file into one module per capability, pre-wired by the foundation, or merge the capabilities into one lane |
| single-head | a migration chain with one head, a lockfile, a generated file such as string codegen output, an IDE project file, ordered DI or module lists, settings or build module includes | exactly one unit edits it, the foundation |

- Pick the class from the scout report label. No label → classify from the file's role.
- Split a structural hotspot along the repo's module convention from the scout report.
- Send a split that breaks the module convention to Decisions needed.

## Foundation checklist

Put each item below in the foundation when two or more lanes need its file.

- The data model and the only migration.
- Each registration, pre-wired to a stub file.
- Each module split from a structural hotspot, pre-wired.
- Enum, event and error values.
- Shared types, or a new shared package or module.
- Each frozen cross-repo runtime dependency from Contracts.
- The feature flag key.
- Route constants.
- Ownership of generated strings.
- Dependency declarations plus one lockfile regeneration.
- Test mocks and fixtures that lanes share.

## New module pattern

- Host project file is single-head → put the feature's new code in a new module or package.
- Prefer a new local package to new files in an app target.
- Create the module in the foundation. Lanes then add files to it without editing the project file.

## Lane partition

- Build a graph with one node per capability.
- Connect two capabilities when they edit the same file after the foundation.
- Make each connected component one lane.

## Repo areas

- Give each `repo` value that is an area of one git repo a disjoint path prefix.
- Put each file shared at the git repo root, such as CI config or a lockfile, in one area's foundation.

## Scenario mapping

- Map each scenario to every unit whose change it needs, across repos.
- Flag a scenario that needs both sides of a cross-repo contract but maps to one side only.
- Map a scenario that needs no new code to the lane whose code guarantees it. Make it a test in that lane.

## Contracts

- List every cross-repo contract the lanes depend on, stated or not, with its source: endpoint shape, fields, error codes, event names, flag key.
- List each cross-repo runtime dependency as a contract, such as another repo's event names or a component another lane builds.
- Freeze each runtime dependency in the foundation of its repo when two or more lanes there use it, else in the one lane that uses it.
- Flag each contract the spec and its siblings do not state as a decision needed before dispatch.
- Give each lane every contract it needs before dispatch. Never let a lane read another repo's lane code.

## Resources

- Put a resource in a unit's `resources` only when the host states the unit needs it to build or run at all.
- Put every other contended resource in the unit's `gate_resources`, such as a shared local database or a fixed dev-server port.
- Name a gate resource with a free string. It is not a key of `resource_caps`.
- Never delay a unit for a gate resource. Plan one gate queue per gate resource instead.
- Order each gate queue by batch, then by lane-table order.
- Ask under Decisions needed whether each worker can get an isolated instance, such as its own database name or port.
- Drop the gate queue when the host confirms an isolated instance per worker.
- Let a cap span repos.

## Batching

- Put every foundation in the first batch, unless a cap overflows.
- Add the lanes in lane-table order, each to the first batch after all its blockers.
- Put a lane from a repo with no foundation in the first batch, unless a cap overflows.
- On overflow of a resource cap or `max_agents`, move the latest units to the next batch. Keep each unit in a later batch than its blockers.

## Plan JSON

```json
{
  "scenarios": [{"id": "create-thing", "title": "..."}],
  "units": [
    {"id": "api-F", "repo": "api", "kind": "foundation", "files": ["src/models/thing.py", "src/routes/"], "scenarios": [], "blocked_by": [], "resources": [], "gate_resources": []},
    {"id": "api-create", "repo": "api", "kind": "lane", "files": ["src/routes/create.py"], "scenarios": ["create-thing"], "blocked_by": ["api-F"], "resources": [], "gate_resources": ["local-db"]}
  ],
  "resource_caps": {"ios-simulator": 1},
  "max_agents": null,
  "batches": [["api-F"], ["api-create"]]
}
```

| key | rule |
|---|---|
| `scenarios[].id` | the spec's own id, else a kebab-case slug |
| `units[].id` | unique across the plan |
| `units[].repo` | the host's unit boundary, one foundation at most per value |
| `units[].kind` | `foundation` or `lane` |
| `units[].files` | paths relative to the git repo root, each directory ending in `/` |
| `units[].scenarios` | a foundation usually lists none, at least one id for a lane |
| `units[].blocked_by` | ids of units that must finish first |
| `units[].resources` | optional, keys of `resource_caps` the unit needs to build or run at all, counted against the caps |
| `units[].gate_resources` | optional, free strings naming resources contended only in the test gate, never counted against the caps, never checked |
| `resource_caps` | optional, most units in one batch that use the resource. Absent or `null` → `resources` names stay unchecked and nothing is capped |
| `max_agents` | most units in one batch, `null` for no cap |
| `batches` | lists of unit ids in run order |

## Validator

Path rules:

- Treat a path ending in `/` as a directory that covers every path under it.
- Treat `./`, `.` or an empty path as the git repo root, which overlaps every path.
- Expect the validator to collapse repeated `/`.
- Expect the validator to resolve `..`, and to reject a path that escapes the git repo root or is absolute as malformed input.

Exit codes:

| code | meaning |
|---|---|
| 0 | clean |
| 1 | violations |
| 2 | malformed or unreadable input |

Enforced checks:

| code | fails when |
|---|---|
| `duplicate-unit` | two units share an id |
| `duplicate-scenario` | two scenarios share an id |
| `bad-kind` | a unit kind is not `foundation` or `lane` |
| `unknown-scenario` | a unit names a scenario id that is not in `scenarios` |
| `unknown-unit` | a `blocked_by` entry or a batch names a unit id that does not exist |
| `unknown-resource` | `resource_caps` is present and a `resources` entry is not one of its keys |
| `unbatched` | a unit is in no batch |
| `multi-batched` | a unit is in more than one batch |
| `lane-overlap` | two lanes with one `repo` value share a path |
| `foundation-overlap` | a lane shares a path with the foundation of its `repo` value and does not depend on that foundation, directly or through other units |
| `missing-foundation-edge` | a lane does not depend on the foundation of its `repo` value, directly or through other units |
| `multiple-foundations` | two foundations have one `repo` value |
| `empty-lane` | a lane has no scenarios |
| `uncovered-scenario` | no unit lists a scenario |
| `cycle` | the `blocked_by` edges form a cycle |
| `batch-order` | a unit is in a batch before or with one of its blockers |
| `resource-cap` | a batch has more units using a `resources` entry than its cap |
| `max-agents` | a batch has more units than `max_agents` |

Manual checks, done by the planner:

- Foundation minimality: each file the foundation edits is needed by two or more lanes.
- Contract coverage: no scenario that needs both sides of a cross-repo contract maps to one side only.
- Path existence: each existing file a unit edits is in its scout report.
- Gate queues: each gate resource has its queue, or the host confirmed an isolated instance per worker.
- Confirm each scenario a foundation lists is delivered by the foundation itself.
- Confirm areas of one git repo own disjoint path prefixes.

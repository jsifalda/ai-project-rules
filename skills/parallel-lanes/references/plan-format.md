# Plan format

- Print the sections below in this order. Replace each `<...>` placeholder.
- Write `none` under Decisions needed or Contracts when nothing applies.
- Drop Host mapping when the host has no delivery-unit flow.
- Drop the host option line when the plan has no foundation.
- Write a placeholder such as `<new: unit-id>` for a host id that does not exist yet.

```markdown
## Parallel lanes for <spec title>

<units> units, <lanes> lanes, <batches> batches, coverage <covered>/<total> scenarios.

### Decisions needed before dispatch
- <contract, sibling conflict, module split, isolated instance, external prerequisite or host question>: <what is open, and which units wait on it>

### Contracts
| contract | repos | source | frozen in |
|---|---|---|---|
| <endpoint, field, error code, event name, flag key or component interface> | <provider and consumer repos> | <spec, sibling document, or unstated> | <foundation or lane unit-id, or none> |

### Foundations
| unit | repo | creates or registers once |
|---|---|---|
| <unit-id> | <repo> | <entries, stubs, migration, shared module> |

### Lanes
| lane | repo | owns files | scenarios |
|---|---|---|---|
| <unit-id> | <repo> | <paths> | <scenario ids> |

### Coverage
| scenario | units |
|---|---|
| <scenario-id> <title> | <unit ids across repos> |

### Batches
| batch | units | constraint applied |
|---|---|---|
| <batch> | <unit ids> | <foundation first, resource cap, max agents, or none> |

- Gate queue <gate resource>: <unit ids>, test gate one at a time.
- Host option: stack lanes on the unmerged foundation branch.

### Host mapping
| unit | host unit | Blocked by |
|---|---|---|
| <unit-id> | <host unit or placeholder> | <host unit of its foundation, or none> |

### Agents
- Total: <units> agents.
- Widest batch: <width> agents.
- Deepest gate queue: <gate resource>, <unit count> units, or `none`.
- Cost: <repos> scouts, plus one worker and one reviewer per unit, plus the host gates the orchestrator runs, about <repos + 2 x units> agent runs.
- Validator: <check_lanes.py exit 0, or manual check>. Manual checks: <done>.
```

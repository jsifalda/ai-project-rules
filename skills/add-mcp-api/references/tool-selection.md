# Tool Selection and Confirmation

Use this reference after the read-only application inventory and before architecture selection. Use it with [the plan template](plan-template.md).

## Selection criteria

Select a tool only when it meets all applicable criteria:

- It delivers a user outcome, not an internal route or data model action.
- An existing service boundary already performs the operation.
- The service derives the user and tenant from the authenticated token, or the tool path re-performs the caller's ownership check before it calls the service.
- The required scope is narrow and understandable.
- The input can be validated at runtime.
- The operation has a defined success result and an expected error result.
- The impact is known as read-only, write, destructive, or external side effect.
- The operation can finish inside the target-client timeout, or it has a supported bounded design.
- The user can understand when to use it from its title and description.

Reject a candidate when it leaks implementation detail, bypasses authorization, combines unrelated outcomes, needs unbounded data, or duplicates a safe existing tool.

### Ownership check in the caller

A service can take no user identifier because the route or the handler makes the ownership check. Name the ownership-check symbol in the plan for each such tool. Re-perform that check in the tool path before the service call. Re-verify that a returned record belongs to the named parent. Never wrap an unscoped service in a tool without this check.

## Candidate derivation

Start from user outcomes observed in the application. For each outcome, trace this path:

```text
User outcome -> existing service boundary -> authorization and entitlement -> validated input -> structured result
```

Prefer a small set of high-value tools. Combine closely related read operations only when they share the same scope, service boundary, data class, and result shape. Split an operation when its authorization, impact, failure behavior, or data class differs.

Do not make a tool for:

- direct database access.
- generic internal HTTP forwarding.
- administrative action without a distinct privileged scope.
- a browser-only workflow with no safe service boundary.
- a thin wrapper around every existing route.

## Candidate-tool confirmation table

Present this table before you write a plan. Fill every cell with inventory evidence. Use plain language for the user outcome.

| Tool | User outcome | Existing service boundary | Required scope | Impact | Validated input | Success result | Expected negative path | Evidence | User decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<tool-name>` | `<outcome>` | `<service and symbol>` | `<scope>` | `<read-only, write, destructive, or external>` | `<schema boundary>` | `<structured result>` | `<denied, invalid, absent, conflict, or limit>` | `<path, symbol, or source>` | `<confirm, remove, or change>` |

Ask the user to confirm, remove, or change each row. Also ask the user to confirm the listed scopes. Do not infer a decision from a request that does not name the row.

The confirmation is complete only when every remaining row has an explicit user decision. Remove rejected rows before architecture selection. Return to read-only inventory when a requested change has no demonstrated service boundary.

## Scope rules

Use a scope name that states the protected outcome. Keep read and write access separate. Keep administrative, destructive, tenant-wide, and external actions in separate scopes. Reject unknown scopes. Do not make a missing scope mean full access.

A tool must enforce its scope, entitlement, rate limit, and user boundary in its own request path. Web middleware can add protection but cannot be the only gate.

## Tool contract record

For each confirmed tool, record these plan inputs:

| Field | Record |
| --- | --- |
| Title and description | The user outcome and important limit. |
| Input | Runtime schema, bounds, and prohibited identity fields. |
| Authenticated context | User and tenant derived from the access token. |
| Authorization | Required scope, entitlement, and role checks. |
| Service call | Existing boundary and allowed operation. |
| Result | Typed success content and structured expected errors. |
| Annotation | Read-only, destructive, or external side-effect behavior. |
| Rate limit | Identity-based limit and capacity control. |
| Audit event | Action, authenticated subject, outcome, and safe metadata. |

The inventory can find no audit surface. In that case, the plan introduces one, or the plan states plainly that structured logging is the accepted substitute. A category logger entry is not an audit trail.

Do not place token values, authorization codes, request bodies, or sensitive result data in logs or plan examples.

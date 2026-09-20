# Remote MCP API Plan Template

**Use this template only after the user confirms the candidate-tool table in [tool selection](tool-selection.md) and answers the nginx-phase question. Use [protocol and authorization](protocol-and-auth.md) and [failure prevention](traps.md) for selected facts. Use [nginx VPS deployment](nginx-vps.md) only when that path is selected.**

**Copy only the content below the horizontal rule into the plan. Do not copy this title or this note.**

---

# Remote MCP API Implementation Plan

## Scope and evidence

- Application: `<name and runtime>`
- Target clients: `<clients and current documentation URLs>`
- Canonical public origin: `<configuration name, not a secret>`
- Confirmed tools: `<tool names, outcomes, scopes, and impact>`
- Selected transport: `<transport and protocol evidence>`
- Selected authorization design: `<existing provider, existing library, in-app server, or public access>`
- Selected deployment path: `<existing platform or nginx VPS>`
- Primary evidence: `<current URLs and access date>`
- Repository evidence: `<paths and symbols>`
- Assumptions and uncertainties: `<blocking status and owner>`

State why each selected design fits the current evidence. State each rejected alternative and why it does not fit.

## Plan conventions

Write each phase with these fields:

- Goal
- Repository locations
- Changes
- Security boundary
- Negative-path checks
- Acceptance evidence
- Dependencies

Name the existing files, symbols, configuration names, migrations, and tests where evidence identifies them. Do not invent paths, package names, endpoints, or environment variables.

Size every outer timeout above the measured slowest tool path. A path can have no ceiling at all, for example an unconfigured downstream client timeout. Impose an application ceiling first, then size every outer timeout above that ceiling. An unbounded path cannot be measured, so it cannot be sized.

## Phase 1. Audit the service boundary

Goal: Connect each confirmed tool to an existing application service boundary.

Plan the following work:

- Extract or adapt service methods only where the existing boundary cannot safely serve the tool.
- Keep database access and internal HTTP details behind the service boundary.
- Define runtime input validation and typed success and expected-error results.
- Derive user and tenant identity from the access token.
- Define safe audit events and remove sensitive values from logs.

Negative-path checks: invalid input, absent data, cross-tenant input, unauthorized user, ineligible user, rate-limit exhaustion, and downstream failure.

## Phase 2. Establish authorization and discovery

Goal: Implement the selected authorization design and publish current required metadata.

Plan the selected authorization design from current protocol evidence:

- Define the scope allowlist from the confirmed table.
- Implement the selected grant, token, storage, rotation, expiry, and revocation controls.
- Support the current required request format and client behavior.
- Publish each current required authorization and resource metadata document.
- Build public metadata URLs from explicit deployment configuration.

Negative-path checks: rejected authorization request, rejected redirect, invalid proof, expired grant, reused credential, unknown scope, invalid token, token audience mismatch, missing or wrong `resource` parameter, revoked grant, missing authorization, and altered public URL headers.

## Phase 3. Add the MCP transport and tool gates

Goal: Expose the confirmed tools through the selected remote transport.

Plan the following work:

- Add the stable MCP endpoint on the canonical origin.
- Apply token validation, scope checks, entitlement checks, identity-based limits, and audit events inside every tool path.
- Build an application rate limiter keyed by the authenticated subject when the inventory finds none. Name the storage for that limiter.
- Set accurate tool titles and behavior annotations.
- Return structured expected errors without protected data.
- Return a protocol-layer authorization failure as an HTTP status code with the challenge header. Return 401 for an absent or invalid token. Return 403 with an `insufficient_scope` challenge for a scope failure. Return 400 for a malformed authorization request. Carry only business failures in the structured tool errors.
- Configure streaming, request handling, and timeout budgets from measured tool behavior and client limits.
- Preserve required protocol headers through the selected application and deployment layers.

Negative-path checks: malformed protocol request, missing or invalid token, token audience mismatch, missing or wrong `resource` parameter, valid token with wrong scope, valid token with no entitlement, forged user or tenant input, limit exceeded, slow operation, downstream error, and unsupported client behavior.

## Phase 4. Deploy on the selected path

Goal: Make the MCP endpoint and discovery documents reachable without changing their security properties.

For every deployment path, plan explicit controls for canonical origin, HTTPS, metadata routes, header preservation, streaming, request limits, timeout budgets, safe access logs, restart behavior, and rollback.

### Nginx VPS deployment phase

Include this subsection only after the user explicitly requests the nginx phase. Use [nginx VPS deployment](nginx-vps.md) to plan:

- a loopback application process behind nginx.
- canonical-host and alias redirect behavior.
- exact routing for required well-known paths before broad dot-path rules.
- unbuffered MCP streaming and compatible upstream HTTP behavior.
- header inheritance and authenticated request verification.
- capacity limits that do not use source IP as a user quota.
- safe access-log format that excludes authorization query values.
- measured timeout and restart controls.

Negative-path checks: host-changing redirect, missing discovery route, buffered stream, missing authorization header, blocked well-known route, timeout below tool duration, capacity limit that blocks unrelated users, and authorization values in logs.

## Connection verification ladder

Run these rungs in order. Record the command class, result, and evidence location for each rung.

1. Resolve the canonical host from a public network.
2. Verify the certificate and every canonical redirect.
3. Fetch each required discovery document from a public network.
4. Confirm the MCP endpoint and discovery documents remain on the canonical host.
5. Send an unauthenticated request and confirm the selected discovery mechanism answers. Confirm a 401 that carries a `WWW-Authenticate` header naming `resource_metadata`, or confirm the well-known protected-resource document serves the same location.
6. Send a token that lacks a required scope and confirm a 403 response with an `insufficient_scope` challenge.
7. Send an authenticated request and confirm required authorization and protocol headers reach the application.
8. Exercise a slow supported operation below each configured timeout.
9. Confirm streamed output arrives before the response completes when streaming applies.
10. Confirm access logs exclude authorization codes, tokens, and sensitive request data.
11. Verify capacity controls protect the service without making source IP a user quota.
12. Restart the application process or its equivalent deployment unit and confirm recovery.
13. Connect each target client and complete an authenticated call for each confirmed tool.

Include a local verification path when hosted authorization blocks an inspection client. Test discovery, authorization, and tools independently before target-client connection testing.

## Phase 5. Document operation and support

Goal: Give operators a safe procedure to deploy, observe, revoke, and diagnose the connection.

Plan operator documentation for:

- required configuration names and safe secret provisioning.
- canonical origin, registration, and discovery URLs.
- deployment, rollback, and restart steps.
- timeout, capacity, and identity-based limit settings.
- safe logs, metrics, and audit events.
- grant revocation, token expiry, and incident response.
- the Connection verification ladder and common failure evidence.

Do not place secret values, token values, authorization codes, or customer data in examples.

## Phase 6. Publish the tool page last

Goal: Describe only the deployed and verified connection.

Schedule this phase after the Connection verification ladder passes and target clients complete authenticated tool calls. Plan public content that names only supported tools, scopes, user outcomes, limitations, supported clients, and the verified connection process.

Do not publish claims before the deployed tool registry and documented connection flow prove them.

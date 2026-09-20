---
name: add-mcp-api
description: Create a phased implementation plan for an existing application that needs a remote Model Context Protocol API. Use when a user asks to expose authenticated application capabilities through remote MCP tools, add an MCP endpoint, or plan a remote MCP integration. Do not use for a greenfield application, local stdio MCP server, product code implementation, or general API planning.
---

# Plan a Remote MCP API

Produce an evidence-based implementation plan. Do not write product code, change application files, install packages, configure infrastructure, or publish public copy.

## Read the references

Read these files before you inspect the application:

- [Protocol and authorization](references/protocol-and-auth.md)
- [Failure prevention](references/traps.md)
- [Tool selection](references/tool-selection.md)
- [Plan template](references/plan-template.md)

Read [nginx VPS deployment](references/nginx-vps.md) before you ask the nginx-phase question or include that phase.

## Preflight

Confirm that the target is an existing application. Inspect only enough evidence to confirm all of these conditions:

- The repository has application source code and an established runtime.
- The application has an existing user, tenant, or data boundary that MCP tools can use.
- The user asks for a remotely reachable MCP API, not a local process integration.

Refuse a greenfield request. State that this workflow plans an MCP API for an existing application. Ask the user to first establish the application, its user boundary, and its capabilities.

If a required fact is absent, ask a factual question. Do not use that question as an approval request.

## Inventory the existing application

Keep this stage read-only. Map the existing application before you propose tools or architecture.

1. Identify the runtime, framework, routing model, deployment platform, and package manager. Record the candidate MCP SDK or adapter for that runtime.
2. Locate the authenticated user and tenant derivation path.
3. Locate authorization, entitlement, rate-limit, audit, validation, and error conventions.
4. Map existing service boundaries and their public operations.
5. Identify data classes, destructive operations, and operations with slow downstream work.
6. Identify the target MCP clients, public origin, and current deployment limits.
7. Read the repository's own agent instructions, decision records, architecture notes, and changelog. Record every capability that the project removed, banned, or superseded on purpose.
8. Record evidence as file paths, symbols, configuration names, and public documentation URLs. Do not copy secrets or private values.

Reject a proposed tool when the inventory does not show a safe service boundary. Do not expose a database query, internal HTTP route, or browser-only action as a tool.

Reject a candidate tool that matches a recorded prohibition. This ground is sufficient on its own, even when a service boundary for the capability still exists. A removed capability often leaves working helper functions, database models, and configuration behind, so a boundary test alone does not find it.

## Refresh protocol facts

Before architecture selection, open the current primary sources listed in [Protocol and authorization](references/protocol-and-auth.md). Also open the current official documentation for each target client and the selected SDK or adapter.

Record the current evidence for:

- supported transport and protocol revision.
- public HTTPS reachability and canonical-origin rules.
- authorization flow, PKCE, metadata, registration, and discovery requirements.
- token endpoint request format, scope behavior, and connector timeout ceiling.
- target-client behavior for redirects, streaming, and authorization headers.

State a dated uncertainty when network access or a source is unavailable. Do not present a cached reference as current protocol authority.

## Derive the candidate tools

Use [Tool selection](references/tool-selection.md). Build a small candidate table from demonstrated user outcomes. Include only operations that the existing application already supports through an auditable service boundary.

For each candidate, define the user outcome, required scope, impact, input boundary, service boundary, expected result, and negative path. Keep the tool set small. Prefer a higher-value outcome over a thin wrapper for each existing route.

## Tool-confirmation gate

This is a blocking gate. Present the candidate-tool confirmation table from [Tool selection](references/tool-selection.md). Ask the user to confirm, remove, or change each candidate tool and its scopes.

Do not select final tools, select architecture, or write the implementation plan until the user confirms the table. Do not treat silence, a related request, or a broad approval as confirmation.

## Select the architecture

After tool confirmation, select the smallest architecture supported by inventory and current protocol evidence.

- Select the MCP SDK or adapter for the runtime from the inventory candidate. Record the selected candidate and its current documentation. Add a new dependency only through the target project's own approval rules.
- Select stateless Streamable HTTP when the target clients and selected SDK support it.
- Select an existing identity provider or authorization library when it can act as the authorization server.
- Otherwise, use an in-application authorization server when the application owns user sessions and can safely issue, persist, rotate, and revoke grants.
- Select no authorization only for truly public data. Never use a static API key for user-specific access.
- Keep the MCP endpoint, authorization server, discovery metadata, and canonical public origin compatible with the active specification.
- Preserve existing deployment when it meets streaming, timeout, origin, and discovery requirements. Do not move platforms only to add MCP.

For each selection, cite the inventory and current primary evidence. State rejected alternatives and why they do not fit.

## Nginx-phase gate

This is a blocking gate. Ask the user: “Include the nginx VPS deployment phase in the plan?”

Read [nginx VPS deployment](references/nginx-vps.md) before asking. Explain that the phase applies when a long-running application process behind nginx is the selected deployment path. Do not assume nginx from the application inventory.

Do not write the final plan until the user answers. Include the nginx phase only after an explicit yes. If the user answers no, record that the plan keeps the existing deployment path and verifies its equivalent controls.

## Write the plan

Use [Plan template](references/plan-template.md). Fill every applicable section with confirmed tools, selected architecture, repository locations, current source evidence, and clear acceptance checks.

Keep each phase reviewable and ordered by dependency. Include security and negative-path checks in the phase that introduces each boundary. Name the Connection verification ladder with the exact section name that [Plan template](references/plan-template.md) uses. Include every applicable rung before target-client connection testing.

Place public tool-page work last. Do not plan public claims until deployed tools and the documented connection flow pass verification.

## Deliver

Return only the implementation plan and a concise assumptions list. Mark unresolved facts as blocking or non-blocking. Do not add code, configuration, migration, package, or deployment commands outside the plan.

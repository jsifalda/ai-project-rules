# Protocol and authorization

> Fact status: reviewed 2026-09-20. Claude client facts reviewed 2026-10-11. Client ID metadata document facts and the ChatGPT and VS Code client facts reviewed 2026-10-17. Recheck every `[PRIMARY]` claim against the linked primary sources before a plan becomes binding. `[OBSERVED]` marks a client document value or client behavior observed on 2026-10-16, not a documented claim. Fetch the client's document again before a plan relies on the value. The active protocol and connector behavior can change.

## Contents

- [Transport and public URL](#transport-and-public-url)
- [Authorization server](#authorization-server)
- [OAuth and discovery](#oauth-and-discovery)
- [Client ID metadata documents](#client-id-metadata-documents)
- [Connector interoperability](#connector-interoperability)
- [Tokens and scopes](#tokens-and-scopes)
- [Tool contracts](#tool-contracts)
- [Timeouts and verification](#timeouts-and-verification)
- [Protocol fact refresh](#protocol-fact-refresh)
- [Primary sources](#primary-sources)

## Transport and public URL

- Use a public HTTPS endpoint for a connector that must work from cloud, web, desktop, and mobile clients. `[PRIMARY]`
- Prefer stateless Streamable HTTP when the active SDK and target clients support it. Keep one stable endpoint. `[PRIMARY]`
- Set the public origin from deployment configuration, such as `APP_PUBLIC_URL`. Do not derive issuer, discovery, redirect, or resource URLs from request host or forwarded headers.
- Keep the MCP endpoint, the OAuth discovery documents, and the authorization and token routes on that configured origin.
- Do not redirect an authenticated MCP request across hosts. Disable proxy response buffering on streaming paths.

## Authorization server

Select in this order:

1. Use an existing identity provider or auth library when it can operate as the OAuth authorization server.
2. Otherwise, use an in-application OAuth authorization server on the MCP origin when the application owns user sessions.
   - The server emits `iss` on each authorization response, including an error response. The server advertises `authorization_response_iss_parameter_supported` in its metadata. The client validates `iss` against the expected issuer. See [RFC 9207](https://www.rfc-editor.org/rfc/rfc9207). `[PRIMARY]`
3. Use no authorization only for genuinely public data.

Do not use a static API key for user-specific access. The access token must identify the authenticated principal and tenant.

## OAuth and discovery

- Use the OAuth authorization-code flow with PKCE S256 for user-specific access. `[PRIMARY]`
- Publish the authorization-server metadata and protected-resource metadata required by the active MCP authorization specification. `[PRIMARY]`
- Implement at least one protected-resource discovery mechanism. The active specification requires one of these. `[PRIMARY]`
  - Answer an unauthenticated or invalid-token MCP request with 401 and a `WWW-Authenticate: Bearer resource_metadata="<protected resource metadata URL>"` header. Include the `scope` parameter in that challenge where it applies. See [RFC 9728 section 5.1](https://www.rfc-editor.org/rfc/rfc9728#section-5.1).
  - Serve the protected-resource metadata at its well-known URI. Serve it at the path-inserted location for an endpoint below the root, and at the root location for a root endpoint.
- A client uses the challenge header when the response carries it. A client otherwise falls back to the well-known URIs, and it requests the path-inserted location before the root location. Serve both mechanisms for the widest client support. `[PRIMARY]`
- Choose the client registration path in this order: pre-registered credentials when the client holds them, then client ID metadata documents when the authorization server advertises `client_id_metadata_document_supported`, then Dynamic Client Registration when the authorization server exposes a `registration_endpoint`, then a user prompt for client information. `[PRIMARY]`
- Support client ID metadata documents in the authorization server, and advertise `client_id_metadata_document_supported`. The specification deprecates Dynamic Client Registration and keeps it for backward compatibility with an authorization server that lacks client ID metadata documents. Advertise only the client-authentication methods that the token endpoint accepts. `[PRIMARY]`
- Accept form-encoded token endpoint requests. `[PRIMARY]`
- The client sends the RFC 8707 `resource` parameter in both the authorization request and the token request. The client names the canonical MCP server URI in that parameter. `[PRIMARY]`
- The server validates that the access token was issued specifically for it. The server rejects a token that does not name the server as the audience. `[PRIMARY]`
- The server never passes a received access token through to an upstream API. `[PRIMARY]`
- Validate `Origin` when present. Do not reject a request only because it has no `Origin` header unless the active protocol requires it. `[PRIMARY]`

## Client ID metadata documents

- Accept a client ID only when it is an HTTPS URL with a path, no fragment, and no user name or password. `[PRIMARY]`
- Refuse a client ID whose path is only the root.
- Refuse a client ID with a dot segment in its path. `[PRIMARY]`
- Refuse a client ID whose parsed `href` differs from the raw string.
- Fetch the document only for a signed-in user. Check the session and the entitlement before you resolve the client.
- Resolve a token or refresh request from the client data saved with the grant. Never fetch the document there.
- Read the entitlement from the database, not from a session claim.
- Limit new fetches per authenticated user. Count only real fetches, never a cache hit or a caller that joins a fetch already in progress.
- Fetch over HTTPS only, with `Accept: application/json` and a `User-Agent` that names the authorization server.
- Refuse a private, loopback, link-local, CGNAT, unique-local, multicast, or reserved address. Link-local includes the cloud metadata address `169.254.169.254`.
- Refuse an IPv4-mapped or NAT64 IPv6 address, and any IPv6 address outside global unicast.
- Check an IP-literal host before you connect.
- Pin the connection to the checked address.
- Limit total time and body bytes. Count the bytes while the body streams.
- Follow no redirect during the document fetch. `[PRIMARY]`
- Accept status 200 only.
- Require the document's `client_id` to equal the requested client ID exactly. `[PRIMARY]`
- Parse the document with a non-strict schema that ignores unknown fields.
- Treat the client as public when its `token_endpoint_auth_method` is `none` or absent, or its `token_endpoint_auth_methods_supported` lists `none`.
- Refuse a document that names a `client_secret_*` or other shared-secret method, or that holds `client_secret`. `[PRIMARY]`
- Never fail a public-client token request only because it carries `client_assertion`. As an alternative, verify the assertion and advertise `private_key_jwt`.
- Apply every fetch check to `jwks_uri` when you verify a client assertion. `[PRIMARY]`
- Accept a presented `redirect_uri` only when it matches a registered entry and it is HTTPS, or HTTP on a loopback host.
- Let only the port differ for a loopback redirect URI. `[PRIMARY]`
- Refuse every other redirect URI scheme, even a registered one.
- Cache a document for the lifetime that its HTTP cache headers give, minus its `Age` value. Clamp that lifetime between a minimum and a maximum.
- Bound the cache entry count. Never cache a failure.
- Clean and display `client_name` per [failure prevention](traps.md).

## Connector interoperability

A hosted connector can call the server from provider infrastructure rather than from the user's device. Therefore a hosted connector cannot reach a localhost, stdio, or private-network endpoint. Use a publicly reachable HTTPS origin for broad connector support. `[PRIMARY]`

Confirm the active connector requirements for:

- supported transport and protocol revisions;
- authorization metadata fields and client registration behavior;
- public reachability and redirect behavior;
- callback and host restrictions; and
- the connector request timeout.

### Claude client

- Register the callback `https://claude.ai/api/mcp/auth_callback` for claude.ai, Claude Desktop, mobile, and Cowork. `[PRIMARY]`
- Accept a loopback redirect on any port for Claude Code, at `http://localhost/callback` and `http://127.0.0.1/callback`. `[PRIMARY]`
- claude.ai, Claude Desktop, and mobile use the client ID `https://claude.ai/oauth/mcp-oauth-client-metadata`. Its document registers `https://claude.ai/api/mcp/auth_callback` and declares the method `none`. `[OBSERVED]`
- Claude Code uses the client ID `https://claude.ai/oauth/claude-code-client-metadata`. Its document registers `http://localhost/callback` and `http://127.0.0.1/callback`, and declares the method `none`. `[OBSERVED]`
- Never guess a client ID. On a deployed server, read the client IDs in use from the grant records, per [directory readiness](directory-readiness.md#verification). Otherwise read each one from its published document.
- Advertise `"client_id_metadata_document_supported": true` and list `"none"` in `token_endpoint_auth_methods_supported`, and accept public clients at the token endpoint. Claude selects client ID metadata documents only when both are present. Otherwise Claude falls back to Dynamic Client Registration. `[PRIMARY]`
- Put the intended authorization server first in `authorization_servers`. Claude uses only the first entry. `[PRIMARY]`
- Set the protected-resource `resource` value to the exact MCP URL, path included. `[PRIMARY]`
- Advertise `code_challenge_methods_supported: ["S256"]`. `[PRIMARY]`
- List `offline_access` in `scopes_supported` for a refresh token. Claude requests it only when listed. `[PRIMARY]`
- Answer discovery, registration, and token requests within 10 seconds, and refresh requests within 30 seconds. `[PRIMARY]`
- Return `invalid_grant` for a dead refresh token. `[PRIMARY]`
- Send `WWW-Authenticate` on a 401 response. Claude ignores the header on a 200 response. `[PRIMARY]`
- Apply the payload and timeout limits in [directory readiness](directory-readiness.md#payload-and-timeouts).

### ChatGPT client

- ChatGPT uses the client ID `https://chatgpt.com/oauth/client.json`. `[OBSERVED]`
- Its document registers the redirect URI `https://chatgpt.com/connector_platform_oauth_redirect`. `[OBSERVED]`
- Its document declares `token_endpoint_auth_method: private_key_jwt`, lists `["none", "private_key_jwt"]` in `token_endpoint_auth_methods_supported`, and holds a `jwks_uri`. `[OBSERVED]`
- Accept ChatGPT as a public client per [Client ID metadata documents](#client-id-metadata-documents).
- Emit the `iss` authorization-response parameter per [Authorization server](#authorization-server). ChatGPT relies on it. `[OBSERVED]`

### VS Code client

- VS Code uses the client ID `https://vscode.dev/oauth/client-metadata.json`. `[OBSERVED]`
- Its document registers `https://vscode.dev/redirect` and `http://127.0.0.1:33418/`, and declares the method `none`. `[OBSERVED]`
- Its host serves the document with `Cache-Control: no-store`. `[OBSERVED]`

## Tokens and scopes

- Store access and refresh tokens so a database leak does not expose reusable token values. Prefer opaque tokens and store only a secure hash. `[PRIMARY]`
- Rotate refresh tokens atomically. Consume the old grant and create the replacement in one transaction, so a retry cannot destroy the new grant.
- Treat scopes as an allow-list. Reject an unknown requested scope. Never convert an unknown scope into broad access.
- Grant the smallest scopes that each tool needs. Keep privileged, write, administrative, and tenant-wide actions in distinct scopes.
- Rate-limit by authenticated identity, not source IP. Hosted connector traffic can share a small egress range.

## Tool contracts

- Design tools around user outcomes, not HTTP routes.
- Validate every input at runtime. Define typed output schemas where the SDK supports them.
- Return structured content for a successful tool call. Return a structured error result only for an expected business failure.
- Derive user and tenant identity from the token. Never accept them as trusted tool input.
- Enforce authorization, subscription or entitlement checks, and rate limits inside the tool path. Web middleware may not cover MCP traffic. Report an authorization or entitlement failure with the status contract below, not as a structured tool error.
- Give every tool accurate titles and annotations, including read-only and destructive behavior. `[PRIMARY]`

### Authorization failures compared with tool errors

Separate the error classes below.

- Protocol-layer authorization failures use HTTP status codes and the challenge header:
  - 401 for an absent or invalid access token.
  - 403 with `WWW-Authenticate: Bearer error="insufficient_scope", scope="..."` for a scope failure.
  - 400 for a malformed authorization request.
- Structured tool errors carry only in-scope business failures, such as absent data, a conflict, or a downstream error.

This separation prevents one concrete failure. The server returns a scope denial as a success status with a structured error body. The client cannot start step-up authorization from that response. The user then sees a permanently dead tool instead of a re-consent prompt.

## Timeouts and verification

- Set each timeout in the request path above the slowest supported tool: application, runtime, load balancer, proxy, and client. `[PRIMARY]`
- Keep the slowest tool within the active connector timeout ceiling. `[PRIMARY]`
- Keep a local test path when production OAuth restricts authorized hosts or callbacks.
- Verify discovery documents and the MCP endpoint from a public network before connector testing.

## Protocol fact refresh

Before planning implementation:

1. Read the current MCP specification, transport guidance, and authorization guidance.
2. Read the current connector documentation for each target client.
3. Check the selected SDK or adapter against those documents.
4. Record each material difference in the plan, including unresolved uncertainty.
5. If network access is unavailable, continue only with a dated uncertainty note. Do not present this reference as current protocol authority.

## Primary sources

The dated deep links below point at revision `2026-07-28`, which is a snapshot. The unversioned specification index resolves to the current revision, so use it as the always-current entry point. Some clients still implement the 2025 revisions, so a server may need to answer more than one revision era. Claude follows the 2025-03-26, 2025-06-18, and 2025-11-25 authorization specifications.

- [MCP specification](https://modelcontextprotocol.io/specification) `[PRIMARY]`
- [MCP transport specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports) `[PRIMARY]`
- [MCP authorization specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) `[PRIMARY]`
- [OAuth 2.1 draft](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1) `[PRIMARY]`
- [PKCE specification](https://www.rfc-editor.org/rfc/rfc7636) `[PRIMARY]`
- [RFC 8414 authorization server metadata](https://www.rfc-editor.org/rfc/rfc8414) `[PRIMARY]`. This document settles the authorization-server metadata fields and the well-known location that serves them.
- [RFC 9728 protected resource metadata](https://www.rfc-editor.org/rfc/rfc9728) `[PRIMARY]`. This document settles the protected-resource metadata document, its well-known location, and the 401 challenge header.
- [RFC 7591 dynamic client registration](https://www.rfc-editor.org/rfc/rfc7591) `[PRIMARY]`. This document settles the legacy dynamic registration request and response.
- [RFC 8707 resource indicators](https://www.rfc-editor.org/rfc/rfc8707) `[PRIMARY]`. This document settles the `resource` parameter and the audience restriction of an access token.
- [RFC 9207 issuer identification](https://www.rfc-editor.org/rfc/rfc9207) `[PRIMARY]`. This document settles the `iss` parameter and the metadata flag that advertises it.
- [OAuth client ID metadata document draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-client-id-metadata-document/) `[PRIMARY]`. This document settles the client ID URL form, the document fetch, and the `client_id` match.
- [RFC 8252 OAuth for native apps](https://www.rfc-editor.org/rfc/rfc8252) `[PRIMARY]`. This document settles loopback redirect URIs and their variable port.
- [RFC 9700 OAuth security best current practice](https://www.rfc-editor.org/rfc/rfc9700) `[PRIMARY]`. This document settles exact redirect URI matching and open-redirector attacks.
- [Claude custom integration guidance](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) `[PRIMARY]`
- [Claude connector authentication](https://claude.com/docs/connectors/building/authentication) `[PRIMARY]`. This document settles the Claude client facts above.

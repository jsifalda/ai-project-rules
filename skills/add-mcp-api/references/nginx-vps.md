# Nginx VPS deployment for a remote MCP API

A long-running application process runs behind nginx.

```text
Internet HTTPS -> nginx -> loopback application process
```

This topology satisfies these conditions:

- One public origin holds the authorization server and the MCP endpoint.
- No execution ceiling limits a tool call.
- The operator controls redirects, buffering, headers, and timeouts directly.

The `## Alternatives` section holds the platform decision.

## Public origin

- Set `<CANONICAL_HOST>` in application configuration. Build public URLs from it, not from request or forwarded headers.
- Point public DNS for `<CANONICAL_HOST>` at the VPS.
- Register only `<CANONICAL_HOST>` with the connector.
- Put each non-canonical host in a redirect-only server block.
- Do not redirect the canonical MCP endpoint or OAuth discovery paths to another host.
- Commit a template like this one. Keep host names, ports, certificate paths, and process-manager settings in deployment configuration.

## Placeholder configuration

Place the `log_format` and `limit_req_zone` directives in the `http` context. Place the server blocks in the site configuration included from that context.

```nginx
# http context
# $uri excludes the query string. Do not log $request here.
# A referring URL can carry a query string, so this format omits it.
log_format mcp_safe '$remote_addr - $remote_user [$time_local] '
                    '"$request_method $uri $server_protocol" $status $body_bytes_sent '
                    '"$http_user_agent"';

# This is one shared capacity budget for the public host.
# Do not key this zone by $binary_remote_addr or another client address.
limit_req_zone $server_name zone=mcp_capacity:1m rate=<CAPACITY_RATE>r/s;

upstream mcp_application {
    server 127.0.0.1:<APP_PORT>;
    keepalive <UPSTREAM_IDLE_CONNECTIONS>;
}

# Canonical HTTP host: serve ACME, then redirect only to its HTTPS form.
server {
    listen 80;
    server_name <CANONICAL_HOST>;

    location ^~ /.well-known/acme-challenge/ {
        root <ACME_WEBROOT>;
    }

    location / {
        return 308 https://<CANONICAL_HOST>$request_uri;
    }
}

# Each alias needs its own block. Serve ACME before redirecting it cross-host.
server {
    listen 80;
    server_name <NON_CANONICAL_HOST>;

    location ^~ /.well-known/acme-challenge/ {
        root <ACME_WEBROOT>;
    }

    location / {
        return 308 https://<CANONICAL_HOST>$request_uri;
    }
}

# The alias also needs an HTTPS listener. Its certificate must cover the alias name.
server {
    listen 443 ssl;
    server_name <NON_CANONICAL_HOST>;

    ssl_certificate <ALIAS_CERTIFICATE_PATH>;
    ssl_certificate_key <ALIAS_CERTIFICATE_KEY_PATH>;

    # This block serves no application traffic.
    return 308 https://<CANONICAL_HOST>$request_uri;
}

# Unknown host name on HTTPS. This block serves no application traffic.
server {
    listen 443 ssl default_server;
    server_name _;

    ssl_certificate <CERTIFICATE_PATH>;
    ssl_certificate_key <CERTIFICATE_KEY_PATH>;

    return 444;
}

# Canonical TLS origin. This block makes no host redirect.
server {
    listen 443 ssl;
    server_name <CANONICAL_HOST>;

    ssl_certificate <CERTIFICATE_PATH>;
    ssl_certificate_key <CERTIFICATE_KEY_PATH>;
    access_log <ACCESS_LOG_PATH> mcp_safe;

    # Keep these at server scope. A proxy_set_header in a child location
    # replaces the inherited proxy_set_header directives.
    proxy_http_version 1.1;
    proxy_set_header Host <CANONICAL_HOST>;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Connection "";

    # Exact and prefix locations outrank a broad dotfile deny rule.
    # Route discovery endpoints to the application before any such rule.
    location = /.well-known/oauth-authorization-server {
        proxy_pass http://mcp_application;
    }

    location = /.well-known/oauth-protected-resource {
        proxy_pass http://mcp_application;
    }

    location = /.well-known/oauth-protected-resource/<MCP_PATH> {
        proxy_pass http://mcp_application;
    }

    # Keep other required well-known paths available to the application.
    location ^~ /.well-known/ {
        proxy_pass http://mcp_application;
    }

    # The authorization and token endpoints need the same capacity control.
    location = /<AUTHORIZE_PATH> {
        proxy_pass http://mcp_application;
        limit_req zone=mcp_capacity burst=<CAPACITY_BURST> nodelay;
        limit_req_status 429;
    }

    location = /<TOKEN_PATH> {
        proxy_pass http://mcp_application;
        limit_req zone=mcp_capacity burst=<CAPACITY_BURST> nodelay;
        limit_req_status 429;
    }

    # A prefix match. An exact match leaves the trailing-slash form and every
    # sub-path to fall through to location /.
    location ^~ /<MCP_PATH> {
        proxy_pass http://mcp_application;
        proxy_buffering off;
        proxy_request_buffering off;
        proxy_connect_timeout <CONNECT_TIMEOUT>;
        proxy_send_timeout <UPSTREAM_SEND_TIMEOUT>;
        proxy_read_timeout <SLOWEST_TOOL_TIMEOUT>;
        client_body_timeout <CLIENT_UPLOAD_TIMEOUT>;
        client_max_body_size <MAX_TOOL_BODY>;
        limit_req zone=mcp_capacity burst=<CAPACITY_BURST> nodelay;
        limit_req_status 429;
    }

    location / {
        proxy_pass http://mcp_application;
    }

    # Add this only after the well-known locations above.
    location ~ /\. {
        deny all;
    }
}
```

Replace every angle-bracket value before deployment. Keep `<SLOWEST_TOOL_TIMEOUT>` above the measured slowest tool duration and at or below the active client ceiling.

The MCP location uses a prefix match. An exact match leaves the trailing-slash form and every sub-path to fall through to `location /`. In `location /` buffering stays on and no MCP timeout applies. The exact well-known locations above still win over this prefix. The application must not redirect between the slash forms of the endpoint.

## Directive decisions

| Directive or rule | Set it to | Reason |
|---|---|---|
| `proxy_http_version` | `1.1` | Preserve upstream HTTP/1.1 behavior for streaming traffic. |
| `proxy_buffering` | `off` on `<MCP_PATH>` | Send streamed output without proxy response buffering. |
| `proxy_request_buffering` | `off` on `<MCP_PATH>` | Send a streaming request body upstream without waiting for nginx to buffer it. Verify that the application needs this behavior. |
| `proxy_connect_timeout` | A short reachable-upstream limit | Fail quickly when the loopback process cannot accept a connection. |
| `proxy_send_timeout` | Above the largest upstream write duration | It bounds writes to the loopback process, not a client upload. |
| `client_body_timeout` | Above the slowest supported client upload | It bounds a slow client upload. The nginx default is 60s. |
| `proxy_read_timeout` | Above the measured slowest tool duration | Do not use the nginx default without checking it against the slowest tool. |
| `client_max_body_size` | The largest validated tool input | nginx answers 413 itself and writes no application log line. The default is 1m. |
| `limit_req_zone` key | `$server_name` | Share one capacity budget for connector traffic. Do not treat an egress IP as a user identity. |
| `limit_req` | Capacity-derived rate and burst | Protect the proxy and application. Apply user limits in the application. |
| `limit_req_status` | `429` | A default 503 reads as a server fault. A client can then retry at once or mark the server unhealthy. |
| `access_log` | A format with `$uri`, not `$request` | Exclude authorization query values such as `code` and `state`. |
| `server_name` | One explicit canonical host per TLS origin | Keep the connector, OAuth issuer, discovery documents, and MCP endpoint on one origin. |

## Redirect rules

A canonical HTTP-to-HTTPS redirect stays on the canonical host. A non-canonical host redirects to `<CANONICAL_HOST>`. Do not apply that redirect to the MCP endpoint or the OAuth discovery flow. A client that starts on the canonical origin must stay there.

Automatic certificate-tool redirects can create a host redirect when both an apex host and a `www` host exist. Inspect generated server blocks. Keep aliases redirect-only and keep the connector registration on the canonical host.

A cross-host redirect can remove `Authorization` from a retried request. Test redirects with an authenticated request, not only with an unauthenticated browser request.

## Well-known endpoints

Reserve OAuth and protected-resource discovery paths before any broad rule that blocks dot paths. A certificate challenge location can also capture `/.well-known/` requests. Limit the challenge location to its ACME subpath.

Serve each discovery path that the authorization design requires. A protected-resource document may be required both at its bare well-known path and at a path-aware location. RFC 9728 section 3.1 inserts the well-known string between the host and the path. For a resource at `https://<CANONICAL_HOST>/<MCP_PATH>`, the metadata path is `/.well-known/oauth-protected-resource/<MCP_PATH>`. The resource path comes after the well-known suffix, never before it. Fetch every required path from outside the VPS.

## Header inheritance

nginx normally forwards request headers, including `Authorization` and `Mcp-*` headers, unless configuration changes them. `proxy_set_header` changes only the named header.

However, a `proxy_set_header` directive in a `location` stops inheritance of all `proxy_set_header` directives from the parent context. Keep the header set in one scope. If a child location needs a header change, repeat every required proxy header in that location and test an authenticated request.

Do not use a broad header-clearing rule. Verify the effective configuration and the application request headers after deployment.

Pin the forwarded `Host` header to `<CANONICAL_HOST>`. A forwarded `$host` gives the application a client-supplied value. That value is the input the public-URL trap exists to defeat. The `default_server` block answers an unknown host name with 444 and serves no application traffic.

## Capacity limits

Connector traffic can arrive through shared egress addresses. A per-IP rate limit can make unrelated users consume one another's budget. Use the nginx limit only to protect VPS and application capacity. Enforce identity-based quotas, authorization, and product limits in the application after token validation.

Set `<CAPACITY_RATE>` and `<CAPACITY_BURST>` from measured application capacity. Start with a load-tested value. Do not copy a generic rate into production.

Apply the capacity limit to the OAuth authorization and token paths, not only to the MCP location. The token endpoint is a credential-replay target. Give the token endpoint its own capacity control.

## Timeout sizing

Measure each tool under realistic data and downstream conditions. Set the application execution ceiling and `proxy_read_timeout` above the slowest supported tool. Set the client-facing ceiling above the proxy timeout only when the client and transport require it.

Keep a margin for network transfer and application cleanup. A timeout that exactly matches a tool duration can fail during normal variation. Reject a tool design that needs a duration above the active connector limit. Split or redesign that operation instead.

## Alternatives

| Option | Use it when | Verify |
|---|---|---|
| Caddy | Its automatic certificate and reverse-proxy behavior meets the same origin, redirect, timeout, buffering, and logging rules. | Inspect generated redirects and configure streaming and timeout behavior explicitly. |
| Traefik | The deployment already uses dynamic routing. | Make routing, middleware, headers, timeouts, and streaming behavior explicit. |
| Cloudflare Tunnel | Inbound network exposure is unavailable. | Confirm OAuth redirects, streamed responses, request limits, and client-visible origin behavior. |
| Serverless | The platform execution ceiling exceeds the slowest tool duration. | Confirm the platform preserves the origin, headers, discovery routes, streaming, and timeout budget. |

Do not move an existing application platform only to add an MCP endpoint. State the platform ceiling against the slowest tool and offer this topology when the existing platform cannot meet the requirement.

## Nginx verification detail

The canonical sequence is the Connection verification ladder in `plan-template.md`. These rungs are its proxy-layer checks.

1. Resolve `<CANONICAL_HOST>` from a public network.
2. Verify the certificate and each canonical redirect.
3. Fetch every required well-known document from a public network.
4. Confirm that the MCP endpoint and discovery paths do not cross hosts.
5. Send an authenticated request and confirm `Authorization` and required `Mcp-*` headers arrive at the application.
6. Exercise a request longer than the unchecked nginx default and shorter than the configured timeout.
7. Confirm streamed output arrives before the response completes.
8. Inspect access logs and confirm authorization query values are absent.
9. Verify capacity limits protect the service without using an IP address as a user quota.
10. Send a body above `<MAX_TOOL_BODY>` and confirm nginx answers 413 with no application log line.
11. Restart the application process and confirm nginx can reach it again.
12. Connect with the target MCP client and complete an authenticated tool call.

## Claims requiring primary-source verification

Verify these claims against current primary documentation and the installed nginx version before deployment:

- The installed nginx default for `proxy_read_timeout`, including any distribution configuration that overrides it.
- nginx location precedence and `proxy_set_header` inheritance behavior.
- nginx request-header forwarding behavior for `Authorization` and extension headers.
- Certificate automation behavior for generated redirect and ACME challenge locations.
- The target connector timeout ceiling and supported transport behavior.
- The required OAuth authorization-server and protected-resource discovery paths for the active MCP and OAuth specifications.
- The target MCP client's treatment of cross-origin redirects and `Authorization` on a redirect.
- The hosting platform, tunnel, or proxy limits when an alternative is selected.

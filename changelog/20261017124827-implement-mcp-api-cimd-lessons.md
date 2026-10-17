# Cover every client ID metadata document client in implement-mcp-api

- Plans now target every standard client that uses client ID metadata documents, such as Claude, ChatGPT, and VS Code, not one vendor.
- Added the document checks: client ID form, a safe fetch with no private-network access, no redirect during the fetch, an exact `client_id` match, the public-client method rule, the redirect URI scheme rule, cache limits, and a fetch only for a signed-in user with access.
- Added a ban on shared-secret client documents, a rule to read token and refresh requests from the saved grant, and fetch checks on `jwks_uri`.
- Added traps for a client-host allow-list, an anonymous fetch, a private-network fetch, a cross-origin redirect, dot segments, a script redirect URI, a misleading client name, and an unchecked sign-in return path.
- Added the observed client IDs of each target client, the matching plan checks, and live-document fixtures plus a production check after each deploy.
- Why: a host allow-list refused standard clients, and opening it to any client needed these controls.

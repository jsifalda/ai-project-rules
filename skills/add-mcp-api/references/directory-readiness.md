# Claude directory readiness

> Fact status: reviewed 2026-10-11. Connector identity facts reviewed 2026-10-15. Recheck each rule against the [sources](#sources) before a plan becomes binding.

## Contents

- [Tool annotations](#tool-annotations)
- [Names and descriptions](#names-and-descriptions)
- [Prompt-injection bans](#prompt-injection-bans)
- [Read and write split](#read-and-write-split)
- [Errors](#errors)
- [Payload and timeouts](#payload-and-timeouts)
- [Conversation data and service scope](#conversation-data-and-service-scope)
- [Connector identity](#connector-identity)
- [Listing assets](#listing-assets)
- [Reviewer account and seed](#reviewer-account-and-seed)
- [Verification](#verification)
- [Portal steps and limits](#portal-steps-and-limits)
- [Compliance acknowledgments](#compliance-acknowledgments)
- [Sources](#sources)

## Tool annotations

- Set `title` at the top level and in `annotations.title` on every tool.
- Set `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint` explicitly on every tool.
- Set `readOnlyHint: true` only on a tool that changes no data.
- Set `destructiveHint: true` on every tool that modifies or deletes data, an irreversible status change included.
- Set `openWorldHint: true` when the tool, or a job it queues, reaches an external system with open content.
- Set `idempotentHint` from the real repeat behavior of the tool.
- Rely on the client prompt for a destructive tool. Write no confirmation request in its description.
- Fix on the server each tool that the portal flags for a missing title or annotation.

## Names and descriptions

- Keep each tool name at 64 characters or fewer.
- State what the tool does and when it applies, as facts.
- Match each description to the real behavior and the real return shape of the tool.
- Describe no feature that the tool does not deliver.
- Write a reference to another tool as a fact about that tool, never as an order.
- Write no directive phrase in a description or in the server instructions.
- Treat `confirm with the user`, `show the user`, `call <tool> first`, and `before you call` as directive phrases.
- Label third-party content in a result as untrusted content, as a fact, with no instruction on how to treat it.
- Name the target API in the description of a tool that takes a freeform path, query, or body.
- Choose names and descriptions that do not conflict with another connector in the directory.

## Prompt-injection bans

- Apply each ban below to every description and to the server instructions.
- Never tell the model to call a tool or service that the user did not request.
- Never interfere with the model's calls to other tools.
- Never direct the model to take behavior instructions from an external source.
- Never hide, obfuscate, or encode an instruction.
- Never tell the model to act outside the tool's function or to override system instructions.
- Never promote a product or service.
- Never word a description to make other software call the tool without need.

## Read and write split

- Keep safe and unsafe operations in separate tools. Never accept both in one tool.
- Ship no catch-all request tool with a method parameter.
- Never use a description to separate safe and unsafe operations inside one tool.

## Errors

- Return a successful response for every call with valid parameters.
- Validate each input and return an actionable error. Never accept invalid data silently.
- Map every domain error that a tool can throw to a specific message.
- Treat a domain error that reaches the generic catch-all as a review failure.
- Make the catch-all message name a retry and a support contact. Never name internals.
- Name in each error the field, the limit, and an action or tool that exists.
- Keep the `isError: true` result rate at 2% or below. Degraded starts above 5%.

## Payload and timeouts

- Keep the text copy that the SDK adds beside `structuredContent` as compact JSON.
- Cut each unbounded third-party text field at a fixed limit, with a marker that points to the source.
- Size each result to the task. Return a summary, not a full dump, when the request asks for a summary.
- Give an input that excludes unneeded text when a result can be large.
- Keep each tool result under about 150,000 characters for claude.ai and Claude Desktop.
- Keep each tool result under 25,000 tokens for Claude Code.
- Finish each tool call within 240 seconds.

## Conversation data and service scope

- Collect no conversation data beyond what the tool needs.
- Never query Claude's memory, chat history, conversation summaries, or user files.
- Call only the application's own first-party APIs, or APIs that it proxies with permission.
- Serve the MCP endpoint from a domain that matches the service.
- Expose no money or crypto transfer, and no AI image, video, or audio generation.
- Return no ads, sponsored content, or paid placement.
- Use Streamable HTTP. Use no SSE transport, resource subscriptions, sampling, or draft capabilities.

## Connector identity

- Make every icon from the application's existing brand mark. Never redraw it. Only scale, pad, or add a background.
- Keep one source file for the brand mark and one committed command that regenerates the whole icon set.
- Define the icon set in one manifest: file, format, pixel size, and theme. Generate the files and the advertised `icons` from it.
- Default the icon set to square PNGs at 48, 128, 512, and 1024 pixels, an `any`-size SVG, a favicon, and an apple-touch icon.
- Add each size that a target client or the directory portal names.
- Advertise a PNG at every size. Never make the SVG the only entry.
- Make the icon set read on light and dark backgrounds. Use an opaque tile, or one variant per background with `theme` set to it.
- Preview each icon on every background it targets before you ship it.
- Record a missing vector source as a non-blocking open question. Ship the PNG files, and never trace the brand mark.
- Copy each published listing icon into the set unchanged, and pin it with a content-hash test. Change it only on an explicit user decision.
- Add `title`, `websiteUrl`, and `icons` to the server info. Change no existing server info value.
- Build `websiteUrl` and each icon `src` as absolute HTTPS URLs on the canonical public origin, per [failure prevention](traps.md).
- Serve every advertised icon with no authentication, no redirect, and a content type that matches its bytes.

## Listing assets

- Publish a privacy policy that covers data collection, use and storage, third-party sharing, retention, and contact information.
- Publish a support page with a contact channel, not only a mailto link.
- Take the listing icon from the icon set in [Connector identity](#connector-identity).
- State in the plan that the Claude docs give no icon spec, and that the directory portal holds the exact upload rules.
- Publish a public docs page before the listing publish date.
- Show the exact MCP URL with a copy button on the docs page.
- State on the docs page that the user pastes the MCP path, not the docs path.
- Give the setup path for Pro and Max on the docs page: Customize → Connectors → "+ Add" → Add custom connector, then the URL.
- Name the OAuth client option "Use Claude's published identity (Recommended)" on the docs page when the server supports client ID metadata documents only.
- Give the setup path for Team and Enterprise on the docs page: an Owner adds it in Organization settings → Connectors. Members connect it in Customize → Connectors.
- Describe on the docs page the sign-in flow, every tool in plain words, and the data that the connector reads and writes.
- Write at least three working example prompts that show the core functions.

## Reviewer account and seed

- Give the reviewer a fully populated account with real records, real search data, and real write targets.
- Seed the reviewer account with an idempotent script and deterministic ids.
- Read the reviewer password from an environment variable.
- Keep reviewer access active through the review, even when a trial or beta ends.
- Make every seeded state change through the application's own chokepoint functions.
- Make no external call from the seed.
- Write reviewer setup steps with every link, credential, and step, for a reader new to the service.
- Pause each seeded active entity that can start background work in production after the review ends.

## Verification

- Run every tool through the MCP Inspector or a custom connector in Claude before you submit.
- List the tools with the `tools/list` method of the `@modelcontextprotocol/inspector` CLI over HTTP transport.
- Script the real OAuth flow as the allowed client when the authorization server allow-lists client hosts.
- Sign in, authorize with PKCE S256, and read the code from the redirect `Location` header without following it.
- Exchange that code at the token endpoint. Fall back to a token minted in a local database.
- Run every verification in a separate worktree with its own database and queue prefix when the production checkout holds the live database.
- Add a guard test that reads the real `tools/list` and `initialize` wire JSON.
- Fail the guard test on a missing title, a missing explicit hint, a name over 64 characters, or a directive phrase.
- Connect a real MCP client per supported protocol revision. Fail the guard test when any received server info lacks `title`, `websiteUrl`, or `icons`.
- Add an icon test that matches each advertised icon to its manifest entry, `theme` included, and checks the file's bytes against `mimeType` and `sizes`.

## Portal steps and limits

- Submit from a Pro, Max, Team, or Enterprise account. On Team, an Owner submits. On Enterprise, an Owner submits, or a member whose custom role carries the Directory permission.
- Keep one submission-kit doc with one section per portal step. Never keep a second copy.
- Put the field limit and a character count next to each limited field in the kit.
- Choose the listing slug before publish. The slug is permanent once published.
- Send review escalations and requests for other authentication types to `mcp-review@anthropic.com`.

| Portal step | Fields and limits |
| --- | --- |
| Connection | Public HTTPS MCP URL. A URL pattern or several URLs slow the review. |
| Tools | Synced from the server and grouped as read-only or write. |
| Listing | Name up to 100 characters, one-liner up to 200, description up to 2,000, 1–5 categories, docs URL, privacy policy URL, support contact, icon, permanent slug. |
| Use cases | Primary use cases, prerequisites such as accounts or plans, and read, write, or both. |
| Company | Name, website, primary contact. |
| Authentication | OAuth with DCR, OAuth with CIMD, Anthropic-held client credentials, custom connection, or no auth. |
| Data handling | Own API, permitted proxy, or third party. Personal health data. Sponsored content. |
| Test and launch | Reviewer setup with every link, credential, and step. Confirmation that every tool ran. |
| Compliance | Each acknowledgment in [Compliance acknowledgments](#compliance-acknowledgments). |
| Review and submit | Quality warnings, which reviewers also see. |

## Compliance acknowledgments

- Back each acknowledgment with a passing check in the plan before you submit.

| Acknowledgment | Rules in this file |
| --- | --- |
| Directory guidelines | Every section |
| First-party API usage | Conversation data and service scope |
| Financial transactions | Conversation data and service scope |
| AI media generation | Conversation data and service scope |
| Prompt injection | Names and descriptions, Prompt-injection bans |
| Conversation data collection | Conversation data and service scope |
| Public documentation | Listing assets |

## Sources

- [Connector review criteria](https://claude.com/docs/connectors/building/review-criteria)
- [Connector submission](https://claude.com/docs/connectors/building/submission)
- [Publish to the directory](https://claude.com/docs/directory/publish)
- [Authentication for connectors](https://claude.com/docs/connectors/building/authentication)
- [Test your connector](https://claude.com/docs/connectors/building/testing)
- [Anthropic Software Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy)
- [Get started with custom connectors using remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [MCP icons](https://modelcontextprotocol.io/specification/2026-07-28/basic#icons)

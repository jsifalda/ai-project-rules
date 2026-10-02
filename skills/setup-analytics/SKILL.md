---
name: setup-analytics
description: >-
  Provision Microsoft Clarity and Google Analytics 4 for the current project in the user's
  logged-in browser through the claude-in-chrome extension, then install both tags with a consent
  banner. Reads the stack, existing tags, GA accounts and Clarity projects first, shows one plan
  table, and acts only after explicit approval. Reuses a project or property whose URL matches the
  site, creates the rest, reads back the Clarity Project ID and GA4 Measurement ID, installs them
  (Next.js App Router, or any site with an HTML head), and checks network hits before and after
  consent. Use when the user asks to set up or add analytics, add Google Analytics and Microsoft
  Clarity, create a GA4 property or a Clarity project, or provision analytics for a new site. Do
  NOT use to read or report analytics data, GA reports, Clarity dashboards or recordings, for a
  code-only install with a known ID (use microsoft-clarity or nextjs-ga-tracking directly), or for
  GA4 user access management.
metadata:
  version: "1.0"
---

# Setup Analytics

## Input

- Run in the project root. The project is the input.
- Treat every console label and URL pattern in `references/` as the contract for the browser steps.
- Treat a label marked `(unverified)` as a hint. Match it by role and meaning, then confirm with `read_page`.

## Procedure

### 1. Preflight (read-only)

- Load the browser tools in one call.

```
select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__list_connected_browsers,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__find,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__form_input,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__javascript_tool,mcp__claude-in-chrome__read_network_requests,mcp__claude-in-chrome__tabs_close_mcp
```

- Call `tabs_context_mcp`.
- No answer → stop and tell the user to connect the Claude in Chrome extension.
- Accept any Chromium browser running the extension, Brave included.
- Several browsers connected → call `list_connected_browsers` and ask the user which one.
- Detect the stack. `next` in `package.json` `dependencies` or `devDependencies` → Next path. Anything else → generic path.
- Grep the source for existing tags, excluding `node_modules`, `.next`, `dist`, `build` and `.git`.

```
clarity.ms|clarity.init|G-[A-Z0-9]{6,}|googletagmanager|@next/third-parties|react-microsoft-clarity|NEXT_PUBLIC_GA
```

- Skip a service whose tag is already installed. Report it as skipped with the file and line.
- Skip GA4 only on a `G-` Measurement ID, a `gtag('config'` call, or a `@next/third-parties` `GoogleAnalytics` component.
- A `googletagmanager` hit with only a `GTM-` container → report it at the gate and ask.
- Resolve the production site URL. Order: the Vercel project's production domain, `package.json` `homepage`, the README. None found → ask.
- Read the existing Clarity projects and GA accounts in a new tab, read-only. Follow the reuse check in each console reference.
- Suggest time zone and currency from the system locale (`$LANG`, `date +%Z`).

### 2. Plan gate

- Show one table with every row below, filled with suggestions. Suggest names from the repo name.

| Row | Content |
|---|---|
| Services | Clarity, GA4, or one of them, with any skip from preflight |
| Clarity project | reuse `<name>`, or create `<name>`, industry `<industry>` |
| Clarity cookies switch | on for opt-out, off for opt-in. Shows any change to a reused project |
| Consent model | opt-out, granted until the visitor rejects (default), or opt-in, denied until the visitor accepts |
| GA account | each existing account by name, plus `new account` |
| GA account data sharing | the console defaults, listed |
| GA property name | suggested name |
| GA time zone | country and time zone |
| GA currency | suggested currency |
| GA industry and business size | suggested values |
| GA objectives | `Understand web and/or app traffic`, `View user engagement and retention` |
| GA web stream | stream name and site URL, or reuse `<stream>` |
| GA ToS country | the reporting country, or a fallback when the Terms of Service list lacks it |
| Terms | a new GA account → the skill accepts the GA Terms of Service and the Data Processing Terms on the user's behalf |
| Install path | Next or generic |
| Banner texts | banner description and button labels |
| Packages to add | Next path only, the packages the child skills add |
| Files to touch | each file path |

- Suggest opt-in when the site targets EEA, UK or CH visitors.
- Wait for explicit approval of every row. Apply each edit the user makes, then show the table again.
- Never create, accept or install anything before the approval.

### 3. Provision Clarity

- Follow `references/clarity-console.md` in a new tab.
- Reuse or create the project, then set the `Cookies` switch from the gate. Opt-out → on. Opt-in → off.
- Read the Project ID from the URL `/projects/view/<id>/`, or from Settings → Overview.

### 4. Provision GA4

- Follow `references/ga-console.md` in a new tab.
- Pick or create the account. Accept the Terms dialogs only when the gate approved them.
- Create the property, then the Web data stream.
- Read the Measurement ID `G-…` from the stream details.

### 5. Install

- Next path → invoke the `microsoft-clarity` skill with the Clarity Project ID.
- Next path → invoke the `nextjs-ga-tracking` skill with the Measurement ID and the gate's banner texts.
- Next path → add the consent defaults from `references/install-generic.md` as a `next/script` with `strategy="beforeInteractive"` in the root layout.
- Next path → add the Clarity `consentv2` call from `references/install-generic.md` to the banner's analytics `onAccept` and `onReject`.
- Next path → define the Clarity queue stub from `references/install-generic.md` before that `consentv2` call.
- Next path → write `analytics-consent` to `localStorage` in the Silktide analytics `onAccept` (`granted`) and `onReject` (`denied`).
- Next path → also write the `analytics-consent` cookie there, as the banner script's `write()` in `references/install-generic.md` does.
- Generic path → follow `references/install-generic.md`.

### 6. Verify

- Run the project's own build and checks. Fix every failure.
- Serve the site locally. Static site → `python3 -m http.server <port>` from the site root. Else → the dev script.
- Open the local URL in a new tab.
- Clear the local origin's storage before the first measured load. Run `localStorage.clear()`, expire every cookie for the host, then reload.
- Read cookie names only with `javascript_tool`. Read requests with `read_network_requests`.
- On load → requests show `clarity.ms/tag/<id>` and `googletagmanager.com/gtag/js?id=G-…`.
- Read the `gcs` parameter of each request whose path contains `/g/collect`.
- Match those requests on `google-analytics.com`, `region1.google-analytics.com` and `analytics.google.com`.
- `gcs=G101` → analytics granted. `gcs=G100` → analytics denied.
- Opt-out, before any choice → `gcs=G101` and a cookie name starting with `_ga`.
- Opt-out → clear the captured requests, click the gate's reject label by its `ref`, reload.
- Opt-out, after the reject → expect `gcs=G100` and no cookie name starting with `_ga` or `_clck`.
- Opt-in, before any choice → `gcs=G100` and no `_ga` cookie.
- Opt-in → click the gate's accept label, reload. Expect `gcs=G101` and a `_ga` cookie.
- Close every tab you created. Stop the server.

## Gotchas

- Login wall, account chooser or CAPTCHA → stop. Ask the user to sign in in the connected browser, then continue.
- Never trigger a JS `alert` or `confirm` dialog.
- Find elements by accessible name with `find` or `read_page`.
- Click by `ref`.
- A `ref` click with no effect → click the coordinates `find` returns for that element.
- Scroll a virtual list with `computer` `scroll` at the list's own position.
- A label from the references is missing → take a screenshot, stop, report. Never guess.
- Always open new tabs. Never use a tab the user opened.
- Never paste an ID into a public place other than the project code.
- GA `Exit` discards a draft wizard. Use it only to abandon a wizard on purpose.
- Return plain string arrays from `javascript_tool`. A result with `key=value` text can be blocked.
- Brave Shields or a blocker extension blocks `googletagmanager.com` or `clarity.ms` → ask the user to turn it off for the local URL.
- `window.google_tag_manager` undefined after load → a blocker stubbed the tag.
- A dropdown inside a dialog can close the dialog. Set dropdowns first, then text fields.

## Reporting

- Give the Clarity Project ID and the GA4 Measurement ID.
- Give the Clarity project URL and the GA stream details URL.
- List each changed file.
- Mark each resource as reused or created.
- List the manual next steps: deploy, wait for Clarity "Installation verified", open GA Realtime on the live site.

# Browser automation

Load when driving a browser, configuring browser tooling, or reading a bot-walled site.

## Always Chrome

- Any browser-driven tool — Playwright MCP, a CDP launcher, an agent-browser skill — targets
  the reader's installed Google Chrome. Prefer Playwright's `channel: "chrome"`. Needing an
  explicit binary → take it from `$CHROME_BIN`, and fall back to the platform default
  (`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` on macOS).
- Never Brave. Never bundled Playwright Chromium unless explicitly asked.
- This applies to every `--executable-path` arg, `CHROME_BIN` value, and browser-binary string,
  including examples in docs.

## Bot-walled sites

Login or a flow on a bot-detecting site needs real Chrome, headful, with anti-automation config:

```js
chromium.launch({ channel: "chrome", headless: false,
  args: ["--disable-blink-features=AutomationControlled"] })
context.addInitScript(() =>
  Object.defineProperty(navigator, "webdriver", { get: () => undefined }))
```

- Detect success by polling `context.cookies()` for the auth or session cookie, not a fixed
  wait. Never `page.waitForTimeout`, which detaches on redirect. Use a plain `setTimeout`.

## A 403 network-policy page is rate limiting

- A 403 carrying a "network policy" or "whoa there" page is transient IP rate limiting, not a
  fingerprint wall. It blocks a real browser from the same IP too.
- Do not probe-spam to diagnose. Do not reach for `curl-impersonate`, TLS impersonation, or a
  paid scraper.
- Stop, wait for the block to clear — minutes, up to about an hour — then retry.

## Off-API session reads

A pool of logged-in reader sessions works without an official API:

1. Mint a session with Playwright as above. Operator step, dev only.
2. Store the Playwright `storageState` encrypted at rest, AES-256-GCM.
3. At runtime there is no browser. Decrypt the pooled cookies and replay with a plain HTTP
   client, passing `Cookie`, `User-Agent` and `Accept` headers plus `raw_json: 1`.
   The response is the same JSON the official API returns.
4. Rotate sessions on 429 or 401. Propagate 403, 404 and 451 as "skip this target".

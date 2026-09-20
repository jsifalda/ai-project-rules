# Browser automation

- Target the installed Google Chrome. Prefer Playwright `channel: "chrome"`, else `$CHROME_BIN`, else the platform install path.
- Fail with a clear error when none resolves. Never fall through to Brave or bundled Chromium.
- Launch headful with anti-automation config for a bot-detecting site:
  ```js
  chromium.launch({ channel: "chrome", headless: false,
    args: ["--disable-blink-features=AutomationControlled"] })
  context.addInitScript(() =>
    Object.defineProperty(navigator, "webdriver", { get: () => undefined }))
  ```
- Detect login by polling `context.cookies()` for the session cookie. Never `page.waitForTimeout`, which detaches on redirect. Use a plain `setTimeout`.
- Treat a 403 "network policy" or "whoa there" page as transient IP rate limiting, not a fingerprint wall.
- Stop and wait for that block to clear, minutes up to about an hour, then retry.
- Never probe-spam it. Never reach for `curl-impersonate` or a paid scraper.
- Replay pooled logged-in session cookies with a plain HTTP client for off-API reads.
- Store `storageState` encrypted at rest with AES-256-GCM. Rotate a session on 429 or 401.
- Propagate 403, 404 and 451 as skip this target.

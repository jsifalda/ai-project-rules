# Add brave-submit-site skill

- Added `skills/brave-submit-site/` — submits a site URL or bare domain to Brave Search through the public submit form, driven with Playwright.
- Steps were derived from an actual end-to-end run against two live sites, not from docs, so the skill encodes the real gotchas: the Submit button starts disabled until the URL parses, one page load submits exactly one URL, and success needs both the `Submitted` button state and the Success panel.
- Also captured that Brave ignores the `site:` operator, which otherwise reads as a false negative when checking whether a site got indexed.
- Added the matching row to the README skills table.

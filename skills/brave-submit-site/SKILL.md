---
name: brave-submit-site
description: >-
  Submit a website URL or bare domain to Brave Search for indexing or re-fetching, through the
  public form at search.brave.com/submit-url driven with Playwright browser automation. Normalizes
  the input, fills and submits the form, confirms the Success state before reporting, handles
  several sites in one run by reloading the form between submissions, and explains how to verify
  indexing later. Use when the user asks to submit a site to Brave, get a domain indexed in Brave
  Search, add a site to Brave, ask Brave to re-crawl or re-fetch a page, or says their site is not
  showing up in Brave. Do NOT use for Google Search Console, Bing Webmaster Tools, IndexNow, or any
  other search engine, for SEO audits, keyword research, or sitemap generation, or for running a
  Brave Search query to read results (that is an ordinary web search).
---

# Brave Submit Site

Ask Brave Search to crawl a site through its public submit form. No account, login, or API key is
involved. Submission is a request to fetch, not a promise to index.

## Input

Takes one or more site URLs or bare domains.

- Bare domain (`example.com`) → prepend `https://`. The form rejects input with no scheme.
- Submit the canonical homepage URL. Brave labels the field "Insert the URL to be re-fetched", so
  the same form serves new sites and refreshes of already-indexed ones.
- No URL supplied → ask for one before doing anything.

## Procedure

Repeat per URL:

1. Navigate to `https://search.brave.com/submit-url`.
2. Snapshot the page. Locate the textbox `Enter a valid url` and the button `Submit`.
3. Type the full normalized URL into the textbox.
4. Snapshot again and confirm `Submit` is no longer `[disabled]`. It ships disabled on purpose and
   enables only once the field parses as a valid URL. Still disabled means the URL was rejected,
   almost always a missing `https://`. Fix and retry rather than clicking.
5. Click `Submit`.
6. Snapshot and require **both** signals before calling it done:
   - the button now reads `Submitted` and is `[disabled]`
   - a panel shows `Success` and `Thank you for your submission.`

   A click that returns without those signals is not a submission. Never report success off the
   click alone.
7. More URLs left → go back to step 1. The form does not reset after a submission, so one page load
   submits exactly one URL.

## Verifying indexing

- Check with a `site:example.com` query on Brave. Indexed answers with a "Only showing results from
  example.com" filter chip above real results from the domain.
- Not indexed answers with "search operators were not applied" and "Too few matches were found".
  That is Brave's fallback when the filtered query returns zero hits, so read it as not indexed yet.
  The operator is supported and did run.
- Do not fall back to querying the bare domain as plain text. It ranks lookalike domains and
  third-party mentions, neither of which says anything about the target site.
- Crawling takes days to weeks. An empty result minutes after submitting is the expected state.
  Report it as pending and stop. Do not resubmit on a loop, and do not wait for the index inside the
  same session.
- Brave's crawler sends no distinctive user agent, so server logs cannot confirm its visit. It also
  skips whatever Googlebot is blocked from, making Googlebot-crawlability a precondition.

## Gotchas

- A usage-metrics notice may sit at the bottom of the page with a `Close` button. It overlaps
  nothing and does not block the form. Ignore it.
- Resubmitting the same URL does not accelerate crawling.
- If Brave answers with a CAPTCHA or bot challenge, stop and hand it to the user. Do not attempt to
  work around it.
- Submitting a URL exposes it to a third party. For a private, internal, or unlaunched site, confirm
  with the user before submitting.

## Reporting

List each URL with its outcome, submitted or failed plus the reason. State plainly that submitted
does not mean indexed, and name the verification query the user can run later.

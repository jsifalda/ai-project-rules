# Deep Research Methodology (v2)

Load the section you need. Section numbers are referenced from SKILL.md.

## 1. Modes

| Mode | Tool calls | Min verdict claims fetched | Word cap |
|---|---|---|---|
| quick | 3 to 5 | 1 primary page | 300 |
| standard | 8 to 15 | every verdict claim | 700 |
| deep | 15 to 25 | every claim in the table | 1,500 |

Pick deep when the step is hard to undo: a permit application, legal status, tax residency, health, a large payment, an animal's safety.

## 2. Question classes and freshness

| Class | Typical question | Primary source | Freshness limit |
|---|---|---|---|
| legal | Is it allowed, what permit, what fee, what deadline | law text, gazette, regulator or ministry page, official fee schedule | 30 days |
| price | How much now, which plan | official storefront or price page, vendor quote | 7 days |
| ground-truth | Is X available here, does it work in this town now | none on the web. Web gives leads only | 7 days |
| health | Is it required, is there an outbreak, which drug | WHO, national public health body, ministry of health, drug regulator | 30 days |
| technical | How does X work, which spec | vendor docs, standards, datasheets | 90 days |
| landscape | Who are the options, what is the trend | mix, official data first | 90 days |

Freshness limit = max age of the `Checked` date for a claim in that class. Older → re-verify before use.

## 3. Source ladder

- **Tier 1, primary:** legislation and gazettes, regulator and ministry pages, official fee schedules, court records, official statistics, the seller's own price page, carrier or vendor policy pages, standards, peer-reviewed papers. An embassy page is primary for that embassy's own advice.
- **Tier 2, secondary:** established national press of the country in question, trade press, reputable international press.
- **Tier 3, leads:** forums, Reddit, Facebook groups, blogs, aggregators, SEO list pages, AI summaries. Never count toward `verified`. Use them to find a Tier 1 page, or to write a phone test.

Country ladders (named regulators, press, portals, contacts) live in project memory. When memory has one, use it before generic search.

Source `Type:` label in the report: `primary` (Tier 1), `secondary` (Tier 2), `lead` (Tier 3).

## 4. Query angles

Pick the angles that apply. Standard mode uses 4 to 6.

1. **Official:** regulator name + topic, `site:` the government domain, `filetype:pdf`
2. **Recency:** add the current month and year from today's date
3. **Local press:** national press names + topic
4. **Disconfirming:** the query that would prove the working answer wrong. Always 1
5. **Adjacent rule:** the neighbour regime the question ignores (visa → work permit, import → customs duty, price → regulatory fee)
6. **Practitioners:** forum or group leads (Tier 3)
7. **Contact:** office phone or email, for a phone test

## 5. Tool chain

1. `web_search_fast` → official pages, known entities, simple lookups
2. `web_search` → niche, very recent, prices, local topics, or when fast search returns thin results
3. `web_fetch` → the primary page. Only URLs that a search returned or the user gave. Never build a URL
4. Firecrawl `firecrawl_scrape` → when fetch fails: JS-gated page, robots block, 403, proxy block. Firecrawl `firecrawl_search` → when both search tools are thin
5. PDFs → `web_fetch` with PDF text extraction, or `firecrawl_scrape` with the `pdf` parser
6. Claude Code: use `WebSearch` for search, `WebFetch` for fetch, and the Firecrawl MCP tools when connected.

JS-gated page and Firecrawl also fails → log a dead end, mark the claim `single-source` or `unverified`.

MCP tools such as Firecrawl can need user approval per call. "No approval received" → log it as a dead end, do not retry it this run. Go on with search results and flag the primary page for a user test (section 8).

## 6. Budget and stop rule

- Stop when every verdict claim meets its status target, or the budget is spent.
- Never fetch the same page twice.
- Never repeat a dead end from memory.
- Budget spent with gaps → report the gaps. Do not extend without the user.

## 7. Triangulation and conflicts

- `verified` needs 2 sources from different publishers (different registrable domains), at least 1 primary.
- Same wire story or press release on several sites = 1 source. Cite the origin.
- Conflict tie-breakers, in this order: primacy, recency, authority on that exact point, method. Name the one you used.
- Two sources, same numbers, same date, same wording → suspect one origin. Look for it.

## 8. Ground-truth gate

For "is X available at place Y at time Z":

- Web evidence stays `single-source` or `unverified`, even with many pages.
- Action must start with a test:
  - 10-minute test: the concrete check the user runs (open the app at the location, call the office, ask the landlord for a speed test screenshot)
  - Phone test: who, number if known, exact question to ask
- Rank options on the deciding metric at that place and time. Label a rank built on brand, global size, or popularity `(est.)`.

Primary-page gate, all classes except `landscape`: no claim in the Evidence table cites a primary source → the first Action is a test where the user reads the primary page (official checkout, regulator page, fee schedule). Many press articles that quote one page are still one source.

## 9. Manual checklist (when scripts cannot run)

- [ ] First section is `## Verdict`
- [ ] Sections present: Verdict, Evidence, Conflicts, Action, What changes the verdict, Gaps and dead ends, Sources
- [ ] Every Evidence row has claim, value, `[N]`, `Checked YYYY-MM-DD`, status
- [ ] Every `verified` row has 2 sources, different domains, 1 primary
- [ ] No `Checked` date older than the class limit
- [ ] Every `[N]` has a Sources entry. Every Sources entry has URL, `Type:`, `Checked`
- [ ] Every URL came from a tool result this run
- [ ] Every number is `[N]`, computed, `(est.)`, or `(unverified)`
- [ ] `ground-truth` class → Action has a test
- [ ] No primary source in Evidence (not landscape) → Action has a test
- [ ] Under the word cap. No emoji, em dash, semicolon, placeholder

## 10. Write-back

Draft max 3 facts. Format:

```
- [topic] conclusion, value, checked YYYY-MM-DD, source publisher
- [dead end] URL or query, reason, YYYY-MM-DD
- [contact] name, role, phone or email
```

Save only after the user says ok, unless memory holds a standing instruction.

# Scenario format

## Section

- Write the section in this exact shape, with one block per scenario:

```markdown
## User Scenarios

### <ID>: <title>

- **Given** <the state the user starts in>
- **When** <the action the user takes>
- **Then** <the outcome the user sees>

Verified by: TODO
```

- Add a `- **And** <step>` bullet after a Given, When or Then bullet to extend that step.
- Write one Given, When, Then body per ID.
- Write the title as one line that names the user-visible behavior.

## IDs

- Build each ID as `<DOMAIN>-YYYY-MM-DD-slug`, with today's date.
- Write the slug as 2-5 words in kebab-case, taken from the user-visible behavior.
- Keep each slug unique per domain and date.
- Never give a new scenario an ID that the inventory holds or has retired. A scenario kept from the source's existing `## User Scenarios` section keeps its ID.
- Never edit an ID after you write it.
- Inventory uses an ID scheme other than this one → write dated IDs anyway and name the mismatch in the report. Never take the next number.

## Voice

- Describe what the user perceives in every step, never what the code does.
- Write no code symbols in a step. No function, error class, field, table, column, index or env var names, and no status codes.
- Write no HTTP verb and no route path. Name the action the user takes.
- Write each outcome as what the user sees, never as a status value or an API response.
- Rewrite an underscored status, tier or enum name as the prose the user reads on screen. Keep a single-word name as it is.
- Leave technical detail out of the section. `Verified by:` stays `TODO`.

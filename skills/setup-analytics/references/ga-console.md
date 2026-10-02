# GA4 console

## Contents

- URLs (L16-27)
- Account picker (L29-36)
- Reuse check (L38-43)
- Create menu (L45-48)
- Create an account (L50-61)
- Create a property (L63-85)
- Terms and data collection (L87-95)
- Web stream (L97-111)
- Measurement ID (L113-119)
- Stable selectors (L121-128)

## URLs

- Replace `<acct>` and `<prop>` with ids read from the page. `<prop>` is `0` when the account has no property.

| Page | URL |
|---|---|
| Entry | `https://analytics.google.com/analytics/web/` → redirects to `#/a<acct>p<prop>/admin` |
| Admin of one property | `#/a<acct>p<prop>/admin` |
| Create account | `#/a<acct>p<prop>/admin/account/create` |
| Create property | `#/a<acct>p<prop>/admin/property/create` |
| Data streams | `#/a<acct>p<prop>/admin/streams/table` |
| Stream details | `#/a<acct>p<prop>/admin/streams/table/<streamId>` |

## Account picker

- Open it with the button `Open the universal picker.`.
- Read the tabs `All`, `Favourites`, `Recent`, and the columns `Analytics Accounts` and `Properties & Apps`.
- Read rows as `role=option`. Each row text is `<name> <id>`.
- Scroll the `cdk-virtual-scroll-viewport` with the mouse wheel to render more rows. Setting `scrollTop` from JS does not re-render it.
- Read again after each scroll until no new row shows.
- Click the picker `Search` box. It opens a global search panel that finds properties by name and shows each property id.

## Reuse check (read-only)

- Search the site domain, then the project name, in the picker `Search` panel.
- Open the data streams page of each candidate property.
- Read the stream URLs with `get_page_text`.
- A web stream URL with the site's domain → reuse that property and stream. Never create a second one.

## Create menu

- Click `Create` in the left nav, then the `role=menuitem` `Account` or `Property`.
- `find` can return the left-nav `Account` expander instead. Filter `[role=menuitem]` by its text.

## Create an account

- Stepper: `Account creation` → `Property creation` → `Business details` → `Business objectives` → `Data collection`.
- Heading `Create an account`, card `Account details`.
- Fill the account name textbox. Visible label `Account name (Required)`, accessible name `My New Account Name`.
- Set the `Account Data Sharing Settings` checkboxes from the gate:
  - `Google products and services` (off by default)
  - `Modelling contributions & business insights` (on by default)
  - `Technical support` (on by default)
  - `Recommendations for your business` (on by default)
- Click `Next`. It stays disabled until the name is filled.
- Continue with "Create a property" below.

## Create a property

- Stepper: `Property creation` → `Business details` → `Business objectives` → `Data collection`.
- Step `Property creation`, heading `Create a property`, card `Property details`:
  - Fill `Property name (Required)` (`input#name`).
  - `Reporting time zone` has a country menu and a time zone menu. Set the country first. The time zone list depends on it.
  - Open each menu with its `[debug-id=menu-open-button]`. Type into `Type to filter`, then pick the `role=option`.
  - Country has no own time zone entry → pick a zone with the same UTC offset as that country. Report the zone.
  - The country menu sits in `ga-country-selector`. Its default comes from the browser locale.
  - Set `Currency` in `currency-selector` the same way.
  - Click `Next` (`[debug-id=next-step-button]`). It stays disabled until the name is filled.
- Step `Business details`, heading `Describe your business`:
  - Set `Industry category (Required)` in `industry-selector`. It starts as `Select one`.
  - Expect localized industry names that follow the browser locale. Pick the closest equivalent to the gate's industry. Report it.
  - Set `Business size (Required)`. The radio accessible names are only `1` to `4`. Pick by the visible text.
  - Visible texts: `Small – 1 to 10 employees`, `Medium – 11 to 100 employees`, `Large – 101 to 500 employees`, `Very Large - 501+ employees`.
  - Click `Next`. It stays disabled until both fields are set.
- Step `Business objectives`, heading `Choose your business objectives`:
  - Check the gate's objectives by their titles. Keep at most two.
  - Titles: `Generate leads`, `Drive sales`, `Understand web and/or app traffic`, `View user engagement and retention`, `Other business objectives`.
  - Property-only flow → click `Create`. Its accessible name is `Create a property`. This is the commit point.
  - New-account flow → click `Create an account with a property`. This is the commit point.
- Leave a draft with `Back to the previous page` → dialog `Exit and go back to Admin?` → `Exit` or `Cancel`. `Exit` discards all selections.

## Terms and data collection

- A new account shows the Terms of Service dialog after `Create an account with a property`.
- Set its country to the gate's `GA ToS country`. The list can lack the reporting country.
- Ignore the cookie notice inside the dialog's iframe (`OK, got it`).
- Check the Data Processing Terms checkbox, as the gate approved (unverified).
- Click `I Accept` (unverified). Never accept Terms the gate did not approve.
- A follow-up email preferences dialog shows → keep every box unchecked and save (unverified).
- Step `Data collection` asks for a platform → pick `Web` (unverified). It opens the web stream form below.

## Web stream

- Existing property → Admin → `Property settings` → `Data collection and modification` → `Data streams`.
- Click `Add stream` → menuitem `Web`.
- A `Notice` dialog "Are you sure that you want to create another web stream?" → the property has a web stream.
- Stop at that dialog and return to the reuse check.
- Panel `Set up data stream`, card `Set up your web stream`:
  - Keep `https://` in the combobox `URL protocol selector`.
  - Fill `Website URL` with the host, no protocol.
  - Fill `Stream name`. Its accessible name is `My Website`.
  - Keep `Enable enhanced measurement` on.
  - Click `Create and continue`. It stays disabled until the fields are filled.
- Expect a stream list with a `Next` button. `Next` opens the `Set up a Google tag` panel in an iframe.
- Skip that panel. `get_page_text` cannot read it.
- Close the setup panel without saving with `Close web stream setup`.

## Measurement ID

- The stream details URL opened directly shows only the stream table.
- Click the stream row → panel `Web stream details` → section `Stream details`.
- Read the value under `MEASUREMENT ID` with `find`. It starts with `G-`.
- Read the stream id under `STREAM ID` for the report URL.
- Close with `Close web stream details`.

## Stable selectors

- Use accessible names and `debug-id`s. Never coordinates.
- Picker: `Open the universal picker.`, rows `role=option`.
- Wizard: `input#name`, `[debug-id=menu-open-button]`, `[debug-id=next-step-button]`, `Type to filter`, `Create a property`.
- Material menu options render in `.cdk-overlay-pane [role=menu] [role=option]`. Read them after the menu opens.
- Dialogs `Exit`, `Cancel`, `Yes`, `No` are Material dialogs, not JS dialogs.
- Streams: `Add stream`, `Website URL`, `My Website`, `Create and continue`, `Copy Measurement ID`, `Close web stream details`.

# Clarity console

## URLs

| Page | URL |
|---|---|
| Projects list | `https://clarity.microsoft.com/projects` |
| One project | `https://clarity.microsoft.com/projects/view/<id>/dashboard` |
| New project landing | `https://clarity.microsoft.com/projects/view/<id>/gettingstarted` |

- `/projects` shows the project list, or redirects to the last opened project. Handle both.
- Redirected → click the Clarity logo, then the header button `My Projects`.
- Never open `/projects/view/<id>/settings` directly. It redirects to `gettingstarted`. Click the `Settings` tab.

## Sign-in check

- Treat a `Welcome back!` card with `Sign in to Microsoft`, `Sign in to Facebook` and `Sign in to Google` as a login wall.
- Login wall → stop and ask the user to sign in.
- A cookie banner with `Accept`, `Reject` and `Manage cookies` → click `Reject`.

## Reuse check (read-only)

- Read the project cards with `get_page_text`. Each card shows the project name and the site URL.
- Reuse the project whose site URL has the site's domain. Never create a second one.
- Never click a card's `Delete` button.

## Create a project

1. Click the toolbar button `New project` (accessible name `Add new project`). A dialog `Add new project` opens on the `Website` tab.
2. Open the `Website industry` dropdown (`role=combobox`, shows `Select one`) first. Pick the gate's Clarity industry.
3. Wait until the dropdown closes and the dialog is still open.
4. Fill `Name` with the gate's project name.
5. Fill `Website URL` with the site URL.
6. Click the dialog's `Add new project` button. It stays disabled until every field is filled.
7. Expect a redirect to `/projects/view/<id>/gettingstarted`.

## Project ID

- Read `<id>` from the URL segment after `/projects/view/`.
- Confirm it in `Settings` → `Overview`, next to the text `Project ID:` and the `Copy` button.
- Never press `Save` or `Delete this project` on the `Overview` form.

## Cookie setting

- Open the `Settings` tab → `Setup` → card `Advanced settings` → switch `Cookies` (`role=switch`).
- Expect `Cookies` on in a new project.
- Read `aria-checked` before any click. Click only when the state differs from the gate.
- Gate says off until consent → set `Cookies` to off.
- Gate says on → leave `Cookies` on.
- The switch has no `Save` button. Re-read `aria-checked` after the click to confirm the state.
- Leave `Bot detection` unchanged.

## Tracking code

- `Settings` → `Setup` → `Install manually` → `Get tracking code` shows the official snippet.
- Use that code when it differs from the loader in `install-generic.md`.

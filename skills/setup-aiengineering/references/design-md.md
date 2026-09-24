# Design Source of Truth Template (`DESIGN.md`)

SKILL.md Step 5b runs this module. It writes or keeps a `DESIGN.md` at the target repo root, then
injects the `## Design` block below into the project's agent instructions file. Copy the block
verbatim, except for the substitutions named under `## Substitutions`.

**Why.** `DESIGN.md` is compact design context for agents. Token values also live in code, so one
file must govern, and this block names it. A stale `DESIGN.md` is worse than none. An agent trusts
it and copies the wrong value. That is why the "Design in sync" gate exists.

**Format.** The target's `DESIGN.md` follows the Google Labs DESIGN.md spec
(`github.com/google-labs-code/design.md`, alpha). YAML front matter holds the token values. Markdown
prose holds the intent. Keep the canonical section order: Overview, Colors, Typography, Layout,
Elevation & Depth, Shapes, Components, Do's and Don'ts. Project sections come after them.
The skeleton lives in `assets/DESIGN.template.md`.

## Applicability

Scan the target repo for UI signals, read-only:

- **Framework dependency** in the manifest: `react`, `vue`, `svelte`, `solid`, `angular`, `next`,
  `nuxt`, `astro`, `remix`, `react-native`, `expo`, `flutter`.
- **Styling**: a Tailwind config, or a CSS `@theme` block.
- **Style files**: any CSS or SCSS file.
- **Templates**: HTML templates.
- **Native views**: SwiftUI or Compose views.
- **Design tokens**: a DTCG or other token JSON or YAML file, for example `tokens.json` or
  `design-tokens.*`.
- **Theme**: a theme provider or theme object in source.
- **Existing design file**: a `DESIGN.md` or `design.md` already at the repo root. This signal
  alone still counts → route to `## Existing file`, never `N/A (no UI)`.

Then branch:

- **Signals found** → offer the module in the Step 4 menu, default ON.
- **No signals, greenfield repo** (greenfield per `references/backfill-guide.md`) → ask *"Will this
  repo have a UI?"* Yes → offer the module, default ON. No → label it `N/A (no UI)`.
- **No signals, working repo** → label it `N/A (no UI)`. Do not offer it.

## Existing file

A `DESIGN.md` or `design.md` already at the repo root → **never overwrite it.**

- **Keep its file-name case.** The file is the user's, and a rename breaks their links to it.
- **Diff its sections against `assets/DESIGN.template.md`.** Offer only the missing sections. Ask per
  section, and add only the ones the user accepts.
- **Skip the backfill and the greenfield flow below.** The file is the user's. Do not re-derive it.
  Exception: the kept file's `## Source of truth` section names no token source → run Backfill
  step (a), read-only, only to resolve `{{TOKEN_SOURCE}}`.
- **The kept file counts as written** for the gate conditions in `## Gate pointer`.

## Backfill (working repo with UI)

**Runs whatever the user answered in Step 3.** A `DESIGN.md` that does not describe today's code is
wrong from its first day. The user can still decline the draft at the end.

- Step 3 ran its survey → reuse it, and read only the design sources it did not cover.
- Step 3 did not run it → read every design source below.

**a. Inventory the token sources.** Find each one and record its path:

- Tailwind config, or a CSS `@theme` block.
- CSS custom properties (`:root` blocks).
- Theme providers (a theme object passed to a provider component).
- DTCG or other token JSON or YAML files.
- Font loading (`next/font`, `@fontsource/*`, font `<link>` tags, `@font-face`).
- The component library and its import paths.

**b. Measure the drift.** Count the distinct values in use:

- Raw colours outside the token sources.
- Spacing values off the scale.
- Distinct font sizes.
- Distinct radii.
- Distinct shadows.

**c. Reconcile the baseline rules.** Compare the template's baseline Do's and Don'ts with the
current code. Drop every baseline rule the current code breaks, so the file describes reality
only. Keep the rules the code already follows. Report every dropped rule in the Step 8 report. A
rule the code already breaks would fail the Design-in-sync gate on every UI change.

**d. Record reality.** The canonical value for each token is the most-used one. Put it in the front
matter. Put the off-scale values in a `## Known inconsistencies` section, as debt. Agents read that
section as values not to copy.

**e. Ask for the intent.** Run a short interview:

1. **Audience.** Who uses this app?
2. **Use case.** What single job does it do?
3. **Tone.** One extreme, not "clean and modern".
4. **Aesthetic reference.** One concrete product, site or artefact, not adjectives.

Never invent intent. Mark anything inferred from the code `(inferred)`.

**f. List the components.** The Components section names the existing components with their import
paths. Agents then reuse them and never rebuild them.

**Hard limits.**

- Never redesign during setup. Record what is there.
- Never change app code.
- Never create a token file.
- No code token file exists → write `Token source: none yet` in the Source of truth section.
  Extracting a token file is a separate task, done only on request.

**Show the draft, write on a yes.** Then close with one optional line: *"Run `hallmark audit` later
to find design debt."* It is a suggestion only. Do not run it.

## Greenfield with UI intent

- **`frontend-design` and `hallmark` both available** → run hallmark's design-context gate
  (audience, use case, tone) and frontend-design's direction step (purpose, tone, differentiation).
  This is the same pairing those skills use together. Then ask for one concrete aesthetic
  reference, since the template's Overview and first Do rule both require one. Their answers fill
  the template. Mark any value either skill inferred `(inferred)`. Never invent intent.
- **Either skill unavailable** → tell the user which one. Then ask audience, use case and tone, plus
  one concrete aesthetic reference. Fill the template from the answers and the template's baseline
  Do's and Don'ts.

**Show the filled file, write on a yes.**

**The user declines** → skip the module and write no file. Label it `skipped (declined)`.

**Never write a placeholder `DESIGN.md`.** A placeholder teaches agents to ignore the file.

## Availability guard

Same pattern as SKILL.md Step 6. Before invoking `frontend-design` or `hallmark`, confirm it is
available on this machine.

- **Available** → invoke it.
- **Absent** → tell the user, name the missing skill, and use the fallback questions above.
- **Never fail silently.** The Step 8 report names any skill that was missing.

---

## Design

`{{DESIGN_FILE}}` is the source of truth for how this app looks. Code implements it.

- Read `{{DESIGN_FILE}}` before any UI change.
- Use only the tokens it names. No raw colour, size, radius, shadow or font value outside
  {{TOKEN_SOURCE}}.
- Reuse the components it lists. Never rebuild one it names.
- Code and `{{DESIGN_FILE}}` disagree → `{{DESIGN_FILE}}` wins, fix the code. The user decides the
  code is right → update `{{DESIGN_FILE}}` in the same change.
- The user asks for a visual change → update `{{DESIGN_FILE}}` first, in the same change as the
  code.
- A new token, pattern or deviation the user did not ask for → draft the `{{DESIGN_FILE}}` change
  and ask first.
- New UI work → load the `frontend-design` and `hallmark` skills when available. `{{DESIGN_FILE}}`
  wins over both.
- Read `{{DESIGN_FILE}}` on demand. Never `@`-import it into this file. It would load in every
  session.

---

## Substitutions

- **`{{DESIGN_FILE}}`** → the design file's actual name at the repo root — `DESIGN.md` for a file
  this step writes, or the kept file's exact name and case (`DESIGN.md` or `design.md`).
- **`{{TOKEN_SOURCE}}`** → the token file path or paths from backfill step a, in backticks, e.g.
  `` `tailwind.config.ts` and `src/styles/tokens.css` ``. The file was kept (the `## Existing
  file` branch skips the backfill) → take the token source from the kept file's `## Source of
  truth` section. That section is absent or names none → run backfill step (a), read-only, to
  find it. Still nothing found → the no-token-file case.
- **No-token-file case** → replace the whole raw-value bullet in the block with: "Use only the
  values the `{{DESIGN_FILE}}` front matter lists. Add no colour, size, radius, shadow or font
  value that it does not list." Keep the original bullet for the token-file case.

## Injection notes

- **Heading already there.** A `## Design` heading already in the target → diff it against this
  block and ask. Never duplicate it, like every injected block.
- **Scope block row.** Add the content-home row for the design file to the scope block, under its
  actual name, only when this step wrote or kept a design file. Step 1 omits the row.
  `references/instructions-scope.md` owns the row.
- **Provenance note.** List `Design` in the provenance note sections (SKILL.md Step 5).

## Gate pointer

The "Design in sync" tail gate text lives in `references/verification-protocol.md`. Do not copy it
here. SKILL.md Step 6b appends it only when all of these hold: this module was selected, the
verification module was selected, and this step wrote or kept a `DESIGN.md`.

## Re-run

- **An existing `## Design` section** → diff it against this template and ask. Preserve local edits.
  Never clobber.
- **An existing `DESIGN.md`** → follow `## Existing file` above.

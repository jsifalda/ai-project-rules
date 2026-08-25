---
description: The Tailwind v4 preflight change that removed `cursor: pointer` from buttons, and the one `@layer base` fix. Named by `rules/builder.md` — read from there when the chosen stack includes Tailwind v4 and shadcn/ui.
applyTo: '**/*.{css,tsx,jsx}'
paths:
  - '**/*.css'
  - '**/*.tsx'
  - '**/*.jsx'
---

# Tailwind v4 cursor trap (shadcn/ui default stack)

- Tailwind v3's preflight set `button, [role="button"] { cursor: pointer }`. Tailwind v4 removed
  that rule (a documented breaking change). Result: every `<button>` and `[role="button"]` falls
  back to the UA default `cursor: default`, while `<a href>` keeps `cursor: pointer` — links feel
  clickable, buttons do not.
- `<summary>`, `<select>`, and a checkbox or radio `<label>` are not part of that regression —
  Tailwind's preflight never set a pointer on them in v3 either. They read as clickable and are
  not, so fix them in the same place.
- Fix once, in the global stylesheet's `@layer base` — never per-component `cursor-pointer`
  utilities, which just hide the bug in each new component instead of fixing it:
  ```css
  @layer base {
    button:not(:disabled):not([aria-disabled="true"]),
    [role="button"]:not([aria-disabled="true"]):not(:disabled),
    summary,
    select:not(:disabled),
    label:has(input:is([type="checkbox"], [type="radio"]):not(:disabled)),
    input[type="checkbox"]:not(:disabled),
    input[type="radio"]:not(:disabled),
    input[type="file"]:not(:disabled),
    input[type="file"]:not(:disabled)::file-selector-button {
      cursor: pointer;
    }
  }
  ```
- Text inputs and textareas are deliberately excluded — they keep the text caret.
- A `<label for>` that does not wrap its input is out of reach — CSS cannot see the target's type
  through `for=`. shadcn/ui's `<Label htmlFor>` + `<Checkbox>` pairs are the common case. That pair
  is the one place a `cursor-pointer` utility on the label is correct.

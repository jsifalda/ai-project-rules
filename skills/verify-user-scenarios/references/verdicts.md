# Verdict rubric

Every scenario gets exactly one verdict. Use the decision test to pick between a verdict and
its nearest neighbor. Evidence always comes from the browser, never from reading code.

## pass

1. **Definition.** The browser did what the Then step says.
2. **Decision test** (nearest neighbor: `fail`). Did the observed outcome match the Then step
   with no deviation? Yes → `pass`. A close match with one wrong detail is `fail`, not `pass`.
3. **Example.** A visitor searches a marketplace by keyword. The Then step says matching
   listings appear, sorted newest first. The browser shows exactly that.
4. **Severity.** Not scored. A pass has nothing to fix or decide.

## fail

1. **Definition.** The feature is implemented, and it behaves differently from the Then step.
   A real defect.
2. **Decision test** (nearest neighbor: `gap`). Does a control, route, or page for this
   behavior exist at all? Yes, and it does the wrong thing → `fail`. No control exists at
   all → `gap`.
3. **Example.** A seller sets a price filter on a catalog page. The Then step says only items
   inside the range appear. The browser shows items above the upper bound too.
4. **Severity.** High: a core flow breaks, data is lost or corrupted, or private information
   is exposed. Medium: the feature works but degrades the experience — wrong order, wrong
   copy, a wrong count. Low: a cosmetic mismatch with no behavior change.

## gap

1. **Definition.** The scenario is documented, and the behavior is absent. No UI surface, a
   dead control, a missing page where one is described.
2. **Decision test** (nearest neighbor: `fail`). Same question as above, asked from this side:
   is there nothing to click, load, or trigger for this behavior? Yes → `gap`. Something
   exists and misbehaves → `fail`.
3. **Example.** The scenario describes a "report this listing" link on a listing page. The
   browser loads the page and no such link, button, or menu item exists anywhere on it.
4. **Severity.** High: a documented primary flow — completing a purchase, publishing a
   listing, signing in — has no surface at all. Medium: a secondary feature is missing. Low: a
   minor documented affordance, such as a shortcut or a filter, is missing.

## drift

1. **Definition.** The app is correct, and the scenario is wrong. The behavior changed on
   purpose and the doc was never updated, or the scenario was never accurate. Also covers a
   `Verified by:` pointer aimed at a test that does not actually assert this scenario.
2. **Decision test** (nearest neighbor: `fail`). Before recording `fail`, ask once: is this
   the behavior the product intends today? Yes, deliberately → `drift`. No, this is an
   unintended defect → `fail`.
3. **Example.** The scenario says free accounts can post five listings a day. The product now
   caps free accounts at three, agreed and shipped weeks ago. The app enforces three
   correctly; the doc still says five.
4. **Severity.** Judged by how misleading the doc is, never by how the app behaves — the app
   is already correct. High: the doc states the opposite of reality, or misstates a privacy or
   money rule a reader would trust. Medium: the doc describes an earlier version of the
   behavior. Low: the wording is imprecise but leaves no wrong impression.

## blocked

1. **Definition.** The scenario could not be reached. A missing fixture, an unconfigured
   provider, a failed prerequisite scenario, a bucket that does not exist, a missing required
   environment variable. The reason must be named. For a missing environment variable, name
   the variable itself — not just "a variable is missing".
2. **Decision test** (nearest neighbor: `fail`). Did something outside the behavior under
   test stop the run before it could observe an outcome? Yes → `blocked`, and name what
   stopped it. No, the run reached the behavior and it was wrong → `fail`.
3. **Example.** The scenario needs a verified account, and the verification email never
   arrives in the local mail capture. The browser never reaches the step under test.
4. **Severity.** High: the block sits on a prerequisite that many other scenarios also
   depend on. Medium: the block affects a small group of scenarios or has a known, quick
   fix. Low: one isolated scenario is blocked, with a documented workaround.

## Tie-breakers

- Could not reach it → `blocked`, never `pass`, never `fail`. An unreached scenario has no
  evidence either way.
- The control exists but does the wrong thing → `fail`. The control does not exist at all →
  `gap`.
- Before recording `fail`, ask once whether the Then step is still what the product intends.
  If the app is deliberately right, it is `drift`.
- A prerequisite scenario that failed makes its dependants `blocked`, not `fail`. Say which
  prerequisite.
- "The code looks right" is never evidence. The verdict comes from what the browser did.
- One verdict per scenario. A scenario that seems to deserve two is really two scenarios, and
  that is itself a `drift` finding against the inventory.

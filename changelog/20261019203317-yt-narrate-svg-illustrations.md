# yt-narrate-video: inline SVG illustrations, no install

- Removed the watercolor painting engine, its example scene and its reference (moved to trash).
- Illustrations are now original inline SVG in the page, colored through theme classes, with a `rep()` helper for repeated shapes. New `references/illustrations.md`.
- `assemble.py` now only checks the page, with the standard library. `shoot.py` drives a system Chrome or Chromium and skips cleanly when none is found.
- Non-video sources use chapter labels in place of timestamps.
- Skill version 2.0, README row updated.
- Why: OpenCV, numpy, Pillow and the browser automation package were often missing, so the skill failed before it could ship a page.

# code-review-full opens its report and gains a security lens

- The HTML report now opens automatically at the end of Stage 9, before the posting offer. It
  was the deliverable, but the skill deliberately printed only a path, so the reader had to
  open it by hand every run. A failed open never fails the run.
- Added a security lens as Stage 4c. It delegates to the host's `security-review` skill when
  the host provides one, and runs inline against the new `references/security-review.md`
  otherwise, which matches how the structure and council lenses already degrade. The structural
  lens puts security out of scope, so no lens covered it before.
- The security lens is pointed at the pinned diff, because `security-review` reviews the
  checked-out branch by default and this pipeline reviews a diff that is often a different
  branch.
- Reviewer-set counts now name the set instead of counting it, per the repo counts rule. Adding
  one lens forced count edits in about ten places, which is the drift the rule exists to stop.
- No new dependency. `security-review` is a host built-in, not a skill in this repo, so the
  README `Depends on` cell is unchanged.

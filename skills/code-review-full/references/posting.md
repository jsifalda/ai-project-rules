# Posting the approved comments

Stage 10. Runs after the verdict, the comments and the report are already out, so
the user has read the report before deciding anything.

**Nothing here relaxes the read-only rule.** That rule protects the code under review.
Stage 10 writes exactly one thing, a comment the user approved individually, in the
same turn they approved it. Close, merge, approve, delete and edits to repository files
stay banned at every point.

## When Stage 10 runs at all

Three gates. All three must pass, and a failed gate is stated in one line, never
silently skipped.

| Gate | Passes when | One-line skip note |
|---|---|---|
| Source | `$SOURCE` was an MR or PR URL, or `MR !N` / `PR #N` | `Nothing to post to, this was a <branch/commit-range/working-tree> review.` |
| Interactivity | There is a channel to ask the user | `Posting skipped, this run cannot ask for approval.` |
| Findings | At least one comment survived to the verdict | `Nothing to post, no findings were kept.` |

**The source gate does not go looking for a target.** If the review was pinned by
branch name, do not resolve that branch's open MR and offer to post there. A silently
resolved target is the one way this stage can put a comment on the wrong MR, and the
cost of being wrong is a notification to everyone watching a merge request the user
never mentioned. They can rerun against the MR URL.

**The interactivity gate is absolute.** The user's approval is the entire safety
mechanism, so a run that cannot ask cannot post. There is no "post the blockers
anyway" case.

## Where the offer appears

When all three gates pass, the offer **replaces** the closing next action in
`output-contract.md` §1 rather than being appended after it. That section forbids
closing on a question, and this is the exception it was shaped around: posting is one
concrete action, which is exactly what the closing line is for.

```
Next: post these 3 comments to MR !1234? I'll go one at a time.
```

Not `Would you like me to...`, not a list of what could happen next. One action.

## Before the picker

Ask the host what is already there, so a second run on the same MR does not quietly
duplicate the whole set.

```bash
python3 "$SKILL_DIR/scripts/post-comment.py" --host gitlab --target <iid> --list-existing
```

It returns the `file:line` anchors it found in existing comments. Every comment this
skill writes opens with its anchor, so an anchor already present means that finding
was raised before. Flag those in the picker as already posted. **Flag, do not remove.**
The user may be deliberately re-raising something that was ignored.

## The picker

One comment per prompt. Never batch, never present a multi-select. The user asked for
one at a time because each one is a message to a colleague, and a checklist invites
approving five things after reading one.

Each prompt shows the comment body in full, its anchor, and the placement it will take
(inline, or general with the reason). Four choices:

| Choice | Effect |
|---|---|
| **Post** | Post it, report the outcome, move to the next |
| **Skip** | Do not post, move to the next |
| **Edit** | Take replacement text from the user, show it back, then post that |
| **Stop** | Abandon the rest of the queue, go straight to the summary |

**Stop is not the same as skipping the rest.** A bad first comment usually means the
whole set needs rework, and the user should not have to decline four more to get out.
Report the remaining comments as not offered, not as skipped.

**Edit posts what the user wrote, verbatim.** Do not re-run it through the shaping
rules, do not restore an anchor they removed, do not fix their spelling. They saw the
generated version and chose to change it. Show the replacement back before posting so
a paste accident is caught, then post exactly that.

## Posting one comment

Never build the API call by hand. Write the body to a file and call the script.

```bash
printf '%s' "$COMMENT_BODY" > "$RUN/comment-F1.md"
python3 "$SKILL_DIR/scripts/post-comment.py" \
  --host gitlab --target 1234 \
  --file src/Search.kt --line 84 \
  --body-file "$RUN/comment-F1.md" \
  --diff "$RUN/diff.patch"
```

Two failures the script exists to prevent, both of which look like success:

- Comment bodies are multi-line prose with backticks and quotes. Interpolating one
  into `glab mr note create -m "..."` mangles it, and a backtick pair makes the shell
  execute what is between them.
- A GitLab inline discussion needs a **nested** `position` object.
  `glab api --field 'position[new_path]=x'` sends that literal string as a JSON key,
  which the API ignores, so the comment lands as a general note while reporting
  success. Only a raw JSON body nests correctly.

The script returns one JSON object. `placement` is `inline` or `general`, `reason`
explains any fallback, `url` is the posted comment where the host returns one.

### Placement

Inline first, anchored to the diff line. The script pre-checks whether the line is an added line in the pinned diff and falls back to a general comment if not. Three distinct cases trigger rejection: the path has no hunks in the pinned diff, the line is outside the diff hunks, or the line is unchanged context, not a line this change added. A comment on an unchanged context line is technically postable but belongs on a line the change actually made. The old range check used to accept context lines, which put comments on unrelated code in past runs. This guard requires an added line, which is stronger. But it does not catch every wrong anchor, because a wrong anchor that happens to be added still passes it. Stage 6 runs a text check to confirm the anchored line carries the mechanism the claim turns on.

A fallback is never a failure and never blocks the post. The comment's first line
already carries the `file:line` anchor, so a general comment still says where it
belongs. Report the fallback in the summary, do not re-prompt the user about it.

### Failures

A failed post does not abort the queue. Report it, move to the next comment, and list
it in the summary with the reason. One unreachable host or one rejected position is
not a reason to strand four approved comments.

### Attribution

Post the body and nothing else. No footer, no marker, no note that a review pipeline
produced it, no mention of the council or of any model. The comment is from the user.

## Dry runs

`--dry-run` makes zero network calls and prints the exact request it would send.
Verification runs must use it. Without it a sub-agent following this reference reaches
a real merge request, and a review comment is awkward to walk back once colleagues are
notified.

## The summary

After the queue, one compact block. This is the only record of what was posted, since
the report was already rendered and is deliberately not re-rendered.

```
Posted 2, skipped 1, stopped before 1.

  src/Search.kt:84    posted inline    <url>
  src/Widget.kt:262   posted general   <url>   line not in the diff
  src/Sync.kt:41      skipped
  src/Cache.kt:12     not offered, you stopped the queue

Next: open MR !1234 and check the two comments landed where you expect.
```

Anchors, outcomes and URLs. No finding IDs, no severity labels, no restating what the
comments said. Close on one concrete action as everywhere else.

**The summary is user-facing prose, so the Language rules in `output-contract.md` §2 bind
it too.** No em-dashes, no semicolons, no emoji or check marks, no hype. Plain words and a
period. Verification runs drifted into `(dry run — no url)` and trailing tick marks, which
is exactly the drift those rules exist to stop.

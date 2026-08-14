#!/usr/bin/env python3
"""Post one approved review comment to a GitLab MR or a GitHub PR.

Stage 10 of the code-review-full skill. The agent never builds these API calls by
hand. Two reasons, both of which produce silent breakage when ignored:

1. Comment bodies are multi-line prose containing backticks, quotes and newlines.
   Interpolating one into `glab mr note create -m "..."` mangles it or executes it.
2. A GitLab inline discussion needs a NESTED `position` object. `glab api --field
   'position[new_path]=x'` sends the literal JSON key `"position[new_path]"`, which
   the API ignores, so the comment silently lands as a general note instead of
   inline. Only a raw JSON body via `--input -` nests correctly.

Placement follows the skill's fallback rule. Try inline, and when the line is not
part of the diff, or the host rejects the position, post the identical text as a
general comment. A comment is never dropped for want of a position, because its
first line already carries the `file:line` anchor.

The inline pre-check (`line_in_diff`) only accepts lines the MR actually added
(leading `+`). A GitLab or GitHub inline comment on a context line is technically
postable, but anchoring a review finding to unchanged code is always wrong. Restricting
to added lines turns a plausible-but-wrong anchor into a clean general-comment
fallback instead of a confidently misplaced inline comment.

Usage
-----
Post one comment::

    post-comment.py --host gitlab --target 1234 \
        --file src/Search.kt --line 84 \
        --body-file body.md --diff "$RUN/diff.patch"

Rehearse without touching the network, which is what verification runs use::

    post-comment.py ... --dry-run

`--dry-run` makes ZERO network calls, including the diff_refs and head-sha lookups
that a real inline post needs. It substitutes placeholder SHAs so the rehearsal
reports the placement the real run would take. Without that substitution a dry run
both reaches the live MR and misreports inline posts as fallbacks. `--dry-run`
also short-circuits `--list-existing` to an empty result.

List anchors already present on the target, for duplicate detection before the
picker starts::

    post-comment.py --host gitlab --target 1234 --list-existing

Output
------
One JSON object on stdout, always, including on failure::

    {"ok": true, "placement": "inline", "url": "https://...",
     "reason": null, "dry_run": false}

    {"ok": false, "placement": null, "url": null,
     "reason": "glab exited 1: 404 Not Found", "dry_run": false}

`placement` is "inline" or "general". `reason` explains a fallback or a failure and
is null on a clean inline post. Exit code is 0 on success, 1 on failure, so the
caller can branch on either the code or the `ok` field.

For --list-existing::

    {"ok": true, "anchors": ["src/Search.kt:84", "src/Widget.kt:262"],
     "count": 7}

Constraints
-----------
Read-only toward everything except the one comment it is told to post. It never
closes, merges, approves or deletes. It posts exactly one comment per invocation,
so the per-comment approval in the picker maps one to one onto a network write.
"""

import argparse
import json
import os
import re
import subprocess
import sys


HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def fail(reason, placement=None, dry_run=False):
    """Emit the failure envelope and exit non-zero."""
    json.dump(
        {
            "ok": False,
            "placement": placement,
            "url": None,
            "reason": reason,
            "dry_run": dry_run,
        },
        sys.stdout,
    )
    sys.stdout.write("\n")
    sys.exit(1)


def succeed(placement, url, reason=None, dry_run=False):
    json.dump(
        {
            "ok": True,
            "placement": placement,
            "url": url,
            "reason": reason,
            "dry_run": dry_run,
        },
        sys.stdout,
    )
    sys.stdout.write("\n")
    sys.exit(0)


def run(cmd, stdin_text=None):
    """Run a command, returning (returncode, stdout, stderr) as text."""
    try:
        proc = subprocess.run(
            cmd,
            input=stdin_text,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except OSError as exc:
        return 127, "", str(exc)
    return proc.returncode, proc.stdout, proc.stderr


def _path_matches(new_path, target_file):
    """True when the b-side path from a diff header matches the target anchor.

    Diff headers carry an `a/` / `b/` prefix; finding anchors usually do not.
    Suffix matching handles both a bare filename and a partial path.
    """
    return (
        new_path == target_file
        or new_path.endswith("/" + target_file)
        or target_file.endswith("/" + new_path)
    )


def _read_diff_lines(diff_path):
    try:
        with open(diff_path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().splitlines(), None
    except IOError as exc:
        return None, "cannot read diff: %s" % exc


def diff_new_side_ranges(diff_path, target_file):
    """Return new-side line ranges for one path in a unified diff.

    A GitLab or GitHub inline comment can only anchor to a line the diff actually
    covers. Checking here turns a guaranteed API rejection into a clean fallback,
    and keeps a failed post from looking like a real error in the picker.

    Matching is suffix-based because a diff header carries an `a/` or `b/` prefix
    and a finding's anchor usually does not.
    """
    lines, err = _read_diff_lines(diff_path)
    if err is not None:
        return None, err

    ranges = []
    in_target = False
    for line in lines:
        if line.startswith("diff --git "):
            in_target = False
            parts = line.split(" b/", 1)
            if len(parts) == 2:
                in_target = _path_matches(parts[1].strip(), target_file)
            continue
        if not in_target:
            continue
        match = HUNK_RE.match(line)
        if match:
            start = int(match.group(1))
            count = 1 if match.group(2) is None else int(match.group(2))
            if count > 0:
                ranges.append((start, start + count - 1))
    return ranges, None


def diff_added_lines(diff_path, target_file):
    """Return the set of new-side line numbers for added (`+`) lines only.

    Context lines and removed lines are excluded. The caller uses this to
    distinguish "line is in a hunk but unchanged" from "line was actually added",
    so a review comment never lands inline on code the MR never touched.

    Parsing rules:
    - `@@ -a,b +c,d @@`: b and d are optional (default 1); c seeds new_lineno.
    - A leading space (context) advances new_lineno but does not add the line.
    - A leading `+` (added) advances new_lineno and records it.
    - A leading `-` (removed) does not advance new_lineno.
    - `\\ No newline at end of file` advances nothing.
    - `---` / `+++` header lines must not be counted as body lines.
    """
    lines, err = _read_diff_lines(diff_path)
    if err is not None:
        return None, err

    added = set()
    in_target = False
    in_hunk = False
    new_lineno = 0

    for line in lines:
        if line.startswith("diff --git "):
            in_target = False
            in_hunk = False
            parts = line.split(" b/", 1)
            if len(parts) == 2:
                in_target = _path_matches(parts[1].strip(), target_file)
            continue
        if not in_target:
            continue
        # `---` and `+++` are diff headers, not hunk body lines.
        if line.startswith("--- ") or line.startswith("+++ "):
            in_hunk = False
            continue
        match = HUNK_RE.match(line)
        if match:
            new_lineno = int(match.group(1))
            in_hunk = True
            continue
        if not in_hunk:
            continue
        # `\ No newline at end of file` is a diff annotation, not a source line.
        if line.startswith("\\ "):
            continue
        if line.startswith("+"):
            added.add(new_lineno)
            new_lineno += 1
        elif line.startswith("-"):
            pass  # removed line: new-side counter does not advance
        else:
            # context line (leading space, or empty line inside hunk body)
            new_lineno += 1

    return added, None


def line_in_diff(diff_path, target_file, line):
    """Return (True, None) only when `line` is an added line in the pinned diff.

    Three distinct rejection reasons, each human-readable for the picker:
    - the path has no hunks at all
    - the line is outside every hunk's new-side range
    - the line is inside a hunk but is a context or removed line

    The third case is the one the old range-only check missed.
    """
    ranges, err = diff_new_side_ranges(diff_path, target_file)
    if err is not None:
        return False, err
    if not ranges:
        return False, "%s has no hunks in the pinned diff" % target_file
    in_any_hunk = any(start <= line <= end for start, end in ranges)
    if not in_any_hunk:
        return False, "line %d of %s is outside the diff hunks" % (line, target_file)
    added, err = diff_added_lines(diff_path, target_file)
    if err is not None:
        return False, err
    if line not in added:
        return False, (
            "line %d of %s is unchanged context, not a line this change added"
            % (line, target_file)
        )
    return True, None


# --------------------------------------------------------------------------
# GitLab
# --------------------------------------------------------------------------


def gitlab_diff_refs(target):
    code, out, err = run(
        ["glab", "api", "projects/:id/merge_requests/%s" % target]
    )
    if code != 0:
        return None, "glab api exited %d: %s" % (code, (err or out).strip())
    try:
        payload = json.loads(out)
    except ValueError as exc:
        return None, "unparseable MR payload: %s" % exc
    refs = payload.get("diff_refs") or {}
    missing = [k for k in ("base_sha", "head_sha", "start_sha") if not refs.get(k)]
    if missing:
        return None, "MR payload missing diff_refs: %s" % ", ".join(missing)
    return refs, None


def gitlab_post_inline(target, path, line, body, refs, dry_run):
    payload = {
        "body": body,
        "position": {
            "position_type": "text",
            "base_sha": refs["base_sha"],
            "head_sha": refs["head_sha"],
            "start_sha": refs["start_sha"],
            "new_path": path,
            "new_line": line,
        },
    }
    cmd = [
        "glab",
        "api",
        "--method",
        "POST",
        "projects/:id/merge_requests/%s/discussions" % target,
        "--input",
        "-",
    ]
    if dry_run:
        return {"cmd": cmd, "payload": payload}, None
    code, out, err = run(cmd, stdin_text=json.dumps(payload))
    if code != 0:
        return None, "glab api exited %d: %s" % (code, (err or out).strip())
    try:
        note = json.loads(out)
    except ValueError:
        return {"url": None}, None
    return {"url": _gitlab_note_url(note)}, None


def _gitlab_note_url(discussion):
    notes = discussion.get("notes") or []
    if not notes:
        return None
    first = notes[0]
    # GitLab does not return a web URL on the note, so build one when it gave us
    # enough to do so. A missing URL is not an error, the post still succeeded.
    return first.get("web_url")


def gitlab_post_general(target, body, dry_run):
    cmd = ["glab", "mr", "note", "create", str(target), "--unique"]
    if dry_run:
        return {"cmd": cmd, "payload": {"body": body}}, None
    code, out, err = run(cmd, stdin_text=body)
    if code != 0:
        return None, "glab mr note exited %d: %s" % (code, (err or out).strip())
    url = None
    for token in out.split():
        if token.startswith("http"):
            url = token.strip()
            break
    return {"url": url}, None


def gitlab_list_existing(target):
    code, out, err = run(
        [
            "glab",
            "api",
            "--paginate",
            "projects/:id/merge_requests/%s/notes?per_page=100" % target,
        ]
    )
    if code != 0:
        return None, "glab api exited %d: %s" % (code, (err or out).strip())
    return _collect_anchors(out)


# --------------------------------------------------------------------------
# GitHub
# --------------------------------------------------------------------------


def github_head_sha(target):
    code, out, err = run(
        ["gh", "pr", "view", str(target), "--json", "headRefOid"]
    )
    if code != 0:
        return None, "gh pr view exited %d: %s" % (code, (err or out).strip())
    try:
        return json.loads(out).get("headRefOid"), None
    except ValueError as exc:
        return None, "unparseable PR payload: %s" % exc


def github_post_inline(target, path, line, body, head_sha, dry_run):
    payload = {
        "body": body,
        "commit_id": head_sha,
        "path": path,
        "line": line,
        "side": "RIGHT",
    }
    cmd = [
        "gh",
        "api",
        "--method",
        "POST",
        "repos/{owner}/{repo}/pulls/%s/comments" % target,
        "--input",
        "-",
    ]
    if dry_run:
        return {"cmd": cmd, "payload": payload}, None
    code, out, err = run(cmd, stdin_text=json.dumps(payload))
    if code != 0:
        return None, "gh api exited %d: %s" % (code, (err or out).strip())
    try:
        return {"url": json.loads(out).get("html_url")}, None
    except ValueError:
        return {"url": None}, None


def github_post_general(target, body, dry_run):
    cmd = ["gh", "pr", "comment", str(target), "--body-file", "-"]
    if dry_run:
        return {"cmd": cmd, "payload": {"body": body}}, None
    code, out, err = run(cmd, stdin_text=body)
    if code != 0:
        return None, "gh pr comment exited %d: %s" % (code, (err or out).strip())
    url = None
    for token in out.split():
        if token.startswith("http"):
            url = token.strip()
            break
    return {"url": url}, None


def github_list_existing(target):
    anchors = []
    total = 0
    for endpoint in (
        "repos/{owner}/{repo}/issues/%s/comments?per_page=100" % target,
        "repos/{owner}/{repo}/pulls/%s/comments?per_page=100" % target,
    ):
        code, out, err = run(["gh", "api", "--paginate", endpoint])
        if code != 0:
            return None, "gh api exited %d: %s" % (code, (err or out).strip())
        found, sub_err = _collect_anchors(out)
        if sub_err is not None:
            return None, sub_err
        anchors.extend(found["anchors"])
        total += found["count"]
    return {"anchors": sorted(set(anchors)), "count": total}, None


# --------------------------------------------------------------------------
# Shared
# --------------------------------------------------------------------------


ANCHOR_RE = re.compile(r"`?([\w./+-]+\.[A-Za-z0-9]{1,8}):(\d+)")


def _collect_anchors(raw):
    """Pull `path:line` anchors out of a JSON array of comment payloads.

    Every comment this skill posts opens with its anchor, so an anchor already
    present on the target means that finding was raised before. Cheap, and it
    stops a second run quietly duplicating the whole set.
    """
    try:
        items = json.loads(raw)
    except ValueError as exc:
        return None, "unparseable comment list: %s" % exc
    if not isinstance(items, list):
        return None, "expected a list of comments"
    anchors = []
    for item in items:
        body = (item or {}).get("body") or ""
        for match in ANCHOR_RE.finditer(body):
            anchors.append("%s:%s" % (match.group(1), match.group(2)))
    return {"anchors": sorted(set(anchors)), "count": len(items)}, None


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Post one approved review comment to a GitLab MR or GitHub PR."
    )
    parser.add_argument("--host", required=True, choices=["gitlab", "github"])
    parser.add_argument(
        "--target", required=True, help="MR iid or PR number"
    )
    parser.add_argument("--file", help="path the comment anchors to")
    parser.add_argument("--line", type=int, help="new-side line number")
    parser.add_argument("--body-file", help="file holding the comment body")
    parser.add_argument("--diff", help="the pinned diff, for the inline pre-check")
    parser.add_argument(
        "--general",
        action="store_true",
        help="skip the inline attempt and post a general comment",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="rehearse without any network call",
    )
    parser.add_argument(
        "--list-existing",
        action="store_true",
        help="list anchors already present on the target, then exit",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)

    if args.list_existing:
        if args.dry_run:
            json.dump({"ok": True, "anchors": [], "count": 0, "dry_run": True},
                      sys.stdout)
            sys.stdout.write("\n")
            return 0
        lister = gitlab_list_existing if args.host == "gitlab" else github_list_existing
        result, err = lister(args.target)
        if err is not None:
            fail(err)
        json.dump({"ok": True, "anchors": result["anchors"], "count": result["count"]},
                  sys.stdout)
        sys.stdout.write("\n")
        return 0

    if not args.body_file:
        fail("--body-file is required unless --list-existing is given",
             dry_run=args.dry_run)
    if not os.path.isfile(args.body_file):
        fail("body file not found: %s" % args.body_file, dry_run=args.dry_run)
    with open(args.body_file, "r", encoding="utf-8") as handle:
        body = handle.read().strip()
    if not body:
        fail("body file is empty: %s" % args.body_file, dry_run=args.dry_run)

    # Decide placement before doing anything, so a rejection the pre-check can
    # foresee becomes a stated fallback rather than a surprise error.
    reason = None
    want_inline = not args.general and bool(args.file) and bool(args.line)
    if want_inline and args.diff:
        ok, why = line_in_diff(args.diff, args.file, args.line)
        if not ok:
            want_inline = False
            reason = why
    elif want_inline and not args.diff:
        reason = "no --diff given, inline attempted without a pre-check"

    if args.host == "gitlab":
        placement, result, reason = _post_gitlab(args, body, want_inline, reason)
    else:
        placement, result, reason = _post_github(args, body, want_inline, reason)
    _emit(result, placement, reason, args.dry_run)


def _post_gitlab(args, body, want_inline, reason):
    """Post to a GitLab MR, inline where possible, general otherwise.

    Returns (placement, result, reason). Control flow stays in this function and
    returns a value rather than exiting from a nested helper, so a caller that
    traps SystemExit cannot fall through into the GitHub path and double-post.
    """
    if want_inline:
        # A dry run must not touch the network at all, or it is not a rehearsal.
        # Fetching diff_refs here would both reach the real MR and make the
        # rehearsal report a fallback the real run would not take.
        if args.dry_run:
            refs, err = {k: "<%s>" % k for k in
                         ("base_sha", "head_sha", "start_sha")}, None
        else:
            refs, err = gitlab_diff_refs(args.target)
        if err is not None:
            reason = "falling back to a general comment: %s" % err
        else:
            result, err = gitlab_post_inline(
                args.target, args.file, args.line, body, refs, args.dry_run
            )
            if err is None:
                return "inline", result, reason
            reason = "host rejected the inline position: %s" % err
    result, err = gitlab_post_general(args.target, body, args.dry_run)
    if err is not None:
        fail(err, placement="general", dry_run=args.dry_run)
    return "general", result, reason


def _post_github(args, body, want_inline, reason):
    """Post to a GitHub PR, inline where possible, general otherwise."""
    if want_inline:
        if args.dry_run:
            head_sha, err = "<head_sha>", None
        else:
            head_sha, err = github_head_sha(args.target)
        if err is not None:
            reason = "falling back to a general comment: %s" % err
        else:
            result, err = github_post_inline(
                args.target, args.file, args.line, body, head_sha, args.dry_run
            )
            if err is None:
                return "inline", result, reason
            reason = "host rejected the inline position: %s" % err
    result, err = github_post_general(args.target, body, args.dry_run)
    if err is not None:
        fail(err, placement="general", dry_run=args.dry_run)
    return "general", result, reason


def _emit(result, placement, reason, dry_run):
    if dry_run:
        json.dump(
            {
                "ok": True,
                "placement": placement,
                "url": None,
                "reason": reason,
                "dry_run": True,
                "would_run": result.get("cmd"),
                "would_send": result.get("payload"),
            },
            sys.stdout,
        )
        sys.stdout.write("\n")
        sys.exit(0)
    succeed(placement, result.get("url"), reason, False)


if __name__ == "__main__":
    sys.exit(main())

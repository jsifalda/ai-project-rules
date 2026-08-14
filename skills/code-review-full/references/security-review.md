# Stage 4c: Security Review, inline fallback

Use this ONLY when the host provides no `security-review` skill. When it does, delegate to it
and ignore this file.

This lens hunts exploitable defects in the pinned diff. It asks whether the change gives an
attacker something the code did not give before. It does NOT hunt correctness bugs, that is
Stage 2's job, nor architecture, that is Stage 3's, nor spec gaps, that is Stage 4b's. A duplicate
raised here is noise that Stage 5 will merge away.

## Scope

| In scope | Out of scope |
|---|---|
| Injection: SQL, command, template, path traversal | Correctness bugs |
| Authentication and authorization gaps | Architecture and abstraction quality |
| Secret and credential handling | Spec and ticket gaps |
| Unsafe deserialization | Style nits and lint violations |
| Server-side request forgery | Performance |
| Cryptography misuse | Theoretical vulnerabilities with no reachable path here |
| Unsafe defaults | Generic hardening advice with no defect behind it |
| Missing input validation on a trust boundary | Findings about code outside the pinned diff |
| Dependency and supply-chain risk this diff adds | Compliance paperwork and policy sign-off |

## The guiding principle, reachability

A finding must name a path from attacker-controlled input to the dangerous sink. Name where the
value enters the process, and name the operation it reaches. A construct that only looks unsafe,
with no reachable input path, is not a finding.

If the honest answer is "no security defects", say that and return no findings. A security review
with nothing to say is a valid result. Manufacturing a finding to look thorough is the exact noise
this pipeline exists to remove.

Invention is the worst failure this lens can commit. A false security finding is the one that gets
acted on fastest, because the category name alone creates urgency. It sends the author to change
working code under pressure, and it spends the trust the other lenses earn.

## How to run it

1. **Read the pinned diff first, then the surrounding files.** Start at `$RUN/diff.patch`. Read
   branch state with `git show <ref>:<path>` only, never `checkout` and never `stash`. Read the
   whole file when the trust boundary is not visible inside the hunk. The guard that makes a
   line safe often sits far above it.
2. **Trace the input.** For every candidate, follow the value back to where it enters the
   process, a request parameter, an environment variable, a file, a message or a command
   argument, and forward to the sink. Report only when both ends are established.
3. **Take every anchor from `$RUN/anchors.json`.** The only legal anchors are the added lines
   listed there. Find the anchor by grepping that file for the construct being described and
   taking its `line` value. Never count lines by eye in a file read. A context line, a removed
   line, or any line outside the hunks is not a legal anchor. **A guard this change DELETED is
   your highest-value finding, and a removed line cannot carry it.** Anchor to the added line
   that now runs unguarded, and name the deleted guard in the body. Move the anchor. Never drop
   the finding. When the diff adds no line the deletion reaches, mark the finding not postable
   and say so in it. Stage 6 of `SKILL.md` holds that rule.
4. **Say whether the defect is pre-existing or new.** Read the history of the region with
   `git log` and `git show`. A pre-existing issue that this change only moves is still
   reportable, and it ranks below a defect this change introduces.
5. **Confirm a literal secret at the byte level before you report it.** Read the "Tooling can lie
   about file contents" block in Stage 6 of `SKILL.md` and follow it. Do not report a hardcoded
   secret, placeholder or mask until that check passes.

## What to look for

- **Concatenated query or command.** A string built with `+` or interpolation, then given to a
  database driver, a shell or a process spawn. The tell is a parameter name inside the literal.
- **Path built from input.** A path joined from a caller-supplied value with no normalization,
  so `../` walks out of the intended directory.
- **Template rendered from input.** Untrusted text given to a template engine or an
  `eval`-shaped API, which executes the text instead of printing it.
- **A route that lost its guard.** A new endpoint, handler or method with no authentication
  check where its neighbours in the same file all have one.
- **Authorization checked on the wrong subject.** The code confirms the caller is signed in, but
  never confirms the record belongs to that caller. The tell is an identifier taken from the
  request and used to read or write a row.
- **A credential in the source.** A key, token, password or connection string as a literal, or a
  secret written to a log, an error message or a URL query string.
- **Deserialization of untrusted bytes.** A native object deserializer, or a loader that builds
  arbitrary types from the payload.
- **A request URL taken from input.** An outbound call whose host comes from the caller, which
  reaches internal addresses and cloud metadata endpoints.
- **Cryptography misuse.** A home-made scheme, a fixed or reused initialization vector, a fast
  hash for passwords, a secret comparison that stops at the first different byte, or a disabled
  certificate check.
- **An unsafe default.** A permissive cross-origin rule, debug mode left on, a wildcard
  permission, a cookie without `HttpOnly` or `Secure`, or a check that fails open.
- **Validation missing at the boundary.** Size, type, range and format unchecked on data that
  crosses into the process from outside.
- **A dependency this change adds.** A new package, a version moved backwards, or a script
  pulled from a URL at build time.

## Output

Report every claim as `file:line`, plus the defect, the reachable path from input to sink, the
concrete consequence if it is exploited, and the direction of the fix. A claim you cannot anchor
to a line must not be reported, the pipeline's verification gate will drop it. Move the anchor
first, per step 3 above. Drop a finding only when the defect itself is not real.

Rank by exploitability and blast radius, not by how alarming the category name sounds.

This lens gets no special treatment at the cap of 5 findings. A security finding competes on the
same bar and goes through the same council ranking as a finding from any other lens.

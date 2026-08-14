# Stage 3: Structural Review, inline fallback

Use this ONLY when the `code-review-nuclear` skill is absent. When it is installed, delegate to
it and ignore this file.

This is the architectural conscience of the pipeline. It asks whether the change makes the
codebase better or worse. It does NOT hunt correctness bugs, that is Stage 2's job, and a
correctness bug raised here is noise that Stage 5 will merge away as a duplicate.

## Scope

| In scope | Out of scope |
|---|---|
| Structural quality and architectural health | Correctness bugs |
| Abstraction quality and decomposition | Style nits and formatting |
| Complexity growth, spaghetti detection | Test coverage gaps |
| Layer violations and architectural drift | Security vulnerabilities |
| File size and modularity | Performance micro-optimizations |
| Type boundary and contract cleanliness | Lint violations |

## The guiding principle, code judo

Actively search for restructurings that preserve behaviour while making the implementation
dramatically simpler, smaller and more direct. Do not stop at "this could be a bit cleaner".
Look for moves where whole branches, helpers, modes, conditionals or layers disappear
entirely. Prefer the solution that feels inevitable in hindsight.

If the honest answer is "this is well structured", say that and return no findings. A
structural review with nothing to say is a valid result. Manufacturing a finding to look
thorough is the exact noise this pipeline exists to remove.

## How to run it

1. **Read whole files, not hunks.** For every file with more than 10 changed lines, read the
   entire file from `git show <ref>:<path>`. Structural judgement depends on surrounding
   patterns, the file's size before the change, and consistency with existing conventions.
   Read whole files to understand the change, but never take an anchor from that read. An
   anchor comes from `$RUN/anchors.json`, found by grepping it for the construct being
   described rather than by counting lines. Looking up anchors this way is cheaper than
   counting inside a 300-line blob, and it cannot drift.
2. **Record pre-change size.** For files already over 800 lines, note the count before the
   change. A file crossing 1000 lines is a finding on its own.
3. **Compare against the repo's own conventions**, not a general ideal. A pattern that is
   consistent with the surrounding codebase is not a finding, even when you would have written
   it differently. Deviation from the local convention IS a finding.

## What to look for

- **Duplication with intent.** The same logic in two places that must now change together. Name
  both sites.
- **Abstractions earning nothing.** A wrapper, helper or layer that only forwards. Deleting it
  should be the proposal.
- **Speculative generality.** Configuration, parameters, or branches for a need nobody has
  stated. One caller passing one value means the parameter is not needed.
- **Layer violations.** A module reaching across a boundary it should not know about, or shared
  mutable state used as a back channel.
- **Complexity growth.** Nesting depth, branch count and file length rising without a matching
  rise in what the code does.
- **Contract leakage.** Internal types escaping through a public surface, or a function whose
  signature no longer describes what it does.
- **Single-purpose erosion.** A file or function that has quietly become two things.

## Output

Report every claim as `file:line`, plus what is structurally wrong, the concrete restructuring
proposed, and what disappears if it is applied. A claim you cannot anchor to a line must not be
reported, the pipeline's verification gate will drop it.

Rank by how much complexity the proposed move removes, not by how much text the finding takes
to explain.

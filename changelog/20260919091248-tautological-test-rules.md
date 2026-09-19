# Ban tautological tests, require public-interface testing

- Added two bullets to `## Testing` in `rules/general.md`: never write a test that
  restates the implementation or would pass with a wrong implementation, and assert
  on what a module promises its callers rather than on its internals.
- `### TDD` already listed Kent Beck's `Behavioral` and `Structure-insensitive`
  desiderata, but a label is not an instruction. These bullets sit at the top level
  so they bind every test, not only a TDD cycle.
- The wording took two review rounds. The first draft let an agent delete a failing
  test by calling it tautological. The second overcorrected into an unconditional
  delete ban that contradicted `Remove only one no longer needed.` on the line above.
  The shipped text scopes the delete ban to the tautology reason alone.

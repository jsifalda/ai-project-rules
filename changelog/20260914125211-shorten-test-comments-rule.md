# Shorten the test-comments rule and make it language-agnostic

- Cut `### Comments in tests` in `rules/general.md` to about two thirds of its length. Every ban survives.
- Replaced the JavaScript vocabulary (`//`, JSDoc, `describe`/`it`, `@vitest-environment`, `eslint-disable`) with neutral terms: doc comment, docstring, compiler or linter directive.
- Dropped the "decision record" clause, `# DOCUMENTATION` already states it.
- Why: the rule file loads on every session in every language, and the JS-only examples made it read as a JS rule.

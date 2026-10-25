#!/bin/sh
# Regression tests. Run from the skill root: sh tests/run_tests.sh
# Fixtures are built in a temp dir, because a committed SKILL.md with a bare $<digit> would fail the pre-commit validator.
set -u
V=scripts/quick_validate.py; ok=0
D=$(mktemp -d) || exit 1
trap 'rm -rf "$D"' EXIT

fixture() { # dir name, body line
  mkdir -p "$D/$1"
  printf -- '---\nname: %s\ndescription: test skill\nmetadata:\n  version: "1.0"\n---\n\n%s\n' "$1" "$2" > "$D/$1/SKILL.md"
}
pass() { python3 $V --require-version "$D/$1" >/dev/null || { echo "FAIL $1 should pass"; ok=1; }; }
fail() { python3 $V --require-version "$D/$1" >/dev/null && { echo "FAIL $1 should fail"; ok=1; }; }

fixture bare-one 'printf "%s" "$1"';        fail bare-one
fixture bare-ten 'echo $10';                fail bare-ten
fixture double-escape 'echo \\$1';          fail double-escape
fixture braced 'printf "%s" "${1}"';        pass braced
fixture word-after 'echo $1abc';            pass word-after
fixture escaped 'costs \$1.00';             pass escaped
mkdir -p "$D/front-only"
printf -- '---\nname: front-only\ndescription: costs $1\nmetadata:\n  version: "1.0"\n---\n\nbody\n' > "$D/front-only/SKILL.md"
pass front-only

python3 $V "$D/bare-one" | grep -q "line 8: bare positional parameter '\$1'" || { echo "FAIL bare-one message names line 8"; ok=1; }

[ $ok -eq 0 ] && echo "ALL TESTS PASS"
exit $ok

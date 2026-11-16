#!/bin/sh
# Regression tests. Run from the skill root: sh tests/run_tests.sh
set -u
F=tests/fixtures; S=scripts; ok=0
python3 $S/validate_answer.py --answer $F/valid_answer.md >/dev/null || { echo "FAIL valid_answer should pass"; ok=1; }
python3 $S/validate_answer.py --answer $F/invalid_answer.md >/dev/null && { echo "FAIL invalid_answer should fail"; ok=1; }
n=$(python3 $S/validate_answer.py --answer $F/empty_fields.md | grep -c "empty")
[ "$n" -eq 2 ] || { echo "FAIL empty_fields should report 2 empty fields, got $n"; ok=1; }
[ $ok -eq 0 ] && echo "ALL TESTS PASS"
exit $ok

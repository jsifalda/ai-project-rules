#!/bin/sh
# Regression tests. Run from the skill root: sh tests/run_tests.sh
set -u
F=tests/fixtures; S=scripts; T=2026-09-28; ok=0
python3 $S/validate_report.py --report $F/valid_report.md --today $T >/dev/null || { echo "FAIL valid_report should pass"; ok=1; }
python3 $S/verify_citations.py --report $F/valid_report.md --seen $F/seen_urls.txt >/dev/null || { echo "FAIL valid citations should pass"; ok=1; }
python3 $S/validate_report.py --report $F/real_run_starlink.md --today $T >/dev/null || { echo "FAIL real run should pass"; ok=1; }
python3 $S/verify_citations.py --report $F/real_run_starlink.md --seen $F/real_run_seen_urls.txt >/dev/null || { echo "FAIL real run citations should pass"; ok=1; }
python3 $S/validate_report.py --report $F/invalid_report.md --today $T >/dev/null && { echo "FAIL invalid_report should fail"; ok=1; }
python3 $S/verify_citations.py --report $F/invalid_report.md --seen $F/seen_urls.txt >/dev/null && { echo "FAIL invalid citations should fail"; ok=1; }
[ $ok -eq 0 ] && echo "ALL TESTS PASS"
exit $ok

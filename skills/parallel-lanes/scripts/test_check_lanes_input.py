import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import check_lanes  # noqa: E402
from test_check_lanes import base_plan, codes_for, mutated, set_unit, unit_of  # noqa: E402

SCRIPT = os.path.join(SCRIPT_DIR, "check_lanes.py")


class ParsePlanTest(unittest.TestCase):
    def test_missing_top_level_key_is_rejected(self):
        plan = base_plan()
        del plan["batches"]
        with self.assertRaises(check_lanes.PlanError):
            check_lanes.parse_plan(plan)

    def test_wrong_type_is_rejected(self):
        plan = base_plan()
        plan["units"][0]["files"] = "src/"
        with self.assertRaises(check_lanes.PlanError):
            check_lanes.parse_plan(plan)

    def test_non_positive_max_agents_is_rejected(self):
        with self.assertRaises(check_lanes.PlanError):
            check_lanes.parse_plan(dict(base_plan(), max_agents=0))

    def test_boolean_max_agents_is_rejected(self):
        with self.assertRaises(check_lanes.PlanError):
            check_lanes.parse_plan(dict(base_plan(), max_agents=True))

    def test_non_object_resource_caps_is_rejected(self):
        for bad in ([], [1], 3, True, "x"):
            plan = base_plan()
            plan["resource_caps"] = bad
            with self.assertRaises(check_lanes.PlanError, msg=repr(bad)):
                check_lanes.parse_plan(plan)

    def test_boolean_resource_cap_value_is_rejected(self):
        plan = base_plan()
        plan["resource_caps"] = {"ios-simulator": True}
        with self.assertRaises(check_lanes.PlanError):
            check_lanes.parse_plan(plan)

    def test_null_resource_caps_means_no_caps(self):
        plan = base_plan()
        plan["resource_caps"] = None
        self.assertEqual(codes_for(plan), [])

    def test_scenario_without_id_is_rejected(self):
        plan = base_plan()
        plan["scenarios"].append({"title": "no id"})
        with self.assertRaises(check_lanes.PlanError):
            check_lanes.parse_plan(plan)

    def test_unit_that_is_not_an_object_is_rejected(self):
        plan = base_plan()
        plan["units"].append("api-extra")
        with self.assertRaises(check_lanes.PlanError):
            check_lanes.parse_plan(plan)

    def test_path_escaping_the_repo_root_is_rejected(self):
        for bad in ("../x.py", "..", "src/../../x.py", "./../lib/"):
            with self.assertRaises(check_lanes.PlanError, msg=bad):
                check_lanes.parse_plan(mutated(set_unit("api-list", files=[bad])))

    def test_absolute_path_is_rejected(self):
        for bad in ("/abs/src/a.py", "//abs/src/a.py", "/"):
            with self.assertRaises(check_lanes.PlanError, msg=bad):
                check_lanes.parse_plan(mutated(set_unit("api-list", files=[bad])))

    def test_dot_dot_inside_the_repo_is_accepted(self):
        for path in ("src/../src/list.py", "..list.py"):
            self.assertEqual(codes_for(mutated(set_unit("api-list", files=[path]))), [], path)


class CliTest(unittest.TestCase):
    def run_cli(self, content):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "plan.json")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(content)
            return subprocess.run([sys.executable, SCRIPT, path],
                                  capture_output=True, text=True)

    def test_clean_plan_exits_zero_with_summary(self):
        result = self.run_cli(json.dumps(base_plan()))
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stdout.startswith("OK: 6 units"))

    def test_violating_plan_exits_one_with_fail_line(self):
        plan = mutated(lambda p: unit_of(p, "api-list").update(scenarios=[]))
        result = self.run_cli(json.dumps(plan))
        self.assertEqual(result.returncode, 1)
        self.assertIn("VIOLATION empty-lane:", result.stdout)
        self.assertIn("FAIL: 2 violations", result.stdout)

    def test_malformed_input_exits_two(self):
        self.assertEqual(self.run_cli("{not json").returncode, 2)
        self.assertEqual(self.run_cli("{}").returncode, 2)

    def test_path_escaping_the_repo_root_exits_two(self):
        result = self.run_cli(json.dumps(mutated(set_unit("api-list", files=["../x.py"]))))
        self.assertEqual(result.returncode, 2)
        self.assertIn("escapes the repo root", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_absolute_path_exits_two(self):
        result = self.run_cli(json.dumps(mutated(set_unit("api-list", files=["/abs/src/a.py"]))))
        self.assertEqual(result.returncode, 2)
        self.assertIn("is absolute", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_non_utf8_file_exits_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "plan.json")
            with open(path, "wb") as handle:
                handle.write(b"\xff\xfe\x00\x80")
            result = subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_deeply_nested_json_exits_two(self):
        result = self.run_cli("[" * 100000)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_list_resource_caps_exits_two(self):
        plan = base_plan()
        plan["resource_caps"] = []
        self.assertEqual(self.run_cli(json.dumps(plan)).returncode, 2)

    def test_missing_file_exits_two(self):
        result = subprocess.run([sys.executable, SCRIPT, "/nonexistent/plan.json"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()

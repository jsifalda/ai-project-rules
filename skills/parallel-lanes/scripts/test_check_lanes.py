import copy
import os
import sys
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import check_lanes  # noqa: E402


def unit(uid, repo, kind, files, scenarios=(), blocked_by=(), resources=(),
         gate_resources=()):
    return {"id": uid, "repo": repo, "kind": kind, "files": list(files),
            "scenarios": list(scenarios), "blocked_by": list(blocked_by),
            "resources": list(resources), "gate_resources": list(gate_resources)}


def base_plan():
    return {
        "scenarios": [{"id": f"S{n}", "title": f"scenario {n}"} for n in range(1, 5)],
        "units": [
            unit("api-F", "api", "foundation", ["src/models/thing.py", "src/routes/"]),
            unit("api-create", "api", "lane", ["src/create.py"], ["S1"], ["api-F"]),
            unit("api-list", "api", "lane", ["src/list.py"], ["S2"], ["api-F"]),
            unit("web-F", "web", "foundation", ["app/shared/"]),
            unit("web-form", "web", "lane", ["app/form.tsx"], ["S3"], ["web-F"]),
            unit("web-map", "web", "lane", ["app/map.tsx"], ["S4"], ["web-F"],
                 ["ios-simulator"]),
        ],
        "resource_caps": {"ios-simulator": 1},
        "max_agents": None,
        "batches": [["api-F", "web-F"],
                    ["api-create", "api-list", "web-form", "web-map"]],
    }


def codes_for(plan):
    parsed = check_lanes.parse_plan(plan)
    return [code for code, _ in check_lanes.check_plan(parsed)]


def mutated(change):
    plan = copy.deepcopy(base_plan())
    change(plan)
    return plan


def unit_of(plan, uid):
    return next(u for u in plan["units"] if u["id"] == uid)


def codes_after(change):
    return codes_for(mutated(change))


def set_unit(uid, **fields):
    return lambda p: unit_of(p, uid).update(fields)


class CheckPlanTest(unittest.TestCase):
    SINGLE_VIOLATIONS = {
        "duplicate_unit_id_is_reported": ("duplicate-unit", lambda p: p["units"].append(copy.deepcopy(p["units"][1]))),
        "duplicate_scenario_id_is_reported": ("duplicate-scenario", lambda p: p["scenarios"].append({"id": "S1", "title": "again"})),
        "bad_kind_is_reported": ("bad-kind", lambda p: unit_of(p, "api-list").update(kind="worker")),
        "unknown_scenario_is_reported": ("unknown-scenario", lambda p: unit_of(p, "api-list")["scenarios"].append("S9")),
        "unknown_blocker_is_reported": ("unknown-unit", lambda p: unit_of(p, "api-list")["blocked_by"].append("ghost")),
        "unknown_unit_in_batch_is_reported": ("unknown-unit", lambda p: p["batches"][1].append("ghost")),
        "unit_in_no_batch_is_reported": ("unbatched", lambda p: p["batches"][1].remove("web-map")),
        "unit_in_two_batches_is_reported": ("multi-batched", lambda p: p["batches"].append(["web-map"])),
        "lanes_in_same_repo_with_equal_paths_overlap": ("lane-overlap", lambda p: unit_of(p, "api-list")["files"].append("src/create.py")),
        "directory_prefix_overlap_is_detected": ("lane-overlap", lambda p: unit_of(p, "api-list").update(files=["src/"])),
        "leading_dot_slash_is_ignored_for_overlap": ("lane-overlap", lambda p: unit_of(p, "api-list").update(files=["./src/create.py"])),
        "lane_without_scenarios_is_reported": ("empty-lane", lambda p: unit_of(p, "api-list").update(scenarios=[])),
        "scenario_listed_by_no_unit_is_reported": ("uncovered-scenario", lambda p: p["scenarios"].append({"id": "S5", "title": "orphan"})),
        "resource_use_above_cap_in_one_batch_is_reported": ("resource-cap", lambda p: unit_of(p, "web-form")["resources"].append("ios-simulator")),
        "batch_wider_than_max_agents_is_reported": ("max-agents", lambda p: p.update(max_agents=3)),
        "unknown_resource": ("unknown-resource", lambda p: unit_of(p, "web-form")["resources"].append("gpu")),
        "resource_cap_of_zero": ("resource-cap", lambda p: p["resource_caps"].update({"ios-simulator": 0})),
        "two_foundations_in_one_repo": ("multiple-foundations", set_unit("web-F", repo="api")),
        "self_loop": ("cycle", set_unit("api-list", blocked_by=["api-list"])),
        "earlier_lane_owning_directory": ("lane-overlap", set_unit("api-create", files=["src/"])),
    }

    def test_each_mutation_reports_its_violation(self):
        for name, (code, change) in self.SINGLE_VIOLATIONS.items():
            with self.subTest(name):
                self.assertIn(code, codes_for(mutated(change)))

    def test_valid_plan_has_no_violations(self):
        self.assertEqual(codes_for(base_plan()), [])

    def test_summary_reports_counts(self):
        line = check_lanes.summary(check_lanes.parse_plan(base_plan()))
        self.assertEqual(line, "OK: 6 units (2 foundation, 4 lanes), 2 batches, "
                               "widest batch 4, scenarios 4/4 covered")

    def test_similar_name_without_trailing_slash_does_not_overlap(self):
        plan = mutated(lambda p: unit_of(p, "api-list").update(files=["src/create.pyc"]))
        self.assertEqual(codes_for(plan), [])

    def test_lanes_in_different_repos_with_identical_paths_pass(self):
        def change(p):
            unit_of(p, "web-form")["files"] = ["src/create.py"]
        self.assertEqual(codes_for(mutated(change)), [])

    def test_lane_overlapping_foundation_without_dependency_is_reported(self):
        def change(p):
            lane = unit_of(p, "api-list")
            lane["files"] = ["src/routes/list.py"]
            lane["blocked_by"] = []
        self.assertEqual(sorted(codes_for(mutated(change))),
                         ["foundation-overlap", "missing-foundation-edge"])

    def test_lane_without_path_to_its_foundation_is_reported_with_ids(self):
        parsed = check_lanes.parse_plan(mutated(set_unit("api-list", blocked_by=[])))
        found = check_lanes.check_plan(parsed)
        self.assertEqual([code for code, _ in found], ["missing-foundation-edge"])
        self.assertIn("api-list", found[0][1])
        self.assertIn("api-F", found[0][1])

    def test_lane_reaching_its_foundation_through_another_lane_passes(self):
        def change(p):
            unit_of(p, "api-create")["blocked_by"] = ["api-list"]
            p["batches"] = [["api-F", "web-F"], ["api-list", "web-form", "web-map"],
                            ["api-create"]]
        self.assertEqual(codes_after(change), [])

    def test_lane_overlapping_its_foundation_via_blocked_by_passes(self):
        plan = mutated(lambda p: unit_of(p, "api-list").update(files=["src/routes/list.py"]))
        self.assertEqual(codes_for(plan), [])

    def test_transitive_dependency_on_foundation_passes(self):
        def change(p):
            unit_of(p, "api-create")["files"] = ["src/routes/create.py"]
            unit_of(p, "api-create")["blocked_by"] = ["api-list"]
            unit_of(p, "api-list")["files"] = ["src/list.py"]
            p["batches"] = [["api-F", "web-F"], ["api-list", "web-form", "web-map"],
                            ["api-create"]]
        self.assertEqual(codes_for(mutated(change)), [])

    def test_blocked_by_cycle_is_reported_with_ids(self):
        def change(p):
            unit_of(p, "api-F")["blocked_by"] = ["api-create"]
        parsed = check_lanes.parse_plan(mutated(change))
        messages = [m for c, m in check_lanes.check_plan(parsed) if c == "cycle"]
        self.assertEqual(len(messages), 1)
        self.assertIn("api-F", messages[0])
        self.assertIn("api-create", messages[0])

    def test_blocker_in_same_batch_is_reported(self):
        plan = mutated(lambda p: p.update(batches=[["api-F", "web-F", "api-create"],
                                                   ["api-list", "web-form", "web-map"]]))
        self.assertIn("batch-order", codes_for(plan))

    def test_blocker_in_later_batch_is_reported(self):
        plan = mutated(lambda p: p.update(batches=[["api-create", "web-F"],
                                                   ["api-F", "api-list", "web-form", "web-map"]]))
        self.assertIn("batch-order", codes_for(plan))

    def test_resource_use_split_across_batches_passes(self):
        def change(p):
            unit_of(p, "web-form")["resources"].append("ios-simulator")
            p["batches"] = [["api-F", "web-F"], ["api-create", "api-list", "web-form"],
                            ["web-map"]]
        self.assertEqual(codes_for(mutated(change)), [])

    def test_batch_within_max_agents_passes(self):
        plan = mutated(lambda p: p.update(max_agents=4))
        self.assertEqual(codes_for(plan), [])

    def test_every_violation_is_reported_not_only_the_first(self):
        def change(p):
            unit_of(p, "api-list")["scenarios"] = []
            p["batches"][1].remove("web-map")
        found = codes_for(mutated(change))
        self.assertIn("empty-lane", found)
        self.assertIn("unbatched", found)

    def test_missing_optional_keys_mean_no_caps(self):
        plan = copy.deepcopy(base_plan())
        del plan["resource_caps"]
        del plan["max_agents"]
        self.assertEqual(codes_for(plan), [])

    def test_gate_resources_do_not_count_against_caps(self):
        for name in ("ios-simulator", "gpu"):
            self.assertEqual(codes_after(set_unit("web-form", gate_resources=[name])), [])

    def test_gate_resources_must_be_a_list_of_strings(self):
        for bad in ("gpu", [1], None):
            plan = mutated(set_unit("web-form", gate_resources=bad))
            with self.assertRaises(check_lanes.PlanError, msg=repr(bad)):
                check_lanes.parse_plan(plan)

    def test_lane_overlapping_foundation_in_another_repo_passes(self):
        self.assertEqual(codes_after(set_unit("web-form", files=["src/routes/x.py"])), [])

    def test_repo_with_only_lanes_and_no_foundation_passes(self):
        def change(p):
            p["units"].remove(unit_of(p, "web-F"))
            unit_of(p, "web-form")["blocked_by"] = []
            unit_of(p, "web-map")["blocked_by"] = []
            p["batches"] = [["api-F", "web-form", "web-map"], ["api-create", "api-list"]]
        self.assertEqual(codes_after(change), [])

    def test_repo_root_path_overlaps_every_path_in_the_repo(self):
        for root in ("./", ".", "", "././"):
            self.assertIn("lane-overlap", codes_after(set_unit("api-list", files=[root])), root)

    def test_repeated_slashes_equal_the_clean_path(self):
        self.assertTrue(check_lanes.paths_overlap("src//a.py", "src/a.py"))
        self.assertIn("lane-overlap", codes_after(set_unit("api-list", files=["src//create.py"])))

    def test_dot_dot_segments_equal_the_resolved_path(self):
        self.assertTrue(check_lanes.paths_overlap("src/../src/create.py", "src/create.py"))
        self.assertIn("lane-overlap", codes_after(set_unit("api-list", files=["src/../src/create.py"])))

    def test_trailing_dot_segment_marks_a_directory(self):
        for directory in ("src/.", "src/routes/.."):
            self.assertTrue(check_lanes.paths_overlap(directory, "src/create.py"), directory)

    def test_earlier_foundation_owning_directory_overlaps_later_lane_file(self):
        def change(p):
            unit_of(p, "api-F")["files"] = ["src/"]
            unit_of(p, "api-list")["blocked_by"] = []
        self.assertIn("foundation-overlap", codes_after(change))

    def test_cycle_with_foundation_overlap_reports_both(self):
        def change(p):
            unit_of(p, "api-F")["blocked_by"] = ["api-create"]
            unit_of(p, "api-list").update(files=["src/routes/list.py"], blocked_by=[])
        found = codes_after(change)
        self.assertIn("cycle", found)
        self.assertIn("foundation-overlap", found)

    def test_disjoint_cycles_are_both_reported(self):
        def change(p):
            unit_of(p, "api-F")["blocked_by"] = ["api-create"]
            unit_of(p, "web-F")["blocked_by"] = ["web-form"]
        self.assertEqual(codes_after(change).count("cycle"), 2)


if __name__ == "__main__":
    unittest.main()

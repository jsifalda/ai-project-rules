#!/usr/bin/env python3
"""Validate a parallel execution plan. Stdlib only.

Usage: python3 check_lanes.py <plan.json>
Exit 0 = clean, 1 = violations, 2 = unreadable or malformed input.
"""
import argparse
import itertools
import json
import posixpath
import re
import sys

EXIT_CLEAN = 0
EXIT_VIOLATIONS = 1
EXIT_BAD_INPUT = 2
FOUNDATION = "foundation"
LANE = "lane"
KINDS = (FOUNDATION, LANE)
DIRECTORY_SEGMENTS = (".", "..")
UNIT_LIST_FIELDS = ("files", "scenarios", "blocked_by", "resources",
                    "gate_resources")


class PlanError(Exception):
    pass


def normalize(path):
    is_dir = path.endswith("/") or posixpath.basename(path) in DIRECTORY_SEGMENTS
    path = posixpath.normpath(re.sub("/+", "/", path) or ".")
    if path == ".":
        return ""
    return path + "/" if is_dir else path


def paths_overlap(a, b):
    a, b = normalize(a), normalize(b)
    if not a or not b or a == b:
        return True
    return (a.endswith("/") and b.startswith(a)) or (
        b.endswith("/") and a.startswith(b))


def first_overlap(files_a, files_b):
    for a, b in itertools.product(files_a, files_b):
        if paths_overlap(a, b):
            return a, b
    return None


def require(condition, message):
    if not condition:
        raise PlanError(message)


def is_str_list(value):
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


def parse_unit(raw, index):
    require(isinstance(raw, dict), f"units[{index}] must be an object")
    for key in ("id", "repo", "kind"):
        require(isinstance(raw.get(key), str), f"units[{index}].{key} must be a string")
    unit = {key: raw[key] for key in ("id", "repo", "kind")}
    for key in UNIT_LIST_FIELDS:
        value = raw.get(key, [])
        require(is_str_list(value), f"units[{index}].{key} must be a list of strings")
        unit[key] = value
    for path in unit["files"]:
        require(not path.startswith("/"),
                f"units[{index}].files entry {path!r} is absolute")
        require(normalize(path).split("/")[0] != "..",
                f"units[{index}].files entry {path!r} escapes the repo root")
    return unit


def parse_plan(data):
    require(isinstance(data, dict), "top level must be an object")
    for key in ("scenarios", "units", "batches"):
        require(key in data, f"missing top-level key: {key}")
    require(isinstance(data["scenarios"], list), "scenarios must be a list")
    for i, s in enumerate(data["scenarios"]):
        require(isinstance(s, dict) and isinstance(s.get("id"), str),
                f"scenarios[{i}].id must be a string")
    require(isinstance(data["units"], list), "units must be a list")
    units = [parse_unit(u, i) for i, u in enumerate(data["units"])]
    batches = data["batches"]
    require(isinstance(batches, list) and all(is_str_list(b) for b in batches),
            "batches must be a list of lists of strings")
    caps = data.get("resource_caps")
    require(caps is None or (isinstance(caps, dict) and all(
        isinstance(v, int) and not isinstance(v, bool) and v >= 0
        for v in caps.values())), "resource_caps must be null or map names to non-negative integers")
    max_agents = data.get("max_agents")
    require(max_agents is None or (
        isinstance(max_agents, int) and not isinstance(max_agents, bool)
        and max_agents > 0), "max_agents must be null or a positive integer")
    return {"scenarios": [s["id"] for s in data["scenarios"]], "units": units,
            "batches": batches, "caps": caps, "max_agents": max_agents}


def duplicates(ids):
    seen, dupes = set(), []
    for i in ids:
        if i in seen and i not in dupes:
            dupes.append(i)
        seen.add(i)
    return dupes


def reachable(start, deps):
    seen, stack = set(), list(deps.get(start, []))
    while stack:
        node = stack.pop()
        if node not in seen:
            seen.add(node)
            stack.extend(deps.get(node, []))
    return seen


def find_cycles(deps):
    reach = {u: reachable(u, deps) for u in deps}
    on_cycle = {u for u in deps if u in reach[u]}
    groups = {frozenset(v for v in on_cycle if v in reach[u] and u in reach[v])
              for u in on_cycle}
    return sorted(sorted(g) for g in groups)


def check_ids(plan):
    out = []
    for i in duplicates([u["id"] for u in plan["units"]]):
        out.append(("duplicate-unit", f"unit id {i} is defined more than once"))
    for i in duplicates(plan["scenarios"]):
        out.append(("duplicate-scenario", f"scenario id {i} is defined more than once"))
    for u in plan["units"]:
        if u["kind"] not in KINDS:
            out.append(("bad-kind", f"unit {u['id']} has kind {u['kind']!r}, expected foundation or lane"))
    return out


def check_references(plan, unit_ids):
    out, scenarios = [], set(plan["scenarios"])
    for u in plan["units"]:
        for s in u["scenarios"]:
            if s not in scenarios:
                out.append(("unknown-scenario", f"unit {u['id']} references unknown scenario {s}"))
        for b in u["blocked_by"]:
            if b not in unit_ids:
                out.append(("unknown-unit", f"unit {u['id']} is blocked_by unknown unit {b}"))
        for r in u["resources"]:
            if plan["caps"] is not None and r not in plan["caps"]:
                out.append(("unknown-resource", f"unit {u['id']} names resource {r} missing from resource_caps"))
    for n, batch in enumerate(plan["batches"]):
        for i in batch:
            if i not in unit_ids:
                out.append(("unknown-unit", f"batch {n} references unknown unit {i}"))
    return out


def batch_indexes(plan):
    index = {}
    for n, batch in enumerate(plan["batches"]):
        for i in batch:
            index.setdefault(i, []).append(n)
    return index


def check_batching(plan):
    out, index = [], batch_indexes(plan)
    for u in plan["units"]:
        found = index.get(u["id"], [])
        if not found:
            out.append(("unbatched", f"unit {u['id']} appears in no batch"))
        elif len(found) > 1:
            out.append(("multi-batched", f"unit {u['id']} appears in batches {found}"))
    by_id = {u["id"]: u for u in plan["units"]}
    for uid, mine in index.items():
        for b in by_id.get(uid, {}).get("blocked_by", []):
            theirs = index.get(b)
            if theirs and max(theirs) >= min(mine):
                out.append(("batch-order", f"unit {uid} in batch {min(mine)} is not after blocker {b} in batch {max(theirs)}"))
    return out


def check_overlaps(plan, deps):
    out = []
    for a, b in itertools.combinations(plan["units"], 2):
        if a["kind"] == b["kind"] == LANE and a["repo"] == b["repo"]:
            hit = first_overlap(a["files"], b["files"])
            if hit:
                out.append(("lane-overlap", f"lanes {a['id']} and {b['id']} overlap on {hit[0]} and {hit[1]}"))
    foundations = [u for u in plan["units"] if u["kind"] == FOUNDATION]
    for lane in (u for u in plan["units"] if u["kind"] == LANE):
        upstream = reachable(lane["id"], deps)
        for f in foundations:
            hit = first_overlap(lane["files"], f["files"]) if f["repo"] == lane["repo"] else None
            if hit and f["id"] not in upstream:
                out.append(("foundation-overlap", f"lane {lane['id']} overlaps foundation {f['id']} on {hit[0]} and {hit[1]} without depending on it"))
    return out


def check_foundation_edges(plan, deps):
    out, foundations = [], [u for u in plan["units"] if u["kind"] == FOUNDATION]
    for lane in (u for u in plan["units"] if u["kind"] == LANE):
        upstream = reachable(lane["id"], deps)
        for f in foundations:
            if f["repo"] == lane["repo"] and f["id"] not in upstream:
                out.append(("missing-foundation-edge", f"lane {lane['id']} does not depend on foundation {f['id']} through blocked_by"))
    return out


def check_foundations(plan):
    by_repo = {}
    for u in plan["units"]:
        if u["kind"] == FOUNDATION:
            by_repo.setdefault(u["repo"], []).append(u["id"])
    return [("multiple-foundations", f"repo {repo} has {len(ids)} foundations: {', '.join(ids)}")
            for repo, ids in by_repo.items() if len(ids) > 1]


def check_coverage(plan):
    out = []
    for u in plan["units"]:
        if u["kind"] == LANE and not u["scenarios"]:
            out.append(("empty-lane", f"lane {u['id']} has no scenarios"))
    listed = {s for u in plan["units"] for s in u["scenarios"]}
    for s in plan["scenarios"]:
        if s not in listed:
            out.append(("uncovered-scenario", f"scenario {s} is listed by no unit"))
    return out


def check_batch_limits(plan):
    out, by_id = [], {u["id"]: u for u in plan["units"]}
    for n, batch in enumerate(plan["batches"]):
        members = list(dict.fromkeys(batch))
        limit = plan["max_agents"]
        if limit is not None and len(members) > limit:
            out.append(("max-agents", f"batch {n} has {len(members)} units, max_agents is {limit}"))
        for resource, cap in (plan["caps"] or {}).items():
            users = [i for i in members if resource in by_id.get(i, {}).get("resources", [])]
            if len(users) > cap:
                out.append(("resource-cap", f"batch {n} has {len(users)} units using {resource} ({', '.join(users)}), cap is {cap}"))
    return out


def check_plan(plan):
    unit_ids = {u["id"] for u in plan["units"]}
    deps = {u["id"]: [b for b in u["blocked_by"] if b in unit_ids] for u in plan["units"]}
    out = check_ids(plan) + check_references(plan, unit_ids)
    out += check_batching(plan) + check_overlaps(plan, deps)
    out += check_foundation_edges(plan, deps)
    out += check_coverage(plan) + check_foundations(plan)
    for ids in find_cycles(deps):
        out.append(("cycle", f"blocked_by cycle among {', '.join(ids)}"))
    return out + check_batch_limits(plan)


def summary(plan):
    units = plan["units"]
    foundations = sum(1 for u in units if u["kind"] == FOUNDATION)
    widest = max((len(set(b)) for b in plan["batches"]), default=0)
    listed = {s for u in units for s in u["scenarios"]}
    covered = sum(1 for s in set(plan["scenarios"]) if s in listed)
    return (f"OK: {len(units)} units ({foundations} foundation, {len(units) - foundations} lanes), "
            f"{len(plan['batches'])} batches, widest batch {widest}, "
            f"scenarios {covered}/{len(set(plan['scenarios']))} covered")


def load_plan(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return parse_plan(json.load(handle))
    except (OSError, ValueError, RecursionError, PlanError) as error:
        raise PlanError(f"cannot use {path}: {error}") from error


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate a parallel execution plan.")
    parser.add_argument("plan", help="path to plan.json")
    args = parser.parse_args(argv)
    try:
        plan = load_plan(args.plan)
    except PlanError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return EXIT_BAD_INPUT
    violations = check_plan(plan)
    if not violations:
        print(summary(plan))
        return EXIT_CLEAN
    for code, message in violations:
        print(f"VIOLATION {code}: {message}")
    print(f"FAIL: {len(violations)} violations")
    return EXIT_VIOLATIONS


if __name__ == "__main__":
    sys.exit(main())

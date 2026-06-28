"""
Tests for verify-models.py

Written from the spec, blind to the implementation.
All transcripts are synthesised in a per-test tempdir; no external files
are required except the optional shipped fixture.

Run:  python3 skills/op/scripts/test_verify_models.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(_HERE, "verify-models.py")
FIXTURE = os.path.join(_HERE, "fixtures", "sample-run.jsonl")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_script(transcript_path, *extra_args):
    """Invoke verify-models.py as a subprocess. Returns CompletedProcess."""
    cmd = [sys.executable, SCRIPT, transcript_path] + list(extra_args)
    return subprocess.run(cmd, capture_output=True, text=True)


def write_jsonl(path, records):
    with open(path, "w") as fh:
        for rec in records:
            fh.write(json.dumps(rec) + "\n")


def make_dispatch(tool_id, requested_model, task_desc="task", name="Agent"):
    """
    Build an assistant record that dispatches a subagent via Agent/Task tool_use.
    Pass requested_model=None to omit input.model entirely (absent-model case).
    """
    inp = {
        "description": task_desc,
        "subagent_type": "general-purpose",
        "prompt": "do the thing",
    }
    if requested_model is not None:
        inp["model"] = requested_model

    return {
        "type": "assistant",
        "message": {
            "model": "claude-opus-4-8",
            "content": [
                {
                    "type": "tool_use",
                    "id": tool_id,
                    "name": name,
                    "input": inp,
                }
            ],
        },
    }


def make_result(tool_id, resolved_model,
                input_tokens=10, output_tokens=90,
                cache_creation=100, cache_read=4800,
                duration_ms=1000):
    """
    Build a user record containing the toolUseResult for a completed subagent.
    total = sum of all four token fields.
    """
    total = input_tokens + output_tokens + cache_creation + cache_read
    return {
        "type": "user",
        "message": {
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": [],
                }
            ]
        },
        "toolUseResult": {
            "status": "completed",
            "agentType": "general-purpose",
            "resolvedModel": resolved_model,
            "totalDurationMs": duration_ms,
            "totalTokens": total,
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cache_creation_input_tokens": cache_creation,
                "cache_read_input_tokens": cache_read,
            },
            "toolUseID": tool_id,
        },
    }


def make_orchestrator(model="claude-opus-4-8",
                      input_tokens=100, output_tokens=200,
                      cache_creation=50, cache_read=150):
    """Build an orchestrator assistant turn with a usage block."""
    return {
        "type": "assistant",
        "message": {
            "model": model,
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cache_creation_input_tokens": cache_creation,
                "cache_read_input_tokens": cache_read,
            },
        },
    }


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

class TestVerifyModels(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="test_vm_")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _path(self, name):
        return os.path.join(self.tmpdir, name)

    # ------------------------------------------------------------------
    # 1. MISMATCH: requested haiku, resolvedModel is opus
    # ------------------------------------------------------------------
    def test_mismatch_wrong_tier(self):
        """
        Dispatch requests 'haiku' but resolvedModel contains 'opus'.
        'haiku' is not a substring of 'claude-opus-4-8' (case-insensitive),
        so this is a mismatch.
        Expected: stdout contains ROUTING PROBLEM and MISMATCH, exit code 1.
        """
        path = self._path("mismatch.jsonl")
        write_jsonl(path, [
            make_dispatch("toolu_1", "haiku", "task A"),
            make_result("toolu_1", "claude-opus-4-8"),
        ])
        result = run_script(path)
        self.assertEqual(
            result.returncode, 1,
            msg=f"Expected exit 1 for mismatch.\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )
        self.assertIn("ROUTING PROBLEM", result.stdout,
                      msg=f"Expected ROUTING PROBLEM warning.\nstdout: {result.stdout}")
        self.assertIn("MISMATCH", result.stdout,
                      msg=f"Expected MISMATCH marker in routing table.\nstdout: {result.stdout}")

    # ------------------------------------------------------------------
    # 2. CLEAN: two matched dispatches + orchestrator turn
    # ------------------------------------------------------------------
    def test_clean_no_mismatch(self):
        """
        haiku->claude-haiku-4-5-20251001 and sonnet->claude-sonnet-4-6 are both
        on-tier. Expected: no MISMATCH, exit 0, MODEL USAGE section present.
        """
        path = self._path("clean.jsonl")
        write_jsonl(path, [
            make_orchestrator(model="claude-opus-4-8",
                              input_tokens=100, output_tokens=200,
                              cache_creation=50, cache_read=150),
            make_dispatch("toolu_1", "haiku", "task A"),
            make_result("toolu_1", "claude-haiku-4-5-20251001"),
            make_dispatch("toolu_2", "sonnet", "task B"),
            make_result("toolu_2", "claude-sonnet-4-6"),
        ])
        result = run_script(path)
        self.assertEqual(
            result.returncode, 0,
            msg=f"Expected exit 0 for clean run.\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )
        self.assertNotIn("MISMATCH", result.stdout,
                         msg=f"Unexpected MISMATCH in clean output.\nstdout: {result.stdout}")
        self.assertIn("MODEL USAGE", result.stdout,
                      msg=f"Expected MODEL USAGE section.\nstdout: {result.stdout}")

    # ------------------------------------------------------------------
    # 3. ZERO-DISPATCH: no Agent/Task tool_use in transcript
    # ------------------------------------------------------------------
    def test_zero_dispatch(self):
        """
        Transcript contains only orchestrator assistant turns and ordinary user
        messages. No Agent/Task tool_use → NO SUBAGENTS DISPATCHED, exit 2.
        """
        path = self._path("zero.jsonl")
        write_jsonl(path, [
            make_orchestrator(model="claude-opus-4-8",
                              input_tokens=50, output_tokens=100,
                              cache_creation=0, cache_read=0),
            {
                "type": "user",
                "message": {"content": [{"type": "text", "text": "hello"}]},
            },
            make_orchestrator(model="claude-opus-4-8",
                              input_tokens=30, output_tokens=60,
                              cache_creation=0, cache_read=0),
        ])
        result = run_script(path)
        self.assertEqual(
            result.returncode, 2,
            msg=f"Expected exit 2 for zero dispatches.\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )
        self.assertIn("NO SUBAGENTS DISPATCHED", result.stdout,
                      msg=f"Expected NO SUBAGENTS DISPATCHED.\nstdout: {result.stdout}")

    # ------------------------------------------------------------------
    # 4. USAGE SUM: --json token totals must be arithmetically exact
    # ------------------------------------------------------------------
    def test_json_usage_sums(self):
        """
        In --json mode the usage entry for each role/model must carry
        the exact token sum (input+output+cache_creation+cache_read)
        taken from the transcript, and summary counts must be correct.
        """
        path = self._path("clean_json.jsonl")

        # Orchestrator: 100+200+50+150 = 500
        oi, oo, occ, ocr = 100, 200, 50, 150
        expected_orch = oi + oo + occ + ocr  # 500

        # Haiku subagent: 10+90+100+4800 = 5000
        hi, ho, hcc, hcr = 10, 90, 100, 4800
        expected_haiku = hi + ho + hcc + hcr  # 5000

        # Sonnet subagent: 20+180+200+9600 = 10000
        si, so, scc, scr = 20, 180, 200, 9600
        expected_sonnet = si + so + scc + scr  # 10000

        write_jsonl(path, [
            make_orchestrator(model="claude-opus-4-8",
                              input_tokens=oi, output_tokens=oo,
                              cache_creation=occ, cache_read=ocr),
            make_dispatch("toolu_1", "haiku", "task A"),
            make_result("toolu_1", "claude-haiku-4-5-20251001",
                        input_tokens=hi, output_tokens=ho,
                        cache_creation=hcc, cache_read=hcr),
            make_dispatch("toolu_2", "sonnet", "task B"),
            make_result("toolu_2", "claude-sonnet-4-6",
                        input_tokens=si, output_tokens=so,
                        cache_creation=scc, cache_read=scr),
        ])

        result = run_script(path, "--json")
        self.assertEqual(
            result.returncode, 0,
            msg=f"Expected exit 0.\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            self.fail(f"--json output is not valid JSON: {exc}\nstdout: {result.stdout}")

        # Summary counts
        summary = data.get("summary", {})
        self.assertEqual(summary.get("dispatch_count"), 2,
                         msg=f"dispatch_count mismatch: {summary}")
        self.assertEqual(summary.get("mismatch_count"), 0,
                         msg=f"mismatch_count mismatch: {summary}")

        usage = data.get("usage", [])

        # Orchestrator token sum
        orch_entries = [u for u in usage if u.get("role") == "orchestrator"]
        self.assertTrue(orch_entries,
                        msg=f"No orchestrator entry in usage: {usage}")
        self.assertEqual(orch_entries[0]["tokens"], expected_orch,
                         msg=f"Orchestrator tokens wrong. Got {orch_entries[0]['tokens']}, want {expected_orch}")

        # Haiku subagent token sum
        haiku_entries = [u for u in usage
                         if "haiku" in u.get("model", "").lower()
                         and u.get("role") != "orchestrator"]
        self.assertTrue(haiku_entries,
                        msg=f"No haiku subagent entry in usage: {usage}")
        self.assertEqual(haiku_entries[0]["tokens"], expected_haiku,
                         msg=f"Haiku tokens wrong. Got {haiku_entries[0]['tokens']}, want {expected_haiku}")

        # Sonnet subagent token sum
        sonnet_entries = [u for u in usage
                          if "sonnet" in u.get("model", "").lower()
                          and u.get("role") != "orchestrator"]
        self.assertTrue(sonnet_entries,
                        msg=f"No sonnet subagent entry in usage: {usage}")
        self.assertEqual(sonnet_entries[0]["tokens"], expected_sonnet,
                         msg=f"Sonnet tokens wrong. Got {sonnet_entries[0]['tokens']}, want {expected_sonnet}")

    # ------------------------------------------------------------------
    # 5. ABSENT-MODEL: dispatch with no input.model is never a mismatch
    # ------------------------------------------------------------------
    def test_absent_model_not_mismatch(self):
        """
        A dispatch record that has no input.model must never be flagged as a
        mismatch regardless of resolvedModel.
        Human mode: exit 0, no MISMATCH, requested field shows '-'.
        JSON mode: requested is null or '-', mismatch is false.
        """
        path = self._path("absent.jsonl")
        write_jsonl(path, [
            make_dispatch("toolu_1", None, "auto-routed task"),
            make_result("toolu_1", "claude-sonnet-4-6"),
        ])

        # Human mode
        result = run_script(path)
        self.assertEqual(
            result.returncode, 0,
            msg=f"Expected exit 0 for absent-model dispatch.\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )
        self.assertNotIn("MISMATCH", result.stdout,
                         msg=f"Absent-model dispatch must not produce MISMATCH.\nstdout: {result.stdout}")
        self.assertIn("-", result.stdout,
                      msg="Expected '-' placeholder for absent requested model in human output.")

        # JSON mode
        result_json = run_script(path, "--json")
        self.assertEqual(result_json.returncode, 0,
                         msg=f"--json exit code wrong.\nstdout: {result_json.stdout}")
        try:
            data = json.loads(result_json.stdout)
        except json.JSONDecodeError as exc:
            self.fail(f"--json output is not valid JSON: {exc}\nstdout: {result_json.stdout}")

        dispatches = data.get("dispatches", [])
        self.assertEqual(len(dispatches), 1,
                         msg=f"Expected 1 dispatch entry, got: {dispatches}")
        req = dispatches[0].get("requested")
        self.assertIn(req, [None, "-", ""],
                      msg=f"requested field for absent model should be null/'-', got: {req!r}")
        self.assertFalse(dispatches[0].get("mismatch"),
                         msg=f"Absent-model dispatch must not be flagged mismatch: {dispatches[0]}")

    # ------------------------------------------------------------------
    # 6. SHIPPED FIXTURE: sample-run.jsonl (skipped if absent)
    # ------------------------------------------------------------------
    @unittest.skipUnless(os.path.exists(FIXTURE), "fixtures/sample-run.jsonl not present")
    def test_shipped_fixture_has_mismatch(self):
        """
        The shipped sample-run.jsonl is documented to contain a routing problem.
        Expected: exit 1 and stdout contains MISMATCH.
        """
        result = run_script(FIXTURE)
        self.assertEqual(
            result.returncode, 1,
            msg=f"Fixture expected exit 1.\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )
        self.assertIn("MISMATCH", result.stdout,
                      msg=f"Fixture expected MISMATCH in output.\nstdout: {result.stdout}")

    # ------------------------------------------------------------------
    # Bonus A: routing-table header labels both columns
    # ------------------------------------------------------------------
    def test_routing_table_header_labels(self):
        """
        The human-mode output must include a header line that contains both
        the word 'requested' and the word 'actual' (case-insensitive).
        """
        path = self._path("header.jsonl")
        write_jsonl(path, [
            make_dispatch("toolu_1", "haiku", "task A"),
            make_result("toolu_1", "claude-haiku-4-5-20251001"),
        ])
        result = run_script(path)
        lower = result.stdout.lower()
        self.assertIn("requested", lower,
                      msg=f"'requested' missing from routing header.\nstdout: {result.stdout}")
        self.assertIn("actual", lower,
                      msg=f"'actual' missing from routing header.\nstdout: {result.stdout}")

    # ------------------------------------------------------------------
    # Bonus B: MODEL USAGE section contains a percentage for orchestrator
    # ------------------------------------------------------------------
    def test_orchestrator_percentage_shown(self):
        """
        The MODEL USAGE section must show a percentage (e.g. '82%') on the
        orchestrator model line, as required by the spec.
        """
        path = self._path("pct.jsonl")
        write_jsonl(path, [
            make_orchestrator(model="claude-opus-4-8",
                              input_tokens=800, output_tokens=200,
                              cache_creation=0, cache_read=0),
            make_dispatch("toolu_1", "haiku", "task A"),
            make_result("toolu_1", "claude-haiku-4-5-20251001",
                        input_tokens=10, output_tokens=90,
                        cache_creation=0, cache_read=0),
        ])
        result = run_script(path)
        self.assertIn("MODEL USAGE", result.stdout,
                      msg=f"MODEL USAGE section missing.\nstdout: {result.stdout}")
        self.assertIn("%", result.stdout,
                      msg=f"Percentage missing from MODEL USAGE.\nstdout: {result.stdout}")

    # ------------------------------------------------------------------
    # Bonus C: 'Task' tool name is recognised as a dispatch (not just 'Agent')
    # ------------------------------------------------------------------
    def test_task_tool_name_counts_as_dispatch(self):
        """
        Tool records named 'Task' must be treated identically to 'Agent'.
        A single matched Task dispatch must produce exit 0, not exit 2.
        """
        path = self._path("task_name.jsonl")
        write_jsonl(path, [
            make_dispatch("toolu_1", "haiku", "task A", name="Task"),
            make_result("toolu_1", "claude-haiku-4-5-20251001"),
        ])
        result = run_script(path)
        self.assertNotIn("NO SUBAGENTS DISPATCHED", result.stdout,
                         msg=f"Task tool_use must count as a dispatch.\nstdout: {result.stdout}")
        self.assertEqual(
            result.returncode, 0,
            msg=f"Expected exit 0 for clean Task dispatch.\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )

    # ------------------------------------------------------------------
    # Bonus D: nonexistent transcript path → exit 2
    # ------------------------------------------------------------------
    def test_nonexistent_transcript_exits_2(self):
        """Passing a path that does not exist must produce exit code 2."""
        result = run_script("/nonexistent/path/does-not-exist.jsonl")
        self.assertEqual(
            result.returncode, 2,
            msg=f"Expected exit 2 for missing file.\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )

    # ------------------------------------------------------------------
    # Bonus E: summary line carries both dispatch count and mismatch count
    # ------------------------------------------------------------------
    def test_summary_line_contains_counts(self):
        """
        The final summary line must contain the numeric dispatch count and
        mismatch count. We verify with one dispatch / one mismatch.
        """
        path = self._path("summary.jsonl")
        write_jsonl(path, [
            make_dispatch("toolu_1", "haiku", "task A"),
            make_result("toolu_1", "claude-opus-4-8"),  # mismatch
        ])
        result = run_script(path)
        stdout = result.stdout
        # There must be a line that mentions both counts (both are 1 here)
        lines = [l for l in stdout.splitlines()
                 if ("1" in l) and
                    ("dispatch" in l.lower() or "mismatch" in l.lower())]
        self.assertTrue(lines,
                        msg=f"No summary line with dispatch/mismatch counts found.\nstdout: {stdout}")

    # ------------------------------------------------------------------
    # Bonus F: sonnet mismatch (requested sonnet, got haiku)
    # ------------------------------------------------------------------
    def test_mismatch_sonnet_got_haiku(self):
        """
        Requested 'sonnet' but resolved to 'claude-haiku-4-5-20251001'.
        'sonnet' is not in 'claude-haiku-4-5-20251001' → MISMATCH, exit 1.
        """
        path = self._path("sonnet_mismatch.jsonl")
        write_jsonl(path, [
            make_dispatch("toolu_1", "sonnet", "task A"),
            make_result("toolu_1", "claude-haiku-4-5-20251001"),
        ])
        result = run_script(path)
        self.assertEqual(
            result.returncode, 1,
            msg=f"Expected exit 1 for sonnet→haiku mismatch.\nstdout: {result.stdout}",
        )
        self.assertIn("MISMATCH", result.stdout,
                      msg=f"Expected MISMATCH marker.\nstdout: {result.stdout}")

    # ------------------------------------------------------------------
    # Bonus G: mixed clean+mismatch dispatches → exit 1, count correct
    # ------------------------------------------------------------------
    def test_mixed_clean_and_mismatch(self):
        """
        Three dispatches: haiku-OK, sonnet-OK, opus-got-haiku.
        Expected: exit 1, exactly one MISMATCH row, dispatch_count=3 in --json.
        """
        path = self._path("mixed.jsonl")
        write_jsonl(path, [
            make_dispatch("toolu_1", "haiku", "task A"),
            make_result("toolu_1", "claude-haiku-4-5-20251001"),
            make_dispatch("toolu_2", "sonnet", "task B"),
            make_result("toolu_2", "claude-sonnet-4-6"),
            make_dispatch("toolu_3", "opus", "task C"),
            make_result("toolu_3", "claude-haiku-4-5-20251001"),  # wrong
        ])
        result = run_script(path)
        self.assertEqual(
            result.returncode, 1,
            msg=f"Expected exit 1 for mixed.\nstdout: {result.stdout}",
        )
        self.assertIn("MISMATCH", result.stdout,
                      msg=f"Expected MISMATCH marker.\nstdout: {result.stdout}")

        # JSON check
        result_json = run_script(path, "--json")
        data = json.loads(result_json.stdout)
        self.assertEqual(data["summary"]["dispatch_count"], 3)
        self.assertEqual(data["summary"]["mismatch_count"], 1)
        mismatched = [d for d in data["dispatches"] if d.get("mismatch")]
        self.assertEqual(len(mismatched), 1,
                         msg=f"Expected exactly 1 mismatch dispatch: {data['dispatches']}")
    # ------------------------------------------------------------------
    # Bonus H: --all must let a mismatch (exit 1) win over a no-dispatch
    #          transcript (exit 2). A numeric max would mask the mismatch.
    # ------------------------------------------------------------------
    def test_all_mismatch_beats_zero_dispatch(self):
        """
        With --all over a project that has one mismatched transcript and one
        zero-dispatch transcript, the aggregate exit code must be 1 (a routing
        failure exists), never 2.
        """
        # A self-contained fake config dir + project so --all resolves here.
        # Use realpath: the script derives its slug from os.getcwd(), which
        # canonicalises symlinks (e.g. /var -> /private/var on macOS).
        config_dir = os.path.join(self.tmpdir, "cfg")
        workdir = os.path.realpath(os.path.join(self.tmpdir, "work"))
        os.makedirs(workdir)
        slug = workdir.replace("/", "-")
        project_dir = os.path.join(config_dir, "projects", slug)
        os.makedirs(project_dir)

        write_jsonl(os.path.join(project_dir, "a-mismatch.jsonl"), [
            make_dispatch("toolu_1", "haiku", "task A"),
            make_result("toolu_1", "claude-opus-4-8"),  # mismatch
        ])
        write_jsonl(os.path.join(project_dir, "b-zero.jsonl"), [
            make_orchestrator(model="claude-opus-4-8"),
        ])

        env = dict(os.environ, CLAUDE_CONFIG_DIR=config_dir)
        result = subprocess.run(
            [sys.executable, SCRIPT, "--all"],
            capture_output=True, text=True, cwd=workdir, env=env,
        )
        self.assertEqual(
            result.returncode, 1,
            msg=f"--all must exit 1 when any transcript has a mismatch, "
                f"even alongside a zero-dispatch transcript.\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

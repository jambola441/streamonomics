#!/usr/bin/env python3
"""Quick tests for plan_parse.py. Run: python3 tools/test_plan_parse.py"""
import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plan_parse  # noqa: E402

HERE = Path(__file__).resolve().parent

GOOD = textwrap.dedent("""\
    ---
    name: Stream Manager
    slug: stream-manager
    status: active          # idea | active | paused | shipped | archived
    slot: weekend           # tue | thu | weekend | any
    linear:
      team: Streamonomics
      project: "Stream Manager"
      project_id:           # written by /sync-plan
    ---
    # Stream Manager: Plan

    ## Goal
    Claude runs the stream.

    ## Milestones

    ### v0: Local only <!-- linear-milestone: -->
    - [ ] Build `sm` CLI state commands `est:3` `slot:weekend`
      - state get/set, session start/stop
      - writes stream/state.json
    - [x] Some finished thing [STR-12]

    ### v1: OBS control <!-- linear-milestone: abc-123 -->
    - [ ] Scene switching [STR-13] `est:2`

    ## Parking lot
    <!-- not synced to Linear -->
    - maybe-someday idea
    - an old ticket [STR-99]
    """)


def parse_text(text, folder="stream-manager"):
    d = Path(tempfile.mkdtemp()) / folder
    d.mkdir()
    p = d / "plan.md"
    p.write_text(text)
    return plan_parse.parse(p)


def errors(result):
    return [w["message"] for w in result["warnings"] if w["level"] == "error"]


class GoodPlan(unittest.TestCase):
    def setUp(self):
        self.r = parse_text(GOOD)

    def test_no_errors(self):
        self.assertEqual(errors(self.r), [])
        self.assertFalse(plan_parse.has_errors(self.r))

    def test_frontmatter(self):
        fm = self.r["frontmatter"]
        self.assertEqual(fm["status"], "active")  # comment stripped
        self.assertEqual(fm["linear"]["team"], "Streamonomics")
        self.assertEqual(fm["linear"]["project"], "Stream Manager")  # quotes stripped
        self.assertIsNone(fm["linear"]["project_id"])
        self.assertEqual(self.r["frontmatter_lines"]["linear.project_id"], 9)

    def test_goal_and_title(self):
        self.assertEqual(self.r["title"], "Stream Manager: Plan")
        self.assertEqual(self.r["goal"], "Claude runs the stream.")

    def test_milestones(self):
        ms = self.r["milestones"]
        self.assertEqual([m["title"] for m in ms], ["v0: Local only", "v1: OBS control"])
        self.assertIsNone(ms[0]["linear_milestone_id"])
        self.assertEqual(ms[1]["linear_milestone_id"], "abc-123")
        self.assertEqual(ms[0]["line"], 18)

    def test_deliverables(self):
        d0, d1 = self.r["milestones"][0]["deliverables"]
        self.assertEqual(d0["title"], "Build `sm` CLI state commands")  # plain code span kept
        self.assertEqual((d0["est"], d0["slot"], d0["id"], d0["done"]), (3, "weekend", None, False))
        self.assertEqual(d0["description"], ["- state get/set, session start/stop",
                                             "- writes stream/state.json"])
        self.assertEqual(d0["line"], 19)
        self.assertEqual((d1["title"], d1["id"], d1["done"]), ("Some finished thing", "STR-12", True))

    def test_parking_lot_and_counts(self):
        self.assertEqual([p["text"] for p in self.r["parking_lot"]],
                         ["maybe-someday idea", "an old ticket [STR-99]"])
        self.assertEqual(self.r["parking_lot"][1]["id"], "STR-99")
        self.assertEqual(self.r["counts"], {"milestones": 2, "deliverables": 3, "done": 1,
                                            "unsynced": 1, "parking_lot": 2})


class BadPlans(unittest.TestCase):
    def body(self, milestones):
        head = GOOD.split("## Milestones")[0]
        return head + "## Milestones\n" + textwrap.dedent(milestones)

    def test_checkbox_before_milestone(self):
        r = parse_text(self.body("- [ ] orphan line\n### M1 <!-- linear-milestone: -->\n"))
        self.assertTrue(any("before any '### ' milestone" in e for e in errors(r)))

    def test_bad_tags(self):
        r = parse_text(self.body("### M1 <!-- linear-milestone: -->\n- [ ] a `est:lots` `slot:friday`\n"))
        errs = errors(r)
        self.assertTrue(any("est:lots" in e for e in errs))
        self.assertTrue(any("slot:friday" in e for e in errs))

    def test_duplicate_ids(self):
        r = parse_text(self.body("### M1 <!-- linear-milestone: -->\n- [ ] a [STR-1]\n- [ ] b [STR-1]\n"))
        self.assertTrue(any("duplicate issue ID STR-1" in e for e in errors(r)))

    def test_malformed_checkbox_and_id(self):
        r = parse_text(self.body("### M1 <!-- linear-milestone: -->\n-[ ] squished\n- [ ] a [str-1]\n"))
        errs = errors(r)
        self.assertTrue(any("malformed checkbox" in e for e in errs))
        self.assertTrue(any("malformed issue ID" in e for e in errs))

    def test_placeholder_blocks_sync(self):
        r = parse_text(self.body("### Next up <!-- linear-milestone: -->\n- [ ] TODO: fill me in\n"))
        self.assertTrue(any("placeholder" in e for e in errors(r)))

    def test_bad_frontmatter(self):
        r = parse_text("---\nname: X\nstatus: vibing\n---\n## Milestones\n", folder="x")
        errs = errors(r)
        self.assertTrue(any("status 'vibing'" in e for e in errs))
        self.assertTrue(any("missing 'linear.team'" in e for e in errs))

    def test_missing_frontmatter(self):
        r = parse_text("# Just a heading\n", folder="x")
        self.assertTrue(any("missing frontmatter" in e for e in errors(r)))

    def test_missing_milestone_comment_is_only_a_warning(self):
        r = parse_text(self.body("### M1\n- [ ] a\n"))
        self.assertEqual(errors(r), [])
        self.assertTrue(any("no <!-- linear-milestone" in w["message"] for w in r["warnings"]))


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(HERE / "plan_parse.py"), *args],
                              capture_output=True, text=True)

    def test_exit_codes(self):
        d = Path(tempfile.mkdtemp()) / "stream-manager"
        d.mkdir()
        (d / "plan.md").write_text(GOOD)
        ok = self.run_cli(str(d / "plan.md"))
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertEqual(json.loads(ok.stdout)["counts"]["deliverables"], 3)
        (d / "plan.md").write_text(GOOD.replace("`est:3`", "`est:x`"))
        self.assertEqual(self.run_cli(str(d / "plan.md")).returncode, 1)
        self.assertEqual(self.run_cli("/nope/plan.md").returncode, 2)

    def test_all_returns_list_without_template(self):
        r = self.run_cli("--all")
        data = json.loads(r.stdout)
        self.assertIsInstance(data, list)
        self.assertFalse(any("_template" in p["path"] for p in data))


if __name__ == "__main__":
    unittest.main()

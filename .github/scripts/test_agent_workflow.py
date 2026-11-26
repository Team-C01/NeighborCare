"""Tests of deterministic workflow logic (no network or AI calls)."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import agent_workflow as a
import verify_reports as v

class ScopeTests(unittest.TestCase):
    def test_app_and_test_are_separate(self):
        self.assertTrue(a.permitted_path("implementazione", "backend/src/main/java/X.java", "A"))
        self.assertTrue(a.permitted_path("correzione", "frontend/src/App.jsx", "M"))
        self.assertFalse(a.permitted_path("implementazione", "frontend/tests/App.test.jsx", "A"))
        self.assertFalse(a.permitted_path("correzione", "backend/src/test/X.java", "M"))
        self.assertTrue(a.permitted_path("test", "backend/src/test/X.java", "A"))
        self.assertTrue(a.permitted_path("test", "frontend/src/App.test.jsx", "M"))
        self.assertFalse(a.permitted_path("test", "frontend/src/App.jsx", "M"))
        self.assertFalse(a.permitted_path("test", "frontend/tests/App.test.jsx", "D"))

    def test_workflow_and_credentials_are_protected(self):
        for path in (".github/workflows/ci.yml", "AGENTS.md", "backend/pom.xml",
                     "frontend/package-lock.json", "docs/rad/C01_RAD.pdf",
                     "frontend/public/.env", "frontend/src/../../AGENTS.md",
                     "backend/src/main/private.pem", "frontend/src/AGENTS.md"):
            for phase in a.ROLE:
                self.assertFalse(a.permitted_path(phase, path, "M"), (phase, path))

    def test_non_regular_files_rejected(self):
        with patch.object(a, "git", side_effect=["A\0frontend/src/link.jsx\0", "120000 x"]):
            with self.assertRaises(ValueError):
                a.check_scope("implementazione")

    def test_linked_issue(self):
        self.assertEqual(a.linked_issue("Closes #44\nText"), 44)
        self.assertEqual(a.linked_issue("Refs #123"), 123)
        self.assertIsNone(a.linked_issue("No issue"))

    def test_issue_fingerprint_ignores_assignment_and_labels(self):
        issue = {"title": "A", "body": "B", "labels": ["x"]}
        other = dict(issue, labels=["y"], assignees=["z"])
        self.assertEqual(a.fingerprint(issue), a.fingerprint(other))
        self.assertNotEqual(a.fingerprint(issue), a.fingerprint(dict(issue, body="C")))

    def test_approval_legacy_and_new_marker(self):
        issue = {"number": 1, "title": "A", "body": "B", "assignees": [{"login": "tm"}]}
        plan = {"id": 1, "user": {"login": "github-actions[bot]"},
                "body": a.PLAN_HEADER + "\n<!-- neighborcare-plan: " + a.fingerprint(issue) + " -->"}
        with patch.object(a, "pages", return_value=[plan]):
            self.assertEqual(a.latest_plan(issue), plan)
            with self.assertRaises(ValueError):
                a.latest_plan(dict(issue, body="Changed"))
        old = dict(plan, body=a.PLAN_HEADER)
        with patch.object(a, "pages", return_value=[old]):
            self.assertEqual(a.latest_plan(issue), old)

    def test_ci_dispatch(self):
        with patch.object(a, "cmd", return_value="") as call:
            self.assertIn("CI avviata", a.dispatch_ci("agent/issue-1-implementazione"))
            self.assertIn("--ref", call.call_args.args)

    def test_ordinary_documentation_allowed(self):
        self.assertTrue(a.permitted_path("implementazione", "docs/guida.md", "A"))
        self.assertFalse(a.permitted_path("correzione", "docs/rad/uc/UC.md", "M"))

    def test_reports_count_skipped_and_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "report.xml"
            p.write_text('<testsuite><testcase classname="DatabaseIntegrationTest"><skipped/></testcase><testcase/><testcase><failure/></testcase></testsuite>')
            self.assertEqual(v.count_reports([p]), (2, 1, 1, True))

if __name__ == "__main__":
    unittest.main()

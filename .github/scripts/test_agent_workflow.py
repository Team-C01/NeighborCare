"""Tests of deterministic workflow logic (no network or AI calls)."""
import json
import os
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

    def test_planning_history_preserves_conversation(self):
        comments = [
            {"id": 1, "user": {"login": "github-actions[bot]"}, "body": a.PLAN_HEADER + "\nPiano 1"},
            {"id": 2, "user": {"login": "tm"}, "body": "Prima osservazione"},
            {"id": 3, "user": {"login": "github-actions[bot]"}, "body": a.PLAN_HEADER + "\nPiano 2"},
            {"id": 4, "user": {"login": "tm"}, "body": "AGENTE PIANO: ultima richiesta"},
        ]
        evidence = {"issue": {"body": "Obiettivo"}, "request": comments[-1]["body"]}
        a.planning_history(comments, evidence)
        self.assertEqual(evidence["previous_plan"], comments[2]["body"])
        self.assertEqual([c["id"] for c in evidence["issue_comments"]], [1, 2, 3, 4])
        self.assertNotIn("history_notice", evidence)

    def test_planning_history_prioritizes_recent_comments(self):
        comments = [
            {"id": 1, "user": {"login": "tm"}, "body": "x" * 4000},
            {"id": 2, "user": {"login": "github-actions[bot]"}, "body": a.PLAN_HEADER + "\nUltimo piano"},
            {"id": 3, "user": {"login": "tm"}, "body": "AGENTE PIANO: correzione"},
        ]
        evidence = {"request": comments[-1]["body"]}
        a.planning_history(comments, evidence, limit=1500)
        self.assertEqual(evidence["previous_plan"], comments[1]["body"])
        self.assertEqual([c["id"] for c in evidence["issue_comments"]], [2, 3])
        self.assertIn("history_notice", evidence)

    def test_ci_evidence_ignores_approval_only_run(self):
        blocked = {"id": 3, "status": "completed", "conclusion": "action_required"}
        green = {"id": 2, "status": "completed", "conclusion": "success"}
        red = {"id": 4, "status": "completed", "conclusion": "failure"}
        active = {"id": 5, "status": "in_progress", "conclusion": None}
        self.assertEqual(a.select_ci_run([blocked, green]), green)
        self.assertEqual(a.select_ci_run([red, blocked, green]), red)
        self.assertEqual(a.select_ci_run([active, green]), green)
        self.assertEqual(a.select_ci_run([active, blocked]), active)
        self.assertIsNone(a.select_ci_run([blocked]))

    def test_commit_traces_request_without_fake_coauthor(self):
        message = a.commit_message("test", "issue #55", "demr64",
                                   ["kappq", "demr64"], "https://github.com/run")
        self.assertIn("(demr64)", message)
        self.assertIn("Requested-by: demr64", message)
        self.assertIn("Task-assignees: kappq, demr64", message)
        self.assertEqual([line for line in message.splitlines() if line.startswith("Co-authored-by:")],
                         ["Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"])

    def test_confirmed_coauthors_are_assigned_self_declared_and_unused(self):
        users = [{"login": "tm", "id": 123, "type": "User"},
                 {"login": "other", "id": 456, "type": "User"}]
        comments = [
            {"id": 1, "user": users[0], "body": "COAUTORE: test - Definiti i casi limite",
             "created_at": "2026-11-26T10:00:00Z"},
            {"id": 2, "user": users[1], "body": "COAUTORE: implementazione - Scritto il componente",
             "created_at": "2026-11-26T10:00:00Z"},
            {"id": 3, "user": {"login": "outsider", "id": 789}, "body": "COAUTORE: test - Definiti i casi limite",
             "created_at": "2026-11-26T10:00:00Z"},
        ]
        selected = a.confirmed_coauthors(users, comments, "test", set(), "2026-11-26T11:00:00Z")
        self.assertEqual(selected, [(users[0], 1)])
        self.assertEqual(a.confirmed_coauthors(users, comments, "test", {"1"}, "2026-11-26T11:00:00Z"), [])
        self.assertEqual(a.confirmed_coauthors(users, comments, "test", set(), "2026-11-26T09:00:00Z"), [])
        message = a.commit_message("test", "issue #55", "tm", ["tm", "other"], "url", selected)
        self.assertIn("Coauthor-claim: 1", message)
        self.assertEqual(message.count("Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"), 1)
        self.assertNotIn("Co-authored-by: other", message)
        self.assertTrue(message.endswith("Co-authored-by: tm <123+tm@users.noreply.github.com>"))

    def test_apply_new_approved_plan(self):
        pr = {"number": 60, "body": "Closes #59\n<!-- neighborcare-approved-plan: 1 -->\nPiano approvato: https://github.com/old\n"}
        with patch.object(a, "repo_api") as api:
            a.apply_approved_plan(pr, {"id": 2, "html_url": "https://github.com/new"})
            body = api.call_args.args[2]["body"]
            self.assertIn("Closes #59", body)
            self.assertIn("neighborcare-approved-plan: 2", body)
            self.assertNotIn("neighborcare-approved-plan: 1", body)

    def test_pr_plan_preserves_approved_version(self):
        comments = [
            {"id": 1, "user": {"login": "github-actions[bot]"}, "body": a.PLAN_HEADER + " v1",
             "created_at": "2026-11-26T10:00:00Z"},
            {"id": 2, "user": {"login": "github-actions[bot]"}, "body": a.PLAN_HEADER + " v2",
             "created_at": "2026-11-26T11:00:00Z"},
        ]
        pr = {"body": "<!-- neighborcare-approved-plan: 1 -->", "created_at": "2026-11-26T10:30:00Z"}
        self.assertEqual(a.approved_pr_plan({}, pr, comments), comments[0]["body"])
        self.assertEqual(a.approved_pr_plan({}, dict(pr, body="Closes #55"), comments), comments[0]["body"])

    def test_publish_creates_assigned_pr_and_one_ci(self):
        issue = {"number": 58, "title": "Task tecnico", "body": "Requisiti",
                 "assignees": [{"login": "tm"}]}
        ctx = {"issue": issue, "pr": None, "plan": {"id": 42, "html_url": "https://github.com/plan"},
               "base": "a" * 40, "head": "a" * 40, "branch": "agent/issue-58-implementazione"}
        with tempfile.TemporaryDirectory() as tmp, patch.multiple(
                a, ARTIFACT=Path(tmp), PHASE="implementazione", ACTOR="tm",
                REPO="Team-C01/NeighborCare"):
            (Path(tmp) / "state.json").write_text(json.dumps(a.state_for(ctx)))
            (Path(tmp) / "report.md").write_text("Implementato")
            (Path(tmp) / "changes.patch").write_text("patch")
            def fake_git(*args):
                return "b" * 40 + "\n" if args[:2] == ("rev-parse", "HEAD") else ""
            with patch.dict(a.os.environ, {"GITHUB_RUN_ID": "123"}), \
                 patch.object(a, "context", return_value=ctx), \
                 patch.object(a, "pages", return_value=[]), \
                 patch.object(a, "checkout"), patch.object(a, "git", side_effect=fake_git) as git, \
                 patch.object(a, "check_scope", return_value=["frontend/src/App.jsx"]), \
                 patch.object(a, "repo_api", side_effect=[{"number": 59}, {}]) as api, \
                 patch.object(a, "dispatch_ci", return_value="CI avviata") as dispatch, \
                 patch.object(a, "comment") as comment:
                a.publish()
            self.assertEqual(api.call_args_list[0].args[:2], ("pulls", "POST"))
            self.assertIn("neighborcare-approved-plan: 42", api.call_args_list[0].args[2]["body"])
            self.assertEqual(api.call_args_list[1].args, ("issues/59/assignees", "POST", {"assignees": ["tm"]}))
            dispatch.assert_called_once_with(ctx["branch"])
            comment.assert_called_once_with(59, "CI avviata")
            messages = [x.args[2] for x in git.call_args_list if x.args[:2] == ("commit", "-m")]
            self.assertEqual(len(messages), 1)
            self.assertIn("Requested-by: tm", messages[0])

    def test_no_changes_does_not_commit_or_dispatch(self):
        pr = {"number": 59, "assignees": [{"login": "tm"}]}
        ctx = {"issue": None, "pr": pr, "plan": None,
               "base": "a" * 40, "head": "b" * 40, "branch": "agent/issue-58-implementazione"}
        with tempfile.TemporaryDirectory() as tmp, patch.multiple(
                a, ARTIFACT=Path(tmp), PHASE="test", ACTOR="tm", REPO="Team-C01/NeighborCare"):
            (Path(tmp) / "state.json").write_text(json.dumps(a.state_for(ctx)))
            (Path(tmp) / "report.md").write_text("Test gia adeguati")
            (Path(tmp) / "changes.patch").write_text("")
            with patch.dict(a.os.environ, {"GITHUB_RUN_ID": "124"}), \
                 patch.object(a, "context", return_value=ctx), patch.object(a, "checkout"), \
                 patch.object(a, "git") as git, patch.object(a, "dispatch_ci") as dispatch, \
                 patch.object(a, "complete_testing") as complete:
                a.publish()
            git.assert_not_called()
            dispatch.assert_not_called()
            self.assertIn("Nessuna modifica proposta", complete.call_args.args[3])
            self.assertIn("Fase avviata da: @tm", complete.call_args.args[3])
            self.assertFalse(complete.call_args.args[4])

    def test_tester_reuses_current_ci_without_duplicate(self):
        run = {"id": 1, "html_url": "https://github.com/run", "status": "completed"}
        job = {"name": "repository-checks", "status": "completed", "conclusion": "success", "steps": []}
        with patch.object(a, "test_ci_run", return_value=run), \
             patch.object(a, "wait_for_test_ci", return_value=(run, None)), \
             patch.object(a, "dispatch_ci") as dispatch, \
             patch.object(a, "repo_api", return_value={"jobs": [job]}), \
             patch.object(a, "pages", return_value=[]):
            passed, message = a.testing_result(59, "b"*40, "branch", False)
        self.assertTrue(passed)
        dispatch.assert_not_called()
        self.assertIn("riutilizzata", message)
        self.assertIn("SUPERATA", message)

    def test_tester_executes_ci_once_and_reports_failure(self):
        run = {"id": 1, "html_url": "https://github.com/run", "status": "completed"}
        job = {"name": "repository-checks", "status": "completed", "conclusion": "failure",
               "steps": [{"name": "Build e test", "conclusion": "failure"}]}
        summary = {"user": {"login": "github-actions[bot]"}, "body":
                   "<!-- neighborcare-ci-summary -->\nCommit: `" + "b"*40 +
                   "`\n- Backend: 1 superati, 1 falliti/errori, 0 saltati\n- Test backend falliti: Example.TF_01\n[CI](https://github.com/r/actions/runs/1)"}
        with patch.object(a, "dispatch_ci", return_value="CI avviata") as dispatch, \
             patch.object(a, "wait_for_test_ci", return_value=(run, None)), \
             patch.object(a, "repo_api", return_value={"jobs": [job]}), \
             patch.object(a, "pages", return_value=[summary]), \
             patch.object(a, "comment") as comment, \
             patch.object(a, "dispatch_revision"):
            with self.assertRaises(ValueError):
                a.complete_testing(59, "b"*40, "branch", "Test scritti", True)
        dispatch.assert_called_once_with("branch")
        body = comment.call_args.args[1]
        self.assertIn("NON SUPERATA", body)
        self.assertIn("1 falliti/errori", body)
        self.assertIn("Build e test", body)
        self.assertIn("### Risultati dei test (JUnit)", body)
        self.assertIn("### Altri controlli CI", body)
        self.assertIn("Example.TF_01", body)

    def test_tester_rejects_outdated_commit(self):
        with patch.object(a, "repo_api", return_value={"state": "open", "head": {"sha": "c"*40}}):
            result, problem = a.wait_for_test_ci(59, "b"*40, "branch")
        self.assertIsNone(result)
        self.assertIn("commit cambiato", problem)

    def test_revision_dispatch_only_on_ready_current_commit(self):
        pr = {"state": "open", "draft": True, "head": {"sha": "b"*40}}
        with patch.object(a, "repo_api", return_value=pr), patch.object(a, "cmd") as call:
            a.dispatch_revision(59, "b"*40)
            call.assert_not_called()
            pr["draft"] = False
            a.dispatch_revision(59, "c"*40)
            call.assert_not_called()
            a.dispatch_revision(59, "b"*40)
            self.assertIn("revisione.yml", call.call_args.args)
            self.assertIn("pr_number=59", call.call_args.args)

    def test_ci_dispatch(self):
        with patch.object(a, "cmd", return_value="") as call:
            self.assertIn("CI avviata", a.dispatch_ci("agent/issue-1-implementazione"))
            self.assertIn("--ref", call.call_args.args)

    def test_ordinary_documentation_allowed(self):
        self.assertTrue(a.permitted_path("implementazione", "docs/guida.md", "A"))
        self.assertFalse(a.permitted_path("correzione", "docs/rad/uc/UC.md", "M"))

    def test_report_summary_survives_failed_and_missing_tests(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = os.getcwd()
            try:
                os.chdir(tmp)
                Path("backend/target/surefire-reports").mkdir(parents=True)
                Path("backend/target/surefire-reports/TEST-Failure.xml").write_text(
                    '<testsuite><testcase><failure/></testcase><testcase/></testsuite>')
                with patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": str(Path(tmp) / "summary"),
                                             "GITHUB_OUTPUT": str(Path(tmp) / "output")}), \
                     patch.object(v.sys, "argv", ["verify_reports.py", "--summary"]):
                    self.assertEqual(v.main(), 1)
                report = Path("summary").read_text()
                self.assertIn("| Backend | 1 | 1 | 0 |", report)
                self.assertIn("| Frontend | N/D | N/D | N/D |", report)
                self.assertIn("backend=1 superati, 1 falliti/errori, 0 saltati", Path("output").read_text())
            finally:
                os.chdir(original)

    def test_failed_test_names_are_reported_without_assertion_details(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "test.xml"
            report.write_text('<testsuite><testcase classname="Example" name="TF_01"><failure>secret assertion</failure></testcase><testcase name="TF_02"/><testcase classname="App" name="TF_03"><error/></testcase></testsuite>')
            names = v.failed_test_names([report])
            self.assertEqual(names, "Example.TF_01; App.TF_03")
            self.assertNotIn("secret assertion", names)

    def test_reports_count_skipped_and_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "report.xml"
            p.write_text('<testsuite><testcase classname="DatabaseIntegrationTest"><skipped/></testcase><testcase/><testcase><failure/></testcase></testsuite>')
            self.assertEqual(v.count_reports([p]), (2, 1, 1, True))

if __name__ == "__main__":
    unittest.main()

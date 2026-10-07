"""Regression tests for advisory freshness warnings and genuine failures."""

import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-freshness.py"


class FreshnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "docs").mkdir()
        (self.root / "docs" / "reference.md").write_text("Reference\n", encoding="utf-8")
        self.manifest = {
            "schema": 1,
            "default_review_interval_days": 30,
            "sources": [{
                "id": "nixpkgs-docs",
                "input": "nixpkgs",
                "url": "https://example.com/docs",
                "last_reviewed": "2000-01-01",
                "references": ["docs/reference.md"],
            }],
        }
        self.lock = {"nodes": {"nixpkgs": {"locked": {"rev": "current-revision"}}}}
        self.write_manifest()
        self.write_json("flake.lock", self.lock)

    def write_json(self, path, value):
        (self.root / path).write_text(json.dumps(value), encoding="utf-8")

    def write_manifest(self):
        self.write_json("docs/freshness-sources.json", self.manifest)

    def run_check(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *args],
            capture_output=True, text=True, check=False,
        )

    def test_overdue_review_warns_without_failing_or_mutating_inputs(self):
        manifest_before = (self.root / "docs/freshness-sources.json").read_bytes()
        lock_before = (self.root / "flake.lock").read_bytes()
        result = self.run_check("--github-warnings")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("::warning title=Documentation review due::nixpkgs-docs:", result.stderr)
        self.assertIn("due since 2000-01-31", result.stderr)
        self.assertIn("documentation nixpkgs-docs: due", result.stdout)
        self.assertEqual((self.root / "docs/freshness-sources.json").read_bytes(), manifest_before)
        self.assertEqual((self.root / "flake.lock").read_bytes(), lock_before)

    def test_warnings_preserve_json_and_summary(self):
        summary = self.root / "summary.md"
        result = self.run_check("--github-warnings", "--format", "json", "--github-summary", str(summary))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "attention")
        self.assertIn("review due", summary.read_text(encoding="utf-8"))
        self.assertIn("::warning", result.stderr)

    def test_current_review_does_not_warn(self):
        self.manifest["sources"][0]["last_reviewed"] = "9998-01-01"
        self.write_manifest()
        result = self.run_check("--github-warnings", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "current")
        self.assertEqual(result.stderr, "")

    def test_review_is_due_on_interval_boundary(self):
        today = dt.datetime.now(dt.timezone.utc).date()
        self.manifest["sources"][0]["last_reviewed"] = (today - dt.timedelta(days=30)).isoformat()
        self.write_manifest()
        result = self.run_check("--github-warnings")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"due since {today.isoformat()}", result.stderr)

    def test_candidate_drift_is_advisory(self):
        self.manifest["sources"][0]["last_reviewed"] = "9998-01-01"
        self.write_manifest()
        self.write_json("candidate.lock", {"nodes": {"nixpkgs": {"locked": {"rev": "new-revision"}}}})
        result = self.run_check("--github-warnings", "--candidate-lock", str(self.root / "candidate.lock"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("input drift nixpkgs: current-revision -> new-revision", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_invalid_manifest_still_fails(self):
        for value in ("not JSON", json.dumps({**self.manifest, "schema": 2})):
            with self.subTest(value=value):
                (self.root / "docs/freshness-sources.json").write_text(value, encoding="utf-8")
                result = self.run_check("--github-warnings")
                self.assertEqual(result.returncode, 2)
                self.assertIn("freshness error:", result.stderr)
                self.assertNotIn("::warning", result.stderr)

    def test_missing_reference_still_fails(self):
        (self.root / "docs/reference.md").unlink()
        result = self.run_check("--github-warnings")
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing reference", result.stderr)

    def test_invalid_current_or_candidate_lock_still_fails(self):
        self.write_json("invalid.lock", {"nodes": {}})
        for option in ("--lock", "--candidate-lock"):
            with self.subTest(option=option):
                result = self.run_check("--github-warnings", option, str(self.root / "invalid.lock"))
                self.assertEqual(result.returncode, 2)
                self.assertIn("missing locked input", result.stderr)

    def test_explicit_strict_modes_are_preserved(self):
        for option in ("--fail-on-due", "--fail-on-attention"):
            with self.subTest(option=option):
                result = self.run_check("--github-warnings", option)
                self.assertEqual(result.returncode, 2)
                self.assertIn("::warning", result.stderr)

    def test_warnings_are_opt_in(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")

    def test_warning_data_is_escaped(self):
        self.manifest["sources"][0]["id"] = "source%\r\n::error::injected"
        self.write_manifest()
        result = self.run_check("--github-warnings")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("source%25%0D%0A::error::injected", result.stderr)
        self.assertEqual(len(result.stderr.splitlines()), 1)


if __name__ == "__main__":
    unittest.main()

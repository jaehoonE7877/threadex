"""Regression checks for the package validator and isolated trial preparation."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


PLUGIN = Path(__file__).resolve().parents[1] / "plugins/threadex"
sys.path.insert(0, str(PLUGIN / "scripts"))
from prepare_behavior_eval import load_cases, prepare


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "plugin"
        shutil.copytree(PLUGIN, self.root, ignore=shutil.ignore_patterns("__pycache__"))

    def validate(self):
        env = dict(os.environ)
        env.pop("THREADEX_RELEASE_VERSION", None)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(self.root / "scripts/validate_threadex.py"), str(self.root)],
            capture_output=True, text=True, env=env,
        )

    def test_distributed_package_uses_inherited_settings(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_pinned_or_ineffective_agent_settings(self):
        path = self.root / "codex/agents/verifier.toml"
        original = path.read_text()
        for setting in ('model = "old-model"', 'model_reasoning_effort = "high"',
                        'sandbox_mode = "read-only"', 'approval_policy = "never"',
                        'model_provider = "other"', 'mcp_servers = {}'):
            with self.subTest(setting=setting):
                path.write_text(setting + "\n" + original)
                result = self.validate()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("must inherit host settings", result.stderr)

    def test_description_does_not_need_a_fixed_prefix(self):
        path = self.root / "skills/review/SKILL.md"
        text = path.read_text()
        description = next(line for line in text.splitlines() if line.startswith("description:"))
        path.write_text(text.replace(description, "description: Inspect diffs for regressions."))
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_empty_agent_contract_is_rejected(self):
        (self.root / "codex/agents/verifier.toml").write_text(
            'name = "verifier"\ndescription = "Audit a claim"\ndeveloper_instructions = ""\n'
        )
        self.assertNotEqual(self.validate().returncode, 0)

    def test_missing_asset_is_rejected(self):
        (self.root / "assets/threadex-icon.png").unlink()
        self.assertNotEqual(self.validate().returncode, 0)

    def test_missing_connected_evidence_reference_is_rejected(self):
        (self.root / "skills/verify/references/connected_evidence.md").unlink()
        self.assertNotEqual(self.validate().returncode, 0)

    def test_trial_skill_references_resolve(self):
        request = prepare(self.root, "connected_access_denied", self.base / "trial")
        skills = (request.parent / "skills").resolve()
        for entry in skills.glob("*/SKILL.md"):
            for relative in re.findall(r"\]\(([^)]+\.md)\)", entry.read_text()):
                if "://" in relative:
                    continue
                target = (entry.parent / relative).resolve()
                self.assertTrue(target.is_relative_to(skills), relative)
                self.assertTrue(target.is_file(), relative)
                original = self.root / "skills" / target.relative_to(skills)
                self.assertEqual(target.read_bytes(), original.read_bytes())

    def test_release_version_mismatch_is_rejected(self):
        env = dict(os.environ, THREADEX_RELEASE_VERSION="99.0.0", PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run(
            [sys.executable, str(self.root / "scripts/validate_threadex.py"), str(self.root)],
            capture_output=True, text=True, env=env,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must match THREADEX_RELEASE_VERSION", result.stderr)

    def test_trial_has_raw_inputs_but_no_expected_answers(self):
        request = prepare(self.root, "review_and_fix", self.base / "trial")
        case = next(case for case in load_cases(self.root) if case["id"] == "review_and_fix")
        text = request.read_text()
        self.assertIn(case["prompt"], text)
        for check in case["checks"]:
            self.assertNotIn(check, text)
        self.assertFalse((request.parent / "smoke").exists())
        for name, content in case["files"].items():
            self.assertEqual((request.parent / "workspace" / name).read_text(), content)

    def test_existing_trial_is_never_overwritten(self):
        output = self.base / "trial"
        prepare(self.root, "review_and_fix", output)
        source = output / "workspace/checkout.py"
        source.write_text("user changes\n")
        with self.assertRaises(FileExistsError):
            prepare(self.root, "review_and_fix", output)
        self.assertEqual(source.read_text(), "user changes\n")

    def test_trials_are_independent(self):
        first, second = self.base / "first", self.base / "second"
        prepare(self.root, "review_and_fix", first)
        prepare(self.root, "review_and_fix", second)
        (first / "workspace/checkout.py").write_text("changed\n")
        self.assertNotEqual((first / "workspace/checkout.py").read_text(),
                            (second / "workspace/checkout.py").read_text())

    def test_fixture_paths_cannot_escape_workspace(self):
        path = self.root / "smoke/behavior_cases.json"
        data = json.loads(path.read_text())
        for name in ("../outside", "/tmp/outside", ".agents/skills/injected.md", "a/../b"):
            with self.subTest(name=name):
                data["cases"][0]["files"] = {name: "content"}
                path.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    load_cases(self.root)

    def test_duplicate_case_ids_are_rejected(self):
        path = self.root / "smoke/behavior_cases.json"
        data = json.loads(path.read_text())
        data["cases"].append(data["cases"][0])
        path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            load_cases(self.root)

    def test_unknown_case_and_in_package_output_are_rejected(self):
        with self.assertRaises(ValueError):
            prepare(self.root, "unknown", self.base / "trial")
        with self.assertRaises(ValueError):
            prepare(self.root, "review_only", self.root / "trial")


if __name__ == "__main__":
    unittest.main()

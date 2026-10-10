"""Exercise setup orchestration without downloading skills or changing the user's Codex profile."""

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import setup_codex as setup
from build_codex import ROOT


class CodexSetupTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="codex-onboarding-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.project = self.root / "designer project"
        self.project.mkdir()

    def test_setup_installs_then_launches_in_project(self):
        calls = []

        def command(args, **kwargs):
            calls.append((args, kwargs))
            return subprocess.CompletedProcess(args, 0, '{"marketplaces": []}')

        with patch.object(setup.shutil, "which", return_value="/tools/codex"), \
             patch.object(setup.subprocess, "run", side_effect=command), \
             patch.object(setup, "prepare_marketplace", return_value=self.root / "marketplace"), \
             patch.object(setup, "connect_figma") as figma, \
             contextlib.redirect_stdout(io.StringIO()), \
             patch.object(setup.sys.stdin, "isatty", return_value=True), \
             patch.object(setup.sys.stdout, "isatty", return_value=True):
            self.assertEqual(setup.main(["--project", str(self.project)]), 0)
        install = calls[1][0]
        self.assertIn("--target", install)
        self.assertEqual(install[install.index("--target") + 1], "codex")
        figma.assert_called_once_with("/tools/codex", self.project)
        self.assertEqual(calls[-1][0][:3], ["/tools/codex", "-C", str(self.project)])
        self.assertEqual(calls[-1][1]["cwd"], self.project)
        self.assertIn("start-design", calls[-1][0][-1])
        self.assertIn("SETUP.md", calls[-1][0][-1])

    def test_mandatory_failure_never_launches(self):
        calls = []

        def command(args, **kwargs):
            calls.append(args)
            return subprocess.CompletedProcess(args, 0 if "--help" in args else 9)

        with patch.object(setup.shutil, "which", return_value="codex"), \
             patch.object(setup.subprocess, "run", side_effect=command), \
             patch.object(setup, "prepare_marketplace") as build, \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(setup.main(["--project", str(self.project)]), 1)
            build.assert_not_called()
        self.assertEqual(len(calls), 2)

    def test_no_launch_can_defer_companions_and_figma(self):
        with patch.object(setup.shutil, "which", return_value="codex"), \
             patch.object(setup.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, '{"marketplaces": []}')) as run, \
             patch.object(setup, "prepare_marketplace", return_value=self.root), \
             patch.object(setup, "connect_figma") as figma, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            result = setup.main(["--project", str(self.project), "--no-launch", "--skip-companions", "--skip-figma"])
        self.assertEqual(result, 0)
        self.assertEqual(run.call_count, 4)  # preflight, list, marketplace, plugin
        figma.assert_not_called()
        self.assertIn("Next:", output.getvalue())
        self.assertIn(str(self.project), output.getvalue())

    def test_release_reuse_and_local_edit_protection(self):
        with patch.object(setup, "ROOT", self.root):
            root = setup.prepare_marketplace()
            catalog = root / ".agents/plugins/marketplace.json"
            package = root / json.loads(catalog.read_text())["plugins"][0]["source"]["path"]
            version = json.loads((package / "plugin.json").read_text())["version"]
            self.assertIn("+", version)
            self.assertTrue((package / "skills/design-context-setup/references/scaffold-map.md").is_file())
            self.assertTrue((package / "skills/design-context-setup/LICENSE").is_file())
            setup.prepare_marketplace()
            edited = package / "CODEX_RUNTIME.md"
            edited.write_text("local customization")
            with self.assertRaises(RuntimeError):
                setup.prepare_marketplace()
            self.assertEqual(edited.read_text(), "local customization")

    def test_printed_launch_preserves_custom_codex_profile(self):
        profile = self.root / "codex cli only"
        with patch.dict(os.environ, {"CODEX_HOME": str(profile)}), \
             patch.object(setup.shutil, "which", return_value="codex"), \
             patch.object(setup.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, '{"marketplaces": []}')), \
             patch.object(setup, "prepare_marketplace", return_value=self.root), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(setup.main(["--project", str(self.project), "--no-launch", "--skip-companions", "--skip-figma"]), 0)
        import shlex
        command = shlex.split(output.getvalue().split("Next: ", 1)[1])
        self.assertEqual(command[:3], ["env", "CODEX_HOME=" + str(profile), "codex"])

    def test_figma_failure_does_not_print_token(self):
        token = "figd_fake_test_only"
        with patch.object(setup.shutil, "which", return_value="npx"), \
             patch.object(setup.getpass, "getpass", return_value=token), \
             patch.object(setup.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, token, token)), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            setup.connect_figma("codex", self.project)
        self.assertNotIn(token, output.getvalue())
        self.assertIn("failed", output.getvalue())

    def test_existing_figma_is_not_overwritten(self):
        with patch.object(setup.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as run, \
             patch.object(setup.getpass, "getpass") as prompt, contextlib.redirect_stdout(io.StringIO()):
            setup.connect_figma("codex", self.project)
        self.assertEqual(run.call_count, 1)
        prompt.assert_not_called()

    def test_duplicate_skills_backup_keeps_edits(self):
        skill = self.project / ".agents/skills/start-design"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("customized skill")
        with patch.object(setup.sys.stdin, "isatty", return_value=True), \
             patch("builtins.input", return_value="y"), contextlib.redirect_stdout(io.StringIO()):
            setup.migrate_copies(self.project)
        self.assertFalse(skill.exists())
        saved = list((self.project / ".design-stuff-kit-backup").glob("*/start-design/SKILL.md"))
        self.assertEqual(saved[0].read_text(), "customized skill")

    def test_launcher_propagates_failure_exit_status(self):
        fake = self.root / "codex"
        fake.write_text("#!/bin/sh\nexit 7\n")
        fake.chmod(0o755)
        result = subprocess.run([sys.executable, str(ROOT / "start-codex"), "--project", str(self.project)],
                                env={**os.environ, "PATH": str(self.root)}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Setup stopped", result.stderr)
        self.assertFalse((self.project / ".agents").exists())

    def test_marketplace_migration_rolls_back_on_failure(self):
        old = self.root / "old checkout"
        catalog = old / ".agents/plugins/marketplace.json"
        catalog.parent.mkdir(parents=True)
        catalog.write_text(json.dumps({"name": setup.MARKETPLACE, "plugins": [{"name": "design-stuff-kit"}]}))
        listing = json.dumps({"marketplaces": [{"name": setup.MARKETPLACE, "root": str(old),
                            "marketplaceSource": {"sourceType": "local", "source": str(old)}}]})
        calls = []

        def command(args, **kwargs):
            calls.append(args)
            if args[-1] == str(self.root / "new checkout"):
                return subprocess.CompletedProcess(args, 1)
            return subprocess.CompletedProcess(args, 0, listing)

        with patch.object(setup.subprocess, "run", side_effect=command), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(RuntimeError):
                setup.register_marketplace("codex", self.root / "new checkout", self.project)
        self.assertEqual(calls[-1], ["codex", "plugin", "marketplace", "add", str(old)])
        self.assertTrue(catalog.exists())

    def test_custom_marketplace_is_never_removed(self):
        old = self.root / "custom"
        catalog = old / ".agents/plugins/marketplace.json"
        catalog.parent.mkdir(parents=True)
        catalog.write_text(json.dumps({"name": setup.MARKETPLACE, "plugins": [{"name": "other-plugin"}]}))
        listing = json.dumps({"marketplaces": [{"name": setup.MARKETPLACE, "root": str(old),
                            "marketplaceSource": {"sourceType": "local", "source": str(old)}}]})
        with patch.object(setup.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, listing)) as run:
            with self.assertRaises(RuntimeError):
                setup.register_marketplace("codex", self.root / "new", self.project)
        self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()

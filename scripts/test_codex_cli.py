"""Opt-in real CLI checks: DESIGN_KIT_TEST_CODEX_CLI=1 python3 -m unittest discover -s scripts -p 'test*codex*.py'."""

import contextlib
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import setup_codex as setup


@unittest.skipUnless(os.environ.get("DESIGN_KIT_TEST_CODEX_CLI") == "1", "opt-in real Codex CLI test")
class CodexCliTests(unittest.TestCase):
    def test_install_repeat_and_upgrade_in_isolated_profile(self):
        codex = shutil.which("codex")
        self.assertIsNotNone(codex, "Install Codex CLI to run this check")
        with tempfile.TemporaryDirectory(prefix="kit-cli-test-") as temporary:
            root = Path(temporary).resolve()
            project = root / "design project"
            project.mkdir()
            profile = root / "isolated profile"
            profile.mkdir()
            checkout = root / "kit checkout"
            (checkout / "skills").mkdir(parents=True)
            (checkout / "codex/skills").mkdir(parents=True)
            legacy = project / "CLAUDE.md"
            legacy.write_text("Existing design decisions\n")
            progress = project / "SETUP.md"
            progress.write_text("## Decided against\n- No Rive work\n")
            options = ["--project", str(project), "--no-launch", "--skip-companions", "--skip-figma"]
            populate = setup.populate

            def updated_package(destination):
                populate(destination)
                with (destination / "CODEX_RUNTIME.md").open("a") as stream:
                    stream.write("\nCLI upgrade fixture.\n")

            def installed():
                result = subprocess.run([codex, "plugin", "list", "--json", "--marketplace", setup.MARKETPLACE],
                                        cwd=project, capture_output=True, text=True, check=True, timeout=30)
                entries = json.loads(result.stdout)["installed"]
                self.assertEqual(len(entries), 1)
                self.assertTrue(entries[0]["enabled"])
                return entries[0]

            with patch.dict(os.environ, {"CODEX_HOME": str(profile)}), patch.object(setup, "ROOT", checkout), \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(setup.main(options), 0)
                first = installed()
                self.assertEqual(setup.main(options), 0)
                self.assertEqual(installed()["version"], first["version"])
                with patch.object(setup, "populate", side_effect=updated_package):
                    self.assertEqual(setup.main(options), 0)
                latest = installed()
                self.assertNotEqual(latest["version"], first["version"])

            cached = profile / "plugins/cache" / setup.MARKETPLACE / "design-stuff-kit" / latest["version"]
            self.assertTrue((cached / "skills/start-design/SKILL.md").is_file())
            self.assertIn("CLI upgrade fixture", (cached / "CODEX_RUNTIME.md").read_text())
            self.assertEqual(len(list((cached / "skills").glob("*/SKILL.md"))), 21)
            self.assertEqual(legacy.read_text(), "Existing design decisions\n")
            self.assertEqual(progress.read_text(), "## Decided against\n- No Rive work\n")
            self.assertEqual(sorted(p.name for p in project.iterdir()), ["CLAUDE.md", "SETUP.md"])


if __name__ == "__main__":
    unittest.main()

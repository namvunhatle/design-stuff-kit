"""Offline package and installer regression tests: python3 -m unittest discover -s scripts -p 'test_codex.py'."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from build_codex import ROOT, build, inventory, marketplace


class CodexPackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="codex-kit-test-")
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(self.temporary.name)
        self.package = build(self.work / "package with spaces")

    def run_script(self, script, *args, success=True):
        result = subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def test_relocatable_package_and_license(self):
        original = ROOT / "skills" / "content-research-writer"
        self.assertEqual(inventory(original), inventory(self.package / "skills" / original.name))
        manifest = json.loads((self.package / "plugin.json").read_text())
        onboarding = manifest["extensions"]["com.openai"]["onboardingSkill"]
        self.assertTrue((self.package / onboarding).is_file())
        for skill in (self.package / "skills").glob("*/SKILL.md"):
            content = skill.read_text()
            self.assertTrue(content.startswith("---\n"), skill)
            self.assertIn("\nname: " + skill.parent.name + "\n", content)
            self.assertIn("\ndescription: ", content)
            self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", content)
            self.assertNotIn("/design-stuff-kit:", content)
            if skill.parent.name != "content-research-writer":
                self.assertTrue((skill.parent / "../../CODEX_RUNTIME.md").is_file())
        catalog = json.loads(marketplace(self.package).read_text())
        self.assertEqual((self.work / catalog["plugins"][0]["source"]["path"]).resolve(), self.package.resolve())

    def test_build_repeat_and_edit_protection(self):
        before = inventory(self.package)
        build(self.package)
        self.assertEqual(before, inventory(self.package))
        local = self.package / "CODEX_RUNTIME.md"
        local.write_text("local edit")
        with self.assertRaises(ValueError):
            build(self.package)
        self.assertEqual(local.read_text(), "local edit")

    def test_zip_preserves_layout_and_executable_helpers(self):
        output, archive = self.work / "zip package", self.work / "kit.zip"
        self.run_script(ROOT / "scripts/build_codex.py", "--output", output, "--zip", archive)
        with ZipFile(archive) as package:
            self.assertIn("plugin.json", package.namelist())
            self.assertIn(".codex-plugin/plugin.json", package.namelist())
            self.assertTrue(package.getinfo("bin/wx-init").external_attr >> 16 & 0o111)
        self.run_script(ROOT / "scripts/build_codex.py", "--output", output, "--zip", archive, success=False)

    def test_helper_runs_outside_package_without_overwrite(self):
        project = self.work / "design project"
        project.mkdir()
        command = [str(self.package / "bin/wx-init"), "explore/onboarding", "--wireframe"]
        result = subprocess.run(command, cwd=project, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        html = project / "explore/onboarding/explore.html"
        self.assertIn('data-mode="wireframe"', html.read_text())
        html.write_text("user's edited prototype")
        subprocess.run(command, cwd=project, check=True, capture_output=True)
        self.assertEqual(html.read_text(), "user's edited prototype")

    def test_companion_targets_and_existing_files(self):
        upstream = self.work / "upstream"
        for name in ("ux-designer", "ui-designer", "ux-copywriter", "interactive-prototype", "figma-console-api"):
            skill = upstream / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Fixture skill\n---\n")
        for target, directory in (("claude", ".claude"), ("codex", ".agents")):
            project = self.work / target
            project.mkdir()
            arguments = ["--project", project, "--upstream-dir", upstream]
            if target == "codex":
                arguments += ["--target", "codex"]
            self.run_script(self.package / "scripts/assemble.py", *arguments)
            installed = project / directory / "skills/ux-designer/SKILL.md"
            self.assertTrue(installed.is_file())
            self.assertFalse((project / (".claude" if target == "codex" else ".agents")).exists())
            installed.write_text("user customization")
            self.run_script(self.package / "scripts/assemble.py", *arguments)
            self.assertEqual(installed.read_text(), "user customization")
            # All installed skills skip the downloader, even without gdown.
            result = self.run_script(self.package / "scripts/install.py", "--project", project, "--target", target, "--gdown", "nonexistent-gdown-test")
            self.assertIn("Nothing to download", result.stdout)
        self.run_script(self.package / "scripts/install.py", "--project", self.work / "codex", "--target", "codex", "--with-rules", success=False)


if __name__ == "__main__":
    unittest.main()

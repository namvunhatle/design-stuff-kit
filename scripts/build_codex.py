#!/usr/bin/env python3
"""Build a relocatable Codex plugin from the shared Claude edition (no network)."""

import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist" / "codex" / "design-stuff-kit"
COPIED_DIRS = ("skills", "agents", "rules", "templates", "bin")
COPIED_FILES = ("LICENSE", "THIRD_PARTY.md", "CHANGELOG.md", "external-skills.json", "upstream-packages.json")


def adapt(text):
    """Translate host syntax only; keep upstream URLs and attribution intact."""
    for old, new in (
        ("${CLAUDE_PLUGIN_ROOT}", "${KIT_ROOT}"),
        (".claude/skills/", ".agents/skills/"),
        ("`CLAUDE.md`", "`AGENTS.md`"),
        ("/design-stuff-kit:", "$"),
        ("SendMessage in Claude Code", "the available Codex agent continuation tool"),
        ("claude mcp add --transport http rive http://127.0.0.1:9791/mcp",
         "codex mcp add rive --url http://127.0.0.1:9791/mcp"),
        ("are on the PATH in Claude Code", "must be run by absolute path or added to PATH for the current shell call"),
    ):
        text = text.replace(old, new)
    return text


def inject_runtime(text):
    head, body = text[4:].split("\n---", 1)
    return "---\n" + head + "\n---\n\nRead [Codex runtime guidance](../../CODEX_RUNTIME.md) before this workflow.\n" + body


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def populate(output):
    for directory in COPIED_DIRS:
        shutil.copytree(ROOT / directory, output / directory,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", "node_modules"))
    for name in COPIED_FILES:
        shutil.copy2(ROOT / name, output / name)
    (output / "scripts").mkdir()
    for name in ("assemble.py", "install.py"):
        shutil.copy2(ROOT / "scripts" / name, output / "scripts" / name)
    (output / "docs").mkdir()
    shutil.copy2(ROOT / "docs" / "CODEX.md", output / "docs" / "CODEX.md")
    shutil.copy2(ROOT / "docs" / "FIGMA_SETUP_CODEX.md", output / "docs" / "FIGMA_SETUP_CODEX.md")

    # Codex overrides may include additional onboarding skills and references.
    for skill in (ROOT / "codex" / "skills").iterdir():
        if skill.is_dir():
            shutil.copytree(skill, output / "skills" / skill.name, dirs_exist_ok=True)
    for source in (ROOT / "commands").glob("*.md"):
        front, body = source.read_text(encoding="utf-8")[4:].split("\n---", 1)
        description = re.search(r"^description: (.+)$", front, re.M).group(1)
        target = output / "skills" / source.stem / "SKILL.md"
        target.parent.mkdir()
        body = body.replace("$ARGUMENTS", "the feature/path and options in the user's request")
        target.write_text(f"---\nname: {source.stem}\ndescription: {description}\n---\n{body}", encoding="utf-8")

    for directory in COPIED_DIRS:
        for path in (output / directory).rglob("*.md"):
            # This Apache-licensed upstream skill is retained byte-for-byte.
            if "content-research-writer" in path.parts:
                continue
            text = adapt(path.read_text(encoding="utf-8"))
            if directory == "agents" and text.startswith("---\n"):
                text = text[4:].split("\n---", 1)[1].lstrip()
            if path.name == "SKILL.md" and directory == "skills":
                text = inject_runtime(text)
            path.write_text(text, encoding="utf-8")

    # Remove misleading host loading claims from the Codex rule templates.
    explore = output / "rules" / "explore.md"
    text = explore.read_text(encoding="utf-8")[4:].split("\n---", 1)[1].lstrip()
    text = re.sub(r"Loads only when Claude.*?first file\.",
                  "Apply these instructions to web exploration work. To activate them in Codex, merge them into explore/AGENTS.md.",
                  text, flags=re.S)
    explore.write_text(text, encoding="utf-8")
    memory = output / "rules" / "project-memory.md"
    text = memory.read_text(encoding="utf-8")
    text = re.sub(r"^- \*\*Do not split.*$", "- Keep detailed context in supporting files and read it when relevant.", text, flags=re.M)
    text = re.sub(r"^- \*\*Nested product folders.*$", "- Read the target product's applicable AGENTS.md and current memory files before working on that product; refresh relevant context after compaction.", text, flags=re.M)
    memory.write_text(text, encoding="utf-8")

    shutil.copy2(ROOT / "codex" / "runtime.md", output / "CODEX_RUNTIME.md")
    original = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    identity = {key: original[key] for key in ("name", "version", "description", "author", "homepage", "repository", "license", "keywords")}
    identity["version"] = (ROOT / "codex" / "version.txt").read_text().strip()
    interface = {"displayName": "Design Stuff Kit", "shortDescription": "Product design workflows for Codex", "category": "Productivity"}
    write_json(output / "plugin.json", {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        **identity,
        "extensions": {"com.openai": {"interface": interface, "onboardingSkill": "./skills/start-design/SKILL.md"}},
    })
    write_json(output / ".codex-plugin" / "plugin.json", {
        **identity, "skills": "./skills/", "interface": interface,
        "extensions": {"com.openai": {"onboardingSkill": "./skills/start-design/SKILL.md"}},
    })


def inventory(root):
    return {str(p.relative_to(root)): (hashlib.sha256(p.read_bytes()).hexdigest(), bool(p.stat().st_mode & 0o111))
            for p in root.rglob("*") if p.is_file()}


def build(output):
    # Build before touching the destination; never overwrite a user's edited package.
    with tempfile.TemporaryDirectory(prefix="design-stuff-kit-codex-") as temporary:
        staged = Path(temporary) / "plugin"
        staged.mkdir()
        populate(staged)
        if output.exists():
            if not output.is_dir() or any(p.is_symlink() for p in output.rglob("*")) or output.is_symlink() or inventory(output) != inventory(staged):
                raise ValueError(f"Output exists with different content: {output}. Use --output with a new directory, then update your marketplace path.")
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(staged, output)
    return output


def marketplace(output):
    path = output.parent / ".agents" / "plugins" / "marketplace.json"
    data = {
        "name": "design-stuff-kit-local",
        "interface": {"displayName": "Design Stuff Kit Local"},
        "plugins": [{
            "name": "design-stuff-kit",
            "source": {"source": "local", "path": "./" + output.name},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        }],
    }
    if path.exists() and json.loads(path.read_text(encoding="utf-8")) != data:
        raise ValueError(f"Marketplace exists with different content: {path}. Merge it manually.")
    write_json(path, data)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Plugin directory; existing differing content is never overwritten")
    parser.add_argument("--zip", dest="zip_path", type=Path, help="Also create an installable ZIP at a new path")
    parser.add_argument("--marketplace", action="store_true", help="Create a local marketplace in the output's parent directory")
    args = parser.parse_args()
    if args.zip_path and args.zip_path.expanduser().exists():
        parser.error("ZIP destination already exists; choose a new path")
    try:
        output = build(args.output.expanduser().absolute())
        if args.marketplace:
            print(f"Marketplace: {marketplace(output)}")
        if args.zip_path:
            archive = args.zip_path.expanduser().absolute()
            if archive.is_relative_to(output):
                parser.error("ZIP destination must be outside the plugin directory")
            archive.parent.mkdir(parents=True, exist_ok=True)
            with ZipFile(archive, "x", ZIP_DEFLATED) as package:
                for path in sorted(output.rglob("*")):
                    if path.is_file():
                        package.write(path, str(path.relative_to(output)))
            print(f"ZIP: {archive}")
    except ValueError as exc:
        parser.error(str(exc))
    print(f"Built {len(list((output / 'skills').glob('*/SKILL.md')))} skills: {output}")
    print("Build only: not installed or enabled. See docs/CODEX.md for local marketplace setup.")


if __name__ == "__main__":
    main()

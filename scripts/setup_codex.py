"""One-command Codex setup, matching the Claude edition's start workflow."""

import argparse
import getpass
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from .build_codex import ROOT, inventory, populate, write_json
except ImportError:
    from build_codex import ROOT, inventory, populate, write_json

MARKETPLACE = "design-stuff-kit-local"
SELECTOR = "design-stuff-kit@" + MARKETPLACE
PROMPT = ("Use the Design Stuff Kit start-design skill to onboard this project now. "
          "If context is missing, run the bundled design-context-setup interview, one question at a time. "
          "If SETUP.md already exists, resume it. Then help choose rules and begin my first design task. "
          "Use my language and do not invent product facts.")


def run(command, **kwargs):
    result = subprocess.run(command, **kwargs)
    if result.returncode:
        raise RuntimeError(f"Setup step failed (exit {result.returncode}): {shlex.join(map(str, command))}")
    return result


def prepare_marketplace():
    """Keep releases immutable; refresh only the catalog entry owned by this launcher."""
    root = ROOT / "dist" / "codex-setup"
    catalog = root / ".agents/plugins/marketplace.json"
    if catalog.exists():
        previous = json.loads(catalog.read_text())
        if previous.get("name") != MARKETPLACE or [p.get("name") for p in previous.get("plugins", [])] != ["design-stuff-kit"]:
            raise RuntimeError(f"Custom marketplace at {catalog}; refusing to replace it.")
    with tempfile.TemporaryDirectory(prefix="design-kit-setup-") as temporary:
        staged = Path(temporary) / "plugin"
        staged.mkdir()
        populate(staged)
        digest = hashlib.sha256(json.dumps(inventory(staged), sort_keys=True).encode()).hexdigest()[:16]
        # Distinct versions prevent clients from reusing an old cached onboarding skill.
        for relative in ("plugin.json", ".codex-plugin/plugin.json"):
            path = staged / relative
            manifest = json.loads(path.read_text())
            manifest["version"] += "+" + digest
            write_json(path, manifest)
        target = root / ("design-stuff-kit-" + digest)
        if target.exists():
            if target.is_symlink() or any(p.is_symlink() for p in target.rglob("*")) or inventory(target) != inventory(staged):
                raise RuntimeError(f"Generated package has local edits: {target}; preserve them before retrying.")
        else:
            root.mkdir(parents=True, exist_ok=True)
            shutil.copytree(staged, target)
    write_json(catalog, {
        "name": MARKETPLACE,
        "interface": {"displayName": "Design Stuff Kit Local"},
        "plugins": [{"name": "design-stuff-kit",
                     "source": {"source": "local", "path": "./" + target.name},
                     "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                     "category": "Productivity"}],
    })
    return root


def connect_figma(codex, project):
    for name in ("figma-console", "figma_console"):
        result = subprocess.run([codex, "mcp", "get", name], cwd=project, capture_output=True, text=True)
        if result.returncode == 0:
            print("Figma Console is configured. Onboarding will verify that it is connected.")
            return
    if not shutil.which("npx"):
        print("Figma setup skipped: install Node.js, then rerun ./start-codex.")
        return
    print("\nConnect Figma Console? Paste a Figma personal access token below, or press Return to skip.")
    print("The token is stored in your local Codex user configuration, not in this project. See docs/FIGMA_SETUP_CODEX.md.")
    token = getpass.getpass("Figma token (hidden): ").strip()
    if not token:
        print("Skipped Figma; onboarding can continue without it.")
        return
    if not token.startswith("figd_"):
        print("Unrecognized token format; Figma was not configured. Rerun setup to retry.")
        return
    # Never echo command arguments or subprocess output here: either could contain the token.
    result = subprocess.run([codex, "mcp", "add", "figma-console", "--env", "FIGMA_ACCESS_TOKEN=" + token,
                             "--env", "ENABLE_MCP_APPS=true", "--", "npx", "-y", "figma-console-mcp@latest"],
                            cwd=project, capture_output=True, text=True)
    if result.returncode:
        print("Figma configuration failed. No token or command output is printed. See docs/FIGMA_SETUP_CODEX.md to retry.")
        return
    print("Figma Console configured. In Figma Desktop, import ~/.figma-console-mcp/plugin/manifest.json")
    print("after the connector first starts, run the Desktop Bridge plugin, and leave its window open.")


def register_marketplace(codex, source, project):
    result = run([codex, "plugin", "marketplace", "list", "--json"], cwd=project, capture_output=True, text=True)
    entries = json.loads(result.stdout)["marketplaces"]
    existing = next((item for item in entries if item.get("name") == MARKETPLACE), None)
    old_source = None
    if existing:
        old_source = existing.get("marketplaceSource", {}).get("source")
        if not old_source or existing.get("marketplaceSource", {}).get("sourceType") != "local":
            raise RuntimeError(f"Existing {MARKETPLACE} is not a managed local source; update it manually.")
        if Path(old_source).resolve() == source.resolve():
            return
        catalog = Path(existing["root"]) / ".agents/plugins/marketplace.json"
        data = json.loads(catalog.read_text())
        if data.get("name") != MARKETPLACE or [p.get("name") for p in data.get("plugins", [])] != ["design-stuff-kit"]:
            raise RuntimeError(f"Existing {MARKETPLACE} contains custom entries; refusing to replace it.")
        print(f"Updating this kit's marketplace source from {old_source} to {source}.")
        run([codex, "plugin", "marketplace", "remove", MARKETPLACE], cwd=project)
    try:
        run([codex, "plugin", "marketplace", "add", str(source)], cwd=project)
    except (RuntimeError, OSError):
        if old_source:
            run([codex, "plugin", "marketplace", "add", old_source], cwd=project)
            print("Restored the previous marketplace source.")
        raise


def migrate_copies(project):
    skills = project / ".agents/skills"
    names = {p.name for parent in (ROOT / "skills", ROOT / "codex/skills") for p in parent.iterdir() if (p / "SKILL.md").is_file()}
    names.update(("render", "design-review"))
    found = [skills / name for name in sorted(names) if (skills / name).exists()]
    if not found:
        return
    print("\nProject skills with the same names as plugin skills:")
    for path in found:
        print("  " + str(path.relative_to(project)))
    if not sys.stdin.isatty() or input("Move these copies into a backup, preserving local edits? [y/N] ").strip().lower() != "y":
        print("Kept existing copies. Choose Design Stuff Kit's plugin entry if the skill picker shows duplicates.")
        return
    backup = project / ".design-stuff-kit-backup"
    backup.mkdir(exist_ok=True)
    destination = Path(tempfile.mkdtemp(prefix="skills-", dir=backup))
    for path in found:
        shutil.move(str(path), destination / path.name)
    print("Saved copies at " + str(destination))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Design project (default: current working directory)")
    parser.add_argument("--no-launch", action="store_true", help="Prepare setup without opening Codex")
    parser.add_argument("--skip-figma", action="store_true", help="Skip the optional Figma token prompt")
    parser.add_argument("--skip-companions", action="store_true", help="Defer the five optional Yummy Labs downloads")
    parser.add_argument("--gdown", default="gdown", help="Downloader executable for companion skills")
    args = parser.parse_args(argv)
    if sys.version_info < (3, 10):
        parser.error("Python 3.10 or newer is required")
    project = args.project.expanduser().resolve()
    if not project.is_dir() or project == ROOT or ROOT in project.parents:
        parser.error("Choose an existing design project outside the kit folder")
    codex = shutil.which("codex")
    if not codex:
        parser.error("Install Codex CLI and sign in first, then rerun ./start-codex")
    profile = Path(os.environ.get("CODEX_HOME") or "~/.codex").expanduser().resolve()
    print(f"Codex profile: {profile}", flush=True)
    try:
        # Fail before downloads/project mutations if this CLI cannot install plugins.
        run([codex, "plugin", "add", "--help"], capture_output=True, text=True)
        if not args.skip_companions:
            print("Installing/checking the five Yummy Labs companion skills…", flush=True)
            run([sys.executable, str(ROOT / "scripts/install.py"), "--target", "codex", "--project", str(project),
                 "--gdown", args.gdown, "--venv", str(ROOT / ".venv")])
        else:
            print("Companion downloads deferred; the bundled context interview is still available.")
        source = prepare_marketplace()
        register_marketplace(codex, source, project)
        run([codex, "plugin", "add", SELECTOR], cwd=project)
        migrate_copies(project)
        if not args.skip_figma and sys.stdin.isatty():
            connect_figma(codex, project)
        elif not args.skip_figma:
            print("Figma token prompt skipped without a terminal; rerun interactively or see docs/FIGMA_SETUP_CODEX.md.")
        print("\nSetup is ready. Onboarding will resume SETUP.md or begin the context interview.")
        launch = [codex, "-C", str(project), "-c", f'plugins."{SELECTOR}".enabled=true', PROMPT]
        if args.no_launch or not (sys.stdin.isatty() and sys.stdout.isatty()):
            # Preserve the selected profile when this command is pasted into
            # another terminal with different shell initialization.
            print("Next: " + shlex.join(["env", "CODEX_HOME=" + str(profile), *launch]))
            return 0
        print("Opening Codex onboarding…", flush=True)
        return subprocess.run(launch, cwd=project).returncode
    except (RuntimeError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        print("Setup stopped. Completed steps are kept; fix the error and rerun to resume.", file=sys.stderr)
        return 1

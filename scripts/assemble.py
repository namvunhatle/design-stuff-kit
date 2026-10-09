#!/usr/bin/env python3
"""Install the Yummy Labs skills the design workflow needs into a Claude Code project.

The kit's own skills, agents, and commands come from the design-stuff-kit plugin, not from here.
"""

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Dict, Optional


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = json.loads((ROOT / "external-skills.json").read_text(encoding="utf-8"))
EXTERNAL_BY_NAME = {item["name"]: item for item in EXTERNAL}
# Upstream files that a bundled skill reads at run time.
REQUIRED_UPSTREAM_FILES = {
    "voice-tone-builder": "ux-copywriter/references/voice-tone-builder.md",
}


def name_from_skill(path: Path) -> Optional[str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    frontmatter = text.split("---", 2)[1]
    match = re.search(r"^name:\s*['\"]?([a-z0-9-]+)['\"]?\s*$", frontmatter, re.M)
    return match.group(1) if match else None


def reject_symlinks(path: Path) -> None:
    if path.is_symlink() or any(child.is_symlink() for child in path.rglob("*")):
        raise ValueError(f"Skill contains a symlink: {path}")


def copy_directory(source: Path, target: Path) -> str:
    reject_symlinks(source)
    if target.exists():
        return f"kept existing {target}"
    shutil.copytree(source, target)
    return f"installed {target}"


def find_upstream(root: Path) -> Dict[str, Path]:
    found = {}  # type: Dict[str, Path]
    for entry in root.rglob("SKILL.md"):
        name = name_from_skill(entry)
        if name not in EXTERNAL_BY_NAME:
            continue
        if name in found:
            raise ValueError(f"Multiple upstream copies found for {name}: {found[name]} and {entry}")
        found[name] = entry.parent
    return found


def repair_reference_paths(skill_dir: Path):
    """Move flat reference files into references/, where the author's SKILL.md expects them."""
    references = skill_dir / "references"
    content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    mentioned = set(re.findall(r"references/([A-Za-z0-9_.-]+\.md)", content))
    for flat in sorted(skill_dir.glob("*.md")):
        if flat.name == "SKILL.md" or flat.name.lower().startswith(("license", "notice")):
            continue
        # Leave a file where it is if SKILL.md links to it at the top level.
        if re.search(r"(?<![/\w])" + re.escape(flat.name), content):
            continue
        target = references / flat.name
        if not target.exists():
            references.mkdir(exist_ok=True)
            shutil.move(str(flat), str(target))
        elif target.read_bytes() == flat.read_bytes():
            flat.unlink()
    return sorted(name for name in mentioned if not (references / name).is_file())


def copy_optional_files(source_dir: Path, target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    for source in sorted(source_dir.glob("*.md")):
        target = target_dir / source.name
        if target.exists():
            print(f"kept existing {target}")
        else:
            shutil.copy2(source, target)
            print(f"installed {target}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path, help="Existing Claude Code project directory")
    parser.add_argument("--upstream-dir", type=Path, help="Folder containing skills extracted from the authors' downloads")
    parser.add_argument("--with-rules", "--with-rules-agents", dest="with_rules", action="store_true", help="Also copy the optional Claude Code rules")
    args = parser.parse_args()

    project = args.project.expanduser().resolve()
    if not project.is_dir():
        parser.error(f"Project directory does not exist: {project}")
    if args.upstream_dir and not args.upstream_dir.expanduser().is_dir():
        parser.error(f"Upstream directory does not exist: {args.upstream_dir}")

    dest = project / ".claude" / "skills"
    dest.mkdir(parents=True, exist_ok=True)
    upstream = find_upstream(args.upstream_dir.expanduser().resolve()) if args.upstream_dir else {}
    missing_reference_files = {}
    for name, source in sorted(upstream.items()):
        target = dest / name
        already_installed = target.exists()
        print(copy_directory(source, target))
        if not already_installed:
            missing_references = repair_reference_paths(target)
            if missing_references:
                missing_reference_files[name] = missing_references

    if args.with_rules:
        copy_optional_files(ROOT / "rules", project / ".claude" / "rules")

    missing = [item for item in EXTERNAL if not (dest / item["name"] / "SKILL.md").is_file()]
    if missing:
        print("\nExternal skills still needed for the full workflow:")
        for item in missing:
            print(f"- {item['name']} — {item['author']}: {item['source']}")
        print("Download from the author, extract until each skill folder contains SKILL.md, then rerun with --upstream-dir.")
    else:
        print("\nAll Yummy Labs skills the workflow needs are installed.")
    for skill, relative in sorted(REQUIRED_UPSTREAM_FILES.items()):
        # The kit skill now lives in the plugin; it reads the file from the project's .claude/skills/.
        if not (dest / relative).is_file():
            print(f"\nThe plugin's {skill} skill needs {relative} from the author's package; it is not installed yet.")
    if missing_reference_files:
        print("\nNote (safe to ignore): these optional reference files are mentioned by their author but not included in the download:")
        for name, files in sorted(missing_reference_files.items()):
            print(f"- {name}: {', '.join(files)}")
        print("The skills still work. Add your own product reference later if you want that extra context.")


if __name__ == "__main__":
    main()

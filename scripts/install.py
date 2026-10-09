#!/usr/bin/env python3
"""Fetch author-hosted Yummy Labs skills, then assemble a Claude Code project."""

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile

from assemble import EXTERNAL_BY_NAME, ROOT, find_upstream


PACKAGES = json.loads((ROOT / "upstream-packages.json").read_text(encoding="utf-8"))
MAX_ARCHIVE_MEMBERS = 1000
MAX_FILE_BYTES = 20 * 1024 * 1024
MAX_TOTAL_BYTES = 100 * 1024 * 1024


def gdown_from_venv(venv: Path) -> str:
    """Install gdown into its own virtual environment once, and return its path."""
    bin_dir = venv / ("Scripts" if os.name == "nt" else "bin")
    local = bin_dir / "gdown"
    if local.is_file():
        return str(local)
    if sys.version_info < (3, 10):
        sys.exit("Python 3.10 or newer is needed. Install it from https://www.python.org/downloads/ and try again.")
    print(f"Installing the downloader (gdown) into {venv}. This happens once…", flush=True)
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        subprocess.run([str(bin_dir / "python"), "-m", "pip", "install", "--quiet", "gdown"], check=True)
    except subprocess.CalledProcessError:
        sys.exit("Could not install gdown automatically. Install it with: python3 -m pip install gdown")
    return str(local)


def run_gdown(executable: str, url: str, output: Path = None):
    command = [executable, url, "--no-cookies", "--quiet"]
    if output is None:
        command.append("--json")
    else:
        command.extend(["-O", str(output)])
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"Download failed for {url}: {result.stderr.strip()}")
    return json.loads(result.stdout) if output is None else None


def unpack_archive(archive: Path, target: Path, depth: int = 0) -> None:
    if depth > 3:
        raise ValueError(f"Archive nesting exceeds three levels: {archive}")
    target.mkdir(parents=True, exist_ok=True)
    try:
        with ZipFile(archive) as package:
            files = package.infolist()
            if len(files) > MAX_ARCHIVE_MEMBERS:
                raise ValueError(f"Too many files in {archive}")
            total = sum(item.file_size for item in files)
            if total > MAX_TOTAL_BYTES:
                raise ValueError(f"Expanded archive is too large: {archive}")
            for item in files:
                parts = PurePosixPath(item.filename).parts
                if not parts or parts[0] == "__MACOSX" or any(part.startswith("._") or part == ".DS_Store" for part in parts):
                    continue
                if item.filename.startswith("/") or ".." in parts or "\\" in item.filename:
                    raise ValueError(f"Unsafe archive path: {item.filename}")
                if stat.S_ISLNK(item.external_attr >> 16):
                    raise ValueError(f"Archive contains a symlink: {item.filename}")
                if item.is_dir():
                    continue
                if item.file_size > MAX_FILE_BYTES:
                    raise ValueError(f"Archive member is too large: {item.filename}")
                destination = target.joinpath(*parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                with package.open(item) as source, destination.open("wb") as output:
                    shutil.copyfileobj(source, output)
    except BadZipFile as exc:
        raise ValueError(f"Not a valid skill archive: {archive}") from exc

    nested = [file for file in target.rglob("*") if file.is_file() and file.suffix.lower() in {".zip", ".skill"}]
    for number, file in enumerate(nested):
        # Nested .skill files are ZIP archives. Keep their original bytes in the temp area.
        unpack_archive(file, target / f"_expanded_{depth}_{number}", depth + 1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path, help="Existing Claude Code project directory")
    parser.add_argument("--with-rules", "--with-rules-agents", dest="with_rules", action="store_true", help="Also copy the optional Claude Code rules")
    parser.add_argument("--gdown", default="gdown", help="Path to gdown executable (default: gdown on PATH)")
    parser.add_argument("--venv", type=Path, help="If gdown is missing, install it into this virtual environment")
    args = parser.parse_args()
    if not args.project.expanduser().is_dir():
        parser.error(f"Project directory does not exist: {args.project}")
    skills = args.project.expanduser().resolve() / ".claude" / "skills"
    if all((skills / name / "SKILL.md").is_file() for name in EXTERNAL_BY_NAME):
        print("All five Yummy Labs skills are already in this project. Nothing to download.")
        return
    executable = shutil.which(args.gdown)
    if executable is None and args.venv:
        executable = gdown_from_venv(args.venv.expanduser())
    if executable is None:
        parser.error("gdown is required. Install it with: python3 -m pip install gdown")

    with tempfile.TemporaryDirectory(prefix="design-stuff-kit-") as temporary:
        extracted = Path(temporary) / "extracted"
        extracted.mkdir()
        for package in PACKAGES:
            listing = run_gdown(executable, package["download"])
            archives = [item for item in listing if Path(item["path"]).suffix.lower() in {".zip", ".skill"}]
            if len(archives) != 1:
                raise RuntimeError(f"Expected one archive at {package['source']}; found {len(archives)}. Check the author's page.")
            archive = Path(temporary) / f"{package['id']}.zip"
            print(f"Fetching {', '.join(package['skills'])} from {package['source']}", flush=True)
            run_gdown(executable, archives[0]["url"], archive)
            unpack_archive(archive, extracted / package["id"])

        found = find_upstream(extracted)
        expected = set(EXTERNAL_BY_NAME)
        if set(found) != expected:
            raise RuntimeError(f"Author packages contain {sorted(found)}; expected {sorted(expected)}. Nothing was installed.")
        command = [sys.executable, str(ROOT / "scripts" / "assemble.py"), "--project", str(args.project), "--upstream-dir", str(extracted)]
        if args.with_rules:
            command.append("--with-rules")
        subprocess.run(command, check=True)


if __name__ == "__main__":
    main()

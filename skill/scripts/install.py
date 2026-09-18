#!/usr/bin/env python3
"""Install ContextMe locally. Never downloads packages or modifies CLI permissions."""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from contextme import Store, ContextError, write_json


def install(target: str, home: Path, project: Path | None = None,
            workspace: Path | None = None, replace: bool = False) -> dict:
    source = Path(__file__).resolve().parent.parent
    base = (project or home).expanduser().resolve()
    choices = [target] if target != "both" else ["claude", "codex"]
    destinations = [base / (".claude" if t == "claude" else ".agents") / "skills" / "contextme" for t in choices]
    for dst in destinations:
        if dst.is_symlink():
            raise ContextError(f"Refusing to replace symlink {dst}")
        if dst.resolve() == source or source.is_relative_to(dst.resolve()) or dst.resolve().is_relative_to(source):
            raise ContextError("Source and installation directories must not overlap")
        if dst.exists() and not replace:
            raise ContextError(f"Already installed: {dst}. Use --replace to keep a backup and replace it.")
        if workspace and workspace.resolve().is_relative_to(dst.resolve()):
            raise ContextError("The private workspace must be outside the skill installation")
    result = {"installed": [], "backups": [], "workspace": None}
    for dst in destinations:
        dst.parent.mkdir(parents=True, exist_ok=True)
        temp = Path(tempfile.mkdtemp(prefix=".contextme-install-", dir=dst.parent))
        staging = temp / "contextme"
        try:
            shutil.copytree(source, staging, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", ".git"))
            if dst.exists():
                stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%f")
                # Backup outside the skill scanner so the old skill is not registered twice.
                backup_root = base / ".contextme" / "skill-backups"
                backup_root.mkdir(parents=True, exist_ok=True)
                backup = backup_root / (dst.parent.parent.name.lstrip(".") + "-" + stamp)
                os.replace(dst, backup)
                result["backups"].append(str(backup))
            os.replace(staging, dst)
            result["installed"].append(str(dst))
        finally:
            shutil.rmtree(temp, ignore_errors=True)
    if workspace:
        workspace = workspace.expanduser().resolve()
        Store(workspace).init()
        location = home.expanduser().resolve() / ".contextme" / "location.json"
        write_json(location, {"workspace": str(workspace)})
        result["workspace"] = str(workspace)
        result["workspace_pointer"] = str(location)
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", choices=["both", "claude", "codex"], default="both")
    ap.add_argument("--workspace", help="Optional private workspace to initialize and select")
    ap.add_argument("--project", help="Install project-locally instead of in your home directory")
    ap.add_argument("--replace", action="store_true", help="Replace existing installation while keeping a code backup")
    ap.add_argument("--home", default=str(Path.home()), help=argparse.SUPPRESS)
    args = ap.parse_args()
    try:
        result = install(args.target, Path(args.home), Path(args.project) if args.project else None,
                         Path(args.workspace) if args.workspace else None, args.replace)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ContextError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

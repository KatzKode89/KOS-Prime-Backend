#!/usr/bin/env python3
"""Design, validate, and package KOS-Prime Steam app/game projects."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "config/katz-0s-steam-deck.json"


def world(seed: int, count: int) -> list[dict[str, object]]:
    rng = random.Random(seed)
    return [
        {"id": f"echo-{index:02d}", "x": rng.randint(-100, 100), "y": rng.randint(-100, 100), "kind": "crystal" if index % 2 else "relay"}
        for index in range(count)
    ]


def create_project(kind: str, name: str, output: Path, seed: int, force: bool) -> None:
    if output.exists() and any(output.iterdir()) and not force:
        raise ValueError(f"destination is not empty: {output} (use --force to replace files)")
    output.mkdir(parents=True, exist_ok=True)
    (output / "world.json").write_text(json.dumps({"seed": seed, "nodes": world(seed, 8)}, indent=2) + "\n")
    (output / "steam-build.json").write_text(json.dumps({
        "name": name, "kind": kind, "version": "0.1.0-beta", "scene": "StarterCockpit.unity",
        "targets": ["steam-windows-x64", "steam-linux-x64", "steam-deck", "steam-link"],
        "controller_profile": "config/steam-controller-actions.json", "world_seed": seed,
        "fake_data_only": True, "backend_required": False
    }, indent=2) + "\n")
    (output / "README.md").write_text(f"# {name}\n\nGenerated {kind} design for K@tz-0$-St3@m-D3ck.\n\nWorld seed: `{seed}`\n\nThis is a design/build input package; Unity and Steamworks remain publisher-managed.\n")


def validate_project(project: Path) -> None:
    manifest = json.loads((project / "steam-build.json").read_text(encoding="utf-8"))
    required = {"name", "kind", "version", "targets", "world_seed", "fake_data_only", "backend_required"}
    if not required <= manifest.keys() or manifest["kind"] not in {"app", "game"}:
        raise ValueError("invalid Steam app/game manifest")
    if not manifest["fake_data_only"] or manifest["backend_required"]:
        raise ValueError("starter Steam projects must remain fake-data and backend-independent")
    if not isinstance(manifest["world_seed"], int):
        raise ValueError("world_seed must be an integer")
    world_data = json.loads((project / "world.json").read_text(encoding="utf-8"))
    if world_data["seed"] != manifest["world_seed"] or len(world_data["nodes"]) == 0:
        raise ValueError("world manifest does not match build manifest")


def package_project(project: Path, output: Path) -> None:
    validate_project(project)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(project.rglob("*")):
            if path.is_file():
                archive.write(path, Path(project.name) / path.relative_to(project))
        archive.write(PROFILE, Path("config") / PROFILE.name)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"Packaged {project} -> {output}\nSHA-256: {digest}")


def compile_project(project: Path, unity_editor: str, output: Path) -> None:
    validate_project(project)
    if not shutil.which(unity_editor) and not Path(unity_editor).is_file():
        raise FileNotFoundError(f"Unity editor not found: {unity_editor}")
    output.mkdir(parents=True, exist_ok=True)
    command = [unity_editor, "-batchmode", "-quit", "-projectPath", str(project), "-buildTarget", "StandaloneWindows64", "-buildWindows64Player", str(output / (project.name + ".exe"))]
    subprocess.run(command, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    new = commands.add_parser("new", help="create an app or game design")
    new.add_argument("kind", choices=("app", "game"))
    new.add_argument("name")
    new.add_argument("--output", type=Path, required=True)
    new.add_argument("--seed", type=int, default=1337)
    new.add_argument("--force", action="store_true")
    validate = commands.add_parser("validate")
    validate.add_argument("project", type=Path)
    package = commands.add_parser("package")
    package.add_argument("project", type=Path)
    package.add_argument("--output", type=Path, required=True)
    compile_command = commands.add_parser("compile", help="invoke an installed Unity editor")
    compile_command.add_argument("project", type=Path)
    compile_command.add_argument("--unity-editor", required=True)
    compile_command.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "new":
            create_project(args.kind, args.name, args.output, args.seed, args.force)
            print(f"Created {args.kind} project at {args.output}")
        elif args.command == "validate":
            validate_project(args.project)
            print(f"Validated Steam project: {args.project}")
        elif args.command == "package":
            package_project(args.project, args.output)
        else:
            compile_project(args.project, args.unity_editor, args.output)
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"Steam stack error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
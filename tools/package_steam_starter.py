#!/usr/bin/env python3
"""Package the Unity Steam starter source for handoff or build input."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path


DEFAULT_ROOT = Path("starter/KatzStarterForSteam")
DEFAULT_MANIFEST = Path("config/crystalseekers-steam-beta.json")
SCENE_GUIDE = Path("docs/unity-starter-scene.md")


def package(root: Path, manifest_path: Path, output: Path) -> int:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("data_mode") != "fake-local" or manifest.get("backend_required"):
        raise ValueError("Steam starter must remain fake-local and backend-independent")
    files = sorted(path for path in root.rglob("*") if path.is_file())
    if not files:
        raise ValueError(f"starter directory is empty: {root}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("manifest.json", json.dumps(manifest, indent=2) + "\n")
        for path in files:
            archive.write(path, Path("KatzStarterForSteam") / path.relative_to(root))
        if SCENE_GUIDE.is_file():
            archive.write(SCENE_GUIDE, Path("docs") / SCENE_GUIDE.name)
    return len(files) + 1 + int(SCENE_GUIDE.is_file())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=Path("dist/CrystalSeekers-Echoes-of-Destiny-Beta-source.zip"))
    args = parser.parse_args()
    count = package(args.root, args.manifest, args.output)
    print(f"Packaged {count} files into {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
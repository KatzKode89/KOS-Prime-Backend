#!/usr/bin/env python3
"""Generate a small KOS-Prime game or app starter project."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError("name must contain at least one letter or number")
    return slug


def build_files(kind: str, name: str, description: str, features: list[str]) -> dict[str, str]:
    title = json.dumps(name)
    feature_json = json.dumps(features, indent=2)
    feature_lines = "\n".join(f"- {feature}" for feature in features) or "- Add your first feature"
    entrypoint = "Game" if kind == "game" else "App"
    return {
        "manifest.json": json.dumps(
            {
                "name": name,
                "kind": kind,
                "description": description,
                "features": features,
                "runtime": "python3",
                "kos_prime": {
                    "packet_type": "lattice",
                    "ontology_segment": "KOSPrime.StackArchitectureMap",
                },
            },
            indent=2,
        )
        + "\n",
        "README.md": f"# {name}\n\n{description}\n\n## Features\n\n{feature_lines}\n\n## Run\n\n```bash\npython3 main.py\n```\n",
        "main.py": f'''#!/usr/bin/env python3
"""Generated KOS-Prime {kind} starter."""

import json
from pathlib import Path


def load_manifest() -> dict:
    return json.loads((Path(__file__).parent / "manifest.json").read_text(encoding="utf-8"))


def run_{kind}() -> None:
    manifest = load_manifest()
    print(f"{{manifest['name']}} {entrypoint} ready")
    print(f"Features: {{', '.join(manifest['features']) or 'none configured'}}")
    print(f"PrimeBus segment: {{manifest['kos_prime']['ontology_segment']}}")


if __name__ == "__main__":
    run_{kind}()
''',
        ".gitignore": "__pycache__/\n*.py[cod]\n",
    }


def create_project(
    output: Path,
    kind: str,
    name: str,
    description: str,
    features: list[str],
    force: bool,
) -> list[Path]:
    if output.exists() and any(output.iterdir()) and not force:
        raise FileExistsError(f"destination is not empty: {output} (use --force to replace files)")
    output.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for relative_path, content in build_files(kind, name, description, features).items():
        target = output / relative_path
        target.write_text(content, encoding="utf-8")
        written.append(target)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("game", "app"))
    parser.add_argument("name")
    parser.add_argument("--description", default="A KOS-Prime starter project.")
    parser.add_argument("--feature", action="append", default=[])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    try:
        project_name = args.name.strip()
        if not project_name:
            raise ValueError("name cannot be empty")
        output = args.output or Path("generated") / slugify(project_name)
        written = create_project(
            output,
            args.kind,
            project_name,
            args.description,
            args.feature,
            args.force,
        )
    except (FileExistsError, OSError, ValueError) as error:
        print(f"KOS Maker error: {error}", file=sys.stderr)
        return 1

    print(f"Created {args.kind} starter: {output}")
    for path in written:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
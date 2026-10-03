#!/usr/bin/env python3
"""Update selected nested values in-place while retaining YAML comments/formatting."""
import argparse
from collections.abc import MutableMapping
from pathlib import Path

from ruamel.yaml import YAML


def set_path(document, dotted_path: str, value: str) -> None:
    parts = dotted_path.split(".")
    if not parts or any(not part for part in parts):
        raise ValueError(f"invalid dotted YAML path: {dotted_path!r}")
    current = document
    for part in parts[:-1]:
        if part not in current or current[part] is None:
            current[part] = {}
        if not isinstance(current[part], MutableMapping):
            raise ValueError(f"cannot traverse non-mapping at {part!r} in {dotted_path!r}")
        current = current[part]
    current[parts[-1]] = value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("values_file")
    parser.add_argument("--tag-path", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--digest-path", required=True)
    parser.add_argument("--digest", required=True)
    args = parser.parse_args()

    path = Path(args.values_file)
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    with path.open(encoding="utf-8") as stream:
        document = yaml.load(stream)
    if not isinstance(document, MutableMapping):
        raise SystemExit("values YAML root must be a mapping")
    set_path(document, args.tag_path, args.tag)
    set_path(document, args.digest_path, args.digest)
    with path.open("w", encoding="utf-8", newline="") as stream:
        yaml.dump(document, stream)


if __name__ == "__main__":
    main()

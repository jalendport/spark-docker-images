#!/usr/bin/env python3
"""Check that the image workflows agree with what is on disk.

Every version an image publishes is a directory, and each one is named by a
filter in that image's workflow. Nothing enforces that, so a typo in a filter
path silently stops an image from ever rebuilding, and the workflow still
passes. This checks the two descriptions of the matrix against each other.

Run it from the repository root:

    python3 .github/scripts/validate-workflows.py
"""

from __future__ import annotations

import glob
import os
import sys

import yaml

# Filter keys that name something other than a version directory
NON_VERSION_KEYS = {"shared", "readme"}


def flatten(value):
    """Yield leaf strings from a filter's patterns, which nest via YAML anchors."""
    for item in value:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def check_workflow(path: str) -> list[str]:
    workflow = yaml.safe_load(open(path))
    inputs = workflow["jobs"]["generic"]["with"]
    image = inputs["image-name"]
    filters = yaml.safe_load(inputs["filters"])
    aliases = yaml.safe_load(inputs.get("aliases") or "{}") or {}

    versions = [key for key in filters if key not in NON_VERSION_KEYS]
    errors = []

    for key in versions:
        if not key.startswith(f"{image}-"):
            errors.append(f"{path}: filter {key!r} is not prefixed with {image!r}")
            continue

        version = key[len(image) + 1 :]
        if not os.path.isdir(os.path.join(image, version)):
            errors.append(f"{path}: filter {key!r} has no directory {image}/{version}")

        for pattern in flatten(filters[key]):
            target = pattern[:-3] if pattern.endswith("/**") else pattern
            if not os.path.exists(target):
                errors.append(f"{path}: filter {key!r} matches nothing: {pattern}")

    for entry in sorted(os.listdir(image)):
        if os.path.isdir(os.path.join(image, entry)) and f"{image}-{entry}" not in versions:
            errors.append(f"{path}: {image}/{entry} has no filter, so it is never built")

    for key in aliases:
        if key not in versions:
            errors.append(f"{path}: alias {key!r} points at a version that is not built")

    return errors


def main() -> int:
    workflows = sorted(glob.glob(".github/workflows/*-images.yml"))
    if not workflows:
        print("no image workflows found; run this from the repository root", file=sys.stderr)
        return 1

    errors = []
    for path in workflows:
        errors += check_workflow(path)

    for error in errors:
        print(error, file=sys.stderr)

    if errors:
        print(f"\n{len(errors)} problem(s) found", file=sys.stderr)
        return 1

    print(f"{len(workflows)} workflows agree with the directories on disk")
    return 0


if __name__ == "__main__":
    sys.exit(main())

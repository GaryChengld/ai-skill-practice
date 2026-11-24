"""Print an estimated context budget. Requires PyYAML (`python -m pip install PyYAML`)."""

import argparse
import os
from pathlib import Path

import yaml


def files_under(root):
    for directory, subdirs, filenames in os.walk(root):
        subdirs[:] = sorted(name for name in subdirs if name != "tests" and not name.startswith("."))
        for filename in sorted(filenames):
            if not filename.startswith("."):
                yield Path(directory) / filename


def estimate(text):
    return (len(text.strip()) + 3) // 4


def skill_content(path):
    lines = path.read_text(encoding="utf-8-sig").splitlines(keepends=True)
    fences = [i for i, line in enumerate(lines) if line.rstrip() == "---"]
    if len(fences) < 2 or fences[0] != 0:
        raise ValueError(f"{path}: missing YAML frontmatter")
    end = fences[1]
    metadata = yaml.safe_load("".join(lines[1:end]))
    if not isinstance(metadata, dict) or any(
        not isinstance(metadata.get(key), str) or not metadata[key].strip()
        for key in ("name", "description")
    ):
        raise ValueError(f"{path}: expected nonempty string fields for name and description")
    return metadata["name"], metadata["description"], "".join(lines[end + 1:])


def resource_size(path):
    try:
        contents = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return "N/A (binary or non-UTF-8)"
    return "N/A (binary)" if "\x00" in contents else estimate(contents)


def report(root):
    files = sorted(files_under(root))
    skills = {path.parent: path for path in files if path.name == "SKILL.md"}
    resources = {directory: [] for directory in skills}
    for path in files:
        owner = next((parent for parent in path.parents if parent in skills), None)
        if owner is not None and path != skills[owner]:
            resources[owner].append(path)

    yield "| Skill folder | Metadata | Description | Body | Resource | Resource tokens |"
    yield "| --- | ---: | ---: | ---: | --- | ---: |"
    total = 0
    for directory, skill in skills.items():
        name, description, body = skill_content(skill)
        metadata = estimate(f"{name.strip()}\n{description.strip()}")
        total += metadata
        yield f"| `{directory.relative_to(root).as_posix()}` | {metadata} | {estimate(description)} | {estimate(body)} | | |"
        for resource in resources[directory]:
            yield f"| | | | | `{resource.relative_to(directory).as_posix()}` | {resource_size(resource)} |"
    yield f"| **Total metadata** | **{total}** | | | | |"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="repository root to scan")
    root = parser.parse_args().root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    try:
        print("\n".join(report(root)))
    except (OSError, ValueError, yaml.YAMLError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()

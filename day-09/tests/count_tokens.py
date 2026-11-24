"""Print an estimated context budget using only the Python standard library."""

import argparse
import json
import os
from pathlib import Path
import re
from textwrap import dedent

FIELD = re.compile(r"(name|description):[ \t]*(.*)")


def files_under(root):
    for directory, subdirs, filenames in os.walk(root):
        subdirs[:] = sorted(name for name in subdirs if name != "tests" and not name.startswith("."))
        for filename in sorted(filenames):
            if not filename.startswith("."):
                yield Path(directory) / filename


def estimate(text):
    return (len(text.strip()) + 3) // 4


def scalar(value, continuation):
    """Read plain, quoted, or implicitly indented block scalar fields."""
    if value.startswith("'"):
        match = re.fullmatch(r"'((?:[^']|'')*)'[ \t]*(?:#.*)?", value)
        if match:
            return match[1].replace("''", "'")
    elif value.startswith('"'):
        decoded, end = json.JSONDecoder().raw_decode(value)
        tail = value[end:].strip()
        if not tail or tail.startswith("#"):
            return decoded
    else:
        value = re.split(r"[ \t]+#", value, maxsplit=1)[0].strip()
        if value in {"|", "|-", "|+", ">", ">-", ">+"}:
            block = dedent("".join(continuation)).strip("\n")
            if value.startswith("|"):
                return block
            lines = block.splitlines()
            result = []
            for line, following in zip(lines, lines[1:] + [""]):
                result.append(line)
                if line.startswith(" ") or following.startswith(" ") or not line:
                    result.append("\n")
                elif following:
                    result.append(" ")
            return "".join(result)
        if value and value[0] not in "[{&*!%@`#|>":
            return value
    raise ValueError("expected a text scalar")


def skill_content(path):
    lines = path.read_text(encoding="utf-8-sig").splitlines(keepends=True)
    fences = [i for i, line in enumerate(lines) if line.rstrip() == "---"]
    if len(fences) < 2 or fences[0] != 0:
        raise ValueError(f"{path}: missing YAML frontmatter")
    end = fences[1]
    metadata = {}
    for index in range(1, end):
        match = FIELD.fullmatch(lines[index].rstrip())
        if not match:
            continue
        key, value = match.groups()
        next_line = index + 1
        while next_line < end and (lines[next_line][0].isspace() or not lines[next_line].strip()):
            next_line += 1
        try:
            metadata[key] = scalar(value, lines[index + 1:next_line])
        except ValueError as error:
            raise ValueError(f"{path}:{index + 1}: invalid {key}: {error}") from error
    if not all(metadata.get(key, "").strip() for key in ("name", "description")):
        raise ValueError(f"{path}: expected nonempty name and description fields")
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
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()

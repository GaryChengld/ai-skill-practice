# /// script
# requires-python = ">=3.10"
# dependencies = ["PyYAML==6.0.2"]
# ///
"""Lint the YAML frontmatter of one or more Agent Skills."""

import argparse
from codecs import BOM_UTF8
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys


STRING = "tag:yaml.org,2002:str"
MAPPING = "tag:yaml.org,2002:map"
FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def finding(code, field, line, message, fix):
    return {"code": code, "field": field, "line": line, "message": message, "fix": fix}


class ParseFailure(Exception):
    def __init__(self, code, line, message, fix, field="frontmatter"):
        super().__init__(message)
        self.finding = finding(code, field, line, message, fix)


def line_of(node):
    return node.start_mark.line + 2


def yaml_failure(error, lines):
    mark = getattr(error, "problem_mark", None)
    reason = getattr(error, "problem", None) or str(error).splitlines()[0]
    line = mark.line + 2 if mark else 2
    if mark and line <= len(lines) and reason == "mapping values are not allowed here":
        source = lines[line - 1]
        entry = re.match(r"([A-Za-z][A-Za-z0-9-]*):[ \t]+([^\s'\"\[\]{|>].*)", source)
        if entry and entry.start(2) <= mark.column and source[mark.column:mark.column + 2] == ": ":
            field = entry[1]
            return ParseFailure("yaml-syntax", line, f"Unquoted colon followed by a space in {field}.",
                                f"Quote the entire {field} value or rephrase it to remove the colon-space.", field)
    return ParseFailure("yaml-syntax", line, f"YAML could not be parsed ({reason}).",
                        "Correct the YAML at this line. Check quoting and indentation.")


def read_frontmatter(path, yaml):
    try:
        raw = path.read_bytes().removeprefix(BOM_UTF8)
    except OSError as error:
        raise ParseFailure("file-read", None, f"Could not read SKILL.md: {error}",
                           "Check the file's permissions and retry.") from error
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as error:
        line = 1 + len(re.findall(rb"\r\n|\n|\r", raw[:error.start]))
        raise ParseFailure("invalid-utf8", line, "SKILL.md must be UTF-8. Found an invalid byte sequence.",
                           "Save the whole file as UTF-8 in your editor and retry.") from error

    if not lines or lines[0].rstrip(" \t") != "---":
        raise ParseFailure("frontmatter-missing", 1, "Expected an opening --- on the first line.",
                           "Start the file with --- and place the YAML fields immediately after it.")
    end = next((index for index in range(1, len(lines)) if lines[index].rstrip(" \t") == "---"), None)
    if end is None:
        raise ParseFailure("frontmatter-unclosed", len(lines) + 1, "Expected a closing --- after the YAML fields.",
                           "Add a --- line between the YAML fields and the Markdown body.")
    try:
        root = yaml.compose("\n".join(lines[1:end]) + "\n", Loader=yaml.SafeLoader)
    except yaml.YAMLError as error:
        raise yaml_failure(error, lines) from error
    if not is_mapping(root, yaml):
        raise ParseFailure("frontmatter-not-mapping", line_of(root) if root else 2,
                           "Expected a YAML mapping of frontmatter fields.",
                           "Write name: and description: as top-level key/value pairs.")
    return root


def is_mapping(node, yaml):
    return isinstance(node, yaml.MappingNode) and node.tag == MAPPING


def is_string(node, yaml):
    return isinstance(node, yaml.ScalarNode) and node.tag == STRING


def mapping_items(node, yaml, parent=""):
    seen = set()
    for key, value in node.value:
        if isinstance(key, yaml.ScalarNode):
            identity = (key.tag, key.value)
            if identity in seen:
                raise ParseFailure("yaml-duplicate-key", line_of(key), f"Repeated YAML key {key.value!r}.",
                                   "Keep exactly one entry for this key.", parent + key.value)
            seen.add(identity)
        yield key, value


def check_string(field, node, yaml, errors):
    if is_string(node, yaml):
        return True
    kind = {"seq": "a list", "map": "a mapping", "bool": "a boolean", "int": "an integer",
            "float": "a number", "null": "null"}.get(node.tag.rsplit(":", 1)[-1], "a non-string value")
    errors.append(finding(f"{field}-type", field, line_of(node), f"{field} must be a YAML string. Found {kind}.",
                          ("Use a quoted space-separated string such as 'Read Bash'." if field == "allowed-tools"
                           else "Quote the value to make it a string.")))
    return False


def check_length(field, node, limit, errors):
    value = node.value
    if not value.strip():
        errors.append(finding(f"{field}-empty", field, line_of(node), f"{field} must be nonempty.",
                              f"Provide a nonempty {field} string."))
        return
    if limit is not None and len(value) > limit:
        errors.append(finding(f"{field}-length", field, line_of(node),
                              f"{field} has {len(value)} characters. Expected at most {limit}.",
                              f"Shorten {field} to {limit} characters or fewer."))


def check_name(node, directory, errors):
    value = node.value
    if not value.strip():
        return
    restrictions = (
        (re.search(r"[A-Z]", value), "uppercase", "Name must use lowercase letters.",
         "Lowercase the name and rename the parent directory to match."),
        (re.search(r"[^A-Za-z0-9-]", value), "characters", "Name may contain only a-z, 0-9, and hyphens.",
         "Replace disallowed characters and rename the parent directory to match."),
        (value.startswith("-"), "leading-hyphen", "Name cannot start with a hyphen.",
         "Remove leading hyphens and rename the parent directory to match."),
        (value.endswith("-"), "trailing-hyphen", "Name cannot end with a hyphen.",
         "Remove trailing hyphens and rename the parent directory to match."),
        ("--" in value, "consecutive-hyphens", "Name cannot contain consecutive hyphens.",
         "Replace each run of hyphens with one hyphen and rename the parent directory to match."),
        (value != directory, "directory-mismatch", f"Name {value!r} must match parent directory {directory!r}.",
         "Set the name to the directory name or rename the directory to a valid matching name."),
    )
    for failed, code, message, fix in restrictions:
        if failed:
            errors.append(finding(f"name-{code}", "name", line_of(node), message, fix))


def check_metadata(node, yaml, errors):
    if not is_mapping(node, yaml):
        errors.append(finding("metadata-type", "metadata", line_of(node), "Metadata must map strings to strings.",
                              "Use key/value pairs such as version: '1.0'."))
        return
    for key, value in mapping_items(node, yaml, "metadata."):
        if not is_string(key, yaml):
            errors.append(finding("metadata-key-type", "metadata", line_of(key), "Metadata keys must be strings.",
                                  "Quote keys that YAML treats as booleans or numbers."))
        if not is_string(value, yaml):
            field = f"metadata.{key.value}" if is_string(key, yaml) else "metadata"
            errors.append(finding("metadata-value-type", field, line_of(value), "Metadata values must be strings.",
                                  "Quote scalar values such as '1.0' or replace nested values with text."))


def lint(path, yaml):
    errors = []
    warnings = []
    parse_error = None
    try:
        root = read_frontmatter(path, yaml)
        fields = {}
        for key, node in mapping_items(root, yaml):
            if not is_string(key, yaml):
                errors.append(finding("field-key-type", "frontmatter", line_of(key), "Field names must be strings.",
                                      "Use a named YAML key, such as name or description."))
            elif key.value not in FIELDS:
                warnings.append(finding("unknown-field", key.value, line_of(key),
                                        f"Unrecognized top-level field {key.value!r}.",
                                        "Remove it or move custom string properties into metadata."))
            else:
                fields[key.value] = node
        for field, limit in (("name", 64), ("description", 1024), ("compatibility", 500), ("license", None)):
            node = fields.get(field)
            if node is None:
                if field in {"name", "description"}:
                    errors.append(finding(f"{field}-missing", field, 1, f"Required field {field} is missing.",
                                          f"Add a nonempty {field}: string between the delimiters."))
            elif check_string(field, node, yaml, errors):
                check_length(field, node, limit, errors)
                if field == "name":
                    check_name(node, path.parent.name, errors)
        if "metadata" in fields:
            check_metadata(fields["metadata"], yaml, errors)
        if "allowed-tools" in fields:
            check_string("allowed-tools", fields["allowed-tools"], yaml, errors)
    except ParseFailure as error:
        parse_error = error.finding
        errors.clear()
        warnings.clear()
    return {"path": str(path), "ok": parse_error is None and not errors,
            "parse_error": parse_error, "errors": errors, "warnings": warnings}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Lint the YAML frontmatter of Agent Skills.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Run with the pinned dependency:
  uv run scripts/lint_frontmatter.py PATH [PATH ...]

Stdout is one JSON object with results (path, ok, parse_error, errors, warnings)
and summary counts (files, errors, warnings, parse_failures). Findings include
code, field, line (one-based or null), message, and fix. Parse failures have
their own count. Errors in the summary count lint findings only.

Exit codes are checked in this order:
  2  Invalid arguments or path; all paths are checked before linting.
  4  PyYAML unavailable; stderr gives the exact uv run command.
  3  At least one file could not be parsed, even if other files have errors.
  1  At least one lint error and no parse failures.
  0  No errors; warnings are allowed.
Stdout is empty on exits 2 and 4. --help prints help instead of JSON.""",
    )
    parser.add_argument("paths", metavar="PATH", nargs="+", help="a skill directory or its SKILL.md file")
    args = parser.parse_args(argv)
    paths = []
    for value in args.paths:
        path = Path(value)
        try:
            if path.is_dir():
                path /= "SKILL.md"
            if path.name != "SKILL.md" or not path.is_file():
                parser.error(f"{value!r} is not a skill directory containing SKILL.md or an existing SKILL.md file.")
            paths.append(path.absolute())
        except OSError as error:
            parser.error(f"cannot inspect {value!r}: {error}. Pass an accessible skill directory or SKILL.md file.")

    try:
        import yaml
    except ImportError:
        command = ["uv", "run", str(Path(__file__).resolve()), *args.paths]
        display = subprocess.list2cmdline(command) if os.name == "nt" else shlex.join(command)
        print(f"PyYAML is unavailable. Run: {display}", file=sys.stderr)
        return 4

    results = [lint(path, yaml) for path in paths]
    summary = {"files": len(results), "errors": sum(len(row["errors"]) for row in results),
               "warnings": sum(len(row["warnings"]) for row in results),
               "parse_failures": sum(row["parse_error"] is not None for row in results)}
    print(json.dumps({"results": results, "summary": summary}))
    if summary["parse_failures"]:
        return 3
    return int(summary["errors"] > 0)


if __name__ == "__main__":
    raise SystemExit(main())

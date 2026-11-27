"""Print a Markdown comparison of the linter and an Agent Skills validator."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


TESTS = Path(__file__).resolve().parent


def compare(reference, fixtures):
    files = sorted(fixtures.glob("*/*/SKILL.md"))
    if not files:
        raise ValueError(f"No fixture skills found below {fixtures}.")
    linter = TESTS.parent / "scripts/lint_frontmatter.py"
    for file in files:
        ours = subprocess.run([sys.executable, str(linter), str(file)], capture_output=True, check=False)
        if ours.returncode not in (0, 1, 3):
            raise ValueError(ours.stderr.decode(errors="replace").strip())
        record, = json.loads(ours.stdout)["results"]
        codes = [entry["code"] for entry in record["errors"] + record["warnings"]]
        if record["parse_error"]:
            codes.append(record["parse_error"]["code"])
        other = subprocess.run([reference, "validate", str(file.parent)], capture_output=True, check=False)
        diagnostic = (other.stdout + other.stderr).decode("utf-8", errors="replace").strip().splitlines()
        detail = "<br>".join(line.strip() for line in diagnostic if line.strip()) or "No diagnostic"
        detail = detail.replace(str(file.parent), file.parent.relative_to(fixtures).as_posix())
        yield file.parent.parent.name, ours.returncode, codes, other.returncode, detail


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", default="skills-ref", help="validator executable supporting validate DIR")
    parser.add_argument("--fixtures", type=Path, default=TESTS / "fixtures")
    args = parser.parse_args()
    reference = shutil.which(args.reference)
    if reference is None:
        parser.error("reference validator not found; pass its path with --reference")
    try:
        rows = list(compare(reference, args.fixtures))
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print("| Fixture | Linter exit and codes | Reference exit | Reference diagnostic on failure |")
    print("| --- | --- | ---: | --- |")
    for name, ours, codes, other, detail in rows:
        findings = ", ".join(f"`{code}`" for code in codes)
        detail = detail.replace("|", r"\|") if other else "—"
        print(f"| `{name}` | {ours}" + (f" · {findings}" if findings else "") + f" | {other} | {detail} |")


if __name__ == "__main__":
    main()

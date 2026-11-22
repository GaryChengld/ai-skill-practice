"""Check the Day 08 assets and the unchanged outputs from the four sessions."""

import argparse
import csv
from itertools import product
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator

TESTS = Path(__file__).resolve().parent
SKILL = TESTS.parent
ASSETS = SKILL / "assets"


def verify_assets():
    frontmatter, body = (SKILL / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1:]
    assert re.search(r"^name: oncall-handoff$", frontmatter, re.M)
    assert len(re.findall(r"^description: \S.+$", frontmatter, re.M)) == 1
    assert len(body.strip().splitlines()) <= 50
    assert not (SKILL / "references").exists()
    for case in "abcde":
        assert 8 <= len((TESTS / f"input-{case}.md").read_text(encoding="utf-8").splitlines()) <= 20

    with (ASSETS / "severity-matrix.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == ["impact", "urgency", "severity"]
        rows = list(reader)
    matrix = {(row["impact"], row["urgency"]): row["severity"] for row in rows}
    impact = ["all-users", "some-users", "internal-only"]
    urgency = ["worsening", "stable", "no-current-impact"]
    assert len(rows) == 9 and matrix.keys() == set(product(impact, urgency))

    schema = json.loads((ASSETS / "handoff.schema.json").read_text(encoding="utf-8"))
    assert schema["$schema"] == Draft202012Validator.META_SCHEMA["$id"]
    Draft202012Validator.check_schema(schema)
    severity = schema["$defs"]["open_item"]["properties"]["severity"]["enum"]
    assert set(matrix.values()) <= set(severity) - {"Unknown"}
    print("Skill size, fixture lengths, CSV coverage, and JSON Schema: PASS")
    return matrix, Draft202012Validator(schema)


def headings(markdown):
    return re.findall(r"^#{1,6} \S.*$", markdown, re.M)


def sections(markdown):
    parts = re.split(r"(?m)^(## \S.*)$", markdown)
    assert not parts[0].strip(), "unexpected text before the first heading"
    return {heading: body.strip("\n") for heading, body in zip(parts[1::2], parts[2::2])}


def entry_patterns(template):
    patterns = {}
    for heading, body in sections(template).items():
        if body.startswith("- "):
            literals = re.split(r"<[^>]+>", body)
            patterns[heading] = re.compile(r"\S(?:.*?\S)?".join(map(re.escape, literals)))
    return patterns


def verify_markdown_sections(output, template, patterns, case):
    assert headings(output) == headings(template), (case, headings(output))
    assert not re.search(r"<[^>\n]+>", output), f"{case}: unfilled template placeholder"
    parts = sections(output)
    assert parts["## Shift summary"].strip(), f"{case}: missing shift summary"
    for heading, pattern in patterns.items():
        body = parts[heading]
        if body == "None reported.":
            continue
        assert body and all(pattern.fullmatch(line) for line in body.splitlines()), (
            f"{case}: {heading} must use the template entry layout or exactly 'None reported.'"
        )
    return parts


def verify_outputs(matrix, validator):
    template = (ASSETS / "handoff-template.md").read_text(encoding="utf-8")
    patterns = entry_patterns(template)
    for case in "abde":
        output = (TESTS / f"output-{case}.md").read_text(encoding="utf-8")
        parts = verify_markdown_sections(output, template, patterns, case)
        open_items = parts["## Open items"]
        if case in "ae":
            declared = {"a": (("PAY-341", "SEV3"), ("PAY-342", "SEV4")), "e": (("MSG-482", "SEV3"),)}
            for ticket, severity in declared[case]:
                assert re.search(rf"^- \*\*{ticket} \| .+ Severity: {severity}\.", open_items, re.M)
        if case == "b":
            severity = matrix["some-users", "worsening"]
            assert re.search(rf"^- \*\*DEL-518.*Severity: {severity}\b", open_items, re.M)
            assert "Threshold or time: Unknown." in parts["## Watch list"]
        if case == "d":
            item = next(line for line in open_items.splitlines() if line.startswith("- **SRC-774"))
            assert "Severity: Unknown." in item
            assert any("urgency" in line.lower() and ("SRC-774" in line or "Product Search Service" in line)
                       for line in parts["## Open questions"].splitlines())
        if case in "ae":
            assert parts["## Open questions"] == "None reported."
        print(f"{case.upper()} headings, all entry layouts, and severity behavior: PASS")

    handoff = json.loads((TESTS / "output-c.json").read_text(encoding="utf-8"))
    validator.validate(handoff)
    assert [(item["ticket"], item["severity"]) for item in handoff["open_items"]] == [("IDN-221", "SEV3")]
    assert handoff["open_questions"] == []
    print("C raw JSON, draft 2020-12 validation, and declared severity: PASS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets-only", action="store_true", help="Check assets before any sessions have run.")
    options = parser.parse_args()
    matrix, validator = verify_assets()
    if not options.assets_only:
        verify_outputs(matrix, validator)

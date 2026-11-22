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
    for case in "abcd":
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


def verify_outputs(matrix, validator):
    template = (ASSETS / "handoff-template.md").read_text(encoding="utf-8")
    entry = next(line for line in template.splitlines() if line.startswith("- **<ticket>"))
    literals = re.split(r"<[^>]+>", entry)
    entry_pattern = re.compile(r".+?".join(re.escape(literal) for literal in literals))
    for case in "abd":
        output = (TESTS / f"output-{case}.md").read_text(encoding="utf-8")
        assert headings(output) == headings(template), (case, headings(output))
        assert not re.search(r"<[^>\n]+>", output), f"{case}: unfilled template placeholder"
        open_items = output.split("## Open items", 1)[1].split("## Watch list", 1)[0].strip()
        assert all(entry_pattern.fullmatch(line) for line in open_items.splitlines() if line.strip()), (
            f"{case}: open item layout changed"
        )
        if case == "a":
            for ticket, severity in (("PAY-341", "SEV3"), ("PAY-342", "SEV4")):
                assert re.search(rf"^{re.escape('- **' + ticket)}.*Severity: {severity}\b", output, re.M)
        if case == "b":
            severity = matrix["some-users", "worsening"]
            assert re.search(rf"^- \*\*DEL-518.*Severity: {severity}\b", output, re.M)
        if case == "d":
            item = next(line for line in output.splitlines() if line.startswith("- **SRC-774"))
            assert "Severity: Unknown." in item
            questions = output.split("## Open questions", 1)[1]
            assert any("urgency" in line.lower() and ("SRC-774" in line or "Product Search Service" in line)
                       for line in questions.splitlines())
        print(f"{case.upper()} headings and severity behavior: PASS")

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

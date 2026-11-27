"""Exercise the CLI against the frozen fixture matrix."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("lint_frontmatter.py")
TESTS = SCRIPT.parent.parent / "tests"
FIXTURES = TESTS / "fixtures"


def fixture(case):
    return next((FIXTURES / case).glob("*/SKILL.md"))


def run_cli(*paths, isolated=False):
    args = [sys.executable, *(["-I", "-S"] if isolated else []), str(SCRIPT), *map(str, paths)]
    return subprocess.run(args, capture_output=True, check=False)


class FrontmatterTest(unittest.TestCase):
    def test_frozen_fixtures(self):
        table = (TESTS / "EDGE-CASES.md").read_text(encoding="utf-8")
        cases = [line.strip("|").split("|") for line in table.splitlines() if line.startswith("| ")
                 and line[2:4].isdigit()]
        self.assertEqual({row[0].strip() for row in cases}, {path.name for path in FIXTURES.iterdir()})
        for case, _, exit_code, codes in cases:
            case = case.strip()
            with self.subTest(case=case):
                result = run_cli(fixture(case))
                self.assertEqual(result.returncode, int(exit_code), result.stderr)
                self.assertEqual(result.stderr, b"")
                payload = json.loads(result.stdout)
                row, = payload["results"]
                findings = row["errors"] + row["warnings"] + ([row["parse_error"]] if row["parse_error"] else [])
                expected = [code.strip() for code in codes.split(",") if code.strip() != "-"]
                self.assertCountEqual([entry["code"] for entry in findings], expected)
                self.assertEqual(row["ok"], result.returncode == 0)
                self.assertEqual(payload["summary"], {"files": 1, "errors": len(row["errors"]),
                                                      "warnings": len(row["warnings"]),
                                                      "parse_failures": int(result.returncode == 3)})
                for entry in findings:
                    if entry["code"] == "description-missing":
                        self.assertIsNone(entry["line"])
                    else:
                        self.assertGreater(entry["line"], 0)
                    self.assertTrue(all(entry[key] for key in ("field", "message", "fix")))

    def test_byte_sensitive_fixtures(self):
        bom = fixture("15-crlf-bom").read_bytes()
        self.assertTrue(bom.startswith(b"\xef\xbb\xbf---\r\n"))
        self.assertGreater(bom.count(b"\r\n"), 0)
        self.assertEqual(bom.count(b"\r\n"), bom.count(b"\n"))
        with self.assertRaises(UnicodeDecodeError):
            fixture("16-invalid-utf8").read_bytes().decode("utf-8")

    def test_file_line_numbers(self):
        for case, line in (("11-yaml-colon", 3), ("12-missing-close", 4), ("16-invalid-utf8", 3),
                           ("22-duplicate-key", 4)):
            with self.subTest(case=case):
                payload = json.loads(run_cli(fixture(case)).stdout)
                self.assertEqual(payload["results"][0]["parse_error"]["line"], line)

    def test_actionable_details_for_colon_space_and_list(self):
        parse_error = json.loads(run_cli(fixture("11-yaml-colon")).stdout)["results"][0]["parse_error"]
        self.assertEqual(parse_error["field"], "description")
        self.assertIn("entire description value", parse_error["fix"])
        errors = json.loads(run_cli(fixture("14-tools-list")).stdout)["results"][0]["errors"]
        self.assertIn("Found a list", errors[0]["message"])

    def test_concrete_line_fixes(self):
        for case, code, line in (("19-multiple-errors", "name-uppercase", "name: bad-name"),
                                 ("13-metadata-value", "metadata-value-type", '  version: "1.0"'),
                                 ("17-name-boolean", "name-type", 'name: "yes"'),
                                 ("23-metadata-key", "metadata-key-type", '  "yes": confirmed')):
            with self.subTest(case=case):
                result = json.loads(run_cli(fixture(case)).stdout)["results"][0]
                error = next(finding for finding in result["errors"] if finding["code"] == code)
                self.assertEqual(error["fix"].splitlines()[0], f"Change line {error['line']} to: {line}")
                if code == "name-uppercase":
                    self.assertIn("Rename the parent directory to bad-name.", error["fix"])
                if code == "name-type":
                    self.assertIn("Keep the directory name yes.", error["fix"])

    def test_flow_mapping_fix_preserves_the_mapping(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "SKILL.md"
            path.write_text(f"---\nname: {path.parent.name}\ndescription: Example.\n"
                            "metadata: {version: 1.0, author: Example}\n---\n", encoding="utf-8")
            result = json.loads(run_cli(path).stdout)["results"][0]
        finding = next(entry for entry in result["errors"] if entry["code"] == "metadata-value-type")
        self.assertEqual(finding["fix"], 'Set metadata.version to the quoted string "1.0".')

    def test_batch_parse_failure_overrides_lint_error(self):
        result = run_cli(fixture("03-uppercase").parent, fixture("11-yaml-colon"), fixture("18-unknown-field").parent)
        self.assertEqual(result.returncode, 3)
        data = json.loads(result.stdout)
        self.assertEqual(data["summary"], {"files": 3, "errors": 1, "warnings": 1, "parse_failures": 1})
        self.assertEqual([row["ok"] for row in data["results"]], [False, False, True])

    def test_bad_path_preempts_parsing_and_missing_dependency(self):
        missing = FIXTURES / "missing"
        for isolated in (False, True):
            with self.subTest(isolated=isolated):
                result = run_cli(fixture("11-yaml-colon"), missing, isolated=isolated)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, b"")
                self.assertIn(b"missing", result.stderr)
                self.assertIn(b"SKILL.md", result.stderr)

    def test_missing_dependency_has_exact_recovery_command(self):
        path = fixture("01-minimal")
        result = run_cli(path, isolated=True)
        self.assertEqual(result.returncode, 4)
        self.assertEqual(result.stdout, b"")
        self.assertIn(b"uv run", result.stderr)
        self.assertIn(str(SCRIPT).encode(), result.stderr)
        self.assertIn(str(path).encode(), result.stderr)

    def test_help_is_available_without_dependency(self):
        result = run_cli("--help", isolated=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, b"")
        for phrase in (b"PATH", b"uv run", b"parse_error", b"parse_failures", b"Exit codes", b"2 and 4"):
            self.assertIn(phrase, result.stdout)

    def test_no_arguments(self):
        result = run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b"")
        self.assertIn(b"usage:", result.stderr)


if __name__ == "__main__":
    unittest.main()

"""Exercise the version calculator through its CLI."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("next_version.py")


class NextVersionTest(unittest.TestCase):
    def run_cli(self, current, commits=b"", path="-"):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--current", current, "--commits", str(path)],
            input=commits, capture_output=True, check=False,
        )

    def calculate(self, current, commits=b"", path="-"):
        result = self.run_cli(current, commits, path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, b"")
        data = json.loads(result.stdout)
        self.assertEqual(data["current"], current)
        return data

    def assert_error(self, result, code, *phrases):
        self.assertEqual(result.returncode, code)
        self.assertEqual(result.stdout, b"")
        for phrase in phrases:
            self.assertIn(phrase, result.stderr)

    def test_feat_beats_patch_and_keeps_prefix_from_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "commits.txt"
            path.write_bytes(b"\xef\xbb\xbffix: keep locale\r\n--END--\r\nfeat: add CSV\r\n--END--\r\n")
            result = self.calculate("v1.4.2", path=path)
        self.assertEqual(result, {"current": "v1.4.2", "next": "v1.5.0", "bump": "minor",
                                  "major_zero_shift": False,
                                  "reasons": [{"header": "feat: add CSV", "rule": "feat"}], "unparsed": []})

    def test_breaking_header_beats_feat(self):
        data = self.calculate("1.4.2", b"feat: add export\n--END--\nrefactor(api)!: remove endpoint\n--END--")
        self.assertEqual((data["next"], data["bump"]), ("2.0.0", "major"))
        self.assertEqual(data["reasons"], [{"header": "refactor(api)!: remove endpoint", "rule": "breaking_header"}])

    def test_breaking_footer_on_fix(self):
        data = self.calculate("1.4.2", b"fix(api): rotate keys\n\nBREAKING CHANGE: old keys fail\n--END--\n")
        self.assertEqual((data["next"], data["bump"]), ("2.0.0", "major"))
        self.assertEqual(data["reasons"], [{"header": "fix(api): rotate keys", "rule": "breaking_footer"}])

    def test_hyphenated_breaking_footer_on_docs(self):
        data = self.calculate("3.2.1", b"docs: update migration\n\nBREAKING-CHANGE: remove old name\n--END--\n")
        self.assertEqual((data["next"], data["reasons"][0]["rule"]), ("4.0.0", "breaking_footer"))

    def test_breaking_footer_after_another_trailer(self):
        data = self.calculate("1.4.2", b"fix: rotate keys\n\nUpdate the handshake.\n\nRefs: AUTH-10\n"
                                       b"BREAKING CHANGE: old keys fail\n  Reload the keyring.\n\n--END--\n")
        self.assertEqual((data["next"], data["reasons"][0]["rule"]), ("2.0.0", "breaking_footer"))

    def test_breaking_marker_adjacent_to_header_is_not_a_footer(self):
        data = self.calculate("1.4.2", b"fix: document key usage\nBREAKING CHANGE: example marker\n--END--\n")
        self.assertEqual((data["next"], data["reasons"][0]["rule"]), ("1.4.3", "fix"))

    def test_breaking_marker_in_earlier_paragraph_is_not_a_footer(self):
        data = self.calculate("1.4.2", b"docs: explain trailers\n\nBREAKING CHANGE: example marker\n\n"
                                       b"Refs: DOCS-10\n--END--\n")
        self.assertEqual((data["next"], data["bump"]), ("1.4.2", "none"))

    def test_fix_and_perf_are_both_decisive_for_patch(self):
        data = self.calculate("1.4.2", b"FIX: handle null\n--END--\nperf: cache result\n--END--\n")
        self.assertEqual((data["next"], data["bump"]), ("1.4.3", "patch"))
        self.assertEqual(data["reasons"], [{"header": "FIX: handle null", "rule": "fix"},
                                           {"header": "perf: cache result", "rule": "perf"}])

    def test_zero_major_breaking_change_bumps_minor(self):
        data = self.calculate("0.9.3", b"fix: detect empty input\n--END--\nfeat!: remove flag\n--END--\n")
        self.assertEqual((data["next"], data["bump"]), ("0.10.0", "minor"))
        self.assertTrue(data["major_zero_shift"])
        self.assertEqual(data["reasons"], [{"header": "feat!: remove flag", "rule": "breaking_header"}])

    def test_zero_major_features_and_fixes_bump_patch(self):
        for header in (b"feat: add export", b"fix: handle empty input", b"perf: cache results"):
            with self.subTest(header=header):
                data = self.calculate("0.9.3", header + b"\n--END--\n")
                self.assertEqual((data["next"], data["bump"]), ("0.9.4", "patch"))
                self.assertTrue(data["major_zero_shift"])

    def test_none_keeps_version_and_build_metadata(self):
        data = self.calculate("v1.2.3+build.019", b"docs: revise guide\n--END--\ncustom: note status\n--END--\n"
                                                     b"unparsed: valid custom type\n--END--\n")
        self.assertEqual(data["next"], "v1.2.3+build.019")
        self.assertEqual((data["bump"], data["reasons"], data["unparsed"]), ("none", [], []))

    def test_empty_input_returns_none(self):
        data = self.calculate("0.3.1")
        self.assertEqual((data["next"], data["bump"], data["reasons"]), ("0.3.1", "none", []))
        self.assertFalse(data["major_zero_shift"])

    def test_bump_omits_old_build_metadata(self):
        data = self.calculate("v1.2.3+build.019", b"fix: retry once\n--END--\n")
        self.assertEqual(data["next"], "v1.2.4")

    def test_invalid_header_never_triggers_a_bump(self):
        data = self.calculate("1.4.2", b"feat missing colon\n\nBREAKING CHANGE: removed feature\n--END--\n"
                                        b"fix:no space\n--END--\n")
        self.assertEqual((data["bump"], data["unparsed"]), ("none", ["feat missing colon", "fix:no space"]))

    def test_inline_mention_of_breaking_label_does_not_trigger(self):
        data = self.calculate("1.4.2", b"docs: explain trailers\n\nUse BREAKING CHANGE: as a trailer.\n--END--\n")
        self.assertEqual(data["bump"], "none")

    def test_malformed_version_exits_2(self):
        for version in ("1.4", "v01.4.2", "2.0.0-rc.03"):
            with self.subTest(version=version):
                self.assert_error(self.run_cli(version), 2, b"Invalid current version", b"--current")

    def test_prerelease_exits_3(self):
        self.assert_error(self.run_cli("v2.0.0-rc.3"), 3, b"prerelease", b"stable tag")

    def test_unterminated_record_exits_2(self):
        self.assert_error(self.run_cli("1.4.2", b"fix: retry once\n"), 2, b"--END--", b"git log")

    def test_non_utf8_input_exits_2(self):
        self.assert_error(self.run_cli("1.4.2", b"\xff"), 2, b"UTF-8", b"--commits")

    def test_unreadable_file_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assert_error(self.run_cli("1.4.2", path=Path(tmp) / "missing"), 2, b"missing", b"readable")

    def test_help_describes_the_interface(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, check=True)
        self.assertEqual(result.stderr, b"")
        for phrase in (b"--current", b"--commits", b"--END--", b"git log --no-merges", b"major_zero_shift",
                       b"final paragraph", b"reasons", b"unparsed", b"Exit codes"):
            self.assertIn(phrase, result.stdout)


if __name__ == "__main__":
    unittest.main()

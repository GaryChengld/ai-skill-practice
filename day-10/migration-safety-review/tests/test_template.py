"""Regression checks for the migration review report structure."""

from pathlib import Path
from runpy import run_path
import unittest

TESTS = Path(__file__).resolve().parent
MATCHES_TEMPLATE = run_path(str(TESTS / "collect-harness.py"))["matches_template"]
TEMPLATE = (TESTS.parent / "assets/review-template.md").read_text(encoding="utf-8")
REVIEW = """## Migration Review: input-3.sql
**Database:** MySQL 8.0
**Overall risk:** High

### Findings
| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | Change column type | High | [Table copy](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html) | Plan an online change |

### Recommended rollout
1. Confirm the current column type.

   ```sql
   SHOW CREATE TABLE orders;
   ```

### Questions for the author
- What is the current definition?
"""


class ReviewTemplateTest(unittest.TestCase):
    def test_accepts_citation_in_why_and_code_nested_under_rollout(self):
        self.assertTrue(MATCHES_TEMPLATE(REVIEW, "input-3.sql", TEMPLATE))

    def test_rejects_standalone_text_at_section_boundaries(self):
        for boundary in ("### Findings", "### Recommended rollout", "### Questions for the author", ""):
            with self.subTest(boundary=boundary or "end"):
                text = "MySQL documents the table rebuild.\n\n"
                answer = REVIEW.replace(boundary, text + boundary, 1) if boundary else REVIEW + text
                self.assertFalse(MATCHES_TEMPLATE(answer, "input-3.sql", TEMPLATE))

    def test_rejects_extra_metadata_and_broken_table(self):
        for expected, replacement in (("**Database:**", "**Notes:** DDL\n**Database:**"),
                                      ("| 1 |", "\n| 1 |"),
                                      ("| High |", "|")):
            with self.subTest(replacement=replacement):
                self.assertFalse(MATCHES_TEMPLATE(REVIEW.replace(expected, replacement), "input-3.sql", TEMPLATE))


if __name__ == "__main__":
    unittest.main()

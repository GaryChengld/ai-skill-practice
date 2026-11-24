# Context budget

Run `python3 day-09/tests/count_tokens.py <repo-root>` with standard Python 3. The scanner reads the top-level `name` and `description` text fields and ignores other frontmatter. It supports plain text, single quotes, JSON-style double quotes, and implicitly indented YAML block scalars. The table uses an estimate of one token per four Unicode characters, rounded up separately for each cell. Inputs are decoded as UTF-8, line endings are normalized to LF, and surrounding whitespace is trimmed. Metadata counts the parsed name and description values joined by one newline. The other metadata keys are excluded.

Metadata is the discovery cost across the listed skill folders, including alternate versions. The body is loaded when its skill is used. Resource rows inventory visible files under each skill folder, including authoring records and evaluations outside `tests/`. Runtime context only incurs a resource's cost when that file is read. Resources in the table are counted individually and excluded from the metadata total.

| Skill folder | Metadata | Description | Body | Resource | Resource tokens |
| --- | ---: | ---: | ---: | --- | ---: |
| `day-01/conventional-commits` | 78 | 73 | 1322 | | |
| | | | | `TRIGGER-TESTS.md` | 809 |
| `day-02/competitors/pr-description` | 83 | 80 | 84 | | |
| `day-02/release-notes` | 112 | 108 | 453 | | |
| | | | | `DESCRIPTIONS.md` | 1181 |
| | | | | `EVAL-RESULTS.md` | 1812 |
| | | | | `evals/trigger-queries.json` | 1402 |
| `day-03/incident-postmortem` | 101 | 96 | 1262 | | |
| | | | | `BEFORE.md` | 268 |
| | | | | `REWRITE-NOTES.md` | 1120 |
| `day-04/stale-branches` | 79 | 75 | 1268 | | |
| | | | | `FIELDS.md` | 863 |
| | | | | `INVALID-EXAMPLES.md` | 492 |
| | | | | `LICENSE.txt` | 267 |
| `day-06/incident-postmortem` | 101 | 96 | 944 | | |
| | | | | `references/rca-methods.md` | 651 |
| | | | | `references/sensitive-incidents.md` | 742 |
| | | | | `references/timezones.md` | 645 |
| `day-07/dependency-fix-plan` | 109 | 104 | 1178 | | |
| | | | | `references/jvm.md` | 951 |
| | | | | `references/npm.md` | 961 |
| | | | | `references/python.md` | 1083 |
| `day-08/oncall-handoff` | 74 | 70 | 387 | | |
| | | | | `assets/handoff-template.md` | 117 |
| | | | | `assets/handoff.schema.json` | 305 |
| | | | | `assets/severity-matrix.csv` | 70 |
| `day-09/conventional-commits` | 57 | 52 | 447 | | |
| **Total metadata** | **794** | | | | |


## Budget limits

- **Description, at most 60 tokens.** Over budget are Day 01 `conventional-commits`, both Day 02 skills (`pr-description` and `release-notes`), Day 03 `incident-postmortem`, Day 04 `stale-branches`, Day 06 `incident-postmortem`, Day 07 `dependency-fix-plan`, and Day 08 `oncall-handoff`.
- **Body, at most 1,000 tokens.** Over budget are Day 01 `conventional-commits`, Day 03 `incident-postmortem`, Day 04 `stale-branches`, and Day 07 `dependency-fix-plan`.

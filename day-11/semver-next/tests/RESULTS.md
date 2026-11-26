# Day 11 results

The [rubric](EXPECTED.md) and four fixtures were committed in `efbd172` before any runs. All eight scored sessions used `gpt-6.1-terra`. P = pass, F = fail.

| Input | Skill | No skill | Script evidence |
| --- | --- | --- | --- |
| 1 · mixed commits | a P, b P, c P | a P, b P, c F | [Exit 0, `v1.5.0`](harness/1-skill.jsonl) |
| 2 · breaking footer | a P, b P | a P, b P | [Exit 0, `2.0.0`](harness/2-skill.jsonl) |
| 3 · major zero | a P, b P | a F, b F | [Exit 0, `0.10.0`](harness/3-skill.jsonl) |
| 4 · prerelease | a P, b P, c P | a F, b F, c F | [Exit 3, diagnostic](harness/4-skill.jsonl) |
| **Total** | **10/10** | **4/10** | |

All four skill runs executed the calculator. The command and tool records show zero source reads, and the no-skill sessions had zero enabled skills and no skill loads. The [manifest](harness/manifest.json) records session IDs, exit statuses, and hashes of the verbatim answers and log excerpts.

```text
$ python -B -m unittest discover -s day-11/semver-next/scripts -p test_next_version.py
Ran 18 tests
OK
$ skills-ref validate day-11\semver-next
Valid skill: day-11\semver-next
```

Input 4 separated the runs most clearly. The baseline recommended a new release candidate. The script returned exit 3 with no version, and the skill asked which stable line to use. For input 3, the same bytes always yield `0.10.0`, even though the baseline chose `1.0.0`. The [initial skill run](harness/initial/3-skill.jsonl) got the tag right but omitted the policy explanation. The final run included it after an instruction change. The script fixes the arithmetic and exit behavior. The explanation and follow-up question still depend on the response.

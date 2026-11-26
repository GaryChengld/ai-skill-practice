# Follow-up evaluation rubric

Run input 5 with the same release-tag prompt and model as the original fixtures. Pass `0.9.3` as the current version. The CLI must exit 0 with `next: 0.9.4`, `bump: patch`, and `major_zero_shift: true`.

| ID | Response check |
| --- | --- |
| 5a | Recommends `0.9.4` and identifies a patch bump. |
| 5b | Identifies the archived-items feature and explains that this policy maps features to patch bumps at major zero. |

Keep the original four response checklists. Score the no-skill response against the same rubric and record what it actually recommends.

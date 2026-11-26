# Frozen evaluation rubric

Use the same ordinary release-tag prompt and model for the skill and no-skill sessions. Supply the last tag from `versions.json` and the named commit file. Judge each check independently and accept equivalent wording. Score the answer separately from the execution and source-read checks in the harness.

| Input | Expected CLI result | ID | Response check |
| --- | --- | --- | --- |
| 1 | Exit 0, `v1.5.0`, minor | 1a | Recommends `v1.5.0` and identifies a minor bump. |
| 1 | Exit 0, `v1.5.0`, minor | 1b | Identifies the CSV reporting feature as decisive. |
| 1 | Exit 0, `v1.5.0`, minor | 1c | Identifies the unparsed `Tidy report snapshots` commit and says it was ignored. |
| 2 | Exit 0, `2.0.0`, major | 2a | Recommends `2.0.0` and identifies a major bump. |
| 2 | Exit 0, `2.0.0`, major | 2b | Identifies the `fix(api)` authorization change and its `BREAKING CHANGE:` footer as decisive. |
| 3 | Exit 0, `0.10.0`, minor | 3a | Recommends `0.10.0` and identifies a minor bump. |
| 3 | Exit 0, `0.10.0`, minor | 3b | Identifies the `feat(config)!` header and explains that a breaking change at major zero raises the minor version. |
| 4 | Exit 3, no next version | 4a | Identifies the current tag as a prerelease and declines to compute a next version from it. |
| 4 | Exit 3, no next version | 4b | Asks which stable tag or stable version line to continue. |
| 4 | Exit 3, no next version | 4c | Proposes no next version or release tag, including conditional recommendations. |

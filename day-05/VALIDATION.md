# Reference validation

Tested 2026-10-24 on Windows, Python 3.12: PyPI package `skills-ref==0.1.1`, executable `agentskills` (not the older source checkout's `skills-ref`).
Installation in a disposable virtual environment outside the repository:
```powershell
python -m venv $env:TEMP/day05-venv
& $env:TEMP/day05-venv/Scripts/python.exe -m pip install skills-ref
# Installed version: 0.1.1; use that interpreter's Scripts/agentskills.exe below.
```
The five original HEAD snapshots also passed when copied to correctly named temporary directories. After repairs, run `agentskills validate <directory>` for each directory; actual stdout (all exit 0):
```text
Valid skill: day-01\conventional-commits
Valid skill: day-02\release-notes
Valid skill: day-02\competitors\pr-description
Valid skill: day-03\incident-postmortem
Valid skill: day-04\stale-branches
```

Each day-04 YAML example replaced the frontmatter of a separate temporary `stale-branches/SKILL.md`; all temporary cases were removed afterward. The compatibility placeholder was expanded to exactly 501 ASCII characters.
| Case | Exit | Actual result |
| --- | --- | --- |
| Numeric and boolean metadata values | 0 | Missed: Valid skill |
| Compatibility, 501 characters | 1 | Caught: exceeds 500 character limit |
| allowed-tools YAML list | 0 | Missed: Valid skill |
| Stale_Branches name | 1 | Caught: lowercase, characters, directory mismatch |
| branch-audit in stale-branches directory | 1 | Caught: directory mismatch |
| Bash(git:*) broad permission | 0 | Accepted: schema-legal, unsafe for this skill |
| Extra platform field disable-model-invocation | 1 | Caught: unexpected field (additional probe) |

The reference validator checks selected structural constraints, not every specification requirement: metadata value types and allowed-tools types need separate checks. Passing also says nothing about safety, routing precision, rationale, or evaluation contamination; the broad Git grant is a quality failure rather than a schema violation. Platform extensions may work in one client while failing this six-field portable schema.

The first single-line day-01 edit failed YAML parsing at the embedded `: `; removing the redundant format parenthesis fixed it. The message format remains in the body.
Generated `catalog.xml` by capturing stdout bytes without editing: `agentskills to-prompt day-01/conventional-commits day-02/release-notes day-02/competitors/pr-description day-03/incident-postmortem day-04/stale-branches`.
Review follow-up: all five revised skills passed validate again; lint includes the day-01 150-line cap, all body/report limits pass, and the unchanged catalog still matches fresh CLI stdout byte-for-byte. Independent routing cases are recorded separately in ROUTING-CHALLENGE.md.
Sources: [specification](https://agentskills.io/specification), [PyPI CLI documentation](https://pypi.org/project/skills-ref/), [upstream reference implementation](https://github.com/agentskills/agentskills/tree/main/skills-ref).

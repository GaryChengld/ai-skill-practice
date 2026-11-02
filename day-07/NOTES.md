# Day-07 notes

## Day-06 follow-up
Ran the unchanged final `day-06/incident-postmortem` in a sixth independent fresh session, using the same ordinary request and original `tests/input-d.md` from disk.
- Session: `01a19a2d-91e3-7d61-882c-a6c7d5c286a5`; no output expectations or table-repair feedback were supplied.
- [Raw final response](dependency-fix-plan/tests/output-day06-d.md) is retained without edits; [harness read evidence](dependency-fix-plan/tests/harness/READS.md) confirms SKILL.md and only references/rca-methods.md.
- All four Action Items rows have five cells: `[5, 5, 5, 5]`. Owner and Due have separate TBD cells. A Detect action addresses the observed monitoring gap.
- The extractor counts unescaped pipe delimiters in the Action Items data rows; its [manifest](dependency-fix-plan/tests/harness/manifest.json) records the counts, source-log hash, and raw tool-result call IDs. This single success closes the requested rerun, not a general table-format reliability claim.

## Validation and scope
The previous temporary validator environment was incomplete, so a new temporary environment was created outside the repository:
```text
python -m venv <temporary-venv>
<temporary-venv>/Scripts/python.exe -m pip install skills-ref==0.1.1
<temporary-venv>/Scripts/agentskills.exe validate day-07/dependency-fix-plan
```
Result: `Valid skill: day-07\dependency-fix-plan`. Skill-creator's `quick_validate.py` also passed. Day-04's optional same-tip edge-case clarification now says to hold for owner review and not recommend deletion; its official validation also passed. Day-06's skill was not edited.

The skill and references were checked against the [Agent Skills specification](https://agentskills.io/specification), [domain organization guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and official manager sources linked in each domain file. The references distinguish manager versions instead of assuming pnpm configuration is identical across releases.
All scanner fixtures are synthetic. Evaluation tasks produced plans only; their proposed installation, scanner, and behavior-test commands were not executed. Sandbox startup failures and unsuccessful reads remain in the tool excerpts and do not count as file loads.

## Review follow-up
Removed the test-specific synthetic-fixture instruction from SKILL.md and adopted the suggested advisory-source rule and description keywords. Body remains 48 lines; references and routing rules were not changed.
Three additional fresh sessions received the same ordinary request format as the original runs. The prompts did not mention testing, desired branches, expected reads, or previous results. Inputs O and H make the available remediation options explicit as repository facts, but do not prescribe the answer.

| Case | Output behavior observed | Result |
| --- | --- | --- |
| [M2](dependency-fix-plan/tests/output-m2.md) | Reads SKILL.md only; leaves ownership Unknown and asks for the scanner path or chain before proposing a file edit. | Pass |
| [O](dependency-fix-plan/tests/output-o.md) | Places a version-qualified parent override in root package.json, keeps the workspace declaration unchanged, and regenerates the root lock. Flags untested compatibility and removes the override only after a compatible parent upgrade passes checks without it. | Pass |
| [H](dependency-fix-plan/tests/output-h.md) | Rejects an incompatible interpreter/API upgrade and ineffective pip constraint; defers with custom uploads disabled, schedules-team ownership, and review on the supplied 2026-11-09 date. Keeps the finding open and states residual exposure. | Pass |

Original M is an easy positive ownership case, not proof of ambiguity handling; M2 adds that missing negative case. O covers one npm override proposal and H one Python deferral proposal, not execution or every domain's override mechanisms. H also flags shortened coordinate aliases in its input as an open question; its conclusion remains conditional on the supplied graph.
Evidence and exact session prompts are in [harness-review](dependency-fix-plan/tests/harness-review/READS.md). Extraction uses `python day-07/dependency-fix-plan/tests/collect-harness.py --review`; baseline artifacts remain intact, and default extraction compares historical file contents at commit `e50e15e` rather than the revised skill.
The M2 Windows TYPE response interleaved stderr filename banners into stdout mid-description. Complete content matches after removing those banners for matching only. Excerpts and outputs remain byte-for-byte/raw-text faithful to the harness; no model was given repair feedback. Validation passed after the two SKILL.md edits.

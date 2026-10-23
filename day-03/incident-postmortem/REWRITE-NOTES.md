# Rewrite Notes

## Problems and changes

| BEFORE problem | Category | Rewrite |
| --- | --- | --- |
| "Helps with incidents" gives no routing boundary. | vague | Name retrospective deliverables and exclude live response and status-page updates. |
| Definitions of incident and postmortem consume space. | known-to-agent | Remove them and spend the space on evidence handling. |
| "Thorough", "high-quality", and "professional" are not observable steps. | vague | Provide a compact template and a final evidence checklist. |
| "NEVER skip any section" demands content even without evidence. | over-constrained | Keep core headings but write Unknown or TBD when needed. |
| Local, UTC, and relative times have equal status. | menu-without-default | Default to dated UTC timestamps and record the conversion basis. |
| Four analysis methods have no default. | menu-without-default | Default to evidence-limited 5 Whys; allow a causal tree for branching failures. |
| Asking who caused it invites blame without improving diagnosis. | missing-why | Analyze system conditions; explain that blame discourages reporting. |
| Exactly five actions is unrelated to incident needs. | over-constrained | Let supported gaps determine count; require tracking fields and success criteria. |
| Filling gaps with estimates manufactures a complete-looking record. | invents-data | Preserve source estimates as unconfirmed and use Unknown/TBD for missing facts. |
| "Short" and "everything in detail" compete without priorities. | contradiction | Use concise sections, put supporting evidence in Appendix, and preserve material uncertainty. |

## Freedom map (decided before drafting)

| New body section | Freedom | Reason |
| --- | --- | --- |
| Evidence and time | low | Fabricated facts or inconsistent clocks corrupt the incident record. |
| Analysis | high | Causal depth and branching depend on evidence; a default method guides without forcing an answer. |
| Actions | medium | Choose relevant actions and count; owner, due date, type, and success criterion are fixed fields. |
| Boundaries | medium | Ongoing incidents, sensitive details, and conflicting reports require context-sensitive handling within explicit safeguards. |
| Gotchas | low | Preserve distinctions that commonly produce false certainty about time, impact, and causality. |
| Output template | medium | Keep comparable core sections while varying detail to match the evidence. |
| Before returning | low | Check factual integrity and required fields consistently before delivery. |

## Evaluation plan

Freeze the rewrite before testing. Use two fresh agents with no inherited conversation, one per variant, with only that variant and the identical input. Use the same request and inherited model settings; allow no tools or file access. Save returned Markdown unchanged and compare observed behavior, including improvements the baseline already achieves. One paired run is illustrative, not a controlled performance estimate.

## References

- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices) informed the defaults, freedom levels, template, and self-check.
- [NIST DST rules](https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst) place October 14, 2026 within daylight saving time; the local system's Pacific timezone conversion independently returned 16:12Z for 09:12 PT.

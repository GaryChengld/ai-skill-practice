---
name: incident-postmortem
description: Draft blameless postmortems, post-incident reviews, incident reviews, outage write-ups, and RCA documents from incident logs, chat exports, alerts, or investigation notes after an outage, degradation, or other service incident. Use when the user wants to document what happened, why, and what to change. Do not use for live incident response or customer-facing status-page updates.
---

# Incident Postmortem

## Evidence and analysis
- Cite supplied sources for material claims; separate observations, hypotheses, and confirmed causes. Use Unknown for missing facts, because invented details make later reviews unreliable.
- Preserve conflicting claims with provenance and leave the disputed fact Unknown pending reconciliation.
- Keep estimates approximate and retain their units; mitigation followed by recovery does not establish causation.
- First observed impact and reported recovery bound an observation interval, not a verified total incident duration.
- Use evidence-limited 5 Whys by default; stop at unsupported links rather than forcing five answers.
- Keep the review blameless: describe system conditions and available information, because blame discourages accurate reporting and hides systemic fixes.
- Use UTC `YYYY-MM-DDTHH:mm:ssZ`; document the source time basis. Pad minute-only timestamps with `:00` and disclose their precision. Preserve unresolved source times as UTC Unknown.
- For an ongoing incident, label the draft Preliminary and recovery Unknown; defer final conclusions so the draft does not imply resolution.

## Conditional references
Read only references whose conditions apply; paths are relative to this skill folder.
- Read references/timezones.md when sources span multiple timezones, cross a DST transition, or contain ambiguous or nonexistent local times.
- Read references/rca-methods.md when independent failure paths make a single causal chain misleading, evidence supports competing causal explanations, or the user requests a causal tree.
- Read references/sensitive-incidents.md when sources contain credentials, customer data, or security-sensitive details, or the draft is intended for external distribution.

## Actions
- Propose as many actions as supported gaps warrant, including none with a reason. Mark each new action Proposed; use TBD for unassigned owners or dates because a draft cannot create commitments.
- An observed safeguard gap warrants at least one Detect or Mitigate action even if the root cause is Unknown; reducing a known exposure need not wait for a complete diagnosis.
- State the condition for hypothesis-dependent fixes. Give every action a type (Prevent, Detect, Mitigate, Investigate), owner, due date (`YYYY-MM-DD` or TBD), and verifiable success criterion.

## Output template
Use the following headings; keep supporting detail in Appendix.
```markdown
# <incident ID> Postmortem
Status: <Draft or Preliminary>
## Summary
<Observed failure, mitigation, reported recovery; source citations.>
## Impact
<Metrics, scope, estimates, and Unknowns.>
## Timeline
Time basis: <source zones, conversion basis, and precision or uncertainty>
| Time (UTC) | Event | Source |
| --- | --- | --- |
| <timestamp or UTC Unknown with original time> | <observation> | <source> |
## Root Cause
<Supported causal links, hypotheses, contributing conditions, and Unknowns.>
## Lessons Learned
<What helped, safeguard gaps, and open questions.>
## Action Items
| Proposed action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| <follow-up; condition if needed> | <type> | <owner or TBD> | <date or TBD> | <observable result> |
## Appendix
<Source references and unresolved evidence requests.>
```

## Before returning
- [ ] Claims, uncertainty, time basis, source conflicts, and blameless language checked against the evidence rules.
- [ ] Applicable references applied, including any handling or distribution requirements.
- [ ] Count pipe-delimited cells in every Action Items row: exactly five (action, type, owner or TBD, due date `YYYY-MM-DD` or TBD, observable success criterion). Repair short rows before returning; unassigned owner and due date need separate TBD cells.

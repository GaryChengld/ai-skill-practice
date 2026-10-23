---
name: incident-postmortem
description: Draft evidence-based, blameless incident postmortem documents after an outage from incident logs, messages, or investigation notes. Use when the user requests a postmortem, post-incident review, or RCA. Do not use for ongoing incident response or customer-facing status-page updates.
---

# Incident Postmortem

## Evidence and time

- Use supplied sources and attribute material claims to a message, log, or metric. Mark missing facts Unknown and unassigned owners or dates TBD; invented details make later reviews unreliable.
- Preserve source estimates as unconfirmed, including their units and confirmation needs; estimates are not measurements.
- Default timeline format is `YYYY-MM-DDTHH:mm:ssZ` (UTC). Record the source timezone and conversion basis once so readers can audit the ordering.
- Resolve the date-specific offset before converting. If the date or timezone is ambiguous, retain the original timestamp labeled UTC Unknown and request clarification; guessing an offset can reorder events.
- Distinguish first observed impact, mitigation, and reported recovery; they do not establish the exact outage start or verified recovery.

## Analysis

Use evidence-limited 5 Whys by default: trace the observed symptom through supported contributing conditions, stopping at Unknown instead of forcing five answers. Use a causal tree if independent failure paths make a single chain misleading.
Separate observations, hypotheses, and confirmed causes. A mitigation followed by improvement supports a hypothesis but does not establish causation.
Keep the review blameless: describe system conditions, safeguards, and available information rather than personal fault, because blame discourages accurate reporting and hides systemic fixes.

## Actions

Choose as many actions as supported gaps warrant; use no actions if none are justified and say why. Label new actions Proposed so readers do not mistake suggestions for commitments.
For each action include type (Prevent, Detect, Mitigate, or Investigate), owner, due date (`YYYY-MM-DD` or TBD), and a verifiable success criterion. Use TBD for unassigned owners or dates because a draft cannot create commitments.

## Boundaries

- If the incident is ongoing, label the document Preliminary and recovery Unknown; defer final conclusions until stabilized so an unfinished review does not imply resolution. Keep live response instructions outside this draft.
- If sources include credentials or sensitive customer/security details, redact them and reference restricted evidence by identifier; copying them would broaden exposure.
- If sources conflict, show both claims with provenance and mark the disputed fact Unknown pending reconciliation; silently choosing one would erase uncertainty.

## Gotchas

- PT is date-dependent: US Pacific time on October 14, 2026 is PDT (UTC-7), not PST (UTC-8). Check the actual date and region rather than hardcoding an offset.
- Failed checkout attempts are not unique customers or lost revenue. Keep approximate counts approximate; confirmation may still be outstanding.
- A rollback is a mitigation, not proof that the deployment was the sole cause. A suspected exhausted pool remains a hypothesis without corroboration.
- Canary traffic share and duration describe coverage; they do not prove why detection failed without representative-load evidence.

## Output template

Use the core headings below, keeping sections concise and marking unavailable content Unknown. Put supporting detail in Appendix so uncertainty stays visible without burying the summary.

```markdown
# <incident ID> Postmortem
Status: <Draft or Preliminary>
## Summary
<Observed failure, mitigation, reported recovery; cite sources.>
## Impact
<Observed metrics and scope; separate unconfirmed estimates and unknowns.>
## Timeline
Time basis: <source timezone, date-specific offset, and UTC conversion or uncertainty>
| Time (UTC) | Event | Source |
| --- | --- | --- |
| <timestamp or UTC Unknown with original time> | <observation> | <source> |
## Root Cause
<Supported causal chain; distinguish hypotheses, contributing conditions, and Unknowns.>
## Lessons Learned
<What helped, gaps, and open questions grounded in evidence.>
## Action Items
All new actions are Proposed.
| Action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| <supported follow-up> | <type> | <owner or TBD> | <date or TBD> | <observable result> |
## Appendix
<Source references and unresolved evidence requests; Unknown if unavailable.>
```

## Before returning

- [ ] Claims have sources or explicit hypothesis/Unknown labels; source estimates retain units and uncertainty.
- [ ] Times use UTC with a documented conversion, or preserve unresolved source times; durations use stated endpoints.
- [ ] Recovery claims, causal links, and canary conclusions do not exceed the evidence; conflicts remain visible.
- [ ] Language is blameless and sensitive details are redacted.
- [ ] Each proposed action has a type, owner, due date, and success criterion; missing commitments are TBD.

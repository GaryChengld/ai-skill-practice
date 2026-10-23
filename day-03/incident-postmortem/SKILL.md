---
name: incident-postmortem
description: Draft blameless postmortems, post-incident reviews, incident reviews, outage write-ups, and RCA documents from incident logs, chat exports, alerts, or investigation notes after an outage, degradation, or other service incident. Use when the user wants to document what happened, why, and what to change. Do not use for live incident response or customer-facing status-page updates.
---

# Incident Postmortem

## Evidence and time

- Attribute material claims to supplied sources and distinguish observations, hypotheses, and confirmed causes. Mark missing facts Unknown rather than inventing them, because false certainty makes later reviews unreliable.
- Default timeline format is `YYYY-MM-DDTHH:mm:ssZ` (UTC). Record the conversion basis once; for ambiguous dates or zones, retain the original time labeled UTC Unknown and request clarification, because guessing can reorder events.

## Analysis

Use evidence-limited 5 Whys by default: trace the observed symptom through supported contributing conditions, stopping at Unknown instead of forcing five answers. Use a causal tree if independent failure paths make a single chain misleading.
Keep the review blameless: describe system conditions, safeguards, and available information rather than personal fault, because blame discourages accurate reporting and hides systemic fixes.

## Actions

Choose as many actions as supported gaps warrant; use no actions if none are justified and say why. Label new actions Proposed so readers do not mistake suggestions for commitments.
An observed safeguard gap, such as a late alert or a canary that missed the failure, is evidence by itself: propose at least one Detect or Mitigate action for it even while the root cause is Unknown, because reducing a known exposure need not wait for a complete diagnosis.
When a fix depends on an unconfirmed hypothesis, state the condition, for example "If retry amplification is confirmed, cap payment-client retries and add backoff." This keeps a useful proposal separate from a confirmed remedy.
For each action include type (Prevent, Detect, Mitigate, or Investigate), owner, due date (`YYYY-MM-DD` or TBD), and a verifiable success criterion. Use TBD for unassigned owners or dates because a draft cannot create commitments.

## Boundaries

- If the incident is ongoing, label the document Preliminary and recovery Unknown; defer final conclusions until stabilized so an unfinished review does not imply resolution. Keep live response instructions outside this draft.
- If sources include credentials or sensitive customer/security details, redact them and reference restricted evidence by identifier; copying them would broaden exposure.
- If sources conflict, show both claims with provenance and mark the disputed fact Unknown pending reconciliation; silently choosing one would erase uncertainty.

## Gotchas

- Convert named local zones using the event date and region's timezone rules, preferably a timezone database. Default "PT" to US Pacific and state that interpretation unless context conflicts; the date determines PDT (UTC-7) or PST (UTC-8), not the label alone. For minute-precision sources, keep the default format with `:00` padding and state that seconds were not observed, so formatting does not imply extra precision.
- Estimates are not measurements: preserve their units, approximate status, and confirmation needs. Failed checkout attempts are not unique customers or lost revenue.
- A rollback is a mitigation, not proof that the deployment was the sole cause. A suspected exhausted pool remains a hypothesis without corroboration.
- A canary that missed the failure establishes a detection gap; its traffic share and duration alone do not establish why. Propose a measurable safeguard improvement without presenting an unverified mechanism as fact.
- First observed impact and reported recovery bound an observation interval, not a verified outage duration; retain that distinction when calculating elapsed time.

## Output template

Use these core headings concisely; place supporting detail in Appendix so it does not bury the summary.

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
| Action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| <supported follow-up> | <type> | <owner or TBD> | <date or TBD> | <observable result> |
## Appendix
<Source references and unresolved evidence requests; Unknown if unavailable.>
```

## Before returning

- [ ] Evidence and Gotchas checks pass; source conflicts and unresolved questions remain visible.
- [ ] Times use UTC with a documented conversion, or preserve unresolved source times.
- [ ] Language is blameless and sensitive details are redacted.
- [ ] Each proposed action has a type, owner, due date, and success criterion; missing commitments are TBD. Observed safeguard gaps have a Detect or Mitigate action; hypothesis-dependent fixes state their conditions.

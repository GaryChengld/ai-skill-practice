# INC-826 Postmortem
Status: Draft

## Summary
Document-search replicas reported stale results after their update subscription stopped. An audit found that the scheduler configuration omitted the lease-renewal task, and the operator confirmed that the subscription lease had expired. The operator enabled a new lease at 2026-11-01T06:05:00Z; all replicas reported current results at 2026-11-01T06:12:00Z. Recovery followed the intervention, but the supplied evidence does not independently establish that the new lease caused recovery. [B1, B2, B3, B5]

## Impact
Search results were stale on the reporting replicas. The affected document count, affected users, request volume, and verified start of impact are Unknown. [B1, B6]

First observed impact at 2026-11-01T05:50:00Z and reported recovery at 2026-11-01T06:12:00Z bound a 22-minute observation interval, not a verified total incident duration. B4's unresolved timestamp could place its stale-result observation after reported recovery; the chronology and any implication for recovery remain Unknown pending reconciliation. [B1, B3, B4]

## Timeline
Time basis: All dated events use 2026-11-01. Sources span America/New_York's backward DST transition and Asia/Singapore. Clocks are synchronized, and supplied numeric offsets are reliable. Each supported timestamp was converted independently using its supplied offset. Source timestamps have minute precision; `:00` is padding, not evidence of second-level precision. B4 has no offset and remains UTC Unknown. [Source packet]

| Time (UTC) | Event | Source |
| --- | --- | --- |
| 2026-11-01T05:50:00Z | Replicas reported stale results after the update subscription stopped. Original: 01:50 America/New_York, UTC-04:00. | B1 |
| 2026-11-01T06:05:00Z | Operator confirmed the lease had expired and enabled a new lease. Original: 14:05 Asia/Singapore, UTC+08:00. | B2 |
| 2026-11-01T06:12:00Z | All replicas reported current results. Original: 01:12 America/New_York, UTC-05:00. | B3 |
| UTC Unknown — original 2026-11-01 01:55 America/New_York, offset unrecorded | Hand-written note: “replica check still stale.” Possible instants are 2026-11-01T05:55:00Z or 2026-11-01T06:55:00Z. It could fall between B1 and B2 or after B3; this row implies no chronological placement. | B4 |
| UTC Unknown — source has no timestamp | Lease audit confirmed no renewal was scheduled because the scheduler configuration omitted the lease-renewal task. | B5 |
| UTC Unknown — source has no timestamp | No lease-expiry alert existed; affected document count was unknown. | B6 |

## Root Cause
The supported causal finding is that omission of the lease-renewal task from scheduler configuration left no renewal scheduled. The lease was confirmed expired, and replicas reported stale results after their update subscription stopped. These findings support an expired, unrenewed subscription lease as the failure mechanism; direct evidence tying lease expiry to the precise subscription-stop instant is not supplied. The reason the task was omitted is Unknown. [B1, B2, B5]

Evidence-limited 5 Whys:

1. Why were search results stale? Replicas reported stale results after their update subscription stopped; the precise propagation mechanism is not documented. [B1]
2. Why did the subscription stop? Lease expiry is the supported explanation from the operator's confirmation, but a directly correlated stop/expiry record is not supplied. [B2]
3. Why was the lease not renewed? The audit confirmed no renewal was scheduled because the configuration omitted the renewal task. [B5]
4. Why was the task omitted? Unknown; the supplied evidence does not support a further causal link.

The absence of a lease-expiry alert was an observed detection gap. Its effect on detection time or impact cannot be quantified from the packet. [B6]

## Lessons Learned
Enabling a new lease was followed by reports of current results, providing a useful recovery observation without proving intervention causality. The configuration omitted a required renewal task, and no lease-expiry alert existed. Renewal scheduling and expiry detection both need safeguards. [B2, B3, B5, B6]

Reliable offsets allow the main events to be ordered across the backward clock transition. The unoffset hand-written note cannot yet be reconciled with reported recovery. Recording UTC or an explicit numeric offset would make future evidence easier to interpret. [B1–B4]

## Action Items
All actions are Proposed. Ownership and deadlines remain unassigned, as stated in the source packet.

| Proposed action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| Proposed — Add the lease-renewal task to scheduler configuration and validate that it executes before expiry. | Prevent | TBD | TBD | Configuration validation detects an omitted task, and a controlled lease lifecycle shows successful renewal before expiry. |
| Proposed — Add an alert for an approaching or expired subscription lease and test delivery to the response channel. | Detect | TBD | TBD | A controlled expiry-risk test triggers the alert within its documented threshold and produces a delivered notification. |
| Proposed — Investigate how the scheduler configuration lost or omitted the renewal task and identify any missing configuration checks. | Investigate | TBD | TBD | Review documents the evidence-backed configuration history and identified check gaps, or explicitly records what remains Unknown. |
| Proposed — Reconcile B4's timestamp and stale-result observation with B3's recovery report. | Investigate | TBD | TBD | Review records B4's offset or correlated event, or documents that chronology remains unresolved and its effect on the recovery conclusion. |

## Appendix
Source references: `tests/input-b.md`, INC-826 source packet. B1: stale replicas/subscription stopped; B2: expired lease/new lease enabled; B3: current results reported; B4: ambiguous hand-written stale-result note; B5: lease audit/scheduler omission; B6: missing alert/unknown document count. The packet states the incident is resolved and follow-up ownership and deadlines are unassigned.

Unresolved evidence requests: subscription-stop and lease-expiry records; scheduler configuration history and validation evidence; B4's original record, offset, or correlated event; impact counts and earliest affected timestamp; recovery verification sufficient to reconcile B3 with B4.

# INC-826 Postmortem

Status: Draft  
Distribution: Internal

## Summary

Document-search replicas reported stale results after their update subscription stopped. Investigation confirmed an expired subscription lease and a scheduler configuration that omitted the lease-renewal task. An operator enabled a new lease; all replicas subsequently reported current results. The sequence supports recovery following mitigation but does not independently establish causation. [B1–B3, B5]

A handwritten stale-results observation has an ambiguous timestamp and could conflict with reported recovery. [B4]

## Impact

- Search results were stale; the affected document count is **Unknown**. [B1, B6]
- Affected users, query volume, and business impact are **Unknown**.
- First observed impact at `2026-11-01T05:50:00Z` and reported recovery at `2026-11-01T06:12:00Z` bound a **22-minute observation interval**, not a verified total incident duration. [B1, B3]
- Total duration and whether degradation persisted or recurred after reported recovery are **Unknown**, pending reconciliation of B4.

## Timeline

Time basis: Source date is 2026-11-01. America/New_York crossed the backward DST transition. Each timestamp was converted independently using its supplied, reliable numeric offset; Singapore used UTC+08:00. Clocks were synchronized. Source timestamps have minute precision; `:00` seconds are padding. B4 has no offset and cannot be placed conclusively.

| Time (UTC) | Event | Source |
| --- | --- | --- |
| 2026-11-01T05:50:00Z | Replicas reported stale results after the update subscription stopped. Original: 01:50 America/New_York, UTC−04:00. | B1 |
| 2026-11-01T06:05:00Z | Operator confirmed lease expiry and enabled a new lease. Original: 14:05 Asia/Singapore, UTC+08:00. | B2 |
| 2026-11-01T06:12:00Z | All replicas reported current results. Original: 01:12 America/New_York, UTC−05:00. | B3 |
| UTC Unknown — original: 2026-11-01 01:55 America/New_York | Handwritten note: “replica check still stale.” Possible instants are `2026-11-01T05:55:00Z` or `2026-11-01T06:55:00Z`. This row has no established chronological position. | B4 |

## Root Cause

The supported failure mechanism is an expired subscription lease, with no renewal scheduled because the scheduler configuration omitted the lease-renewal task. Replicas reported stale results after their update subscription stopped. [B1, B2, B5]

Evidence-limited 5 Whys:

1. **Why were search results stale?** Replicas reported staleness after the update subscription stopped. [B1]
2. **Why did the subscription stop?** Lease expiry is the supported explanation; the operator confirmed expiry. Direct subscription lifecycle logs were not supplied. [B2]
3. **Why was renewal absent?** The scheduler configuration omitted the renewal task; the audit confirmed no renewal was scheduled. [B5]
4. **Why was the task omitted?** **Unknown.** The evidence does not establish how the omission occurred or escaped validation.

The absence of a lease-expiry alert was a detection gap; its effect on detection time is **Unknown**. [B6]

## Lessons Learned

The lease audit identified a concrete configuration gap that can be addressed. [B5] Expiry monitoring was absent, leaving a known exposure even while deeper investigation remains open. [B6]

Explicit offsets made the main timeline resolvable across DST. The handwritten note lacked that information. Its earlier interpretation precedes mitigation; its later interpretation conflicts with the all-replicas recovery report. Neither interpretation is preferred without evidence. [B2–B4]

## Action Items

| Proposed action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| Proposed: Add the lease-renewal task and validate scheduling during configuration checks. | Prevent | TBD | TBD | Validation rejects configurations missing the task; a controlled test demonstrates renewal before expiry. |
| Proposed: Add advance lease-expiry and failed-renewal alerts. | Detect | TBD | TBD | A controlled expiry/renewal-failure test produces an actionable alert before subscription loss. |
| Proposed: Document and exercise lease restoration and replica-freshness verification. | Mitigate | TBD | TBD | An exercise restores the subscription and verifies current results on every replica. |
| Proposed: Reconcile B4 with timestamped replica and subscription records. | Investigate | TBD | TBD | Review records establish its occurrence and reconcile the recovery claim, or explicitly document that evidence remains unavailable. |
| Proposed: Investigate how the renewal task was omitted and measure impact from available telemetry. | Investigate | TBD | TBD | Findings document the configuration history, supported impact estimates, and remaining evidence gaps. |

## Appendix

Source packet: [input-b.md](/C:/Workspaces/ai-skill-practice/day-06/incident-postmortem/tests/input-b.md).

Source identifiers B1–B6 refer to the packet’s labeled observations, operator report, handwritten note, audit, and monitoring findings.

Outstanding evidence requests: subscription lifecycle logs; scheduler configuration history; B4’s offset or correlated timestamp; timestamped replica-freshness records around both possible B4 instants; and affected-document, query, and user counts.

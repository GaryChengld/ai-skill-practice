# INC-482 Postmortem

Status: Draft

## Summary

On 2026-10-14 at 09:12 PT, an alert reported checkout p95 latency of 8 seconds and a 23% error rate. Deployment `7f3a`, which added a payment-client retry loop, was rolled back at 09:30 PT. Errors were reported as dropping at 09:34 PT, followed by “all green” at 09:41 PT. The cause and the rollback’s causal role remain unconfirmed. [S1, S4–S6]

## Impact

- Observed: checkout p95 latency of 8 seconds and a 23% error rate at the alert time. Measurement windows and affected scope are Unknown. [S1]
- Unconfirmed estimate: approximately 1,200 failed checkout attempts, pending Finance confirmation. This is not a count of unique customers or a measure of lost revenue. [S7]
- The first alert and reported recovery bound a 29-minute observation interval. Actual impact onset, verified recovery time, and outage duration are Unknown. [S1, S6]

## Timeline

Time basis: Sources give minute-precision times in “PT” on 2026-10-14 without specifying the region or UTC offset. UTC conversion remains Unknown pending confirmation. If US Pacific time is confirmed, this date uses PDT (UTC−7). Seconds were not observed; `:00` below is padding only.

| Time (UTC) | Event | Source |
| --- | --- | --- |
| UTC Unknown — 2026-10-14 09:12:00 PT | Alert reports checkout p95 latency of 8 seconds and error rate of 23%. | S1 |
| UTC Unknown — 2026-10-14 09:15:00 PT | Maria acknowledges investigation. | S2 |
| UTC Unknown — 2026-10-14 09:21:00 PT | Maria suspects connection-pool exhaustion on `orders-db`. | S3 |
| UTC Unknown — 2026-10-14 09:30:00 PT | Deployment `7f3a`, described as adding a payment-client retry loop, is rolled back. | S4 |
| UTC Unknown — 2026-10-14 09:34:00 PT | Errors reported to be dropping. | S5 |
| UTC Unknown — 2026-10-14 09:41:00 PT | “All green” reported; confirming metrics were not supplied. | S6 |

## Root Cause

**Confirmed root cause: Unknown.**

Evidence-limited causal analysis:

1. **Why were checkout attempts failing or slow?** The alert confirms elevated latency and errors, but the failing requests’ underlying mechanism is Unknown. [S1]
2. **Was database connection-pool exhaustion responsible?** This was an investigation hypothesis. No connection counts, pool-wait metrics, traces, or database logs were supplied to corroborate it. [S3]
3. **Did payment retries contribute to exhaustion or checkout failures?** The rolled-back deployment added a retry loop, but retry amplification and its relationship to `orders-db` are unconfirmed. Recovery reports followed rollback; that sequence does not establish the deployment as the sole cause. [S4–S6]

The causal chain stops here because supporting evidence is unavailable.

The supplied notes indicate that the canary missed the failure and describe its configuration as 2% of traffic for five minutes. This establishes a detection gap; it does not establish why detection failed. [S8]

## Lessons Learned

- An alert surfaced the degradation, and investigation was acknowledged three minutes later. Detection delay from actual impact onset is Unknown. [S1, S2]
- Rollback preceded reported improvement and recovery, making it a useful mitigation candidate for investigation. Its effectiveness requires metric confirmation. [S4–S6]
- Canary coverage needs validation against this failure mode. Traffic share and duration alone cannot explain the miss. [S8]
- Impact reporting needs confirmed attempt counts, customer scope, and recovery evidence. [S6, S7]

## Action Items

| Action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| Proposed: Investigate deployment timing, retry behavior, database pool utilization, and checkout traces. | Investigate | TBD | TBD | A source-linked causal analysis confirms or rejects each suspected link and explicitly records remaining Unknowns. |
| Proposed: Validate and improve canary detection using representative checkout traffic and controlled latency/error degradation. | Detect | TBD | TBD | Repeatable tests demonstrate that documented checkout latency and error gates block promotion when injected degradation exceeds their thresholds. |
| Proposed: Reconcile checkout impact and recovery with monitoring data and Finance. | Investigate | TBD | TBD | The review records the counting method, confirmed failed-attempt count, available customer scope, impact window, and recovery metrics; unavailable facts remain Unknown. |

## Appendix

All references are from the supplied Slack export for `#inc-482`, dated 2026-10-14:

| Reference | Evidence |
| --- | --- |
| S1 | 09:12 PT alert: checkout p95 latency 8s, error rate 23%. |
| S2 | 09:15 PT, Maria acknowledges investigation. |
| S3 | 09:21 PT, Maria suspects an exhausted connection pool on `orders-db`. |
| S4 | 09:30 PT, rollback of deployment `7f3a`; deployment described as adding a payment-client retry loop. |
| S5 | 09:34 PT, errors reported as dropping. |
| S6 | 09:41 PT, “all green” reported. |
| S7 | Untimed note estimating approximately 1,200 failed checkouts, with Finance confirmation pending. |
| S8 | Untimed question about the canary miss; configuration stated as 2% traffic for five minutes. |

Unresolved evidence requests: confirm the region and UTC offset meant by “PT”; supply deployment and rollback completion times, monitoring windows and recovery metrics, retry and database telemetry, canary results and promotion criteria, and Finance’s impact reconciliation.

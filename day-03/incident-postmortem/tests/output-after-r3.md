# INC-482 Postmortem
Status: Draft

## Summary

Checkout p95 latency reached 8 seconds and the error rate reached 23% at the first recorded alert. Deployment `7f3a`, which added a payment-client retry loop, was rolled back. Errors subsequently declined, and “all green” was reported at 16:41 UTC. The root cause and the rollback’s causal role remain unconfirmed. [S1, S3–S5]

## Impact

- Observed checkout metrics: p95 latency of 8 seconds and a 23% error rate at 16:12 UTC. [S1]
- Unconfirmed estimate: approximately 1,200 failed checkout attempts, pending Finance confirmation. This is not a count of unique customers or a measure of lost revenue. [S6]
- The first recorded alert and reported recovery bound a 29-minute observation interval; actual impact onset, verified recovery time, and outage duration are Unknown.
- Affected customer count, geographic scope, and revenue impact are Unknown.

## Timeline

Time basis: Source times are dated 2026-10-14 and labeled PT, interpreted as US Pacific. That date uses PDT (UTC−07:00); seven hours were added for UTC. Source timestamps have minute precision; `:00` seconds are formatting only and were not observed.

| Time (UTC) | Event | Source |
| --- | --- | --- |
| 2026-10-14T16:12:00Z | Alert reported checkout p95 latency of 8 seconds and a 23% error rate. | S1 |
| 2026-10-14T16:15:00Z | Investigation acknowledged. | S2 |
| 2026-10-14T16:21:00Z | Investigator suspected connection-pool exhaustion on `orders-db`. | S3 |
| 2026-10-14T16:30:00Z | Deployment `7f3a`, described as adding a payment-client retry loop, was rolled back. | S4 |
| 2026-10-14T16:34:00Z | Errors were reported to be declining. | S5 |
| 2026-10-14T16:41:00Z | “All green” was reported; supporting recovery metrics were not supplied. | S5 |

## Root Cause

**Confirmed root cause: Unknown.**

Evidence-limited 5 Whys:

1. **Why did checkout degrade?** The alert establishes elevated latency and errors, but the underlying failure mechanism is Unknown. [S1]
2. **What condition might explain the degradation?** Connection-pool exhaustion on `orders-db` was suspected; no pool metrics, database logs, or traces were supplied to confirm it. [S3]
3. **Why might the pool have exhausted?** Unknown. Deployment `7f3a` added a payment-client retry loop, but retry amplification and its connection to database usage are unconfirmed hypotheses. [S4]

The chain stops at Unknown. Error reduction followed rollback, supporting rollback as the recorded mitigation; this sequence does not establish that the deployment was the sole cause. [S4–S5]

## Lessons Learned

- Investigation and rollback were recorded, followed by improving errors and reported recovery. [S2, S4–S5]
- The canary did not catch the failure, establishing a detection gap. Its reported configuration was 2% of traffic for five minutes; those settings alone do not establish why it missed the incident. [S7]
- The available record does not corroborate pool exhaustion, establish retry behavior during the incident, or quantify customer impact.

## Action Items

| Action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| Proposed: Reconstruct the failure using deployment timing, retry telemetry, checkout traces, and database connection metrics. | Investigate | TBD | TBD | Review documents which causal links are supported, rejected, or unresolved, including whether retry amplification and pool exhaustion occurred. |
| Proposed: Evaluate and improve canary detection using a representative checkout regression scenario. | Detect | TBD | TBD | A documented test reproduces the relevant latency/error regression and shows the canary alerting or blocking promotion before wider rollout; traffic and duration choices are justified by results. |
| Proposed: Reconcile the failed-checkout estimate with Finance and checkout records. | Investigate | TBD | TBD | A documented impact calculation states the time window, failed-attempt count, deduplication method, and any supported customer or revenue figures. |
| Proposed: If retry amplification is confirmed as causal, bound payment-client retries and add backoff. | Prevent | TBD | TBD | Under a representative dependency-failure test, retry volume stays within documented limits and checkout/database behavior meets agreed acceptance thresholds. |

## Appendix

All references are from the supplied Slack export for `#inc-482`, dated 2026-10-14:

- **S1:** 09:12 PT alert: checkout p95 latency 8 seconds; error rate 23%.
- **S2:** 09:15 PT investigation acknowledgment.
- **S3:** 09:21 PT investigator hypothesis: connection pool exhausted on `orders-db`.
- **S4:** 09:30 PT rollback of `7f3a`; deployment described as adding a payment-client retry loop.
- **S5:** 09:34 PT errors dropping; 09:41 PT “all green.”
- **S6:** Untimed estimate of approximately 1,200 failed checkouts, pending Finance confirmation.
- **S7:** Untimed note that the canary missed the failure and used 2% traffic for five minutes.

Outstanding evidence: deployment start time, pre-alert metrics, recovery metrics, database connection telemetry, retry counts and configuration, canary results and promotion criteria, and confirmed impact accounting.

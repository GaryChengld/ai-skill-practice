# INC-482 Postmortem
Status: Draft

## Summary

On October 14, 2026, an alert reported checkout p95 latency of 8 seconds and an error rate of 23% at 16:12 UTC [S1]. Deployment `7f3a`, which added a retry loop to the payment client, was rolled back at 16:30 UTC [S4]. Errors were reported as dropping at 16:34 UTC, followed by “all green” at 16:41 UTC [S5–S6].

The exact outage start and verified recovery time are Unknown. Rollback preceded reported improvement, but the available evidence does not establish the cause.

## Impact

- **Observed:** Checkout p95 latency of 8 seconds and an error rate of 23% at the alert timestamp. Metric windows and affected traffic scope are Unknown [S1].
- **Unconfirmed estimate:** Approximately 1.2k failed checkout attempts, pending finance confirmation [S7]. This is not a count of unique customers or a revenue estimate.
- **Unknown:** Unique customers affected, geographic scope, lost revenue, and total impact duration.
- The interval from the first supplied impact observation to reported “all green” was 29 minutes [S1, S6]; this does not establish outage duration.

## Timeline

Time basis: Source timestamps are in PT on October 14, 2026, interpreted as US Pacific daylight time, PDT (UTC−7). UTC timestamps add seven hours. Sources provide minute precision; `:00` seconds are formatting placeholders.

| Time (UTC) | Event | Source |
| --- | --- | --- |
| 2026-10-14T16:12:00Z | Alert reported checkout p95 latency of 8 seconds and error rate of 23%. | S1 |
| 2026-10-14T16:15:00Z | Maria acknowledged the incident. | S2 |
| 2026-10-14T16:21:00Z | Maria suspected exhaustion of the `orders-db` connection pool. | S3 |
| 2026-10-14T16:30:00Z | Dev reported rolling back deployment `7f3a`, which added a payment-client retry loop. | S4 |
| 2026-10-14T16:34:00Z | Errors were reported as dropping. | S5 |
| 2026-10-14T16:41:00Z | “All green” was reported; supporting recovery metrics were not supplied. | S6 |

## Root Cause

**Confirmed cause: Unknown.**

Evidence-limited 5 Whys:

1. **Why was checkout degraded?** Elevated latency and errors were observed [S1]. The failure mechanism is Unknown.
2. **Was database connection exhaustion responsible?** Maria suspected an exhausted `orders-db` connection pool [S3]. No pool metrics or diagnostic logs were supplied to confirm this hypothesis.
3. **Did the deployment contribute?** Deployment `7f3a` added a payment-client retry loop, and rollback preceded reported improvement [S4–S6]. Retry amplification and its relationship to database connections remain hypotheses; the temporal sequence does not prove causation.

Further causal analysis stops at Unknown pending corroborating evidence.

The canary reportedly covered 2% of traffic for five minutes [S8]. Its traffic representativeness, observed metrics, and detection thresholds are Unknown, so the reason it did not detect the issue is not established.

## Lessons Learned

- The supplied alert and response messages provide useful investigation anchors [S1–S6].
- Rollback was followed by reported improvement, making the deployment a useful investigation lead without establishing it as the cause [S4–S6].
- Pool diagnostics, recovery validation, confirmed impact counts, and canary evaluation evidence are missing from the supplied record [S3, S6–S8].

## Action Items

All new actions are Proposed.

| Action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| Investigate the retry-loop change and suspected connection-pool exhaustion. | Investigate | TBD | TBD | A documented analysis correlates deployment timing, retries, pool utilization, and checkout failures, distinguishing confirmed findings from remaining hypotheses. |
| Establish impact boundaries and validate recovery using checkout metrics. | Investigate | TBD | TBD | A metric-backed record identifies first observed degradation and sustained recovery, with measurement windows and remaining uncertainty stated. |
| Reconcile the approximately 1.2k failed-checkout estimate with finance and transaction records. | Investigate | TBD | TBD | Confirmed failed-attempt counts and counting window are documented; unique customers and revenue effects are reported separately where measurable. |
| Evaluate canary coverage and detection criteria against this incident’s failure conditions. | Investigate | TBD | TBD | A documented assessment tests traffic representativeness, duration, and thresholds, with evidence supporting any proposed changes. |

## Appendix

All references are from the supplied Slack export for `#inc-482`, dated October 14, 2026.

| Reference | Source |
| --- | --- |
| S1 | 09:12 PT alert: checkout p95 latency 8s, error rate 23%. |
| S2 | 09:15 PT Maria: “I'm on it.” |
| S3 | 09:21 PT Maria: suspected exhausted connection pool on `orders-db`. |
| S4 | 09:30 PT Dev: rolled back deployment `7f3a`; deployment added a payment-client retry loop. |
| S5 | 09:34 PT: “errors dropping.” |
| S6 | 09:41 PT: “all green.” |
| S7 | Untimed note: approximately 1.2k failed checkouts, finance to confirm. |
| S8 | Untimed canary discussion: 2% traffic for five minutes. |

Outstanding evidence requests: deployment start time and diff; checkout, retry, and connection-pool telemetry; recovery criteria and metrics; confirmed impact counts; and canary traffic composition, results, and thresholds.

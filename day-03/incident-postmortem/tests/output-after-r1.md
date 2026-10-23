# INC-482 Postmortem

Status: Draft

## Summary

On October 14, 2026, checkout alerted with p95 latency of 8 seconds and an error rate of 23%. Deployment `7f3a`, which added a payment-client retry loop, was rolled back. Errors subsequently declined, and “all green” was reported at 09:41 PT. Recovery was reported but not independently verified in the supplied evidence. The root cause remains Unknown. [S1]

## Impact

- Observed: checkout p95 latency of 8 seconds and error rate of 23% at 09:12 PT. Measurement windows and affected scope are Unknown. [S1]
- Unconfirmed estimate: approximately 1,200 failed checkouts, pending Finance confirmation. This is not a count of unique customers or a measure of lost revenue. [S1]
- The first supplied impact observation and reported recovery are 29 minutes apart. This is an observation interval, not a verified outage duration; the actual impact start and end are Unknown.

## Timeline

Time basis: Source times are labeled PT. Interpreting PT as US Pacific, October 14, 2026 falls in PDT (UTC−07:00); seven hours are added below. Source precision is one minute, so seconds are omitted. Confirm the intended timezone.

| Time (UTC) | Event | Source |
| --- | --- | --- |
| 2026-10-14T16:12Z | Alert reports checkout p95 latency of 8 seconds and error rate of 23%. | S1 |
| 2026-10-14T16:15Z | Response acknowledged. | S1 |
| 2026-10-14T16:21Z | Responder suspects connection-pool exhaustion on `orders-db`; no corroborating telemetry supplied. | S1 |
| 2026-10-14T16:30Z | Rollback of deployment `7f3a` reported; deployment had added a payment-client retry loop. | S1 |
| 2026-10-14T16:34Z | Errors reported to be dropping. | S1 |
| 2026-10-14T16:41Z | “All green” reported. | S1 |

## Root Cause

**Confirmed root cause: Unknown.**

Evidence-limited causal analysis:

1. **Why did checkout degrade?** The alert establishes elevated latency and errors, but the failure mechanism is Unknown. [S1]
2. **Was database connection-pool exhaustion responsible?** This was a responder hypothesis. Pool utilization, connection waits, and database telemetry were not supplied. [S1]
3. **Did the payment-client retry loop contribute?** The rolled-back deployment added retries, and errors declined after rollback. This sequence supports investigation but does not prove retry amplification or establish the deployment as the sole cause. [S1]

The canary reportedly ran at 2% traffic for five minutes and did not catch the failure. This establishes a safeguard gap. Its traffic share and duration alone do not explain why the failure escaped detection. [S1]

## Lessons Learned

- Rollback was followed by declining errors and reported recovery, making it a useful observed mitigation. Its causal effect still requires verification. [S1]
- The canary did not identify the incident before broader impact; its coverage and promotion criteria need validation. [S1]
- Missing deployment timing, telemetry, and recovery criteria prevent a confirmed causal chain and precise impact assessment.

## Action Items

All actions below are **Proposed**; owners and dates are unassigned.

| Action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| Proposed: Reconcile deployment timing with checkout, payment-client retry, and database connection telemetry. | Investigate | TBD | TBD | Evidence-backed causal analysis documents whether pool exhaustion and retries contributed, or explicitly records remaining evidence gaps. |
| Proposed: Review canary coverage and add a verified checkout health gate before promotion. | Detect | TBD | TBD | A controlled checkout latency/error failure causes the canary gate to block promotion and notify responders; thresholds and test results are documented. |
| Proposed: Confirm failed-checkout totals and actual impact boundaries with operational and Finance records. | Investigate | TBD | TBD | Reviewed figures state counting method, time window, uncertainty, and distinction between attempts and unique customers. |
| Proposed: If retry amplification is confirmed, constrain retries with an appropriate attempt limit and backoff. | Prevent | TBD | TBD | A representative failure test demonstrates bounded retry volume and no incident-equivalent checkout degradation caused by retries. |

## Appendix

**S1:** Supplied Slack export from `#inc-482`, dated 2026-10-14, including alert messages, response updates, the impact estimate, and canary details.

Unresolved evidence requests:

- Confirmation that PT means US Pacific.
- Deployment start, completion, canary, and promotion timestamps.
- Checkout metric windows, affected scope, and recovery verification.
- Database pool utilization, connection waits, and relevant traces.
- Payment-client retry configuration and observed attempt volumes.
- Canary health checks, thresholds, traffic coverage, and recorded results.
- Finance confirmation of the approximately 1,200 failed-checkout estimate.

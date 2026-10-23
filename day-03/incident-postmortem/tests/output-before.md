# Incident Postmortem: Checkout Degradation — INC-482

## Summary

On October 14, 2026, checkout experienced elevated latency and errors from 09:12 to 09:41 PT, an observed duration of 29 minutes. The initial alert reported checkout p95 latency of 8 seconds and an error rate of 23%.

Responders identified apparent connection pool exhaustion on `orders-db`. Deployment `7f3a`, which added a retry loop to the payment client, was rolled back at 09:30. Errors began decreasing at 09:34, and service was reported healthy at 09:41.

The deployment is the leading suspected trigger; the precise mechanism remains unverified.

## Impact

- **Affected service:** Checkout.
- **Observed degradation:** 8-second p95 latency and 23% errors at the initial alert; these figures are not established incident-wide averages.
- **Estimated failed checkouts:** Approximately 1,200, pending Finance confirmation.
- **Unique customers affected:** Unknown; failed checkout attempts may include repeated attempts by the same customer.
- **Financial impact:** Not yet confirmed.

The incident may have started before the first alert. Payment outcomes, duplicate charges, and eventual checkout completion were not documented in the supplied incident record.

## Timeline

All times are Pacific Time on October 14, 2026.

| Time | Event |
|---|---|
| Before 09:12 | Deployment `7f3a` introduced a payment-client retry loop; deployment time is unknown. |
| 09:12 | Alert reported checkout p95 latency of 8 seconds and a 23% error rate. |
| 09:15 | Maria acknowledged the incident and began investigating. |
| 09:21 | Maria reported apparent connection pool exhaustion on `orders-db`. |
| 09:30 | A responder identified as “dev” reported rolling back deployment `7f3a`. |
| 09:34 | Errors were reported to be decreasing. |
| 09:41 | Service was reported “all green.” |

## Root Cause

**Probable trigger:** The payment-client retry loop introduced in deployment `7f3a`. Recovery after rollback supports this hypothesis but does not independently prove causation.

**Observed failure condition:** Apparent exhaustion of the database connection pool on `orders-db`.

**Working hypothesis:** Retries increased request volume or prolonged checkout processing, increasing database connection demand or connection hold time until the pool exhausted. Retry behavior, transaction boundaries, and connection metrics must be examined to establish the causal chain.

**Detection gap:** The canary received 2% of traffic for five minutes. This limited exposure may not have reproduced the load or duration needed to reveal pool exhaustion. Canary metrics and promotion criteria were not provided.

**Responsibility:** The record does not identify the deployment author or establish that an individual caused the incident. Maria investigated, and “dev” performed the rollback. The corrective focus is on retry safeguards, representative testing, and release controls.

## Lessons Learned

- Rollback was followed by recovery and was an effective mitigation in this incident.
- Retry changes should be reviewed for their effects on downstream load and scarce resources.
- Canary exposure should be sufficient to detect resource saturation under representative conditions.
- Incident records should distinguish failed attempts from unique customers and preserve evidence needed to confirm the cause.

## Action Items

Owners and deadlines below are proposed assignments, not confirmed commitments.

| # | Action | Proposed owner | Target date | Completion evidence |
|---|---|---|---|---|
| 1 | Confirm the causal chain using the deployment diff, request traces, retry counts, and database pool metrics. | Checkout Engineering | 2026-10-21 | Documented findings that confirm or revise the root-cause hypothesis. |
| 2 | Review and constrain payment retries, including attempt limits, backoff, timeouts, and payment idempotency. | Payments Engineering | 2026-10-28 | Reviewed implementation with tests demonstrating bounded retries and safe payment behavior. |
| 3 | Add a load test covering payment failures and database connection pressure. | Checkout Engineering | 2026-10-28 | Test results showing connection usage and checkout behavior under sustained failure conditions. |
| 4 | Revise canary traffic, observation duration, and promotion gates using representative checkout load. | Release Engineering / SRE | 2026-10-28 | Documented rollout policy and a demonstration that relevant degradation blocks promotion. |
| 5 | Reconcile failed checkout attempts, unique customers, payment outcomes, and financial impact. | Finance / Analytics | 2026-10-21 | Validated impact report replacing the provisional estimate. |

## Appendix

**Source:** Supplied Slack export from `#inc-482`, October 14, 2026.

**Outstanding evidence:** Deployment timestamp and author; retry configuration; database connection metrics; traces showing connection lifetime; canary results and promotion criteria; validated customer and financial impact.

**Confidence:** The alert, response, rollback, and recovery times are documented in the supplied export. Customer impact is provisional, and the root-cause mechanism remains a hypothesis.

# INC-1048 Postmortem
Status: Draft

## Summary

On 2026-10-22, west-region dashboards failed to load because browsers received HTTP 403 responses for the JavaScript bundle. East-region dashboards loaded, but live telemetry froze. Two independent configuration rollouts caused separate failures: a storage policy denied bundle reads in the west, while an east-region gateway timeout closed stream connections before clients’ next heartbeat. [D1–D3, D6]

Restoring the west asset policy restored dashboard functionality at 08:20 UTC. Restoring the east gateway timeout restored live telemetry at 08:26 UTC; all dashboards were reported healthy at 08:29 UTC. [D4–D5]

## Impact

- **West:** Dashboards failed to load; functionality was reported restored at 08:20 UTC. [D1, D4]
- **East:** Dashboards loaded, but live telemetry froze; telemetry was reported restored at 08:26 UTC. [D1, D5]
- **Scope:** Affected dashboard and user counts are Unknown. [D7]
- **Timing:** First observed impact at 08:10 and reported health at 08:29 bound a 19-minute observation interval. Actual incident onset and total duration are Unknown. [D1, D5]

## Timeline

Time basis: All source timestamps are UTC on 2026-10-22, observed to the minute. Seconds are padded with `:00` for formatting and do not imply second-level precision.

| Time (UTC) | Event | Source |
| --- | --- | --- |
| 2026-10-22T08:10:00Z | West dashboards failed to load with bundle HTTP 403 responses; east dashboards loaded but live telemetry froze. | D1 |
| 2026-10-22T08:14:00Z | An audit confirmed that the new west storage policy denied bundle reads. That policy was not applied in the east. | D2 |
| 2026-10-22T08:17:00Z | Logs confirmed that the east gateway closed connections after 30 seconds, before clients’ 60-second heartbeat interval. The west gateway retained its previous timeout. | D3 |
| 2026-10-22T08:20:00Z | Restoring the west asset policy restored bundle delivery, dashboard loading, and live telemetry. | D4 |
| 2026-10-22T08:26:00Z | Restoring the east gateway timeout restored live telemetry. | D5 |
| 2026-10-22T08:29:00Z | All dashboards were reported healthy. | D5 |

## Root Cause

Two independent causal paths explain the regional failures:

- **West — confirmed cause:** The new storage policy denied JavaScript bundle reads, producing HTTP 403 responses and preventing dashboards from loading. The audit established the access denial; policy restoration restored functionality. [D1–D2, D4]
- **East — confirmed cause:** The new gateway idle timeout was shorter than the clients’ heartbeat interval: connections closed after 30 seconds, while heartbeats occurred every 60 seconds. Connection logs confirmed this behavior; restoring the timeout restored telemetry. [D3, D5]

The rollouts were separate, and audit records showed neither depended on the other. A single rollout-to-rollout causal chain is therefore unsupported. [D6]

**Safeguard gap:** Pre-rollout checks exercised neither browser bundle access nor live streaming beyond 30 seconds. Whether broader checks would have blocked these particular rollouts remains unverified. Why these checks were absent and why the configurations were selected are Unknown. [D7]

## Lessons Learned

Targeted configuration restoration recovered each region independently. The audit and connection logs provided evidence for distinct failure mechanisms. [D2–D5]

Validation lacked coverage for two user-visible behaviors: retrieving the browser bundle and sustaining live telemetry beyond the gateway’s timeout boundary. Regional checks should exercise both behaviors. [D7]

Detection mechanisms, rollout timing, and the complete affected population remain Unknown.

## Action Items

| Proposed action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| Proposed: Add browser-context bundle-access checks to regional asset-policy rollout gates. | Prevent | TBD | TBD | A policy denying required bundle reads fails validation; a valid policy passes and the dashboard loads. |
| Proposed: Validate gateway idle timeouts against client heartbeat intervals and exercise sustained streaming before rollout. | Prevent | TBD | TBD | The 30-second timeout with a 60-second heartbeat fails validation; an approved configuration sustains telemetry across at least two heartbeat intervals. |
| Proposed: Add regional synthetic monitoring for dashboard loading and sustained live telemetry. | Detect | TBD | TBD | Controlled bundle denial and premature stream closure each produce an alert identifying the affected region. |
| Proposed: Review both rollouts’ configuration decisions and validation coverage. | Investigate | TBD | TBD | A documented review identifies why each configuration passed available checks, records supporting evidence, and explicitly lists remaining Unknowns. |

## Appendix

Source: [INC-1048 source packet](C:/Workspaces/ai-skill-practice/day-06/incident-postmortem/tests/input-d.md). Citations D1–D7 refer to its numbered entries.

Causal tree:

```text
At least one region's dashboard functionality impaired [Observed, D1]
  OR [Supported inference, D1–D6]
  +-- West dashboards fail to load [Observed, D1]
  |     <- Bundle reads denied by new storage policy
  |        [Observed, D2; causal link confirmed, D1–D2, D4]
  +-- East live telemetry freezes [Observed, D1]
        <- Gateway closes connections after 30 seconds,
           before the 60-second client heartbeat
           [Observed, D3; causal link confirmed, D3, D5]

Separate safeguard gap:
Pre-rollout checks omitted bundle access and streams beyond 30 seconds
[Observed, D7; contribution to rollout escape is a supported inference]
```

Evidence requests: rollout timestamps and configuration diffs; validation results and approval criteria; alert and detection records; affected dashboard and user counts; and health-check evidence supporting the 08:29 recovery report. These would establish onset, clarify detection and validation gaps, and substantiate recovery scope.

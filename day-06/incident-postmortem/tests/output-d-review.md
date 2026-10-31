# INC-1048 Postmortem
Status: Draft

## Summary

On 2026-10-22, west-region dashboards failed to load because a new storage policy denied access to their JavaScript bundle. East-region dashboards loaded, but live telemetry froze because the stream gateway’s new 30-second idle timeout was shorter than clients’ 60-second heartbeat interval. These failures followed independent configuration rollouts. [D1–D3, D6]

Restoring the west-region policy restored dashboard functionality at 08:20 UTC. Restoring the east-region gateway timeout restored live telemetry at 08:26 UTC. All dashboards were reported healthy at 08:29 UTC. [D4–D5]

## Impact

- **West region:** Dashboard loading failed; browsers received HTTP 403 responses for the JavaScript bundle. [D1]
- **East region:** Dashboards loaded, but live telemetry froze. [D1]
- **Affected dashboard and user counts:** Unknown. [D7]
- **Observation interval:** 08:10–08:29 UTC, spanning 19 minutes from first observed impact to reported overall health. This is not a verified total incident duration; actual onset is Unknown. [D1, D5]

## Timeline

Time basis: All source timestamps are UTC on 2026-10-22, observed to the minute. Seconds are padded with `:00` and do not imply second-level precision.

| Time (UTC) | Event | Source |
| --- | --- | --- |
| UTC Unknown; original time not supplied | Separate configuration rollouts changed the west-region asset policy and east-region stream timeout. Neither rollout depended on the other. | D6 |
| 2026-10-22T08:10:00Z | West dashboards failed to load, with HTTP 403 responses for the JavaScript bundle. East dashboards loaded, but live telemetry froze. | D1 |
| 2026-10-22T08:14:00Z | Audit confirmed that the new west-region storage policy denied bundle reads. The policy was not applied in the east region. | D2 |
| 2026-10-22T08:17:00Z | Logs confirmed east-region gateway connections closed after 30 seconds; client heartbeats occurred every 60 seconds. The west gateway retained its previous timeout. | D3 |
| 2026-10-22T08:20:00Z | Restoring the west asset policy restored bundle delivery, dashboard loading, and live telemetry. | D4 |
| 2026-10-22T08:26:00Z | Restoring the east gateway timeout restored live telemetry there. | D5 |
| 2026-10-22T08:29:00Z | All dashboards were reported healthy. | D5 |

## Root Cause

Two independent causal paths explain the observed failures:

1. **West-region bundle access denial:** The new storage policy denied JavaScript bundle reads, consistent with the observed HTTP 403 responses and dashboard loading failures. The audit directly identified the denial; recovery after restoration provides additional supporting evidence. [D1, D2, D4]
2. **East-region timeout incompatibility:** The gateway closed connections after 30 seconds, before clients’ 60-second heartbeat interval. The recorded settings and connection closures support this mechanism for the frozen live telemetry. [D1, D3, D5]

Neither rollout depended on the other, and each region retained its previous configuration for the other failure path. A single shared configuration cause is not supported. [D2, D3, D6]

**Safeguard gap:** Pre-rollout checks exercised neither browser bundle access nor a live stream beyond 30 seconds. This left both failure modes untested; it does not establish why the configuration values were selected. [D7]

Why the incompatible configurations were introduced and how rollout approval worked are Unknown. Further causal analysis stops at that evidence boundary.

## Lessons Learned

- Policy audits and connection logs provided evidence for distinct regional failure mechanisms. Restoring the relevant configurations was followed by reported regional recovery. [D2–D5]
- Validation needs to exercise browser asset access and sustained telemetry connections, reflecting the affected user journeys. Existing pre-rollout checks omitted both. [D7]
- Incident onset, affected counts, and the configuration decision process remain unresolved. Monitoring and alert coverage are also Unknown.

## Action Items

| Proposed action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| Proposed: Add browser bundle-access checks before asset-policy rollout. | Prevent | TBD | TBD | A test policy that denies required bundle reads fails validation and blocks rollout. |
| Proposed: Validate gateway idle timeouts against supported client heartbeat intervals. | Prevent | TBD | Validation rejects the observed 30-second timeout with a 60-second heartbeat and accepts a documented compatible configuration. |
| Proposed: Add per-region synthetic checks for dashboard loading and sustained live telemetry. | Detect | TBD | Controlled bundle denial and premature connection closure each trigger an alert; the healthy check demonstrates telemetry updates across multiple heartbeat cycles. |
| Proposed: Investigate rollout decisions, actual onset, and affected scope using available audit records and telemetry. | Investigate | TBD | Findings cite evidence for each conclusion and explicitly retain any unresolvable times, counts, or decision factors as Unknown. |

## Appendix

**Causal tree:** The top event is degradation in at least one region; either regional path is sufficient.

```text
Dashboard functionality degraded in at least one region [Observed, D1]
  OR [Supported inference, D1–D3]
  +-- West: dashboard loading failed [Observed, D1]
  |     <-- Bundle reads denied by new policy [Observed, D2;
  |          causal link supported by D1, D2, D4]
  +-- East: live telemetry froze [Observed, D1]
        <-- Connection lifetime incompatible with heartbeat
            [Supported inference, D3]
              AND
              +-- Gateway closed connections after 30 seconds
              |   [Observed, D3]
              +-- Client heartbeat interval was 60 seconds
                  [Observed, D3]

Separate safeguard gap: pre-rollout checks omitted bundle access
and streams beyond 30 seconds [Observed, D7].
```

**Source references:** D1–D7 refer to the supplied [INC-1048 source packet](C:/Workspaces/ai-skill-practice/day-06/incident-postmortem/tests/input-d.md).

**Unresolved evidence requests:** Rollout execution times and configuration rationale; impact-onset and affected-population evidence; validation and approval records; monitoring coverage and recovery-verification details.

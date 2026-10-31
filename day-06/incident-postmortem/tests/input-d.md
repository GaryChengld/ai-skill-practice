# INC-1048 source packet

Draft an internal postmortem for the resolved live-telemetry dashboard incident.
All timestamps are UTC on 2026-10-22, observed to the minute.

- D1, 08:10: west-region dashboards failed to load; browsers received HTTP 403 for the JavaScript bundle. East-region dashboards loaded but their live telemetry froze.
- D2, 08:14: an asset-policy audit confirmed that the new west-region storage policy denied bundle reads. The policy was not applied in the east region.
- D3, 08:17: connection logs confirmed that the east-region stream gateway closed connections after 30 seconds. Its new idle timeout was shorter than the clients' 60-second heartbeat interval. The west-region stream gateway retained its previous timeout.
- D4, 08:20: restoring the west-region asset policy restored bundle delivery; west dashboards loaded and live telemetry worked.
- D5, 08:26: restoring the east-region gateway timeout restored live telemetry there. All dashboards were reported healthy at 08:29.
- D6: the asset policy and stream timeout were changed by separate configuration rollouts; audit records show neither rollout depended on the other.
- D7: pre-rollout checks did not exercise browser bundle access or a live stream beyond 30 seconds. The affected dashboard and user counts are unknown.

Follow-up owners and deadlines have not been assigned.

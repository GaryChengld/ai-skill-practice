# INC-713 Postmortem
Status: Draft

## Summary
Thumbnail rendering experienced request timeouts on 2026-09-08. At the first recorded observation, 18% of render requests timed out and a synthetic thumbnail check failed. Investigation confirmed a full render cache volume, failed writes with ENOSPC, and a cache eviction job that had remained disabled after maintenance. At 10:16 UTC, the on-call engineer cleared regenerable cache files and re-enabled eviction; synthetic checks and timeout rates returned to normal at 10:21 UTC. Recovery followed these changes, but their individual effects were not measured. [A1–A5]

## Impact
- At 10:05 UTC, 18% of render requests timed out. The packet does not establish this rate for the entire incident. [A1]
- The interval from first observed impact to reported recovery was approximately 16 minutes, from 10:05 to 10:21 UTC. This is an observation interval, not a verified total incident duration; earlier impact onset is Unknown. [A1, A5; source packet context]
- Unique affected users and exact failure counts are Unknown. Broader scope and the number of requests in the measurement window are Unknown. [A6; source packet]

## Timeline
Time basis: All source timestamps are UTC on 2026-09-08, observed to the minute. Seconds are padded with `:00` for formatting and do not imply second-level precision. [Source packet context]

| Time (UTC) | Event | Source |
| --- | --- | --- |
| 2026-09-08T10:05:00Z | Synthetic thumbnail check failed; 18% of render requests timed out. | A1 |
| 2026-09-08T10:09:00Z | Worker logs confirmed the render cache volume was full and writes failed with ENOSPC. | A2 |
| 2026-09-08T10:12:00Z | Investigation confirmed that cache eviction had been disabled during maintenance and not re-enabled. The time it was disabled is Unknown. | A3 |
| 2026-09-08T10:16:00Z | On-call cleared regenerable cache files and re-enabled eviction. | A4 |
| 2026-09-08T10:21:00Z | Synthetic checks and timeout rates returned to normal. | A5 |

## Root Cause
The confirmed failure condition was cache-volume exhaustion causing writes to fail with ENOSPC. Investigation also confirmed that eviction remained disabled after maintenance. The evidence supports disabled eviction as the likely upstream explanation for cache exhaustion and the write failures as the likely mechanism behind rendering timeouts. The packet does not include capacity history or request-level traces that independently verify those links. [A1–A3]

Evidence-limited 5 Whys:
1. **Why were render requests timing out?** Failed cache writes are the likely mechanism, but request-level attribution is not supplied. [A1–A2]
2. **Why did cache writes fail?** The render cache volume was full; worker logs recorded ENOSPC. [A2]
3. **Why did the cache fill?** Eviction remained disabled, providing a supported causal hypothesis; cache-growth measurements are unavailable. [A3]
4. **Why did eviction remain disabled?** It was disabled during maintenance and not re-enabled. Maintenance has no checklist step to restore paused scheduled jobs, a contributing process gap. The precise reason restoration did not occur is Unknown. [A3, A7]

Analysis stops at that evidence boundary. The absence of a cache-capacity alert was a confirmed detection gap; its effect on incident duration is Unknown. [A6]

## Lessons Learned
- Synthetic checks exposed user-visible degradation, and worker logs identified a concrete storage failure. [A1–A2]
- Cache cleanup and eviction restoration preceded recovery. The evidence does not distinguish the contribution of either intervention. [A4–A5]
- A maintenance restoration check and cache-capacity monitoring were absent. These safeguards can be improved without waiting for complete causal verification. [A6–A7]
- Earlier impact onset and the total affected request and user counts remain open questions. [A6; source packet context]

## Action Items
All actions below are Proposed. Owners and due dates have not been assigned. [Source packet context]

| Proposed action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| Proposed: Add cache-capacity monitoring with an actionable alert and response instructions. | Detect | TBD | TBD | A controlled threshold test delivers an alert to the designated responder before the cache is full; instructions identify safe recovery steps. |
| Proposed: Add a maintenance checklist step that inventories paused scheduled jobs and verifies restoration or records an explicit exception. | Prevent | TBD | TBD | A maintenance rehearsal with a paused eviction job cannot close without a successful restoration check or a recorded exception with follow-up ownership. |
| Proposed: Document and validate safe cleanup of regenerable cache files and verification of eviction operation. | Mitigate | TBD | TBD | A controlled exercise restores successful cache writes and demonstrates eviction running, using only confirmed regenerable files. |
| Proposed: Reconstruct cache growth, job state, write errors, and request failures to test the causal links and refine impact estimates. | Investigate | TBD | TBD | A review records which links are confirmed or remain hypotheses, documents available impact counts and onset bounds, and explicitly marks unavailable evidence Unknown. |

## Appendix
Source references: `tests/input-a.md`, INC-713 source packet.

| Source | Evidence |
| --- | --- |
| A1 | Failed synthetic check and 18% render-request timeout rate at 10:05 UTC. |
| A2 | Full render cache volume and ENOSPC write failures confirmed at 10:09 UTC. |
| A3 | Disabled, unrestored cache eviction job confirmed at 10:12 UTC. |
| A4 | Regenerable cache files cleared and eviction re-enabled at 10:16 UTC. |
| A5 | Synthetic checks and timeout rates normal at 10:21 UTC. |
| A6 | No cache-capacity alert; unique affected users and exact failure counts unknown. |
| A7 | No maintenance checklist step to restore paused scheduled jobs. |
| Source packet context | Internal review of a resolved incident; all times UTC with minute precision; impact onset before first alert unknown; no assigned owners or due dates. |

Unresolved evidence requests: cache-capacity history, maintenance and scheduler records, request-level correlations with ENOSPC, the timeout-rate measurement window and denominator, and request/user counts. These may establish earlier impact bounds and strengthen or revise the causal explanation. Their availability is Unknown.

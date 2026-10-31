# INC-713 Postmortem
Status: Draft

## Summary

On 2026-09-08 at 10:05 UTC, a synthetic thumbnail check failed and 18% of render requests timed out. Investigation confirmed a full render cache volume, failed writes, and a cache eviction job that had remained disabled after maintenance. The on-call engineer cleared regenerable cache files and re-enabled eviction at 10:16 UTC. Synthetic checks and timeout rates returned to normal at 10:21 UTC. [A1–A5]

## Impact

- Thumbnail rendering experienced request timeouts; the reported timeout rate at 10:05 UTC was 18%. [A1]
- Unique affected users, exact failure counts, and impact onset are **Unknown**. [A6; source packet]
- First observed impact to reported recovery spans approximately 16 minutes. This is an observation interval, not a verified total incident duration. [A1, A5]
- Broader service impact is **Unknown**.

## Timeline

Time basis: All source timestamps are UTC on 2026-09-08, observed to the minute. Seconds are padded with `:00` and do not indicate second-level precision.

| Time (UTC) | Event | Source |
| --- | --- | --- |
| 2026-09-08T10:05:00Z | Synthetic thumbnail check failed; 18% of render requests timed out. | A1 |
| 2026-09-08T10:09:00Z | Worker logs confirmed a full render cache volume and writes failing with ENOSPC. | A2 |
| 2026-09-08T10:12:00Z | Investigation confirmed eviction had been disabled during maintenance and not re-enabled. | A3 |
| 2026-09-08T10:16:00Z | On-call engineer cleared regenerable cache files and re-enabled eviction. | A4 |
| 2026-09-08T10:21:00Z | Synthetic checks and timeout rates returned to normal. | A5 |

## Root Cause

Evidence-limited 5 Whys:

1. **Why was thumbnail rendering degraded?** Render requests timed out while cache writes were failing. The full cache volume is the supported immediate failure explanation; request-level traces were not supplied. [A1, A2]
2. **Why were cache writes failing?** The cache volume was full, producing ENOSPC errors. [A2]
3. **Why was cache eviction unavailable?** The eviction job had been disabled during maintenance and not re-enabled. This is the supported explanation for unchecked cache accumulation. [A3]
4. **Why was restoration missed?** The maintenance process had no checklist step to restore paused scheduled jobs. This is a confirmed safeguard gap; the specific circumstances behind the missed restoration are **Unknown**. [A7]

The evidence does not support extending the chain further. Clearing cache files and restoring eviction preceded recovery, but their individual contributions to recovery cannot be isolated from the supplied evidence. [A4, A5]

## Lessons Learned

- Synthetic checks detected the degradation, and worker logs exposed the capacity failure. [A1, A2]
- No cache-capacity alert existed, leaving a known detection gap. [A6]
- Maintenance lacked an explicit restoration check for paused scheduled jobs. [A7]
- Impact measurement remains incomplete because onset, affected users, and failure totals are unknown. [A6; source packet]

## Action Items

| Proposed action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| **Proposed:** Add a cache-capacity alert with a documented response threshold. | Detect | TBD | TBD | A controlled threshold breach delivers an actionable alert to the responsible on-call route before capacity exhaustion. |
| **Proposed:** Add maintenance steps to record paused scheduled jobs, restore their intended state, and verify execution. | Prevent | TBD | TBD | A maintenance exercise records every paused job and confirms restoration and successful execution before closure. |
| **Proposed:** Reconstruct impact onset, affected-user scope, and failed-request totals from retained telemetry. | Investigate | TBD | TBD | The review records supported metrics and time bounds, or explicitly documents unavailable evidence and remaining Unknowns. |

## Appendix

Source: [INC-713 source packet](C:/Workspaces/ai-skill-practice/day-06/incident-postmortem/tests/input-a.md).

References A1–A7 correspond to the labeled entries in that packet.

Unresolved evidence requests:

- Request traces or equivalent evidence connecting cache write failures to render timeouts.
- Maintenance records explaining how eviction restoration was missed.
- Historical telemetry establishing earlier impact and cumulative failure counts.

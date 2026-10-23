# Before / After Comparison

Method: On 2026-10-22, two fresh agents (`day03_before`, `day03_after`, `fork_turns=none`) received only their respective skill and the identical input, with the same request to write a postmortem. Neither used tools or inherited this conversation. Outputs are saved unchanged; model settings were inherited, not pinned.

| Check | BEFORE output | AFTER output |
| --- | --- | --- |
| Timezone | Retains PT without specifying the offset. | Uses dated UTC timestamps, correctly converts PDT (UTC-7) to 16:12–16:41Z, and explains minute precision. |
| Personal blame | Does not blame Maria or the deployment author despite the weak instruction. | Uses system-focused language and evidence gaps; no personal blame. |
| Invented impact | Preserves approximately 1,200 as unconfirmed failed checkouts; unique customers remain unknown. | Preserves approximately 1.2k as unconfirmed failed attempts and distinguishes customers and revenue. Neither fabricates an impact number. |
| Actions | Exactly 5, matching the arbitrary requirement; proposes team owners and dates absent from input. | 4 evidence-driven investigations, each with type and success criterion; owner and date remain TBD. |
| Cause and recovery | Labels the cause provisional, but calls rollback effective and places deployment before 09:12 without evidence. | Keeps cause and verified recovery Unknown, with per-claim sources; distinguishes the 29-minute observation interval from outage duration. |

The rewrite improves consistent time handling and avoids unsupported scheduling details in this pair. Blamelessness and cautious impact counts were already present in the baseline; this run does not demonstrate gains there.
Limitations: One pair is not a reliability estimate. The rewrite includes a date-specific timezone gotcha, so this is not a held-out timezone test. Ongoing incidents, sensitive details, and conflicting sources were specified but not behaviorally tested. The after output favors investigation over immediate prevention; revisit that balance when causal evidence becomes available.

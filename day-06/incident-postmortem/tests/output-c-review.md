# INC-937 Postmortem
Status: Draft

## Summary
An automated integration attached a support export containing an API credential and contact data to a broadly readable internal ticket at 2026-09-18T12:10:00Z. Attachments were disabled and the ticket restricted at 12:18; security confirmed credential revocation at 12:20 and verified restricted ticket access at 12:24. The source packet reports the incident as resolved. Whether unauthorized readers downloaded the attachment remains Unknown. [C1–C4; packet introduction]

## Impact
- **Exposed categories:** an API credential and contact data. Two synthetic contact rows were reported; further scope is Unknown. Sensitive values are omitted. [C2, C6]
- **Exposure surface:** a broadly readable internal ticket. The number and identities of readers are Unknown. [C1, C4]
- **Confirmed credential use or exfiltration:** Unknown. Audit retention does not establish whether unauthorized downloads occurred before restriction. [C4]
- **Observation interval:** 14 minutes between attachment and verification of restricted access. This is not a verified total incident duration or proof that all exposure ended then. [C1, C4]

## Timeline
Time basis: All source times are UTC on 2026-09-18, observed to the minute. Seconds are padded with `:00` and do not indicate second-level precision.

| Time (UTC) | Event | Source |
| --- | --- | --- |
| 2026-09-18T12:10:00Z | An automated integration attached a support export to a broadly readable internal ticket. | C1 |
| 2026-09-18T12:14:00Z | Security confirmed that the export contained an API credential and contact data. | C2 |
| 2026-09-18T12:18:00Z | The integration owner disabled attachments and restricted the ticket. | C3 |
| 2026-09-18T12:20:00Z | Security confirmed credential revocation. | C3 |
| 2026-09-18T12:24:00Z | Ticket access scope was verified as restricted; prior unauthorized downloads remained unconfirmed. | C4 |
| UTC Unknown — source provides no time | Configuration inspection confirmed sensitive fields in the default export profile and unchanged acceptance by the ticket integration. No sensitive-field check preceded attachment. | C5, C6 |

## Root Cause
The supported failure mechanism was that the default export profile included secret and contact fields, the ticket integration accepted that profile unchanged, and no sensitive-field check intervened before attachment to a broadly readable ticket. [C1, C5, C6]

Evidence-limited 5 Whys:

1. **Why was sensitive content exposed through the ticket?** The integration attached an export containing that content to a broadly readable ticket. [C1, C2]
2. **Why did the attached export contain sensitive fields?** The default export profile included secret and contact fields, and the integration accepted it unchanged. [C5]
3. **Why did attachment proceed without filtering or blocking?** There was no sensitive-field check before attachment. [C6]
4. **Why were those defaults and safeguards absent?** Unknown. The supplied evidence does not establish the design, review, or configuration history.

This establishes the configuration and safeguard failures. It does not establish unauthorized access, credential use, or exfiltration. [C4]

## Lessons Learned
Disabling attachments, restricting the ticket, confirming revocation, and verifying access scope provided documented containment milestones. The evidence supports those individual outcomes without establishing complete removal of any earlier copies. [C3, C4]

Sensitive export defaults combined with unchanged integration acceptance allowed sensitive content to reach a broader audience. A pre-attachment safeguard could address this known exposure path without waiting for the remaining investigation. [C1, C5, C6]

Audit retention leaves prior downloads unresolved; verified access restriction cannot answer that historical question. [C4]

## Action Items

| Proposed action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| Proposed: Create a support-export profile that excludes secret and contact fields by default. | Prevent | TBD | TBD | A representative export excludes both categories, with any permitted inclusion explicitly configured and reviewed. |
| Proposed: Add a pre-attachment sensitive-field check that blocks unsafe exports and records the decision without recording sensitive values. | Mitigate | TBD | Tests using synthetic secret and contact fields demonstrate blocking; an approved safe export succeeds. |
| Proposed: Establish export-to-ticket audit logging and retention sufficient to investigate attachment access. | Detect | TBD | A controlled exercise reconstructs attachment publication, access scope changes, and downloads over the agreed retention period. |
| Proposed: Assess remaining authorized evidence for prior downloads and credential use. | Investigate | TBD | Findings distinguish confirmed activity, evidence gaps, and questions that cannot be resolved. |
| Proposed: Review why sensitive defaults and unchanged profile acceptance were permitted. | Investigate | TBD | The review documents supported contributing conditions and identifies any additional controls warranted by the findings. |

## Appendix
**Audience:** Restricted internal. External distribution has not been approved. Review status: Pending; reviewers and approval date: Unknown.

**Source references:** C1–C6 refer to the supplied INC-937 source packet. All values are described there as synthetic fixtures. Credential values, email addresses, and account identifiers are omitted from this draft.

**Evidence handling:** Original evidence remains in its existing location. Evidence custodians and approved evidence-store references are Unknown.

**Unresolved evidence requests:**

- Available download/access records and credential-use evidence.
- Scope beyond the two reported synthetic contact rows.
- Configuration and control-review history.
- Follow-up owners, due dates, and review assignments.

# INC-937 Postmortem
Status: Draft

## Summary

An automated integration attached a support export to a broadly readable internal ticket at 2026-09-18T12:10:00Z. Security confirmed that the export contained an API credential and contact data. The integration owner disabled attachments and restricted the ticket at 12:18; credential revocation was confirmed at 12:20, and restricted ticket access was verified at 12:24. The source packet describes the incident as resolved. Unauthorized downloads and credential use remain Unknown. [C1–C4; packet context]

## Impact

- Confirmed exposed content: one API credential, represented here as `[REDACTED CREDENTIAL]`, and two synthetic contact rows. Further scope is Unknown. [C2, C6]
- Exposure location: a broadly readable internal ticket. The number and identities of readers are Unknown. [C1, C4]
- Audit retention does not establish whether an unauthorized reader downloaded the attachment before restriction. Exfiltration is unconfirmed; credential use is Unknown. [C4]
- First observed exposure and verified access restriction bound a 14-minute observation interval. This is not a verified total incident duration or download window. [C1, C4]

The supplied values are synthetic test fixtures; this draft omits credential values and individual contact identifiers. [Packet context]

## Timeline

Time basis: All source times are UTC on 2026-09-18, observed to the minute. Seconds are padded with `:00`; second-level precision is unavailable.

| Time (UTC) | Event | Source |
| --- | --- | --- |
| 2026-09-18T12:10:00Z | An automated integration attached a support export to a broadly readable internal ticket. | C1 |
| 2026-09-18T12:14:00Z | Security confirmed that the export contained a credential and contact data. | C2 |
| 2026-09-18T12:18:00Z | The integration owner disabled attachments and restricted the ticket. | C3 |
| 2026-09-18T12:20:00Z | Security confirmed credential revocation. | C3 |
| 2026-09-18T12:24:00Z | Ticket access scope was verified as restricted. Earlier unauthorized downloads remained unconfirmed. | C4 |
| UTC Unknown — no source time supplied | Configuration inspection confirmed that the default profile included secret and contact fields and the integration accepted it unchanged. No sensitive-field check preceded attachment. | C5, C6 |

## Root Cause

The confirmed failure path was a default export profile containing secret and contact fields, accepted unchanged by the ticket integration, with no sensitive-field check before attachment. This allowed sensitive content to reach a broadly readable ticket. [C1, C5, C6]

Evidence-limited 5 Whys:

1. **Why did sensitive content reach the ticket?** The integration attached an export containing a credential and contact data. [C1, C2]
2. **Why did the export contain those fields?** The default export profile included them. [C5]
3. **Why were they not removed or blocked before attachment?** The integration accepted the profile unchanged, and no sensitive-field check existed. [C5, C6]
4. **Why were those defaults and safeguards in place?** Unknown. The packet provides no design or configuration history.

## Lessons Learned

Disabling attachments, restricting access, and revoking the credential provided containment measures, with revocation and access restriction explicitly confirmed. These measures do not establish that no earlier download or credential use occurred. [C3, C4]

The export defaults and integration boundary both permitted sensitive fields to pass through. A pre-attachment safeguard could reduce this known exposure without waiting for the deeper configuration history to be established. [C5, C6]

Audit retention limits retrospective scope assessment. Uncertainty about earlier downloads must remain visible in the incident record. [C4]

## Action Items

All actions below are Proposed. No follow-up owners or dates have been assigned.

| Proposed action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| Proposed: Exclude secret and contact fields from the default support-export profile. | Prevent | TBD | TBD | A default-profile export using synthetic fixtures contains neither category. |
| Proposed: Add a sensitive-field check before ticket attachment, blocking flagged exports. | Detect | TBD | TBD | Synthetic credential and contact fixtures are detected and blocked before attachment; an approved clean fixture passes. |
| Proposed: Reconcile available export, ticket-access, and credential-use evidence to assess exposure scope. | Investigate | TBD | TBD | A restricted assessment records supported counts, any confirmed downloads or use, and explicit evidence gaps. |
| Proposed: Investigate why the default profile included sensitive fields and why the integration accepted it unchanged. | Investigate | TBD | TBD | Configuration and design history are reviewed, with supported contributing conditions and remaining Unknowns documented. |

## Appendix

**Audience and review:** Restricted internal draft. Review status: Pending. External distribution has not been approved; this document is not designated external-ready.

**Source references:** Supplied INC-937 packet: C1 attachment; C2 content confirmation; C3 containment and revocation; C4 access verification and audit limitation; C5 configuration findings; C6 missing check and contact-row count. Packet context establishes synthetic fixtures and resolved status.

**Evidence handling:** Raw credentials and contact identifiers are omitted. Original evidence should remain in its existing authorized location. Approved evidence-store references and custodians are Unknown.

**Unresolved evidence requests:** Export scope, available historical access and credential-use records, configuration history, and the incident’s actual start and end boundaries.

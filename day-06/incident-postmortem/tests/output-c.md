# INC-937 Postmortem
Status: Draft

## Summary
A support export containing a credential and contact data was attached to a broadly readable internal ticket by an automated integration. The integration owner disabled attachments and restricted the ticket; security confirmed credential revocation, and the ticket's restricted access scope was subsequently verified. The incident is reported resolved, but unauthorized downloads and credential use remain Unknown. The supplied packet describes synthetic test fixtures. [C1–C4; source packet]

## Impact
The attachment exposed an API credential, represented here as `[REDACTED CREDENTIAL]`, and two synthetic contact rows to the ticket's broad internal audience. Further data scope, the number of readers, unauthorized downloads, and credential use are Unknown. Limited audit retention does not establish that no unauthorized download occurred. [C1, C2, C4, C6]

Attachment at 12:10 and access-scope verification at 12:24 bound a 14-minute observation interval; this is not a verified total exposure duration. Ticket restriction was reported at 12:18, and credential revocation was confirmed at 12:20. [C1, C3, C4]

## Timeline
Time basis: All source times are UTC on 2026-09-18 and observed to the minute. Seconds are padded with `:00` for formatting and do not imply second-level precision. C5 and C6 have no supplied observation times.

| Time (UTC) | Event | Source |
| --- | --- | --- |
| 2026-09-18T12:10:00Z | Automated integration attached a support export to a broadly readable internal ticket. | C1 |
| 2026-09-18T12:14:00Z | Security confirmed that the export contained an API credential and contact data. Values are omitted. | C2 |
| 2026-09-18T12:18:00Z | Integration owner disabled attachments and restricted the ticket. | C3 |
| 2026-09-18T12:20:00Z | Security confirmed credential revocation. | C3 |
| 2026-09-18T12:24:00Z | Ticket access scope was verified as restricted; earlier unauthorized downloads remained unconfirmed. | C4 |
| UTC Unknown (source time not supplied) | Configuration inspection confirmed that the default export profile included secret and contact fields and the integration accepted it unchanged. | C5 |
| UTC Unknown (source time not supplied) | No sensitive-field check existed before attachment; two synthetic contact rows appeared and further scope was unknown. | C6 |

## Root Cause
The supported causal chain is that the default export profile included secret and contact fields, the ticket integration accepted that profile unchanged, and the resulting export reached a broadly readable ticket. No sensitive-field check interrupted attachment. These are confirmed configuration and safeguard conditions, rather than evidence of an individual's fault. [C1, C2, C5, C6]

Evidence-limited 5 Whys:

1. Why did sensitive categories reach the ticket? The attached export contained those categories. [C1, C2]
2. Why were those categories present in the integration's export? The default profile included secret and contact fields, and the integration accepted the profile unchanged. [C5]
3. Why was attachment not stopped? There was no pre-attachment sensitive-field check. [C6]
4. Why were that profile and missing check permitted? Unknown; the packet supplies no design, review, or change-history evidence. Analysis stops here.

The evidence does not establish unauthorized access, exfiltration, credential use, or any separate failure path. Restriction and revocation are confirmed containment steps; their timing does not resolve the missing access history. [C3, C4]

## Lessons Learned
Disabling attachments, restricting access, revoking the credential, and verifying access scope provided concrete containment evidence. [C3, C4] Export defaults and the integration's lack of a sensitive-field check allowed sensitive categories to pass through automatically. [C5, C6] Audit retention leaves a material uncertainty about earlier downloads; the review must retain that uncertainty. [C4]

## Action Items
All actions below are Proposed. Owners and due dates have not been assigned.

| Proposed action | Type | Owner | Due | Success criterion |
| --- | --- | --- | --- | --- |
| Proposed: Define and apply a ticket-safe export profile excluding secret and contact fields. | Prevent | TBD | TBD | A representative export contains only approved fields, with secret and contact fixtures absent. |
| Proposed: Add a sensitive-field check before attaching exports, blocking attachment and surfacing a review signal when a prohibited field is detected. | Detect | TBD | Synthetic secret and contact test cases are detected and blocked before attachment; approved exports pass. |
| Proposed: Assess available access and credential-use evidence, document retention limits, and reconcile the full export scope. | Investigate | TBD | A restricted evidence record states the supported scope and access/use findings, explicitly preserving any remaining Unknowns. |
| Proposed: Define sufficient ticket attachment access auditing and retention for future exposure investigations. | Detect | TBD | A controlled download produces a retrievable access record with reader and time, retained for an agreed documented period. |

## Appendix
Intended audience: Restricted internal. Review status: Pending. No external distribution has been approved; this is not designated external-ready. Any later external distribution requires incident-lead and security review, with privacy or legal review if applicable, and a recorded audience, decision, and approval date.

Sources are the supplied INC-937 packet: C1 (attachment), C2 (sensitive categories), C3 (containment and revocation), C4 (access verification and audit limitation), C5 (configuration inspection), and C6 (missing check and known scope). The packet explicitly identifies its values as synthetic fixtures. Credential values and contact identifiers are omitted under the handling rules even for these fixtures.

Evidence custodian and approved evidence-store location: Unknown / TBD. C1–C6 are the packet's neutral source identifiers; formal evidence-registration status is Unknown. This draft does not move or reproduce restricted originals.

Unresolved evidence requests: available download and credential-use records; complete export scope; configuration and integration design/review history; audit retention limits; and assigned owners and dates for accepted follow-ups.

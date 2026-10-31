# Sensitive incident handling

## Select the document audience
- Default to a restricted internal draft until its permitted audience is known.
- Separate the learning narrative from evidence that requires tighter access controls.
- A postmortem for external distribution remains a retrospective, not a live status-page update.
- Record the intended audience and review status in Appendix.

## Redaction checklist
- Replace passwords, tokens, private keys, session cookies, and signed URLs with `[REDACTED CREDENTIAL]`.
- Remove full credential values even if revoked; published examples can encourage unsafe copying.
- Remove customer names, email addresses, account identifiers, and raw payloads unless specifically approved for that audience.
- Retain only the data categories and aggregate scope needed to explain impact.
- Avoid small-group aggregates that let readers infer a customer's identity.
- Remove exploit instructions, vulnerable endpoints, and unpatched attack details from broadly distributed drafts.
- Check code blocks, tables, query strings, log excerpts, and attachments as well as prose.
- Use neutral evidence IDs rather than filenames or links containing sensitive values.

## Preserve evidence without duplicating exposure
1. Refer to restricted material by an approved evidence ID and custodian.
2. Keep original logs in their existing authorized evidence store; this writing task does not authorize moving them.
3. Describe what the evidence establishes without reproducing its secret contents.
4. Distinguish credential exposure from confirmed use, and data access from confirmed exfiltration.
5. If access logs are incomplete, describe the scope as unconfirmed rather than cleared.
6. Record rotation or containment as completed only when supplied evidence confirms it.
7. Propose remaining containment work as a follow-up; this drafting skill does not execute it.

## Example: leaked package-signing key
A build diagnostic exposed signing material in an internal artifact.
The draft says: "Signing material was exposed; restricted evidence SEC-E4 is held by the security team."
It records affected artifact classes and the known exposure interval without embedding key bytes.
If use of that material is unverified, it distinguishes exposure from malicious package signing.
An action may verify revocation and artifact provenance without claiming either has already happened.

## Before external distribution
- Obtain review from the incident lead and security owner for accuracy and remaining exposure.
- Include privacy or legal reviewers when customer information or notification duties are implicated.
- Record reviewers, decision, approved audience, and approval date; use Pending if approval is absent.
- Withhold the external-ready designation until that review is complete, because redaction alone does not establish approval to disclose.
- Keep unreviewed findings in the restricted draft and request an approved external summary.

# Causal analysis beyond one chain

## Choose the structure
- Continue the default method while one evidence-backed chain explains the observed failure.
- Switch to a causal tree when parallel paths, interacting safeguards, or competing explanations cannot fit that chain honestly.
- A user's request for a tree also justifies using one; diagramming does not raise confidence in its claims.
- Do not switch merely to fill a longer document or manufacture more causes.

## Build the tree
1. Define the top event in observable terms and specify the affected scope.
2. List candidate contributing conditions with source identifiers.
3. Use AND when the parent requires all child conditions together.
4. Use OR when any child path is sufficient for the parent event.
5. Mark each link Observed, Supported inference, Hypothesis, or Unknown.
6. Keep disputed alternatives visible and identify the evidence that would distinguish them.
7. Check whether removing a proposed condition would plausibly interrupt that path.
8. Translate supported gaps into follow-ups using the entrypoint's action rules.

## Worked example: scheduled reports unavailable
Evidence: R1 records an expired signing certificate at 08:00 UTC.
R2 shows report delivery failing certificate validation after 08:00 UTC.
R3 shows that no valid replacement certificate was installed.
R4 records no expiry alert before the delivery failure.
No evidence yet explains why certificate renewal did not complete.

```text
Reports unavailable [Observed, R2]
  AND [Supported inference, R1-R3]
  +-- Active signing certificate expired [Observed, R1]
  +-- No valid replacement available [Observed, R3]
        OR [Hypotheses; distinguish with renewal job logs]
        +-- Renewal job did not run [Unknown]
        +-- Renewal ran but installation failed [Unknown]
Separate safeguard gap: expiry alert absent [Observed, R4]
```

The tree distinguishes the combined failure conditions from two unconfirmed renewal paths.
The missing alert can prolong exposure, but it did not make the certificate expire.
Request renewal execution and installation logs to discriminate between the hypotheses.
Propose expiry monitoring with an observable alert test as a Detect action.
Keep renewal or installation changes conditional on those logs rather than selecting a convenient root cause.

## Review the explanation
- Separate triggering events, enabling conditions, and failed safeguards.
- Check that AND/OR labels describe the stated parent event rather than visual convenience.
- Prefer several bounded causal findings over an unsupported single root cause.

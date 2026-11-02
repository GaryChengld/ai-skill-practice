**Defer the dependency upgrade for this release, disable custom rule uploads, and retain built-in schedules.** The only supplied fixed version cannot run on Python 3.9 and removes an API the parent uses.

Ownership: `requirements.txt`, runtime graph; `requirements.in` directly pins `fixture-calendar-engine==3.8.0`. CI uses pip on Python 3.9. Guidance: `references/python.md`.

| Package / advisory | Current → Target | Direct or transitive | Fix | Verification | Risk |
| --- | --- | --- | --- | --- | --- |
| `fixture-rule-eval`; synthetic `FIXTURE-H-06`, supplied in `input-h.md`. Affected: `>=1.6.0,<2.0.0`. | Resolved: `1.6.0`. Only fixed release: `2.0.0`; incompatible with this release. Installed version: Unknown. | Transitive; only supplied path: calendar-engine `3.8.0` → rule-eval `1.6.0`, pinned exactly by the parent. | Keep `requirements.in` and `requirements.txt` unchanged. Disable custom rule uploads through the deployment configuration or feature gate; exact file/key is Unknown. Record a time-limited exception owned by the **schedules team**, reviewed **2026-11-09**. | **Proposed:** clean Python 3.9 installation from `requirements.txt`; `python -m pip check`; `python -m pip inspect`; rerun the supplied scanner and focused schedule tests. | Vulnerable code remains installed. Mitigation depends on disabling the exploit prerequisite in every deployment. The alert remains valid. |

A direct-parent upgrade is preferred, but the supplied inventory contains no compatible release or backport. A pip constraint cannot replace the parent’s exact `1.6.0` requirement. Forcing `2.0.0` would introduce both interpreter and API incompatibilities.

For release acceptance, collect evidence that custom uploads are disabled across deployments and cannot be enabled or reached through alternate upload routes. Test that upload attempts are rejected and built-in schedules still execute. Attach that evidence and the remaining scanner finding to the exception; do not report the vulnerability as fixed.

Revisit the decision when there is:

- A parent release supporting Python 3.9 that resolves to a fixed evaluator, with dependency metadata and compatibility tests.
- A supported security backport, with an advisory identifying its fixed version and tests proving the vulnerable behavior is removed.
- Approved scope for Python migration and parent/API changes, or engine replacement, backed by a reproducible resolution and passing schedule tests.

Open questions: Confirm whether the graph’s shortened names `calendar-engine` and `rule-eval` refer to the `fixture-*` distributions. The requirements compiler and feature-control location are unspecified.

Rollback: No dependency files change under this plan. Reverting the feature mitigation restores the stated exploit prerequisite and requires renewed risk review.

All checks above are **proposed**; no installation, configuration changes, or tests were executed.

# Scanner finding: mixed tooling repository
This is a fictional repository and synthetic advisory data, not a live vulnerability report.
Files: web/package.json, web/package-lock.json, jobs/pyproject.toml, jobs/uv.lock.
The web project builds operational dashboards; the jobs project runs scheduled data processing.
The scanner summary contains a single component entry: fixture-payload-codec, version 4.2.0.
Synthetic advisory FIXTURE-M2-12 affects fixture-payload-codec >=4.2.0,<4.2.3.
The advisory's supplied remediation field is version 4.2.3.
The summary includes severity and version but no manifest path, package URL, or dependency chain.
We have not supplied the contents of either lockfile or either dependency declaration section.
Both lockfiles are active in CI; neither is an abandoned migration artifact.
What should we change to address this finding?

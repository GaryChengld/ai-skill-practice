What should I write for this commit? Here's what I have staged:

- `src/reports/export.ts`: add a CSV download for monthly reports.
- `src/auth/login.ts`: fix a login timeout by clearing the previous request's timer before retrying. This change is independent of the export work.

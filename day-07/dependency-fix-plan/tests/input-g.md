# Scanner finding: telemetry agent
This is a fictional repository and synthetic advisory data, not a live vulnerability report.
Files: go.mod, go.sum, cmd/agent/, internal/transport/; CI uses Go 1.23.
go.mod directly requires example.invalid/fixture/streamheader v1.2.0.
go.sum and the supplied module list agree on v1.2.0; no second copy is reported.
Synthetic advisory FIXTURE-G-31 affects streamheader >=v1.2.0,<v1.2.3.
Scanner location: go.mod, runtime module graph; v1.2.3 is the first fixed patch.
Supplied maintainer notes say v1.2.3 keeps the module path and Go 1.23 compatibility.
The transport header parsing regression suite covers the reported failure mode.
The release job checks the resolved module graph and reruns the same vulnerability scanner.
We need a plan from this snapshot; no dependency edits or installs have been performed yet.

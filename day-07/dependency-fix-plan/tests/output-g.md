## Dependency fix plan

Upgrade `example.invalid/fixture/streamheader` from `v1.2.0` to **`v1.2.3`**, the first fixed patch in the supplied synthetic advisory.

Ownership: telemetry agent’s root `go.mod` and `go.sum`; Go modules, CI uses Go 1.23.  
Guidance: no dedicated Go reference exists in this skill; commands checked against [official Go 1.23 documentation](https://pkg.go.dev/cmd/go@go1.23.0).

| Package / advisory | Current → Target | Direct or transitive | Fix | Verification | Risk |
| --- | --- | --- | --- | --- | --- |
| `example.invalid/fixture/streamheader`; synthetic `FIXTURE-G-31`, affected `>=v1.2.0,<v1.2.3` | Declared and supplied resolved version: `v1.2.0` → `v1.2.3`. Deployed version: Unknown. | Direct runtime dependency; agent → streamheader. No second copy reported. | Change the `go.mod` requirement to `v1.2.3`; regenerate `go.sum` with Go tooling. | **Proposed:** inspect the resolved graph, run header parsing regressions, build the agent, rerun the existing release scanner. | Maintainer notes confirm unchanged module path and Go 1.23 compatibility. Behavior still needs testing; deployed exposure remains until release. |

This direct patch upgrade is the smallest supported fix. An override or broader dependency upgrade is unnecessary. Review any additional dependency changes introduced by the new release.

**Proposed commands**, from the module root using CI’s Go 1.23 toolchain:

```text
go get example.invalid/fixture/streamheader@v1.2.3
go mod tidy
git diff -- go.mod go.sum
```

Go updates the requirement and generates checksums; `go.sum` is a checksum record, not a lockfile. Keep only required changes. [Go module reference](https://go.dev/ref/mod#go-get)

Then, in a fresh CI checkout with an empty module cache:

```text
go mod download
go mod verify
go list -mod=readonly -m all
go mod graph
go test -mod=readonly -count=1 ./internal/transport/... ./cmd/agent/...
go build -mod=readonly ./cmd/agent/...
git diff --exit-code -- go.mod go.sum
```

Require the selected module to be `v1.2.3`, inspect all graph edges involving it, and confirm the header parsing regression suite passes. Rerun the **same vulnerability scanner used by the release job** and require `FIXTURE-G-31` to clear. `go mod verify` checks cache integrity; the scanner provides advisory verification. [Go verification documentation](https://go.dev/ref/mod#go-mod-verify)

Open questions: exact scanner invocation and any required regression-test flags are Unknown. Use the existing CI definitions.

Rollback: revert `go.mod` and `go.sum` together. Returning to `v1.2.0` restores the reported exposure.

No dependency edits, installs, or validation commands were executed.

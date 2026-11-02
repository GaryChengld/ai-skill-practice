# Scanner finding: preview application workspace
This is a fictional repository and synthetic advisory data, not a live vulnerability report.
Files: package.json, package-lock.json, apps/preview/package.json, apps/preview/test/.
Root package.json is private, declares workspaces ["apps/*"], and pins packageManager to npm@10.9.2.
apps/preview/package.json declares runtime dependency @fixture/vector-loader at exact version 2.4.0.
Root package-lock.json resolves preview -> @fixture/vector-loader@2.4.0 -> @fixture/svg-chunk@1.2.0.
The vector-loader publisher pins its svg-chunk dependency to exact version 1.2.0.
Synthetic advisory FIXTURE-O-09 affects svg-chunk >=1.2.0,<1.2.2; 1.2.2 is the fixed patch.
The scanner identifies this sole path in root package-lock.json and the preview workspace.
No published vector-loader version updates the pin; replacing the loader requires a feature migration.
The supplied svg-chunk patch notes state that 1.2.2 preserves the 1.2 public API; loader compatibility is untested.
CI uses npm ci at the root and runs npm test --workspace apps/preview for malformed SVG and preview snapshots.
What is the smallest proposed fix, what must be verified, and when can the temporary change be removed?

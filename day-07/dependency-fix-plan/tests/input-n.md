# Scanner finding: storefront asset pipeline
This is a fictional repository and synthetic advisory data, not a live vulnerability report.
Files: package.json, package-lock.json, src/, test/; packageManager is npm@10.9.2.
package.json declares devDependency @fixture/banner-builder at exact version 3.6.0.
package-lock.json resolves @fixture/banner-builder@3.6.0 -> @fixture/template-reader@1.9.0.
Synthetic finding FIXTURE-N-17 targets @fixture/template-reader versions >=1.8.0,<1.9.2.
The scanner reports the path package-lock.json, development dependency graph.
Publisher notes supplied with the scan say 1.9.2 is the first fixed compatible patch.
@fixture/banner-builder@3.6.1 selects template-reader >=1.9.2,<2; there are no other paths.
The asset snapshot and malformed-template tests run through npm test; CI installs with npm ci.
We need a change proposal for this repository snapshot, including checks and compatibility risks.

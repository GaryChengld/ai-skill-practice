# Scanner finding: message relay
This is a fictional repository and synthetic advisory data, not a live vulnerability report.
Files: pom.xml, relay/pom.xml, mvnw, relay/src/test/; Maven wrapper 3.9.9, Java 17.
relay/pom.xml directly declares org.example.fixture:relay-client:6.1.0.
The supplied tree is relay-client:6.1.0 -> org.example.fixture:frame-parser:2.0.0.
Synthetic advisory FIXTURE-J-08 affects frame-parser >=2.0.0,<2.0.3, fixed in 2.0.3.
Scanner location: relay/pom.xml runtime graph; there are no other affected paths.
The parent POM manages neither coordinate and imports no BOM for this family.
Upstream metadata supplied here says relay-client 6.1.1 requires frame-parser 2.0.3.
That parent patch supports Java 17 and retains the same public API as 6.1.0.
CI runs ./mvnw -pl relay -am verify, then scans the packaged relay distribution.
We want a minimal remediation proposal, not a build-tool or framework migration.

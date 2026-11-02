Change `relay/pom.xml` to upgrade **`org.example.fixture:relay-client` from `6.1.0` to `6.1.1`**. The supplied metadata says this patch brings in fixed `frame-parser:2.0.3`, supports Java 17, and preserves the public API.

Ownership: `relay/pom.xml`, Maven runtime graph; wrapper 3.9.9, Java 17.  
Guidance: `dependency-fix-plan/references/jvm.md`. Advisory data is synthetic.

| Package / advisory | Current → Target | Direct or transitive | Fix | Verification | Risk |
| --- | --- | --- | --- | --- | --- |
| `org.example.fixture:frame-parser`; `FIXTURE-J-08`, affected `>=2.0.0,<2.0.3`, fixed in `2.0.3` | Supplied resolution `2.0.0` → `2.0.3`; installed state unverified | Transitive through directly declared `relay-client:6.1.0`; sole affected path | In `relay/pom.xml`, change `relay-client` version to `6.1.1`. No root POM, BOM, override, wrapper, or framework changes needed. No lockfile is identified in the snapshot. | **Proposed:** inspect effective POM and runtime tree, run clean verification, then scan the packaged distribution. None executed. | Supplied compatibility evidence supports this patch. Confirm behavior and packaged contents before closing the alert. |

Proposed commands, from the repository root:

```sh
./mvnw -pl relay help:effective-pom
./mvnw -pl relay -am dependency:tree -Dscope=runtime "-Dincludes=org.example.fixture:relay-client,org.example.fixture:frame-parser"
./mvnw -pl relay -am clean verify
```

Confirm the effective declaration is `relay-client:6.1.1` and the runtime tree resolves `frame-parser:2.0.3`, with no affected version remaining. Run the existing CI scanner against the newly packaged relay distribution, including embedded or shaded copies. Exercise existing relay framing/parsing tests, particularly valid and malformed messages.

This direct-parent patch is the smallest supported fix and avoids maintaining a separate transitive override.

Open questions: The scanner command and focused test names were not supplied.

Rollback: Revert the `relay/pom.xml` version change and rebuild; rollback restores the vulnerable dependency path. No files were changed.

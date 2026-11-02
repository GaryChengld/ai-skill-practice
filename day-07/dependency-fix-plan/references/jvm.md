# JVM build tools

## Detect
- `pom.xml` selects Maven; `build.gradle` or `build.gradle.kts` selects Gradle.
- Prefer the checked-in Maven/Gradle wrapper and its pinned distribution when present.
- Find the affected module, its parent/platform, dependency scope or configuration, and any version catalog.
- A root aggregator does not necessarily own the affected module's dependency declarations.

## Inspect the tree
- Maven: `mvn dependency:tree -Dincludes=<group>:<artifact>`; include the affected module and scope.
- `mvn help:effective-pom` exposes inherited dependency management and active profile effects.
- Gradle: `./gradlew :<module>:dependencyInsight --dependency <artifact> --configuration runtimeClasspath`.
- Use the actual affected configuration for test/build-only findings; runtimeClasspath is not universal.
- Gradle's `dependencies` report shows paths; `dependencyInsight` explains selection and conflicting constraints.

## Fix a direct dependency
- Maven: change the declaring dependency version or its property; if a BOM owns the version, assess a compatible BOM release first.
- Verify inherited management before adding a local version that bypasses the parent platform.
- Gradle: change the declaring dependency or version-catalog alias; platform-managed versions may live elsewhere.
- Respect the supported Java version and framework alignment when selecting a library or BOM release.
- Build plugins have their own dependency graphs; a project-library change does not automatically update plugin dependencies.

## Override a transitive dependency
- Maven `dependencyManagement` selects a version when the dependency is encountered; it does not add it to the graph.
- Illustrative native-library alignment, not a real advisory:
```xml
<dependencyManagement><dependencies>
  <dependency>
    <groupId>org.example.graphics</groupId><artifactId>sample-raster-core</artifactId>
    <version>5.2.7</version>
  </dependency>
</dependencies></dependencyManagement>
```
- Put management in the POM inherited by the affected module; inspect effective management when a BOM also supplies a value.
- Gradle Kotlin DSL can add a constraint without adding a dependency:
```kotlin
dependencies {
    constraints {
        implementation("org.example.graphics:sample-raster-core:5.2.7") {
            because("align the native raster binding")
        }
    }
}
```
- A normal Gradle version constraint participates in selection and is not an exact force; inspect the selected version.
- Use `strictly` only when an exact compatibility bound is necessary; conflicting strict bounds may make resolution fail.

## Verify
- Maven: re-run the module's dependency tree, then the repository's `verify` lifecycle and vulnerability scanner.
- Gradle: re-run dependencyInsight for every affected configuration; update dependency locks with the existing locking task/options when enabled.
- Run the relevant Gradle `check`/integration tasks and scanner on the resolved artifacts.
- Inspect the packaged artifact for shaded copies; a fixed external coordinate may leave embedded vulnerable classes unchanged.

## Pitfalls
- Maven defaults to the nearest dependency definition, not the newest version; equal-depth ties use declaration order.
- Maven project dependency management does not govern a build plugin's transitive dependencies.
- A BOM can coordinate a family of libraries; overriding one member may break binary compatibility with siblings.
- Gradle constraints apply to configurations that include them; a runtime fix may miss a separate test/tool graph.

## Sources
- [Maven dependency mechanism](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)
- [Gradle dependency constraints](https://docs.gradle.org/current/userguide/dependency_constraints.html)

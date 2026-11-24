Can you draft a commit message for this diff?

```diff
diff --git a/src/config.ts b/src/config.ts
--- a/src/config.ts
+++ b/src/config.ts
@@ -18,3 +18,3 @@
-export function parseConfig(path: string, opts?: ParseOptions): Config {
-  return readConfig(path, opts);
+export function parseConfig(path: string): Config {
+  return readConfig(path);
 }
```

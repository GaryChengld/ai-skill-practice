# Stage-review notes

The validator environment and invalid fixtures live outside the repository. Invalid fixtures were removed; no environment or invalid skill was added to the catalog.
The raw CLI catalog has 2,665 characters (stdout decoded as UTF-8 without newline normalization), or about 666 tokens using characters / 4. This includes absolute locations, XML markup, escaping, and the CLI's Windows line endings; it is a budget estimate, not tokenizer output.
The catalog lists all five original skill directories together; copies are unnecessary because to-prompt accepts multiple directories. Its XML was not hand-edited.
Day-04's new TemporaryDirectory fixture passed on Git 2.21.0.windows.1: cached default develop, dates/authors/worktree, upstream ahead status, merge membership, unchanged refs, and cleanup. The test does not run the language-model report or test branch age classification.
Day-03's example was moved to another domain; the previous outputs still describe earlier versions and cannot demonstrate the effect of that change.
Changes were initially left uncommitted as requested. After explicit commit-and-push authorization, repairs were committed in bc5cf45 and AUDIT.md was updated with that hash. The coach log remains untouched.
The review follow-up was committed in 998c513 after explicit authorization: enforce baseline-equal holds in the main flow, restore the 150-line commit-skill cap, explain three rules, and add four independent routing challenges. This documentation follow-up records the real fix hash and publication limitation.
Catalog locations are absolute paths on this Windows machine. They do not affect these routing decisions, but the catalog is a local test artifact, not a portable publication artifact; regenerate it from installed skill locations when packaging for another environment, preserving raw CLI output.

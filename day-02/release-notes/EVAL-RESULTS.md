# Routing Evaluation Results

The original experiment below is historical evidence for V1/V2/V3 at commit `10f5377`. It includes leading disclaimers in T05, T11, T12, V07, and V08 that make the boundaries easier to classify. Its perfect V2/V3 scores do not demonstrate performance on naturally ambiguous requests and do not evaluate the current R1 description. Review follow-up results are recorded separately below, without overwriting these observations.

## Method - 2026-10-21

This is a competitive metadata-routing experiment, not an application skill-loading test. All candidates were evaluated against the same three-skill catalog, in this order:

1. `release-notes`, using the candidate from DESCRIPTIONS.md.
2. `conventional-commits`, using the parsed name and description from `../../day-01/conventional-commits/SKILL.md`.
3. `pr-description`, using the parsed name and description from `../competitors/pr-description/SKILL.md`.

The competitor stub and queries were written first, followed by all three descriptions. They were frozen before evaluation. The dataset has 20 queries: 12 train (six positive, six negative) and eight validation (four positive, four negative). Seven positive queries omit the literal phrase "release notes". Six negatives explicitly target the competing commit or PR skills; the remainder test internal-report and Git-instruction boundaries.

Tool: `collaboration.spawn_agent`, with `fork_turns: "none"`, a fresh agent per candidate training batch and a separate fresh agent for validation. The inherited model was used without an override; no API model snapshot, temperature, or seed was pinned. Task names were `day02_train_a` (V1), `day02_train_b` (V2), `day02_train_c` (V3), and `day02_validation` (selected V3).

Only the three names and descriptions plus query IDs and query text were provided. Labels, expected skills, split fields, skill bodies, other candidates, and earlier results were withheld. Agents were instructed not to execute queries, use tools, or change files. The routing instruction was:

```text
For each independent query select exactly one skill from this catalog or none
if no description fits. Judge the provided descriptions, not other installed
skills. Return a JSON array of {id, selected_skill, reason}.
```

Each batch evaluated its queries together in one context. This is a single run per candidate, not independent repeated sampling per query. The selected skill was scored after responses arrived. Exact-routing accuracy requires equality with `expected_skill`; trigger accuracy requires that selection of `release-notes` equals `should_trigger`. Both metrics agree on this run. A wrong competing-skill selection would fail exact routing even if it correctly avoided `release-notes`.

V3 was selected and recorded from training results before the validation agent was started. Neither candidates nor labels were changed after evaluation. Validation was run only for V3.

## Results

| Version | Characters | Train exact routing | Train trigger accuracy | Validation exact routing |
| --- | ---: | ---: | ---: | ---: |
| V1 | 74 | 10/12 (83.3%) | 10/12 (83.3%) | Not run |
| V2 | 240 | 12/12 (100%) | 12/12 (100%) | Not run |
| V3 - selected | 477 | 12/12 (100%) | 12/12 (100%) | 8/8 (100%) |

For release-notes detection, V1 produced six true positives, four true negatives, two false positives, and no false negatives. V2 and V3 each produced six true positives and six true negatives on train. V3 produced four true positives and four true negatives on validation, also 8/8 (100%) trigger accuracy.

### Training decisions

| ID | Expected | V1 actual | V2 actual | V3 actual |
| --- | --- | --- | --- | --- |
| T01 | release-notes | release-notes | release-notes | release-notes |
| T02 | release-notes | release-notes | release-notes | release-notes |
| T03 | release-notes | release-notes | release-notes | release-notes |
| T04 | release-notes | release-notes | release-notes | release-notes |
| T05 | release-notes | release-notes | release-notes | release-notes |
| T06 | release-notes | release-notes | release-notes | release-notes |
| T07 | conventional-commits | conventional-commits | conventional-commits | conventional-commits |
| T08 | conventional-commits | conventional-commits | conventional-commits | conventional-commits |
| T09 | pr-description | pr-description | pr-description | pr-description |
| T10 | pr-description | pr-description | pr-description | pr-description |
| T11 | none | release-notes (FAIL) | none | none |
| T12 | none | release-notes (FAIL) | none | none |

### Selected-version validation decisions

| ID | Expected | V3 actual |
| --- | --- | --- |
| V01 | release-notes | release-notes |
| V02 | release-notes | release-notes |
| V03 | release-notes | release-notes |
| V04 | release-notes | release-notes |
| V05 | conventional-commits | conventional-commits |
| V06 | pr-description | pr-description |
| V07 | none | none |
| V08 | none | none |

## Failure Analysis and Selection

1. **T11 - internal infrastructure retrospective.** The query asks for a Markdown summary of CI and test commits, retaining every internal detail and explicitly excluding a product release. V1 selected `release-notes`. Its explanation was that the broad description covers summaries from commits without an audience restriction or release requirement. V1 describes an input transformation but never establishes the intended deliverable. V2's release-oriented activation clause and V3's internal-report exclusion both avoided this false positive.
2. **T12 - engineering report from diffs.** The query asks for modified functions and coverage changes, not a PR description or customer announcement. V1 again selected `release-notes`, explaining that its broad software-summary description includes an internal engineering report. The failure is caused by the shared source format, not a missing exact keyword. V3 explicitly separates source material from deliverable and excludes internal reports; V2 also correctly inferred the intended boundary from its activation clause.

Choose **V3**. V2 and V3 tied on training accuracy; the predeclared tie-break prefers V3, then V2, then V1. V3 makes the commit-message, PR-description, and internal-report boundaries explicit. This run does not demonstrate higher routing accuracy for V3 than V2, and its extra length is a tradeoff. T05 shows that a single merged PR can still be release-note input; T10 and V05 show that mentioning a release-notes component does not override the requested PR or commit deliverable.

## Overfitting and Limits

There is no observed validation drop, and no descriptions or labels were tuned after seeing results. That reduces direct validation leakage but does not establish broad generalization. One author designed both the queries and candidates; several validation queries share training vocabulary and the same internal-report boundary. All queries are English, the catalog order is fixed, and there is one batched judgment per version. Cross-query context and routing nondeterminism may affect the scores.

The experiment measures a model's choice among three supplied metadata entries, not automatic discovery, actual skill-body loading, release-note quality, or portability across products. Next use a newly authored holdout set with unseen wording, mixed deliverables, multilingual requests, and shuffled catalog order; repeat trials and inspect actual loading separately. Do not reuse this validation set as an untouched holdout after revisions.

## Frozen Input Fingerprints

Historical SHA-256 values recorded before the original evaluation. Retrieve these inputs from commit `10f5377` using `git show 10f5377:<path>`; the query set and descriptions have been extended after review, so their current hashes need not match. The conventional-commits hash was taken from a CRLF working-tree file: convert its Git blob's LF line endings to CRLF to reproduce that hash. Its LF Git-blob hash is `172104c6a5bdad9a59cfed74ba6d4d3f87d2ac67b042ee586a9370c6150b3898`. The other three recorded hashes use LF bytes.

| Input | SHA-256 |
| --- | --- |
| evals/trigger-queries.json | `03a0ebaeb372699f54b78f319596f92d071d9675684614cb01c5472eb8d3771e` |
| DESCRIPTIONS.md | `a2868097ec956675c7c75727dfc23b84498ffe5213ae9bbfeb613ce6b5ec178e` |
| ../competitors/pr-description/SKILL.md | `9e22dd93cdfd2f80584ba63729a488ede5d50239b10c8927b0147e0224bdc839` |
| ../../day-01/conventional-commits/SKILL.md | `c15644bbf54d466dbe8c4395ab8403113e579540ce1c2bc1770e11f18c3588c8` |

## Review Follow-up - R1

The current SKILL.md uses R1 (439 characters), supplied during review, rather than the original selected V3 (477 characters). Its first sentence specifies user-facing release documentation. The body now preserves an existing changelog's format, introduction, and Unreleased section while placing the new version above older versions. Its example includes an explicit configuration-key migration.

Six new queries H01-H06 contain no defensive disclaimers. The original 20 queries remain unchanged for historical traceability, giving 26 queries overall: 15 train and 11 validation, both with positives and negatives. The challenge labels and R1 were fixed before the run. Unlike the original selection experiment, this follow-up evaluates all six challenge queries for every compared candidate, including their validation-labeled rows. It is exploratory, not a new untouched validation estimate. R1 has not been rerun on the original 20 queries.

### Boundary policy

- H01 requests a changelog update; select release-notes and inspect the file to establish the target section and existing format.
- H04 requests a GitHub Release body; select release-notes. This requests a draft, not permission to publish it.
- H05 requests a commit message and H06 requests a PR description; select the respective competitor.
- H02 only identifies a sprint demo, and H03 only identifies a tag range. Provisionally abstain from skill selection and clarify audience or output. A customer-facing demo or a tag comparison explicitly intended as release documentation would qualify. This conservative policy was recorded as an assumption before evaluation; the user has not explicitly resolved these two ambiguous labels.

### Method and observations

Use `collaboration.spawn_agent` with `fork_turns: "none"`, one fresh batch per candidate: `day02_review_v2`, `day02_review_v3`, and `day02_review_r1`. Each receives its release-notes description plus the same conventional-commits and pr-description metadata, followed by only the six IDs and query strings. Expected labels, rationales, the boundary policy, and other results are withheld. The shared instruction asks for the best matching skill or `none`, returned as `{id, selected_skill, reason}`. No user query is executed. The inherited model is unpinned, catalog order remains fixed, and there is one batch per candidate.

| ID | Provisional expected route | V2 actual | Original V3 actual | R1 actual |
| --- | --- | --- | --- | --- |
| H01 | release-notes | release-notes | release-notes | release-notes |
| H02 | none - clarify | release-notes | none | none |
| H03 | none - clarify | release-notes | release-notes | none |
| H04 | release-notes | release-notes | release-notes | release-notes |
| H05 | conventional-commits | conventional-commits | conventional-commits | conventional-commits |
| H06 | pr-description | pr-description | pr-description | pr-description |

| Candidate | Challenge exact-routing accuracy | If H02 and H03 instead count as release-notes |
| --- | ---: | ---: |
| V2 | 4/6 (66.7%) | 6/6 (100%) |
| Original V3 | 5/6 (83.3%) | 5/6 (83.3%) |
| R1 | 6/6 (100%) | 4/6 (66.7%) |

V2 classified H02 as a release digest and H03 as a summary between software versions. Original V3 abstained on H02 but still chose release-notes for H03. R1 abstained on both. The new failures expose a source-range versus deliverable ambiguity rather than merely missing release-note keywords. However, both abstaining demo responses assumed an internal audience; the query itself does not establish that. A correct clarification question has not been demonstrated by this routing-only test.

All candidates agree on the four unambiguous cases. The apparent improvement comes entirely from the two policy-sensitive labels; the alternative scoring above reverses the ranking. Retain R1 for its explicit audience and readable scope, not as proof of universally superior routing. The initial perfect scores were overly easy evidence, and this small, author-designed challenge still cannot establish generalization. Do not tune the candidates to these six cases and continue treating them as held out.

### Body smoke test

Agent `day02_review_body` was given the revised skill body and a realistic changelog task with version 1.3.0, date 2026-10-21, CSV export, a login fix, a breaking `timeout` to `requestTimeout` configuration rename, and CI/test-only work. Existing text included an introduction, an Unreleased entry for planned dashboard themes, and version 1.2.0 with a pagination fix. Direct file reading failed in that agent's environment, so the exact skill body was supplied in a follow-up. No expected output or scoring criteria were provided to the agent, and no files were changed.

Its returned draft preserved the introduction, Unreleased entry, old version, and existing bracketed version/date format. It inserted 1.3.0 below Unreleased and above 1.2.0, grouped the user-visible additions/fix/breaking change, and omitted CI and test-only work. The migration text was: "Rename the key in your configuration before upgrading." Manual inspection passed these checks. This validates one supplied-text drafting example; it does not test in-place changelog editing or automatic skill discovery.

### Review input fingerprints

These SHA-256 byte hashes were recorded before the review agents started. No candidate, query, label, skill body, or competitor metadata was edited in response to their results. Byte hashes are line-ending-sensitive; Git checkout conversion may change them without changing the text.

| Input | SHA-256 at review freeze |
| --- | --- |
| DESCRIPTIONS.md | `d2dde43982a085365d0175ededd90485434bbfbc1f508dceb92fa01434f46c5a` |
| SKILL.md | `e4b849281692c8fd173caf7638afb33b09843c6d530056cc8223afd3d08d296f` |
| evals/trigger-queries.json | `162207b19a41c75495bb714fb557c6e1f9f817c569ac7895a53f7cbee3273645` |
| ../competitors/pr-description/SKILL.md | `c6a2fe87b70f8b3e2cab2ecc243c5657547dc98aa75646179f398d9e3c22b8b4` |

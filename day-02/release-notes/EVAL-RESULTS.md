# Routing Evaluation Results

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

SHA-256 values recorded before evaluation; the same bytes remained in place afterward:

| Input | SHA-256 |
| --- | --- |
| evals/trigger-queries.json | `03a0ebaeb372699f54b78f319596f92d071d9675684614cb01c5472eb8d3771e` |
| DESCRIPTIONS.md | `a2868097ec956675c7c75727dfc23b84498ffe5213ae9bbfeb613ce6b5ec178e` |
| ../competitors/pr-description/SKILL.md | `9e22dd93cdfd2f80584ba63729a488ede5d50239b10c8927b0147e0224bdc839` |
| ../../day-01/conventional-commits/SKILL.md | `c15644bbf54d466dbe8c4395ab8403113e579540ce1c2bc1770e11f18c3588c8` |

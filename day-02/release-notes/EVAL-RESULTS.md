# Routing Evaluation Results

Current description: **R2, 431 characters**. All routing scores below belong to earlier evaluated descriptions; R2 has not been benchmarked. The documentation correction does not create new evaluation results.

## Method and History

On 2026-10-21, use `collaboration.spawn_agent` with `fork_turns: "none"`, one fresh batch per candidate, with the same ordered catalog of release-notes, day-01 conventional-commits, and the pr-description stub. Provide only names, descriptions, query IDs, and queries; withhold labels and other results. Return one `selected_skill` or `none` and a reason for each query. Exact accuracy compares with `expected_skill`; trigger accuracy compares release-notes selection with `should_trigger`.

The original experiment froze 12 train and eight validation queries before comparing V1/V2/V3. V3 was chosen on training scores by the predeclared tie-break, then tested on validation. Agents: `day02_train_a`, `day02_train_b`, `day02_train_c`, and `day02_validation`. Original inputs are in commit `10f5377`.

The follow-up compared V2/V3/R1 on all six H queries with both competitors present. Agents: `day02_review_v2`, `day02_review_v3`, and `day02_review_r1`. These cases now use `split: challenge`, correcting their earlier train/validation labels; query text, expected routes, and decisions are unchanged. The current file contains 12 train, eight validation, and six challenge queries.

Full prior run details and fingerprints are preserved in `git show 4113ae7:day-02/release-notes/EVAL-RESULTS.md`. Runs used an inherited, unpinned model, fixed catalog order, and one shared query context per batch. They measure metadata routing, not automatic skill loading or repeated independent trials.

## Original Results

| Version | Characters | Train exact routing | Train trigger accuracy | Validation exact routing |
| --- | ---: | ---: | ---: | ---: |
| V1 | 74 | 10/12 (83.3%) | 10/12 (83.3%) | Not run |
| V2 | 240 | 12/12 (100%) | 12/12 (100%) | Not run |
| V3 - selected | 477 | 12/12 (100%) | 12/12 (100%) | 8/8 (100%) |

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

## Original Failure Analysis

- **T11, infrastructure retrospective:** V1 selected release-notes because its broad description covers any commit summary. The intended internal audience and retention of CI/test detail require `none`; V2/V3 avoided this false positive.
- **T12, engineering report:** V1 again selected release-notes, treating diffs as sufficient evidence of release-documentation intent. The requested function/coverage report is not release notes; V2/V3 abstained.

V2 and V3 tied at 12/12; V3 was selected by the predeclared preference for explicit boundaries, not demonstrated superior accuracy. T05, T11, T12, V07, and V08 contain defensive disclaimers, making the original benchmark easier than natural requests. The 100% scores therefore provide limited evidence of generalization.

## Challenge Results

H01 and H04 request release documentation; H05 and H06 request commit/PR artifacts. For ambiguous H02 (sprint demo) and H03 (bare tag comparison), provisionally use `none` and clarify audience/output before selecting release documentation. This is a policy assumption; the user has not explicitly resolved these labels. All six were evaluated for every compared version, so none is an untouched validation holdout.

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

V2 called H02 a release digest and H03 a release change summary. V3 abstained on H02 but selected release-notes for H03. R1 abstained on both; its demo rationale nevertheless assumed an internal audience that the query does not establish. Actual clarification behavior was not tested.

All versions agree on the four unambiguous cases. Rankings reverse if the two disputed labels are positive, so R1 was retained for readable scope rather than proven universal superiority. Neither descriptions nor expected routes were tuned after this run. Author-designed queries, repeated vocabulary, single trials, and English-only coverage remain overfitting risks.

## Body Smoke Test and Current Corrections

Agent `day02_review_body` received the R1 skill body and a changelog task with version/date, CSV export, a login fix, a breaking configuration rename, and CI/test-only changes. After direct file reading failed, the exact body was supplied; no expected answer was given. The returned draft preserved the introduction, Unreleased entry, previous version, and existing version/date format, inserted the new version above older versions, included migration guidance, and omitted internal changes. Manual inspection passed. No files were edited by that agent.

R2 now puts Breaking Changes first and explicitly says the old `timeout` key is ignored, supported by the revised example input. Its description says "for a release"; the workflow distinguishes updating Unreleased from inserting a new version. These changes received format and consistency checks only. The earlier routing and smoke-test results are not claimed as tests of R2. Future daily method notes should stay brief and prioritize the skill within the 30-minute exercise budget.

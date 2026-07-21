# Foundational Finding Report: `<descriptive title>`

> Use for one and only one planned analysis in a frozen mechanism-free Layer 1 study. Report `COMPLETED`, `NOT_RUN`, `HALTED`, or `INVALID`; never omit an unfavorable or unexecuted analysis. Replace every angle-bracketed placeholder. This report cannot award a Charter mechanism evidence label.

## Document control

| Field | Value |
| --- | --- |
| Finding ID | `<LCMRP-FIND-...>` |
| Finding record ID and version | `<LCMRP-FINDREC-... and integer version>` |
| Record status | `DRAFT`, `PUBLISHED`, `SUPERSEDED`, or `RETRACTED` |
| Applicable layer | `Layer 1 — Foundational Research` |
| Frozen study ID, record ID, and version | `<exact identifiers>` |
| Study-manifest artifact and raw-byte SHA-256 | `<locator and digest>` |
| Subject ID, series, and exact version | `<exact registry identity>` |
| Primary method profile ID, kind, and exact version | `<exact profile identity>` |
| Analysis ID and preregistered mode | `<exact analysis ID; CONFIRMATORY or EXPLORATORY>` |
| Authors | `<names or stable contributor identifiers>` |
| Reviewers | `<names or stable contributor identifiers>` |
| Created | `<ISO 8601 timestamp>` |
| Supersession lineage | `<prior record version and raw-byte digest, or None>` |

## Executive finding or disposition

- Terminal disposition: `COMPLETED`, `NOT_RUN`, `HALTED`, or `INVALID`
- Result classification: `POSITIVE`, `NEGATIVE`, `NULL`, `MIXED`, `INCONCLUSIVE`, `INVALID`, or `NOT_OBSERVED`
- Claim assessment: `SUPPORTS_CLAIM`, `DOES_NOT_SUPPORT_CLAIM`, `PARTIALLY_SUPPORTS_CLAIM`, `INCONCLUSIVE`, or `NOT_ASSESSED`
- Finding statement: `<bounded statement or explicit reason no valid result exists>`
- Principal uncertainty: `<uncertainty>`

Result classification and claim assessment are independent. A positive, negative, null, or mixed result does not automatically determine support for the scoped claim.

## 1. Research question

`<exact question from the frozen study analysis>`

## 2. Layer

- Applicable layer: `Layer 1 — Foundational Research`
- Boundary observed: `<confirm that no mechanism or product integration was evaluated>`
- Mechanism under evaluation: `None`

## 3. Hypothesis

- Scoped claim: `<claim identifier, statement, and scope>`
- Competing explanation: `<from frozen protocol>`
- Predicted observation: `<from frozen protocol>`
- Falsifier: `<from frozen protocol>`
- Assumptions that held or failed: `<assessment>`

## 4. Related mechanisms or prior work

| Source ID | Claim used | Exact source | Relationship to this finding | Remaining uncertainty |
| --- | --- | --- | --- | --- |
| `<SOURCE-...>` | `<claim>` | `<locator>` | `<supports, differs, conflicts, or contextualizes>` | `<uncertainty>` |

Do not introduce uninspected sources or call the finding novel without documented search coverage.

## 5. Experimental or analytical design

- Frozen method profile and exact version: `<identity>`
- Planned procedure: `<summary>`
- Actual procedure: `<summary, or Not run>`
- Unit and coverage: `<details>`
- Controls and comparison conditions: `<details>`
- Deviations: `<items, or None>`
- Stop or integrity condition invoked: `<condition, or None>`

## 6. Baselines or comparison conditions

| Comparison ID | Exact version | Planned role | Observed comparability | Result or non-execution disposition | Limitation |
| --- | --- | --- | --- | --- | --- |
| `<COMPARE-...>` | `<identity>` | `<role>` | `<assessment>` | `<outcome>` | `<limit>` |

If no baseline applied, retain the protocol's reason and explain the effect on interpretation.

## 7. Sources, cases, or scenarios

| Source ID | Role | Version or digest | Planned coverage | Observed coverage | Integrity or access finding |
| --- | --- | --- | --- | --- | --- |
| `<SOURCE-...>` | `<role>` | `<identity>` | `<plan>` | `<outcome or Not observed>` | `<finding>` |

## 8. Metrics or verification outcomes

| Measure or proposition | Operational definition | Observed value or status | Uncertainty | Missing or invalid observation rule |
| --- | --- | --- | --- | --- |
| `<item>` | `<definition>` | `<result, Not observed, or Invalid>` | `<uncertainty>` | `<applied rule>` |

## 9. Results

### Primary result

`<complete bounded result, or explicit NOT_RUN/HALTED/INVALID account>`

### Claim assessment rationale

`<why the result classification does or does not support the scoped claim>`

### Exploratory observations

`<clearly labeled post hoc observations, or None>`

### Raw output artifacts

| Artifact ID and version | Locator | Raw-byte SHA-256 | Role |
| --- | --- | --- | --- |
| `<artifact>` | `<locator>` | `<digest>` | `<result, trace, proof, countermodel, or other role>` |

Completed findings require immutable raw output. A not-run or halted finding has no raw result artifact; retain the failure or non-execution reason instead.

## 10. Failure analysis

| Failure ID | Category | Symptom or condition | Root-cause status | Effect on validity | Disposition |
| --- | --- | --- | --- | --- | --- |
| `<FAIL-...>` | `<subject, profile, source, tool, infrastructure, protocol, security/privacy, invalid, or inconclusive>` | `<details>` | `<confirmed, suspected, or unknown>` | `<effect>` | `<retain, rerun, revise, reject, or investigate>` |

Preserve null, negative, contradictory, failed, invalid, halted, and not-run outcomes. Do not silently remove them from study closeout.

## 11. Security and privacy considerations

- Assets and threats observed: `<details>`
- Controls exercised: `<details>`
- Provenance or substitution findings: `<details>`
- Retention and deletion outcomes: `<details>`
- Incidents or control failures: `<details>`
- Residual risks: `<details>`
- Human subjects or participant data: `None under the v0.1 profile`

## 12. Reproducibility information

- Repository revision and dirty-state record: `<details>`
- Frozen protocol and subject-definition digests: `<details>`
- Profile, source, case, and configuration digests: `<details>`
- Environment, dependency lock, and tool versions: `<details>`
- Seeds or determinism account: `<details>`
- Reproduction procedure: `<details>`
- Unavailable artifacts and resulting limits: `<details>`
- Independent replication status: `<status and exact record, or Not attempted>`

## 13. Limitations

- Internal validity: `<limits>`
- Construct or semantic validity: `<limits>`
- Coverage and external validity: `<limits>`
- Tool and formalization limits: `<limits>`
- Security and privacy coverage: `<limits>`
- Reproducibility and independent-review limits: `<limits>`

## 14. Evidence status

- Finding record status: `<DRAFT or PUBLISHED>`
- Mechanism maturity effect: `Not applicable`
- Awarded mechanism evidence labels: `None`
- Independent validation: `<status>`
- Unresolved validation obligations: `<items>`

This finding is one atomic study outcome or terminal disposition. It is not a mechanism evidence decision and cannot change a mechanism evidence profile.

## 15. Recommended next experiment

- Next falsifiable question: `<question>`
- Reason: `<largest gap, failure, or uncertainty>`
- Required comparison, negative case, countermodel, or replication: `<details>`
- Rejection criterion: `<criterion>`
- Independent validation needed: `<details>`


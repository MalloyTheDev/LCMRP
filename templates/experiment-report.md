# Experiment Report: `<descriptive title>`

> Report all predeclared outcomes, including negative, null, failed, invalid, and aborted runs. Replace every angle-bracketed placeholder. Use `Not run`, `Not observed`, or `Not applicable` rather than representing missing results as zero.

## Document control

| Field | Value |
| --- | --- |
| Report ID | `<stable identifier>` |
| Experiment ID | `<identifier>` |
| Protocol ID and frozen version | `<identifier and version>` |
| Proposal ID and version | `<identifier and version>` |
| Mechanism IDs and versions | `<identifiers>` |
| Authors | `<names or stable contributor identifiers>` |
| Independent reviewers | `<names or stable contributor identifiers>` |
| Report version | `<version>` |
| Report status | `DRAFT`, `REVIEWED`, `REPLICATED`, or `SUPERSEDED` |
| Execution interval | `<ISO 8601 start and end>` |
| Repository revision | `<commit identifier>` |
| Evidence-record IDs | `<identifiers, or Pending>` |

## Executive finding

- Outcome: `SUPPORTED`, `REJECTED`, `INCONCLUSIVE`, `INVALID`, or `ABORTED`
- One-sentence finding: `<bounded statement tied to the tested conditions>`
- Principal uncertainty: `<largest uncertainty>`
- Evidence-state recommendation: `<per-state recommendation; it does not replace or imply other awarded labels>`

## 1. Research question

`<question from the frozen protocol>`

## 2. Layer

- Applicable layer: `Layer 1 — Foundational Research`, `Layer 2 — Product-Independent Reference Implementations`, or `Layer 3 — Future CorpusStudio Integration`
- Boundary observed during execution: `<yes or no, with explanation>`
- Mechanism under investigation: `<mechanism>`
- Supporting infrastructure: `<infrastructure>`

## 3. Hypothesis

### Claim

`<predeclared claim>`

### Assumptions and model

`<assumptions, system model, and which assumptions held>`

### Decision rules

- Support: `<predeclared rule and observed decision>`
- Rejection: `<predeclared rule and observed decision>`
- Inconclusive: `<predeclared rule and observed decision>`
- Abort: `<predeclared rule and observed decision>`

Do not rewrite the hypothesis or thresholds after seeing the results. Label any additional interpretation post hoc.

## 4. Related mechanisms or prior work

| Claim ID | Claim | Evidence label | Source locator | Relationship to this result | Remaining uncertainty |
| --- | --- | --- | --- | --- | --- |
| `<C-001>` | `<atomic claim>` | `<[VERIFIED], [USER], [MEMORY], [VERIFY], or [CONFLICT]>` | `<citation or evidence record>` | `<supports, differs, conflicts, or contextualizes>` | `<uncertainty>` |

### Candidate contribution assessment

`<Describe only what the experiment establishes relative to checked prior work. Do not call the result novel without documented search coverage.>`

## 5. Experimental design

- Design: `<summary>`
- Experimental units: `<units>`
- Conditions and allocation: `<conditions>`
- Time horizon and sessions: `<details>`
- Controls and confounders: `<details>`
- Planned runs: `<count>`
- Completed valid runs: `<count>`
- Failed, invalid, or aborted runs: `<count by category>`

### Protocol deviations

| Deviation ID | Description | Timing | Runs affected | Authorization | Effect on interpretation |
| --- | --- | --- | --- | --- | --- |
| `<DEV-001 or None>` | `<description>` | `<timestamp>` | `<run IDs>` | `<reviewer>` | `<effect>` |

## 6. Baselines

| Baseline ID | Exact version | Comparability assessment | Deviations | Result scope |
| --- | --- | --- | --- | --- |
| `<B-001>` | `<version or digest>` | `<matched inputs, budget, tools, and conditions>` | `<differences>` | `<what comparison permits>` |

## 7. Datasets or scenarios

| Asset ID | Role | Version or digest | Provenance | Split or construction | Contamination and access checks |
| --- | --- | --- | --- | --- | --- |
| `<D-001>` | `<role>` | `<immutable identifier>` | `<source and license>` | `<procedure>` | `<outcome>` |

Report any privacy, consent, licensing, sampling, representation, or distribution-shift limitation affecting interpretation.

## 8. Metrics

| Metric ID | Definition | Planned aggregation | Observed coverage | Missing or failed observations |
| --- | --- | --- | --- | --- |
| `<M-001>` | `<definition>` | `<method>` | `<count and proportion>` | `<handling>` |

Include task quality, latency, storage, compute, token cost, and relevant peak and cumulative resource use. Keep safety-critical or governance-relevant component measures visible rather than only reporting a composite score.

## 9. Results

### Primary results

| Condition | Metric | Estimate | Uncertainty | Baseline comparison | Decision-rule outcome |
| --- | --- | --- | --- | --- | --- |
| `<condition>` | `<metric>` | `<value and unit>` | `<interval or other measure>` | `<effect or difference>` | `<met, not met, or inconclusive>` |

### Ablation, boundary, adversarial, and shift results

| Test ID | Type | Outcome | Diagnostic interpretation | Effect on conclusion |
| --- | --- | --- | --- | --- |
| `<T-001>` | `<type>` | `<result>` | `<bounded interpretation>` | `<effect>` |

### Qualitative observations

`<predeclared qualitative findings and coding reliability, or Not applicable>`

### Post-hoc analyses

`<clearly labeled exploratory findings, or None>`

### Claim-to-evidence ledger

| Result claim | Supporting artifact or analysis | Missing support | Risk if false | Next check |
| --- | --- | --- | --- | --- |
| `<bounded claim>` | `<run IDs, table, trace, or analysis>` | `<gap, or None>` | `<impact>` | `<replication or test>` |

## 10. Failure analysis

| Failure ID | Category | Condition and symptom | Root-cause status | Evidence | Disposition |
| --- | --- | --- | --- | --- | --- |
| `<F-001>` | `<mechanism, implementation, infrastructure, evaluation, security/privacy, or inconclusive>` | `<details>` | `<confirmed, suspected, or unknown>` | `<artifact>` | `<retain, fix and rerun, reject, or investigate>` |

Explain memory interference, catastrophic accumulation, incorrect consolidation, contradiction mishandling, deletion failure, corrupted-memory recovery, and irrelevant-memory retrieval when applicable. Do not silently remove failed runs from denominators.

## 11. Security and privacy considerations

- Threat-model ID and version: `<locator>`
- Adversaries and capabilities tested: `<details>`
- Oracle, tool, and storage access tested: `<details>`
- Leakage and side-channel observations: `<details>`
- Trust assumptions that held or failed: `<details>`
- Security success criteria and outcomes: `<details>`
- Privacy, retention, and deletion outcomes: `<details>`
- Cross-user and authority-boundary outcomes: `<details>`
- Incidents or control failures: `<details>`
- Residual risk: `<details>`

Performance results do not establish security. Security conclusions must be restricted to the declared threat model and tested parameters.

## 12. Reproducibility information

- Source revision and dirty-state record: `<identifier>`
- Model IDs, providers, versions, and digests: `<details>`
- Dataset and scenario digests: `<details>`
- Prompt, policy, and configuration digests: `<details>`
- Random seeds and derivation: `<details>`
- Hardware and firmware: `<details>`
- Operating system, runtime, drivers, and dependency lock: `<details>`
- Storage, retrieval, embedding, and policy component versions: `<details>`
- Raw logs, traces, checkpoints, and result artifacts: `<locations>`
- Resource and cost telemetry: `<locations>`
- Reproduction command or procedure: `<procedure>`
- Independent replication status: `<not attempted, attempted, partial, or completed; cite evidence>`

List every unavailable artifact and the resulting limit on reproducibility.

## 13. Limitations

- Internal validity: `<limitations>`
- External validity and distribution coverage: `<limitations>`
- Measurement validity: `<limitations>`
- Statistical or formal uncertainty: `<limitations>`
- Security-model coverage: `<limitations>`
- Privacy and governance coverage: `<limitations>`
- Compute, storage, model, or vendor dependence: `<limitations>`
- Known unanswered questions: `<questions>`

## 14. Evidence status

| Field | Assessment |
| --- | --- |
| Prior awarded evidence profile | `<set of independently awarded labels and decision IDs>` |
| State under decision | `<exactly one LCMRP evidence state>` |
| Recommended action for that state | `AWARD`, `RETAIN`, `WITHHOLD`, `REVOKE`, or `INCONCLUSIVE` |
| Decision authority | `<reviewer or governance process>` |
| Supporting evidence records | `<identifiers>` |
| Missing obligations | `<requirements not met>` |
| Conflicting evidence | `<identifiers or None>` |

Justify the per-state recommendation against the charter definition. A runnable system can support `PROTOTYPE`, but it does not establish any other label. `REPLICATED`, `BENCHMARKED`, `ROBUSTNESS_TESTED`, `SECURITY_REVIEWED`, and `INDEPENDENTLY_VALIDATED` are distinct claims; one does not imply or replace the others. `INTEGRATION_CANDIDATE` and `PRODUCTION_READY` require their own product and governance evidence.

## 15. Recommended next experiment

- Question: `<next falsifiable question>`
- Reason: `<largest evidence gap or risk>`
- Applicable layer: `<exactly one layer for the proposed experiment>`
- Required baseline or ablation: `<details>`
- Required boundary, adversarial, or shift case: `<details>`
- Rejection criterion: `<criterion>`
- Independent validation needed: `<review or replication>`

## Future CorpusStudio Integration Implications

**RESEARCH-TO-PRODUCT HYPOTHESIS**

`<Optional block: remove this heading, label, and placeholder when there is no CorpusStudio implication. Otherwise describe each provisional implication, the product-independent evidence supporting it, and the independent validation still required. This section is not an architectural decision, implementation commitment, roadmap recommendation, or claim of production readiness.>`

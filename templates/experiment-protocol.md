# Experiment Protocol: `<descriptive title>`

> Complete and freeze this protocol before confirmatory execution. Replace every angle-bracketed placeholder. Write `Not applicable` with a reason rather than deleting a required section.

## Document control

| Field | Value |
| --- | --- |
| Experiment ID | `<stable identifier>` |
| Protocol version | `<version>` |
| Protocol status | `DRAFT`, `FROZEN`, `AMENDED`, or `SUPERSEDED` |
| Proposal ID and version | `<identifier>` |
| Mechanism IDs and versions | `<identifiers>` |
| Applicable layer | `Layer 1`, `Layer 2`, or `Layer 3` |
| Prior awarded evidence profile and evidence-decision IDs | `<set of independently awarded labels and authoritative decision IDs; for a new mechanism, HYPOTHESIS with its originating record>` |
| Evidence state under investigation | `<state this experiment may inform; not an award>` |
| Principal investigator | `<name or stable contributor identifier>` |
| Independent reviewer | `<name or stable contributor identifier>` |
| Freeze timestamp | `<ISO 8601 timestamp, or Not frozen>` |
| Repository revision | `<commit identifier>` |
| Registration record | `<registry path and entry ID>` |

## 1. Research question

`<question copied without substantive change from the approved proposal>`

## 2. Layer and boundaries

- Applicable layer and justification: `<exactly one layer and reason>`
- System under test: `<boundary>`
- Mechanism under investigation: `<mechanism>`
- Supporting infrastructure: `<infrastructure>`
- Explicit exclusions: `<items>`

Layer 1 and Layer 2 protocols must remain product-independent and must not introduce CorpusStudio-specific production requirements. If the proposed work crosses a layer boundary, split it into separately versioned and linked protocols.

## 3. Hypothesis and decision rules

- Claim: `<falsifiable claim>`
- Null or competing hypothesis: `<alternative>`
- Assumptions to verify: `<assumptions>`
- Predicted observation: `<prediction>`
- Support criteria: `<predeclared criteria>`
- Rejection criteria: `<predeclared criteria>`
- Inconclusive criteria: `<predeclared criteria>`
- Safety or integrity abort criteria: `<predeclared criteria>`

No maturity transition follows automatically from satisfying a decision threshold.

## 4. Related mechanisms and evidence dependencies

| Dependency ID | Claim used by this protocol | Evidence label | Source or evidence record | Consequence if unsupported |
| --- | --- | --- | --- | --- |
| `<DEP-001>` | `<atomic claim>` | `<[VERIFIED], [USER], [MEMORY], [VERIFY], or [CONFLICT]>` | `<locator>` | `<impact>` |

Unresolved `[VERIFY]` or `[CONFLICT]` dependencies that could invalidate the design must be resolved before the protocol is frozen.

## 5. Experimental units and variables

- Unit of assignment: `<unit>`
- Unit of analysis: `<unit>`
- Independent variables: `<variables and levels>`
- Dependent variables: `<variables>`
- Controlled variables: `<variables>`
- Covariates: `<variables>`
- Confounders and controls: `<risks and controls>`
- Time model, session count, and horizon: `<details>`

## 6. Baselines and comparability

| Baseline ID | Exact implementation or revision | Inputs and budget | Matching controls | Known limitations |
| --- | --- | --- | --- | --- |
| `<B-001>` | `<versioned baseline>` | `<conditions>` | `<controls>` | `<limitations>` |

Explain any resource, prompt, context, tool-access, or data difference between the mechanism and each baseline. If no no-memory or minimal-memory control is used, justify the omission.

## 7. Datasets, scenarios, and splits

| Asset ID | Role | Version or digest | Provenance and license | Construction or split rule | Sensitive-data status |
| --- | --- | --- | --- | --- | --- |
| `<D-001>` | `<train, development, validation, held-out test, adversarial, or other>` | `<immutable identifier>` | `<source>` | `<procedure>` | `<classification>` |

- Contamination checks: `<method>`
- Leakage prevention: `<method>`
- Access controls: `<method>`
- Consent, lawful basis, and retention: `<details>`
- Scenario generator and generator seed policy: `<details>`
- Held-out material access policy: `<details>`

## 8. Metrics and measurement procedure

| Metric ID | Operational definition | Collection point | Aggregation and uncertainty | Missing or failed observation rule |
| --- | --- | --- | --- | --- |
| `<M-001>` | `<formula or scoring procedure>` | `<where and when>` | `<method>` | `<rule>` |

Record latency, storage, compute, token cost, and relevant peak and cumulative resource measurements. Preserve component-level measures when an aggregate score could hide harmful behavior.

## 9. Run matrix, randomization, and replication

| Run group | Condition | Dataset split | Repetitions | Seed policy | Expected artifacts |
| --- | --- | --- | --- | --- | --- |
| `<RG-001>` | `<mechanism, baseline, or ablation>` | `<split>` | `<count>` | `<fixed list or derivation>` | `<artifacts>` |

- Assignment and randomization procedure: `<procedure>`
- Counterbalancing or ordering controls: `<procedure>`
- Independence assumptions: `<assumptions>`
- Minimum valid runs: `<count and rationale>`
- Replication criterion: `<independent runs, environments, tolerance, and required agreement>`

## 10. Execution procedure

1. `<preflight integrity and access check>`
2. `<environment materialization and verification>`
3. `<data and configuration digest verification>`
4. `<baseline and mechanism execution order>`
5. `<metric and trace capture>`
6. `<artifact sealing and registry update>`
7. `<post-run security, deletion, and completeness checks>`

### Operator interventions

List permitted interventions and how each will be logged. Undeclared intervention invalidates a confirmatory run unless an amendment explicitly permits it.

`<permitted interventions>`

## 11. Analysis plan

- Primary analysis: `<method>`
- Uncertainty estimation: `<method>`
- Multiple comparisons: `<method or Not applicable with reason>`
- Sensitivity analyses: `<analyses>`
- Qualitative coding and reviewer agreement: `<method or Not applicable>`
- Outlier policy: `<predeclared rule>`
- Missing-data policy: `<predeclared rule>`
- Invalid-run policy: `<predeclared rule>`
- Early stopping: `<rule or prohibited>`

Exploratory analyses must be labeled post hoc and kept separate from confirmatory conclusions.

## 12. Ablation, boundary, adversarial, and shift tests

| Test ID | Type | Condition | Threat or mechanism isolated | Decision relevance |
| --- | --- | --- | --- | --- |
| `<T-001>` | `<ablation, boundary, adversarial, or distribution shift>` | `<condition>` | `<purpose>` | `<how it changes interpretation>` |

## 13. Security, privacy, and governance controls

- Threat-model identifier and version: `<locator>`
- Adversaries and capability bounds: `<details>`
- Oracle, model, storage, and tool access: `<details>`
- Trust boundaries and trusted components: `<details>`
- Observable leakage and side channels: `<details>`
- Adversary success criteria: `<criteria>`
- Authentication and authorization controls: `<controls>`
- Isolation and cross-user leakage controls: `<controls>`
- Provenance-integrity controls: `<controls>`
- Poisoning and persistent-injection controls: `<controls>`
- Deletion and derived-state verification: `<controls>`
- Incident and abort procedure: `<procedure>`
- Residual risks accepted for this experiment: `<risks and approver>`

## 14. Reproducibility capture

- Source revision and dirty-state record: `<method>`
- Model IDs, providers, versions, and digests: `<method>`
- Dataset and scenario digests: `<method>`
- Prompt, policy, and configuration digests: `<method>`
- Exact seeds and seed derivation: `<method>`
- Hardware and firmware: `<method>`
- Operating system, runtime, drivers, and locked dependencies: `<method>`
- Storage, retrieval, embedding, and policy component versions: `<method>`
- Environment variables and external-service settings, with secrets redacted: `<method>`
- Raw logs, traces, checkpoints, and result artifacts: `<locations and retention>`
- Cost and resource telemetry: `<method>`

## 15. Deviations, failures, and retention

Protocol changes after freezing require a versioned amendment stating the reason, timing, affected runs, and effect on interpretation. Never overwrite the frozen protocol.

| Deviation ID | Timestamp | Description | Runs affected | Authorized by | Interpretive effect |
| --- | --- | --- | --- | --- | --- |
| `<DEV-001 or None>` | `<timestamp>` | `<deviation>` | `<run IDs>` | `<reviewer>` | `<effect>` |

Classify mechanism failures, implementation defects, infrastructure failures, evaluation invalidity, security or privacy failures, and inconclusive outcomes separately. Retain negative, null, failed, and aborted runs with their provenance.

## 16. Reporting and review plan

- Report template and destination: `<path>`
- Blind or independent review, if any: `<procedure>`
- Evidence-record creation: `<owner and timing>`
- Mechanism-registry update: `<owner and decision authority>`
- Data and artifact release constraints: `<constraints>`
- Required reviewers: `<methodology, security, privacy, governance, or other>`

## Future CorpusStudio Integration Implications

**RESEARCH-TO-PRODUCT HYPOTHESIS**

`<Optional block: remove this heading, label, and placeholder when there is no CorpusStudio implication. Otherwise describe each provisional implication, the product-independent evidence supporting it, and the independent validation still required. This section is not an architectural decision, implementation commitment, roadmap recommendation, or claim of production readiness.>`

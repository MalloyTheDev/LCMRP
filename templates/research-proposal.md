# Research Proposal: `<descriptive title>`

> Replace every angle-bracketed placeholder. Write `Not applicable` with a reason when a section does not apply. Do not delete required sections.

## Document control

| Field | Value |
| --- | --- |
| Proposal ID | `<stable identifier>` |
| Version | `<version>` |
| Document status | `DRAFT`, `APPROVED`, or `SUPERSEDED` |
| Authors | `<names or stable contributor identifiers>` |
| Reviewers | `<names or stable contributor identifiers>` |
| Created | `<YYYY-MM-DD>` |
| Last updated | `<YYYY-MM-DD>` |
| Supersedes | `<proposal ID and version, or None>` |
| Related mechanism IDs | `<registry IDs, or None>` |
| Related experiment IDs | `<registry IDs, or None>` |
| Repository revision | `<commit identifier>` |

## 1. Research question

State one primary question that can be answered by evidence. Define the population, operating conditions, time horizon, and outcome of interest.

`<research question>`

### Secondary questions

- `<question, or None>`

## 2. Layer

Select exactly one applicable layer and explain why.

- Applicable layer: `Layer 1 — Foundational Research`, `Layer 2 — Product-Independent Reference Implementations`, or `Layer 3 — Future CorpusStudio Integration`
- Boundary justification: `<why the work belongs in this layer and what is deliberately excluded>`

Layer 1 and Layer 2 work must not contain CorpusStudio-specific production code or allow a product architecture to determine the research result. If work would cross layer boundaries, create separate linked artifacts for each layer.

## 3. Hypothesis

### Claim

`<precise, falsifiable mechanism or effect claim>`

### Null or competing hypothesis

`<credible alternative explanation or null effect>`

### Assumptions

- `<assumption and how it will be checked>`

### Model

Define the system, memory lifecycle stages, actors, authority boundaries, inputs, outputs, state, and time model relevant to the claim.

`<model>`

### Predicted observation

`<result expected if the claim is supported>`

### Falsifier

`<observation or threshold that would reject or materially weaken the claim>`

### Missing obligations

- `<unproved premise, unimplemented control, unavailable measurement, or unresolved dependency>`

### Evidence profile and state under investigation

- Awarded evidence profile: `<set of independently awarded labels and evidence-decision IDs; for a new mechanism, HYPOTHESIS with its originating record>`
- Evidence state under investigation: `<exactly one state this proposal may inform>`

A proposal cannot award an evidence state. Evidence labels have independent obligations; investigating one state does not replace or imply the rest of the awarded profile.

## 4. Related mechanisms or prior work

Use the evidence labels defined in `references/README.md`. Do not cite a source that has not been inspected. Separate literature findings from project assumptions and proposed extensions.

| Claim ID | Claim | Label | Source locator | Verification notes | Risk if false | Next check |
| --- | --- | --- | --- | --- | --- | --- |
| `<C-001>` | `<atomic claim>` | `<[VERIFIED], [USER], [MEMORY], [VERIFY], or [CONFLICT]>` | `<citation or None>` | `<scope and support>` | `<impact>` | `<action>` |

### Candidate contribution

`<difference from prior mechanisms, described as a candidate contribution or research hypothesis until the literature and adjacent terminology are checked>`

### Search coverage and unresolved conflicts

- Keywords and adjacent terms checked: `<terms>`
- Standards and venues checked: `<sources>`
- Limitation and negative-result searches: `<searches>`
- Unresolved evidence conflicts: `<conflicts, or None>`

## 5. Scope and exclusions

### In scope

- `<item>`

### Out of scope

- `<item>`

### Experimental mechanism versus supporting infrastructure

- Mechanism under investigation: `<component or process>`
- Supporting infrastructure: `<components not being evaluated>`
- Interfaces that must remain replaceable: `<storage, retrieval, model, embedding, policy, or other interfaces>`

## 6. Experimental design

Describe the design at a level that permits a separate protocol to be written without changing the hypothesis.

- Independent variables: `<variables>`
- Dependent variables: `<variables>`
- Controlled variables: `<variables>`
- Confounders: `<known or suspected confounders and controls>`
- Unit of analysis: `<unit>`
- Time horizon and session structure: `<horizon>`
- Randomization or counterbalancing: `<method>`
- Planned repetitions: `<count and rationale>`

## 7. Baselines

Include a no-memory or minimal-memory control where meaningful. A baseline must receive comparable inputs, budgets, and evaluation conditions.

| Baseline ID | Description | Why it is informative | Fairness controls | Known limitations |
| --- | --- | --- | --- | --- |
| `<B-001>` | `<baseline>` | `<comparison purpose>` | `<matched conditions>` | `<limitations>` |

## 8. Datasets or scenarios

Describe representative, held-out, boundary, adversarial, and distribution-shift cases. Document provenance, license, consent or lawful basis, sensitive fields, contamination risks, and split construction.

| Dataset or scenario ID | Role | Provenance | Split or generator | Access constraints | Risks |
| --- | --- | --- | --- | --- | --- |
| `<D-001>` | `<development, validation, held-out test, adversarial, or other>` | `<source>` | `<immutable version or procedure>` | `<constraints>` | `<bias, privacy, contamination, or other risks>` |

## 9. Metrics

Include task quality and operational cost. Define directionality, units, aggregation, uncertainty, and failure handling before execution.

| Metric ID | Definition | Success direction | Aggregation and uncertainty | Failure or missing-data rule |
| --- | --- | --- | --- | --- |
| `<M-001>` | `<operational definition>` | `<higher, lower, range, or constraint>` | `<method>` | `<rule>` |

Measure latency, storage, compute, and token cost where applicable. Do not collapse selective retention, appropriate forgetting, contradiction handling, source sensitivity, deletion, and interference resistance into a single score unless the aggregation is independently justified.

## 10. Analysis and decision rules

### Planned analysis

`<statistical, formal, or qualitative analysis; uncertainty treatment; multiple-comparison handling; and sensitivity checks>`

### Support criteria

- `<predeclared condition that would support the hypothesis without establishing production readiness>`

### Rejection criteria

- `<predeclared condition that would reject the mechanism or its present formulation>`

### Inconclusive criteria

- `<condition requiring a null, underpowered, invalid, or mixed conclusion>`

### Stop and abort conditions

- `<safety, privacy, corruption, resource, or protocol-integrity condition>`

Stopping for safety or integrity must not be reported as evidence that the hypothesis succeeded or failed unless the decision rule explicitly permits that inference.

## 11. Ablations, boundary tests, and adversarial tests

| Test ID | Type | Factor or attack varied | Expected diagnostic value | Outcome that changes the conclusion |
| --- | --- | --- | --- | --- |
| `<T-001>` | `<ablation, boundary, adversarial, or distribution shift>` | `<factor>` | `<what it isolates>` | `<decision rule>` |

Include tests relevant to memory poisoning, persistent prompt injection, unauthorized inference, sensitive-data retention, cross-user leakage, provenance forgery, deletion failure, retrieval manipulation, malicious consolidation, and identity or preference hijacking when they are within the system boundary.

## 12. Security, privacy, and governance

- Assets and sensitive data: `<items>`
- Adversaries and capabilities: `<actors, access, persistence, and resource bounds>`
- Oracle and tool access: `<interfaces an adversary can query or control>`
- Trust assumptions: `<trusted components and principals>`
- Leakage and side channels: `<observable outputs, timing, logs, embeddings, storage, or other channels>`
- Authority model: `<user, AI system, operator, provider, and external-source rights>`
- Success criterion for the adversary: `<testable condition>`
- Required protections and tests: `<controls and verification>`
- Deletion semantics: `<logical, physical, replicated, backup, cached, and derived-state handling>`
- Residual risks: `<known risks after controls>`

Link a completed threat model before executing any experiment that stores sensitive or multi-user information.

## 13. Reproducibility plan

Record enough information to reproduce the experiment without relying on mutable defaults.

- Source revision and dirty-state policy: `<details>`
- Model provider, model ID, exact version or digest: `<details>`
- Dataset version or digest: `<details>`
- Configuration and prompt digests: `<details>`
- Random seeds and seed derivation: `<details>`
- Hardware, operating system, runtime, and dependency lock: `<details>`
- Storage, retrieval, and embedding component versions: `<details>`
- Run logging and immutable artifact locations: `<details>`
- Replication criteria: `<number, independence, tolerance, and required artifacts>`

## 14. Failure analysis and limitations plan

### Failure categories to distinguish

- Mechanism failure: `<examples relevant to this proposal>`
- Implementation defect: `<examples>`
- Infrastructure failure: `<examples>`
- Invalid or contaminated evaluation: `<examples>`
- Security or privacy failure: `<examples>`
- Inconclusive or underpowered result: `<examples>`

### Known limitations

- `<limitation and effect on interpretation>`

Negative results, null findings, aborted runs, and failed mechanisms must be retained with their provenance and must not be silently excluded from aggregate results.

## 15. Planned outputs and next decision

- Artifacts to produce: `<protocol, code, configurations, data, reports, registry records, or other artifacts>`
- Intended evidence-state decision: `<state to assess; not a promised transition>`
- Review required before execution: `<methodological, security, privacy, or governance review>`
- Decision after completion: `<replicate, revise, reject, benchmark, robustness-test, or stop>`

## Future CorpusStudio Integration Implications

**RESEARCH-TO-PRODUCT HYPOTHESIS**

`<Optional block: remove this heading, label, and placeholder when there is no CorpusStudio implication. Otherwise describe each provisional implication, the product-independent evidence supporting it, and the independent validation still required. This section is not an architectural decision, implementation commitment, roadmap recommendation, or claim of production readiness.>`

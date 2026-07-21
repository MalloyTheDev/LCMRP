# Foundational Study Protocol: `<descriptive title>`

> Use only for mechanism-free Layer 1 taxonomy or formal-analysis work supported by the [Foundational Study Contract](../docs/program/FOUNDATIONAL_STUDY_CONTRACT.md). Complete and freeze this protocol before confirmatory analysis. Replace every angle-bracketed placeholder. Do not invent a mechanism, evidence label, registration, result, or artifact digest.

## Document control

| Field | Value |
| --- | --- |
| Foundational study ID | `<LCMRP-FSTUDY-...>` |
| Study record ID and version | `<LCMRP-FSTUDYREC-... and integer version>` |
| Record status | `DRAFT`, `FROZEN`, `SUPERSEDED`, or `WITHDRAWN` |
| Applicable layer | `Layer 1 — Foundational Research` |
| Subject ID, series, and exact version | `<LCMRP-FSUBJ-..., stable series, version>` |
| Subject kind | `MEMORY_TAXONOMY`, `FORMAL_MEMORY_MODEL`, `COGNITIVE_MEMORY_CONCEPT`, or `EVALUATION_CONSTRUCT` |
| Primary method profile ID and version | `<exactly one profile identifier and version>` |
| Primary method profile kind | `STRUCTURAL_OR_TAXONOMY_EVALUATION` or `FORMAL_ANALYSIS` |
| Authors | `<names or stable contributor identifiers>` |
| Reviewers | `<names or stable contributor identifiers>` |
| Freeze timestamp and authority | `<ISO 8601 timestamp and authority, or Not frozen>` |
| Immutable freeze artifact | `<locator and raw-byte SHA-256, or Pending while draft>` |
| Repository revision | `<commit identifier>` |
| Supersession lineage | `<prior record version and raw-byte digest, or None>` |

The subject must resolve to the standalone foundational-subject registry before a frozen study is activated. Registry presence records identity and provenance; it is not a scientific result or a mechanism maturity award.

## 1. Research question

`<one bounded question about the exact foundational subject>`

## 2. Layer and boundaries

- Layer justification: `<why this is mechanism-free Layer 1 work>`
- Subject definition: `<bounded definition>`
- Included concepts, structures, or propositions: `<items>`
- Explicit exclusions: `<items>`
- Mechanism under evaluation: `None`
- Mechanism maturity labels applicable: `None`

If the work evaluates a versioned memory mechanism, use the mechanism experiment contract instead. Product-specific implications require a separate Layer 3 artifact and cannot be inserted into this protocol.

## 3. Hypothesis

- Claim: `<falsifiable claim>`
- Competing explanation: `<credible alternative>`
- Predicted observation: `<predeclared observation>`
- Falsifier: `<observation or integrity failure that rejects or materially weakens the claim>`
- Assumptions and how each will be checked: `<items>`

## 4. Related mechanisms or prior work

| Source ID | Atomic claim used | Source locator and exact version | Role | Verification status | Consequence if wrong |
| --- | --- | --- | --- | --- | --- |
| `<SOURCE-...>` | `<claim>` | `<citation or immutable artifact>` | `<PRIOR_WORK, FORMAL_INPUT, DEVELOPMENT, or case role>` | `<inspected, unresolved, or conflicting>` | `<effect>` |

Do not claim novelty without a documented prior-art search. Separate reproduced source claims from LCMRP inference and unresolved assumptions.

## 5. Experimental or analytical design

- Primary method profile and version: `<exact profile>`
- Unit of analysis: `<case, axiom set, proposition, category assignment, or other unit>`
- Procedure: `<reproducible steps>`
- Controlled conditions: `<conditions>`
- Confounders or alternative interpretations: `<risks and controls>`
- Held-out, boundary, and adversarial cases: `<cases, or Not applicable with reason>`
- Stop or integrity-abort conditions: `<conditions>`

### Structural or taxonomy profile obligations

Complete this subsection for `STRUCTURAL_OR_TAXONOMY_EVALUATION`; otherwise write `Not applicable — FORMAL_ANALYSIS selected`.

- Competency questions: `<questions>`
- Integrity constraints: `<constraints>`
- Versioned category-definition artifact: `<locator and digest plan>`
- Positive-case source IDs: `<IDs>`
- Negative-case source IDs: `<IDs>`
- Adjudication method: `<method and disagreement retention>`
- Coverage rule: `<predeclared rule>`

### Formal-analysis profile obligations

Complete this subsection for `FORMAL_ANALYSIS`; otherwise write `Not applicable — STRUCTURAL_OR_TAXONOMY_EVALUATION selected`.

- Formal-system artifact: `<locator and digest plan>`
- Assumptions: `<assumptions>`
- Propositions: `<stable IDs>`
- Consistency or satisfiability checks: `<checks>`
- Intended entailments: `<entailments>`
- Non-entailments or countermodels: `<obligations>`
- Proof or verification method: `<method>`
- Semantic-validity check: `<check beyond syntax>`
- Counterexample search: `<method and bounds>`
- Tool provenance: `<exact version, environment, and immutable artifact>`

## 6. Baselines or comparison conditions

| Comparison ID | Exact alternative | Why informative | Matched inputs and constraints | Decision relevance | Limitation |
| --- | --- | --- | --- | --- | --- |
| `<COMPARE-...>` | `<competing taxonomy, axiom system, rule set, or null construction>` | `<reason>` | `<controls>` | `<rule>` | `<limitation>` |

If a comparison baseline is genuinely inapplicable, state the reason and name the competing explanation that the design still tests.

## 7. Sources, cases, and provenance

| Source ID | Kind | Role | Exact version or digest | Construction or selection rule | Access and license | Human-data status |
| --- | --- | --- | --- | --- | --- | --- |
| `<SOURCE-...>` | `<allowed non-human source kind>` | `<positive, negative, held-out, formal input, development, or prior work>` | `<identity>` | `<rule>` | `<terms>` | `No human subjects or participant data` |

The v0.1 foundational contract does not permit human-subject studies or participant data.

## 8. Metrics and analysis rules

| Analysis ID | Mode | Question | Measure or verification target | Decision rule | Planned output artifact |
| --- | --- | --- | --- | --- | --- |
| `<ANALYSIS-...>` | `CONFIRMATORY` or `EXPLORATORY` | `<question>` | `<operational definition>` | `<support, reject, inconclusive, invalid, or halt rule>` | `<locator and digest plan>` |

For each planned analysis, one and only one terminal finding must eventually record `COMPLETED`, `NOT_RUN`, `HALTED`, or `INVALID`. Do not declare the study terminal until every analysis has an active, published finding or disposition.

## 9. Rejection and stop criteria

| Criterion ID | Condition | Disposition | Rationale |
| --- | --- | --- | --- |
| `<REJECT-...>` | `<observable condition>` | `REJECT_CLAIM`, `MARK_INCONCLUSIVE`, `HALT_STUDY`, or `INVALIDATE_ANALYSIS` | `<reason>` |

## 10. Security and privacy considerations

- Assets: `<definitions, source integrity, results, or other assets>`
- Threats: `<provenance forgery, source substitution, evaluator manipulation, or other threats>`
- Controls: `<digest, review, isolation, or other controls>`
- Retention and deletion behavior: `<policy for raw and derived artifacts>`
- Residual risks: `<risks>`
- Human subjects involved: `No`
- Human participant data involved: `No`

## 11. Reproducibility information

- Source revision and dirty-state policy: `<details>`
- Subject-definition artifact and raw-byte SHA-256: `<details>`
- Profile-definition artifact and raw-byte SHA-256: `<details>`
- Source and case artifacts: `<details>`
- Environment and locked dependencies: `<details>`
- Configuration and tool versions: `<details>`
- Randomness and seeds: `<Not applicable with reason, or exact policy>`
- Protocol and freeze artifacts: `<details>`
- Replication criteria: `<independence, required agreement, tolerances, and retained artifacts>`

## 12. Failure analysis and retention plan

Distinguish subject-definition failure, method-profile failure, source or case failure, tool or infrastructure defect, protocol deviation, invalid analysis, security or privacy failure, and inconclusive outcome.

- Failure categories and detection: `<details>`
- Invalid-data handling: `<predeclared rule>`
- Deviation recording: `<procedure>`
- Negative, null, contradictory, failed, halted, invalid, and not-run retention: `<procedure>`
- Conditions requiring amendment or a new study record version: `<conditions>`

## 13. Limitations

- Internal validity: `<limits>`
- Construct or semantic validity: `<limits>`
- Coverage and external validity: `<limits>`
- Tool and formalization limits: `<limits>`
- Reproducibility limits: `<limits>`
- Security, privacy, and governance limits: `<limits>`

## 14. Evidence status

- Foundational finding status: `<No finding yet while protocol is planned, or linked finding IDs after execution>`
- Mechanism evidence labels: `Not applicable`
- Independent validation: `<not attempted, planned, or completed with exact record>`
- Missing validation obligations: `<items>`

Structural conformance, formal validity, or a favorable result does not award a Charter mechanism evidence label.

## 15. Recommended next experiment

- Next falsifiable question: `<question>`
- Largest uncertainty or risk: `<gap>`
- Required comparison or counterexample: `<details>`
- Rejection criterion: `<criterion>`
- Independent review or replication required: `<details>`


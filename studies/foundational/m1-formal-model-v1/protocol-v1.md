# Foundational Study Protocol v1 (Frozen): Bounded Formal Analysis of FMO-0.1

> **FROZEN PREREGISTRATION — NOT EXECUTED.** This immutable Layer 1 `FORMAL_ANALYSIS` protocol is bound by the canonical study manifest and repository-local freeze attestation. It is not a result, finding, closeout, proof, validation, evidence award, or implementation authorization. The planned analyzer remains unexecuted and no planned output exists.

## Document control

| Field | Value |
| --- | --- |
| Foundational study ID | `LCMRP-FSTUDY-0002-M1-FORMAL-MODEL` |
| Study record ID and version | `LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL`, version 1 |
| Record status | `FROZEN` |
| Applicable layer | Layer 1 — Foundational Research |
| Subject ID, series, and exact version | `LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL`; `LCMRP-FORMAL-MEMORY-OBJECT-MODEL`; version 1 |
| Subject raw-byte SHA-256 | `82052e424c01d3204828472ef569f74f7c0aad418f827cffda92400562bbfaf3` |
| Subject kind | `FORMAL_MEMORY_MODEL` |
| Primary method profile ID and version | `LCMRP-MPROF-0002-M1-FORMAL-ANALYSIS`, version 1 |
| Primary method profile kind | `FORMAL_ANALYSIS` |
| Authors | `LCMRP-M1-FORMAL-PROTOCOL-AUTHORING-LANE` |
| Reviewers | `LCMRP-M1-STUDY-FREEZE-VERIFICATION-LANE` and LCMRP root steward; internal protocol review only, not independent scientific validation |
| Freeze timestamp and authority | `2026-07-21T21:28:00Z`; `LCMRP-ROOT-STEWARD-FREEZE-2026-07-21` |
| Immutable freeze artifact | `studies/foundational/m1-formal-model-v1/freeze-attestation.json`; exact raw-byte digest bound by the canonical manifest |
| Repository revision | Author package merge `9966c31a86c999c5eda53aced8bb4274f2cbdc2d`; freeze integration is separately exact-head reviewed |
| Supersession lineage | None; initial record version |

The subject resolves through the active foundational-subject registry. That registry fixes identity and provenance only. This frozen protocol activates a preregistration; it does not adopt FMO-0.1, report a result, or create evidence.

## 1. Research question

Within an explicitly bounded, product-independent Boolean encoding of the exact registered FMO-0.1 subject, do the selected invariant constraints admit module-local models; do the encoded intended entailments resist exhaustive counterexample search; do the explicit non-entailments and named countermodels retain witnesses; and which invariant, authority, and deletion claims fail independence or semantic-validity review?

## 2. Layer and boundaries

- **Layer justification:** This is mechanism-free analysis of a candidate formal model. It evaluates no running memory mechanism and assumes no storage, retrieval, model, embedding, vendor, service, application schema, or deployment environment.
- **Subject definition:** The only subject is `LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL` version 1 at the exact registered raw-byte digest above.
- **Included structures:** FMO-INV-01 through FMO-INV-16; FMO-P01 through FMO-P04; FMO-C01 through FMO-C04 as bounded or explicitly unencoded conjectures; intended entailments FMO-IE-01 through FMO-IE-10; all 24 source non-entailment lines represented as FMO-NE-01 through FMO-NE-24 with the two conflict-preference consequents split into FMO-NE-12A and FMO-NE-12B; and FMO-CM-01 through FMO-CM-10.
- **Included boundary analyses:** operation-scoped authority; `DENY` and `UNRESOLVED`; absence of universal authority; target-closure completeness; unknown, accessible, reconstructable, local-erasure-only, failed, and incomplete deletion cases; terminal exact identity; and independent reacquisition.
- **Explicit exclusions:** A complete many-sorted or temporal formalization; a policy calculus; natural-language truth interpretation; distributed-time semantics; liveness; probability or calibration; information-flow noninterference; physical or external deletion; legal or moral authority; human-subject research; controlled empirical evaluation; and all implementation behavior.
- **Mechanism under evaluation:** None.
- **Mechanism maturity labels applicable:** None.

The formal system is a deliberately bounded study instrument. A module-local model is not a model of all FMO-0.1. A kernel entailment is not a proof of the natural-language source claim. A retained witness is not evidence of real-world behavior. The separate semantic-validity analysis is mandatory and can invalidate every machine result.

## 3. Hypothesis

- **Claim:** Under the exact frozen encoding, each enumerated Boolean module will have at least one satisfying valuation; no satisfying valuation will violate an encoded intended entailment; each encoded non-entailment and FMO-CM-01 through FMO-CM-10 will retain a satisfying witness; and independent reviewers will judge every decision-bearing source-to-encoding mapping faithful or narrower rather than broader, circular, ambiguous, or unsupported.
- **Competing explanation:** Apparent success may be created by constraints that restate their conclusions, missing source semantics, independent modules that cannot form one model, or bounds too weak to expose contradictions; therefore the kernel may be satisfiable while FMO-0.1 remains inconsistent, underspecified, or incorrectly encoded.
- **Predicted observation:** The retained output will contain full valuation counts and at least one model per enumerated module, no counterexample for an encoded entailment, a full assignment for every declared non-entailment and named countermodel, one omission disposition per FMO invariant, and two independent semantic mappings plus adjudication for every decision-bearing encoding element.
- **Falsifier:** Reject or materially narrow the claim if any module has no satisfying valuation; any intended entailment has a retained counterexample; any declared non-entailment or named countermodel lacks a valid witness; an invariant omission exposes contradiction or unintended dependence; an authority or deletion boundary accepts a prohibited success; any result-bearing mapping is broader, circular, unsupported, or unresolved after adjudication; or the exact frozen provenance and complete valuation coverage cannot be demonstrated.

### Assumptions and checks

The normative assumption statements and checks are frozen in `artifacts/assumptions.json` under these IDs:

1. `FMO-A01-EXACT-SUBJECT`
2. `FMO-A02-CLASSICAL-BOOLEAN-KERNEL`
3. `FMO-A03-MODULE-LOCALITY`
4. `FMO-A04-ENCODING-IS-INTERPRETIVE`
5. `FMO-A05-FINITE-BOUNDS`
6. `FMO-A06-ENTAILMENT-SCOPE`
7. `FMO-A07-NONENTAILMENT-SCOPE`
8. `FMO-A08-INDEPENDENCE-SCOPE`
9. `FMO-A09-AUTHORITY-ABSTRACTION`
10. `FMO-A10-DELETION-ABSTRACTION`
11. `FMO-A11-DETERMINISTIC-OFFLINE-EXECUTION`
12. `FMO-A12-NO-RESULT-ACCESS-BEFORE-FREEZE`

Failure of A01, A02, A11, or A12 halts the study. Failure or material weakening of A03 through A10 invalidates affected analyses and requires an explicit disposition; it cannot be repaired after result access by silently changing the frozen encoding.

## 4. Related mechanisms or prior work

No mechanism is under evaluation, and no novelty claim is made.

| Source ID | Atomic claim used | Source locator and exact version | Role | Verification status | Consequence if wrong |
| --- | --- | --- | --- | --- | --- |
| `SOURCE-FMO-01` | FMO-0.1 declares candidate invariants, propositions, conjectures, entailments, non-entailments, countermodels, and open proof obligations without asserting results. | `docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md`; subject version 1; SHA-256 `82052e...faf3` | `PRIOR_WORK` and exact subject | Raw-byte digest verified through subject registry; semantic claims require review | Halt for subject mismatch; supersede the draft if source interpretation changes. |
| `SOURCE-FSC-01` | The accepted Layer 1 formal-analysis profile requires a versioned formal system, assumptions, propositions, satisfiability, entailment, non-entailment, countermodel, provenance, semantic-validity, and counterexample-search obligations. | `docs/program/FOUNDATIONAL_STUDY_CONTRACT.md`; repository revision to be frozen | `PRIOR_WORK` | Inspected; exact digest verified in the canonical frozen manifest | A contract mismatch invalidates the study design and requires governance review. |
| `SOURCE-KERNEL-01` | The study-local finite Boolean modules, variables, constraints, bounds, and exclusions define the only machine-checkable semantics used by this study. | `artifacts/formal-system.json`, version 1; exact digest verified in the canonical frozen manifest | `FORMAL_INPUT` | Syntax checked only while draft; no semantic result accessed | Any substitution, parse ambiguity, or incomplete freeze binding halts execution. |
| `SOURCE-PROPOSITIONS-01` | The stable proposition, non-entailment, invariant, and named-countermodel IDs define the frozen query set. | `artifacts/propositions.json`, version 1; exact digest to be bound | `DEVELOPMENT` | Syntax checked only while draft | Missing, duplicate, or altered IDs invalidate coverage. |

FMO-0.1's own natural-language proof sketches and proposed countermodels are inputs, not reproduced findings. The study tests a study-local interpretation of them.

## 5. Experimental or analytical design

- **Primary method profile and version:** `LCMRP-MPROF-0002-M1-FORMAL-ANALYSIS` version 1.
- **Unit of analysis:** A finite module, encoded proposition query, invariant-omission probe, named countermodel assignment, or source-to-encoding mapping row.
- **Controlled conditions:** Exact artifact bytes; CPython 3.12.13 standard library; Boolean valuation domain `{false,true}`; declared module and variable order; no randomness, network, model, external solver, mutable remote source, or participant data; exclusive-create outputs; raw-byte SHA-256 provenance.
- **Confounders:** Tautological encoding, vacuous entailment with an unsatisfied premise, missing variables, underconstrained witness modules, independent-module incompatibility, hidden semantic strengthening, incomplete deletion closure, opaque authority composition, and reviewer dependence. Controls include satisfiability checks, premise-satisfiability review, retained complete assignments, negative baselines, one-at-a-time omissions, scope denials, and independent semantic adjudication.
- **Held-out, boundary, and adversarial cases:** `DENY`, `UNRESOLVED`, role-without-authority, local erasure, unknown target, surviving accessible target, surviving reconstructable target, failed attempt with false verified label, exact-identity resurrection, and independent equivalent-content reacquisition. These are formal cases, not observed system behavior.
- **Stop or integrity-abort conditions:** Any frozen digest mismatch; absent or inconsistent freeze attestation; any output before freeze; dirty or wrong repository revision under the frozen policy; valuation omission or duplication; undeclared coercion; output overwrite; network/model/external-solver use; source substitution; semantic-review conflict left unresolved; or any proof/validation overclaim.

### Procedure

1. Independent verification and root review inspected the draft protocol, draft manifest, exact subject, contract, profile definition, bounded formal system, assumptions, propositions, configuration, environment, tool provenance, and analyzer source without executing the analyzer.
2. The freeze authority resolved review findings before result access, created this final protocol and authority-bound freeze attestation, bound final raw-byte digests, and published the schema-valid `FROZEN` record through the canonical record path.
3. Before execution, resolve the active frozen study record; recompute every immutable digest; confirm all seven unique planned analysis-result paths do not exist; verify the exact clean repository revision; and run schema and source-integrity checks.
4. Invoke the frozen analyzer once with the exact argument vector in `artifacts/configuration.json`, network disabled, and exclusive-create output mode.
5. Retain the raw machine bundle unchanged as the unique planned output for `ANALYSIS-FMO-01-SATISFIABILITY`. Recompute and record its raw-byte SHA-256. Do not summarize it before the raw artifact is retained. Analyses 02 through 06 may cite this shared supporting input but must each publish their own unique interpretation artifact.
6. Two reviewers independently map every decision-bearing variable, constraint, premise, conclusion, witness, and exclusion to the exact FMO-0.1 source. They may inspect the machine output only after their mappings are independently fixed.
7. Adjudicate disagreements while retaining both original mappings. Classify mappings `FAITHFUL`, `NARROWER`, `BROADER`, `CIRCULAR`, `AMBIGUOUS`, or `UNSUPPORTED`.
8. Publish one atomic finding or terminal disposition per analysis ID. Preserve `COMPLETED`, `NOT_RUN`, `HALTED`, and `INVALID` outcomes. Do not edit the frozen record or raw result.
9. Close the study only after an immutable ledger is set-equal to all seven planned analyses and resolves one active published disposition per analysis.

### Structural or taxonomy profile obligations

Not applicable — `FORMAL_ANALYSIS` selected.

### Formal-analysis profile obligations

- **Formal-system artifact:** `studies/foundational/m1-formal-model-v1/artifacts/formal-system.json`, artifact `LCMRP-ARTIFACT-0002-M1-FMO-BOUNDED-FORMAL-SYSTEM` version 1; exact digest verified in the canonical frozen manifest.
- **Assumptions:** FMO-A01 through FMO-A12, exact statements in `artifacts/assumptions.json`.
- **Propositions:** FMO-P01 through FMO-P04; FMO-C01 through FMO-C04; FMO-IE-01 through FMO-IE-10; FMO-NE-01 through FMO-NE-24 with FMO-NE-12A/B; FMO-INV-01 through FMO-INV-16; and FMO-CM-01 through FMO-CM-10.
- **Consistency or satisfiability checks:** Enumerate every valuation for each enumerated module and retain count plus first model. A module with zero models rejects bounded satisfiability. The free non-entailment module uses query-local projection and is not asserted satisfiable as a combined cross-product.
- **Intended entailments:** Search for satisfying premise-true/conclusion-false valuations for FMO-P01 through P04 and FMO-IE-01 through IE-10. Preserve every counterexample. Also verify that each premise is satisfiable; a vacuous result is `INCONCLUSIVE`, not support.
- **Non-entailments or countermodels:** Retain a premise-true/conclusion-false assignment for every FMO-NE query and validate the frozen assignments for FMO-CM-01 through CM-10. A witness demonstrates only freedom in the bounded encoding.
- **Proof or verification method:** Exhaustive finite Boolean model enumeration with complete assignments and one-at-a-time invariant omission, followed by independent human semantic adjudication. Parsing, schema validation, successful execution, and absence of a bounded counterexample are insufficient by themselves.
- **Semantic-validity check:** Two independent mappings and retained adjudication, with decision-bearing `BROADER`, `CIRCULAR`, or `UNSUPPORTED` mappings invalidating the affected machine analysis. `AMBIGUOUS` mappings make the affected conclusion inconclusive unless a frozen rule already resolves them.
- **Counterexample search:** Complete only over variables relevant to a query plus its containing module constraints, or all variables for an enumerated satisfiability module. Bounds and exclusions remain attached to every output.
- **Tool provenance:** `artifacts/tool-provenance.json`, which binds the exact analyzer SHA-256, CPython 3.12.13, standard-library-only method, integrity tools, no-service boundary, and no-full-validation notice. Its immutable digest must be recorded in the frozen manifest.

## 6. Baselines or comparison conditions

| Comparison ID | Exact alternative | Why informative | Matched inputs and constraints | Decision relevance | Limitation |
| --- | --- | --- | --- | --- | --- |
| `BASELINE-FMO-01-SYNTAX-ONLY` | Parse and schema-check the same artifacts without semantic enumeration. | Tests the prohibited interpretation that well-formedness establishes validity. | Exact input bytes and environment; no valuation semantics. | If the primary method cannot produce more inspectable models/counterexamples, reject its claimed analytical value. | Neither condition validates FMO-0.1. |
| `BASELINE-FMO-02-UNCONSTRAINED` | Remove every invariant constraint while retaining the same variables and queries. | Exposes outcomes caused only by free Boolean pairs. | Same variable names, bounds, and serialization. | An entailment that also appears unconstrained indicates a malformed or constant query. | Does not test natural-language fidelity. |
| `BASELINE-FMO-03-AXIOM-OMISSION` | Remove exactly one invariant constraint in its module. | Tests bounded independence and redundancy. | All other module constraints and valuation bounds unchanged. | A retained violating model is an independence witness within the kernel; no witness requires follow-up. | Module-local only; may miss cross-module dependence. |
| `BASELINE-FMO-04-NO-WITNESS-RETENTION` | Report pass/fail without a full retained assignment. | Tests auditability and replay value. | Same query and decision rule. | Any primary output lacking required assignments is invalid. | Retention does not establish semantic correctness. |
| `BASELINE-FMO-05-TRUNCATED-BOUNDARY` | Treat local erasure or incomplete target knowledge as verified deletion. | Direct adversarial comparison for FMO-INV-14. | Same declared root, attempt, and time; closure/materialization/reconstruction facts differ. | If the primary encoding permits verified success, reject the deletion-boundary claim. | Abstract facts do not prove physical deletion. |

## 7. Sources, cases, and provenance

| Source ID | Kind | Role | Exact version or digest | Construction or selection rule | Access and license | Human-data status |
| --- | --- | --- | --- | --- | --- | --- |
| `SOURCE-FMO-01` | `FORMAL_SPECIFICATION` | `PRIOR_WORK` | Registered subject v1, SHA-256 `82052e...faf3` | Exact subject bytes; no excerpt substitution | Public repository; repository license applies | No human subjects or participant data |
| `SOURCE-KERNEL-01` | `FORMAL_SPECIFICATION` | `FORMAL_INPUT` | Artifact version 1; digest verified in the canonical frozen manifest | All and only declared kernel modules | Public repository; repository license applies | No human subjects or participant data |
| `SOURCE-ASSUMPTIONS-01` | `OTHER_NON_HUMAN_SOURCE` | `DEVELOPMENT` | Artifact version 1; digest verified in the canonical frozen manifest | All FMO-A01 through FMO-A12 rows | Public repository; repository license applies | No human subjects or participant data |
| `SOURCE-PROPOSITIONS-01` | `OTHER_NON_HUMAN_SOURCE` | `DEVELOPMENT` | Artifact version 1; digest verified in the canonical frozen manifest | Full catalog, queries, invariant targets, and named witnesses | Public repository; repository license applies | No human subjects or participant data |

No publication corpus, participant record, private dataset, or application telemetry is used.

## 8. Metrics and analysis rules

| Analysis ID | Mode | Question | Measure or verification target | Decision rule | Planned output artifact |
| --- | --- | --- | --- | --- | --- |
| `ANALYSIS-FMO-01-SATISFIABILITY` | `CONFIRMATORY` | Does every enumerated module admit at least one satisfying valuation? | Exact valuation coverage, satisfying-model count, retained first model, and premise satisfiability | `COMPLETED/POSITIVE` only if every module has complete coverage and at least one model; zero models rejects the bounded claim; incomplete coverage is `INVALID`; integrity stop is `HALTED`. | `results/analysis-01-bounded-kernel-raw.json` |
| `ANALYSIS-FMO-02-ENTAILMENT` | `CONFIRMATORY` | Do FMO-P01–P04 and FMO-IE-01–IE-10 resist bounded counterexample search? | One exact query row, satisfiable premise, and retained violating assignment if found | Reject each encoded claim with a valid counterexample; no counterexample is positive only within the kernel; unsatisfied premise is `INCONCLUSIVE`; coverage/tool defect is `INVALID`. | `results/analysis-02-entailment.json` |
| `ANALYSIS-FMO-03-NONENTAILMENT` | `CONFIRMATORY` | Does every frozen FMO-NE query and FMO-CM-01–CM-10 obligation retain a valid witness? | Exact complete assignment satisfying constraints and witness condition | Missing or invalid witness rejects the bounded non-entailment claim; all witnesses retained is positive only within the kernel; semantic mismatch can invalidate. | `results/analysis-03-nonentailment.json` |
| `ANALYSIS-FMO-04-INVARIANT-INDEPENDENCE` | `EXPLORATORY` | Which FMO-INV-01–INV-16 constraints have one-at-a-time omission witnesses? | One omission row and full witness or no-witness record per invariant | Witness means independent only within the module; no witness is reported as `NOT-DEMONSTRATED` and triggers redundancy/contradiction follow-up, never automatic rejection. Missing invariant or incomplete search is `INVALID`. | `results/analysis-04-invariant-independence.json` |
| `ANALYSIS-FMO-05-AUTHORITY` | `CONFIRMATORY` | Does the bounded authority surface forbid successful state change under `DENY`/`UNRESOLVED` and preserve role-without-universal-authority? | FMO-INV-05, FMO-IE-05, FMO-NE-22, relevant omission and witness rows | Any permitted prohibited state-change valuation or absent role-without-authority witness rejects the bounded claim; no policy-composition or legitimacy conclusion is allowed. | `results/analysis-05-authority.json` |
| `ANALYSIS-FMO-06-DELETION` | `CONFIRMATORY` | Do the frozen deletion boundaries prevent verified labels under incomplete scope and exact-identity resurrection? | FMO-INV-14/15/16, FMO-P03, FMO-IE-07/10, FMO-NE-16/18/19, FMO-CM-04/06/10, and adversarial deletion assignments | Any model allowing verified success with unknown/access/reconstruction/local-erasure-only facts, or same-identity resurrection, rejects the bounded claim. No physical, external, or legal deletion conclusion follows. | `results/analysis-06-deletion.json` |
| `ANALYSIS-FMO-07-SEMANTIC-VALIDITY` | `CONFIRMATORY` | Are all decision-bearing source-to-encoding mappings faithful or narrower and non-circular? | Two independent classifications, exact source locations, retained disagreement, adjudication, and affected-analysis map | Any unremedied `BROADER`, `CIRCULAR`, or `UNSUPPORTED` mapping invalidates affected analyses; unresolved `AMBIGUOUS` mapping makes them inconclusive; missing independent review invalidates this analysis. | `results/analysis-07-semantic-validity.json` |

Every analysis must eventually receive exactly one active terminal disposition: `COMPLETED`, `NOT_RUN`, `HALTED`, or `INVALID`. Result class and claim assessment remain separate. No closeout is valid unless its analysis-ID set equals these seven IDs.

## 9. Rejection and stop criteria

| Criterion ID | Condition | Disposition | Rationale |
| --- | --- | --- | --- |
| `REJECT-FMO-01-ZERO-MODEL` | Any enumerated module has zero satisfying valuations under exact frozen constraints. | `REJECT_CLAIM` | Rejects bounded module satisfiability; it may reveal contradiction or encoding defect. |
| `REJECT-FMO-02-ENTAILMENT-COUNTEREXAMPLE` | A satisfying premise-true/conclusion-false assignment exists for an intended entailment. | `REJECT_CLAIM` | Direct bounded counterexample. |
| `REJECT-FMO-03-MISSING-NONENTAILMENT-WITNESS` | No valid witness exists for a frozen non-entailment or named countermodel. | `REJECT_CLAIM` | The bounded encoding does not admit the declared separation. |
| `REJECT-FMO-04-SEMANTIC-MISMATCH` | A decision-bearing mapping is broader, circular, or unsupported. | `INVALIDATE_ANALYSIS` | Machine semantics cannot support the source claim. |
| `REJECT-FMO-05-VACUITY` | An intended-entailment premise has no satisfying model. | `MARK_INCONCLUSIVE` | Absence of a counterexample is vacuous. |
| `REJECT-FMO-06-AUTHORITY-BYPASS` | `DENY` or `UNRESOLVED` coexists with successful state change, or a role entails universal authority. | `REJECT_CLAIM` | Violates the frozen authority boundary. |
| `REJECT-FMO-07-DELETION-FALSE-SUCCESS` | Verified deletion coexists with unknown, accessible, reconstructable, incomplete, or local-erasure-only in-scope facts. | `REJECT_CLAIM` | Violates the scoped success boundary. |
| `REJECT-FMO-08-RESURRECTION` | A terminal deleted exact identity becomes later accessible, non-deleted, or reused. | `REJECT_CLAIM` | Violates exact-identity terminality. |
| `STOP-FMO-01-PROVENANCE` | Any exact identity, version, digest, freeze authority, input, or environment binding fails. | `HALT_STUDY` | Results would not bind to the frozen study. |
| `STOP-FMO-02-PRIOR-RESULT-ACCESS` | Any planned output exists or was inspected before freeze. | `HALT_STUDY` | Confirmatory classification is compromised; a superseding record is required. |
| `STOP-FMO-03-INCOMPLETE-ENUMERATION` | Any required valuation, query, invariant, or countermodel is missing, duplicated, or silently coerced. | `INVALIDATE_ANALYSIS` | Exhaustiveness and auditability fail. |
| `STOP-FMO-04-UNDECLARED-TOOL` | Execution uses a network, model, solver, dependency, or mutable source outside frozen provenance. | `HALT_STUDY` | The method changed after freeze. |
| `STOP-FMO-05-OVERCLAIM` | Any output is characterized as validating or proving all FMO-0.1. | `HALT_STUDY` | Exceeds the formal-system and evidence boundaries. |

Stop criteria take precedence over favorable observations. Corrections after result access require a superseding study-record version and exploratory classification where required by the contract.

## 10. Security and privacy considerations

- **Assets:** Exact subject identity; protocol and freeze integrity; formal-system, assumptions, propositions, configuration, environment, tool, raw output, reviewer mappings, and atomic dispositions; negative and contradictory results.
- **Threats:** Subject or source substitution; forged digest or freeze attestation; execution before freeze; output overwrite; hidden analyzer modification; valuation omission; crafted expression ambiguity; result cherry-picking; deletion-scope overclaim; authority-legitimacy overclaim; reviewer capture; path escape; and injection of undeclared network/model/tool dependencies.
- **Controls:** Raw-byte SHA-256; exact IDs/versions; canonical record resolution; execution guard; repository-relative locators; clean exact revision; no network/model/solver; small expression whitelist; exhaustive bounded enumeration; exclusive-create outputs; complete assignments; independent semantic review; disagreement retention; immutable atomic findings; and closeout set equality.
- **Retention and deletion behavior:** Retain the frozen record, freeze artifact, every input, exact tool source, environment/configuration, raw outputs, digest ledger, reviewer mappings, disagreements, adjudication, deviations, and all dispositions indefinitely as program research records unless a separately governed retention policy requires otherwise. The package contains no participant or personal data. If an accidentally included secret or personal datum is detected, halt, quarantine access, document the incident without reproducing sensitive content, and follow a separately authorized deletion process; do not silently rewrite a frozen record.
- **Residual risks:** SHA-256 and repository review do not establish semantic fidelity or author legitimacy; the Boolean abstraction can hide contradictions; reviewers can share blind spots; a clean local execution can still use a compromised runtime; and abstract deletion variables cannot establish real erasure or absence of inference channels.
- **Human subjects involved:** No.
- **Human participant data involved:** No.

## 11. Reproducibility information

- **Source revision and dirty-state policy:** The frozen manifest binds exact raw bytes derived from author package merge `9966c31a86c999c5eda53aced8bb4274f2cbdc2d`. Execution requires exact digest agreement for every bound artifact and a separately recorded status of unrelated files. Any bound-byte change requires a digest-linked superseding record.
- **Subject-definition artifact:** `docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md`; raw-byte SHA-256 `82052e424c01d3204828472ef569f74f7c0aad418f827cffda92400562bbfaf3` (`VERIFIED`).
- **Profile-definition artifact:** `artifacts/method-profile-definition.json`, version 1; raw-byte SHA-256 verified in the canonical frozen manifest.
- **Formal input and source artifacts:** Exact kernel, assumptions, propositions, contract, and subject references listed above; all raw-byte digests must be verified in the final manifest.
- **Environment and locked dependencies:** CPython 3.12.13 standard library only for semantic execution; no dependency installation. JSON Schema Draft 2020-12 validation uses the repository development environment and is not a semantic result.
- **Configuration and tool versions:** Exact files `artifacts/configuration.json`, `artifacts/environment.json`, `artifacts/tool-provenance.json`, and `analyze_fmo_kernel.py`; tool provenance binds the analyzer raw-byte digest.
- **Randomness and seeds:** Not applicable; deterministic exhaustive enumeration with no random choice.
- **Protocol and freeze artifacts:** This immutable protocol, canonical manifest, active registry entry, and authority-bound attestation are exact-byte bound before any execution.
- **Replication criteria:** An independent implementation must resolve the same frozen record and inputs; enumerate the identical relevant valuations without omission/duplication; agree exactly on model counts, counterexample existence, retained lexicographically first witnesses, and named-countermodel predicates; reproduce all raw input digests; retain any disagreement; and conduct a new independent semantic-validity review. Runtime identity may differ only with disclosed equivalence testing. No numerical tolerance applies.

## 12. Failure analysis and retention plan

- **Subject-definition failure:** Wrong subject ID/version/digest, registry mismatch, or source ambiguity. Halt; do not analyze a substituted source.
- **Method-profile failure:** Missing required formal-analysis obligation, unsupported computational/empirical extension, or semantic check reduced to syntax. Invalidate the study design.
- **Source or case failure:** Missing/duplicate proposition, malformed witness, free variable, stale digest, or path escape. Invalidate affected analysis; supersede after freeze.
- **Tool or infrastructure defect:** Runtime mismatch, incomplete enumeration, serialization defect, overwrite, compromised environment, or hidden service call. Halt and retain logs; do not repair raw output in place.
- **Protocol deviation:** Any post-freeze change, prior result access, altered order/bound, or unreviewed adjudication. Publish a deviation record and apply contract amendment rules.
- **Invalid analysis:** Retain the output and exact reason; publish `INVALID`, never omit it or translate it to null.
- **Security or privacy failure:** Halt, restrict access, preserve non-sensitive audit facts, follow separately authorized incident and deletion procedures, and retain a redacted disposition without leaking the sensitive value.
- **Inconclusive outcome:** Preserve vacuity, ambiguity, no-independence-witness, and outside-kernel limitations as explicit results.
- **Negative, null, contradictory, failed, halted, invalid, and not-run retention:** Mandatory. Each receives an atomic record or terminal disposition, and the closeout ledger must include it.
- **Amendment triggers:** Any bound-byte change; changed analysis ID, mode, premise, conclusion, constraint, bound, baseline, decision rule, tool, environment, reviewer rule, or output locator; discovery of prior result access; or an integrity/security event. After freeze, create a digest-linked superseding record rather than editing history.

## 13. Limitations

- **Internal validity:** Many constraints encode desired consequences directly, creating circularity risk. Exhaustive enumeration prevents missed valuations only inside the encoded kernel.
- **Construct and semantic validity:** Boolean atoms can collapse typed, temporal, modal, quantified, epistemic, and governance meanings. The mandatory human review mitigates but cannot eliminate interpretive error.
- **Coverage and external validity:** Modules are independent, finite, and small. They do not establish a combined nontrivial FMO model, unbounded behavior, distributed histories, natural-language interpretation, or real system behavior.
- **Tool and formalization limits:** The study-local Python enumerator is not an external proof assistant or independently verified model checker. It provides no proof certificates and does not encode all 25 open FMO obligations.
- **Authority limits:** `PERMIT`, `DENY`, and `UNRESOLVED` remain opaque. No delegation, revocation, jurisdiction, obligation, legitimacy, or liveness conclusion is available.
- **Deletion limits:** Closure completeness and non-reconstruction are input propositions, not observations. No claim covers unknown/external copies, physical media, side channels, backups outside the boundary, or legal erasure.
- **Invariant-independence limits:** One-at-a-time module omission can miss joint dependence and cross-module redundancy.
- **Reproducibility limits:** Exact agreement can reproduce the same encoding defect. Independent semantic review is necessary but still judgment-dependent.
- **Security, privacy, and governance limits:** No adversarial runtime, information-flow, participant, legal, or operational evaluation occurs.

## 14. Evidence status

- **Foundational finding status:** No finding. This is a frozen preregistration with no results, and all seven planned outputs remain absent.
- **Mechanism evidence labels:** Not applicable.
- **Independent validation:** Not attempted. Internal protocol verification supported this freeze; independent scientific replication remains required after any findings before broader reliance.
- **Missing validation obligations:** separately governed execution; atomic dispositions for seven analyses; two independent semantic mappings and adjudication; immutable closeout; independent replication; and fuller formalization of the open FMO obligations.

Structural conformance, successful parsing, compilation, schema validity, module satisfiability, bounded entailment, or a retained countermodel cannot award a Charter mechanism evidence label or establish that FMO-0.1 is valid.

## 15. Recommended next experiment

- **Next falsifiable question:** Under this internally reviewed and authoritatively frozen protocol, do the exact bounded kernel and semantic mappings survive the seven preregistered analyses without a retained contradiction, counterexample, missing witness, authority/deletion boundary failure, or invalid encoding?
- **Largest uncertainty:** Whether the Boolean constraints faithfully and non-circularly preserve the typed and temporal meaning of FMO-0.1 while remaining strong enough to expose contradictions.
- **Required comparison or counterexample:** Syntax-only, unconstrained, invariant-omission, no-witness-retention, and truncated-deletion-boundary baselines; every discovered counterexample must be retained.
- **Rejection criterion:** Apply REJECT-FMO-01 through REJECT-FMO-08 and STOP-FMO-01 through STOP-FMO-05 exactly; favorable partial results cannot override a stop or invalidity condition.
- **Independent review or replication required:** One further independent protocol and encoding review before execution; two independent semantic mappings during analysis; and an independently implemented replay before any claim is treated as independently validated.

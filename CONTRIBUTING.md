# Contributing to LCMRP

LCMRP welcomes research questions, taxonomies, formalizations, benchmark designs, reference implementations, replications, negative results, security analyses, governance work, and documentation corrections.

Contributions must preserve the program's independence, evidence discipline, and separation between research and product integration.

## Before starting

For substantive work, begin with a bounded proposal or issue that states:

- Research question or problem
- Primary research layer
- Mechanism or claim in scope
- Falsifiable hypothesis, when applicable
- Assumptions and comparison baselines
- Proposed datasets or scenarios
- Metrics and rejection criteria
- Expected artifacts
- Security, privacy, compute, storage, and licensing constraints
- Evidence state being investigated, not promised

Small editorial corrections do not require a research proposal, but they must not change the meaning of a versioned artifact.

## Declare the research layer

Follow [Research Layers](docs/program/RESEARCH_LAYERS.md). Every substantive contribution must declare Layer 1, Layer 2, or Layer 3 and explain the classification.

Layer 1 and Layer 2 work must remain product-independent. CorpusStudio-specific production code is not accepted.

If CorpusStudio is discussed, isolate the discussion under **Future CorpusStudio Integration Implications**, place **RESEARCH-TO-PRODUCT HYPOTHESIS** immediately below the heading, and identify the validation still missing. Omit the section when there is no relevant implication.

## Define the claim before the mechanism or study contract

A mechanism contribution should make the following reviewable:

1. The claim being tested
2. Assumptions and operating envelope
3. Adversary, trust, authority, and privacy model where applicable
4. Success and failure criteria
5. Baselines and ablations
6. Evidence that would reject or narrow the claim
7. Known limitations and unresolved obligations

Do not describe a candidate contribution as novel or production-ready without the evidence required to support that statement.

A mechanism-free Layer 1 taxonomy, formal-model, concept, or evaluation-construct study must use the [Foundational Study Contract](docs/program/FOUNDATIONAL_STUDY_CONTRACT.md). Register the exact versioned subject before activating a frozen study, publish one atomic finding or terminal disposition per planned analysis, and publish a separate immutable closeout only after its disposition ledger exactly covers every planned analysis. Use the dedicated foundational protocol, finding, and closeout templates. Do not create a placeholder mechanism merely to satisfy the mechanism experiment schema, and do not apply a Charter mechanism maturity label to a foundational subject, finding, or closeout.

## Reproducibility requirements

Record, when applicable:

- Repository revision and mechanism version or digest
- Model provider, model identifier, exact version, and relevant inference settings
- Dataset identity, version, split, license, and transformation lineage
- Configuration files and command invocation
- Random seeds and determinism limitations
- Dependency and runtime versions
- Hardware and operating environment
- Start and end conditions
- Raw or minimally transformed measurements
- Failed runs, exclusions, protocol deviations, and missing data
- Latency, storage, compute, and token-cost measurements

Secrets, credentials, private user data, and restricted data must not be committed as reproducibility artifacts. Use synthetic or appropriately governed data for tests.

## Experiment and report structure

Substantive reports should include, where applicable:

1. Research question
2. Layer
3. Hypothesis
4. Related mechanisms or prior work
5. Experimental design
6. Baselines
7. Datasets or scenarios
8. Metrics
9. Results
10. Failure analysis
11. Security and privacy considerations
12. Reproducibility information
13. Limitations
14. Evidence status
15. Recommended next experiment

Negative, null, and contradictory results are first-class contributions. Preserve them with the same provenance expected for positive results.

## Reference implementation requirements

A Layer 2 implementation must:

- Implement an identified research hypothesis or specification
- Separate experimental logic from supporting infrastructure
- Expose documented interfaces
- Minimize application assumptions
- Provide tests and a reproducible execution path
- Include baseline comparisons
- Document unsupported cases and known failures
- Keep storage, retrieval, model, and embedding components replaceable where practical
- Avoid implying production suitability

A runnable demonstration is evidence of implementability only. It is not evidence of effectiveness, safety, robustness, or product fitness.

## Security and privacy

Read [SECURITY.md](SECURITY.md) before contributing attack demonstrations, persistent-memory inputs, deletion tests, or artifacts derived from sensitive data.

Security experiments must declare assets, actors, adversary capabilities, oracle or tool access, trust boundaries, leakage channels, persistence scope, and success criteria. Potential vulnerabilities may be submitted only through a verified private channel and must be coordinated before a public proof of concept is submitted.

The repository does not guarantee that private vulnerability reporting is currently enabled. Do not submit embargoed vulnerability details, exploit material, durable injection payloads, sensitive samples, or other risky security artifacts until the private channel described in [SECURITY.md](SECURITY.md) has been enabled and verified.

## Evidence-review requests

An evidence-state request must identify the exact mechanism version, claim scope, supporting records, requested state, and proposed reviewer. Reviewer eligibility, conflicts, quorum, and approval follow [GOVERNANCE.md](GOVERNANCE.md).

An originating researcher or solo maintainer may disclose a self-review for states that do not require independence, but that review cannot count as independent corroboration. A request for `INDEPENDENTLY_VALIDATED` must include a documented decision from an eligible external evaluator. The originator cannot self-award that state, and appointing a reviewer does not by itself establish independence.

## Pull requests

Keep each pull request bounded to one independently reviewable claim, protocol, mechanism, result set, or governance change when practical.

A substantive pull request should include:

- Purpose and primary research layer
- Files and contracts changed
- Tests or validation performed
- Reproduction instructions
- Evidence records added or affected
- Security and privacy impact
- Compatibility impact
- Known failures and limitations
- Follow-up work explicitly out of scope

Before requesting review, confirm:

- [ ] The contribution complies with the current Program Charter.
- [ ] Claims are scoped to the evidence actually supplied.
- [ ] Baselines, metrics, and rejection criteria are explicit where applicable.
- [ ] Versions, seeds, configurations, and environments are recorded where applicable.
- [ ] Failed runs and unfavorable results are retained.
- [ ] Tests do not contain secrets or real sensitive user data.
- [ ] Documentation and schemas agree with the implementation.
- [ ] Evidence labels follow [Evidence and Readiness States](docs/program/EVIDENCE_STATES.md).
- [ ] CorpusStudio content is absent or correctly isolated and labeled.

## Review standards

Reviewers evaluate:

- Charter and layer compliance
- Claim clarity and falsifiability
- Baseline and protocol adequacy
- Reproducibility and provenance
- Statistical and qualitative interpretation
- Boundary, adversarial, and failure coverage
- Security, privacy, deletion, and authority behavior
- Evidence-state accuracy
- Compatibility and maintainability of experimental interfaces

Approval means the contribution satisfies its declared scope. It does not independently validate the mechanism or advance its evidence state unless a separate evidence decision establishes that gate.

## Licensing

By submitting a contribution, you agree that it may be distributed under this repository's MIT License. Do not contribute material you do not have the right to distribute, including datasets, model outputs, code, or documentation with incompatible terms.

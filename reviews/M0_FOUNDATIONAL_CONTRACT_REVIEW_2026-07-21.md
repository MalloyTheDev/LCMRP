# M0 Foundational Contract Review — 2026-07-21

## Review status

- **Review type:** Internal research, implementation, and adversarial-testing review
- **Disposition:** Pass for publication in the existing draft pull request
- **M0 completion effect:** None; M0 remains **In progress**
- **Independent validation:** None claimed
- **Scientific or maturity evidence awarded:** None

This review addresses the prior M0 boundary finding that the initial experiment and evidence contracts could not represent a mechanism-free Layer 1 study. It does not validate a taxonomy, formal model, memory mechanism, or product architecture.

> **Completion follow-up — 2026-07-21:** The blockers recorded by this review were closed through a standalone subject registry, immutable all-analysis closeout, exact artifact/index binding, and dedicated human templates. The corrections and negative tests are preserved in [M0 Final Adversarial Review](M0_FINAL_ADVERSARIAL_REVIEW_2026-07-21.md); governance acceptance is recorded in [M0 Completion Decision](M0_COMPLETION_DECISION_2026-07-21.md). The original findings below remain historical context.

## Review method

Three separate work arms were used:

1. A read-only primary-source review assessed provenance, immutable research objects, versioned method profiles, preregistration, null-result retention, taxonomy evaluation, and formal-analysis obligations.
2. A coding and writing pass produced a parallel foundational-study contract without changing the existing mechanism schemas or fixtures.
3. An adversarial testing pass attempted profile ambiguity, missing obligations, mutable digests, result-access leakage, human-study bypasses, Layer 3 field smuggling, maturity-label leakage, cross-record substitutions, source-role mismatches, and invalid registry states.

The final repository review reconciled the three arms and retained unresolved real-registration blockers.

CorpusStudio was not inspected. Its training setup was unnecessary to answer this product-independent Layer 1 contract question. No CorpusStudio file or repository state was modified.

## Accepted design

- `foundational-study-manifest` represents a typed, versioned, non-mechanism subject and exactly one versioned primary method profile.
- v0.1 supports `STRUCTURAL_OR_TAXONOMY_EVALUATION` and `FORMAL_ANALYSIS` only.
- Analysis mode is recorded per analysis.
- Frozen manifests require freeze evidence and immutable subject, profile, source, environment, configuration, and protocol artifacts.
- `research-finding-record` binds an exact study, subject, profile, and analysis while preserving `COMPLETED`, `NOT_RUN`, `HALTED`, and `INVALID` dispositions.
- Result class and claim assessment remain orthogonal.
- A foundational finding has a machine-enforced empty mechanism-label set and cannot contain a mechanism evidence decision.
- Separate empty foundational-study and research-finding indexes provide append-oriented discoverability without fabricating research entries.
- The original mechanism experiment, evidence, registry, and example files remain byte-identical to the previously published draft baseline.

The research basis, source mapping, alternatives, and rejection rules are documented in [Foundational Study Contract v0.1](../docs/program/FOUNDATIONAL_STUDY_CONTRACT.md).

## Validation results

- JSON Schema Draft 2020-12 meta-validation: passed
- All schema/example pairs: passed
- Structural repository validator: passed
- Python compilation: passed
- Dependency health check: passed
- Unit and adversarial tests: **62/62 passed**
- Credential and private-key pattern scan: no findings
- Existing mechanism-contract byte comparison: passed

The added tests cover dynamic schema/example discovery, method-profile obligations, immutable digests, preregistration and amendments, terminal dispositions, result/claim orthogonality, maturity-label isolation, human-study bypasses, Layer 3 smuggling, exact finding-to-study bindings, taxonomy source roles, active-index status gates, and legacy compatibility.

## Resolved draft-publication risks

| Risk | Disposition |
| --- | --- |
| Making mechanisms optional would preserve hidden mechanism-only assumptions. | Rejected; parallel contracts were created. |
| A taxonomy/formal finding could acquire a Charter mechanism label. | Rejected structurally through constant no-effect fields, an empty label set, and additional-property denial. |
| A single global analysis mode could conceal post-result exploration. | Rejected; mode is per analysis and post-result supersession forces exploratory analyses. |
| A taxonomy profile could omit negative cases or structural obligations. | Rejected through required competency, integrity, positive/negative, adjudication, and coverage fields plus source-role checks. |
| A formal profile could treat syntax checking as validity. | Rejected through required consistency/satisfiability, entailment, countermodel, semantic-validity, and tool-provenance fields. |
| A finding could substitute a different study, subject, profile, or analysis. | Rejected by exact cross-record binding validation and raw-byte digest checks. |
| An active index could expose draft records as accepted. | Rejected; active studies must be frozen and active findings must be published. |

## Remaining blockers

The following block M0 completion or registration of a real foundational study, but do not block publication of this explicitly draft, empty-registry contract:

- No machine-enforced one-finding-or-disposition-per-planned-analysis completeness rule exists for terminal studies.
- No standalone foundational-subject registry or subject-supersession validator exists.
- No external registration-service verification exists; the schema records an authority and immutable freeze artifact only.
- Controlled computational/empirical and evidence-synthesis profiles are not defined.
- Frozen taxonomy and formal-analysis protocol families have not been exercised in real adversarial studies or independently reviewed.
- Dedicated human-facing foundational protocol and finding templates remain a usability task.

## Final judgment

The change is suitable for the existing draft pull request. It resolves the immediate representational gap without weakening mechanism evidence gates, adding product assumptions, or asserting a research result. It is not sufficient to mark M0 complete or to accept a real foundational record.

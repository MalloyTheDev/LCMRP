# Lifelong Cognitive Memory Research Program (LCMRP)

LCMRP is an independent research and engineering program investigating lifelong, human-inspired, machine-governed memory for artificial intelligence systems.

The program develops reproducible evidence, taxonomies, benchmarks, product-independent reference implementations, and security and governance analyses. Memory mechanisms remain research artifacts until their effectiveness, safety, and operational characteristics have been independently validated.

## Program boundary

LCMRP is not a CorpusStudio subsystem. CorpusStudio is a motivating use case and a possible future integration target, but it does not determine this program's research agenda, terminology, architecture, experiments, or implementation choices.

Any discussion of CorpusStudio is provisional, must be isolated under a section titled **Future CorpusStudio Integration Implications**, and must be labeled **RESEARCH-TO-PRODUCT HYPOTHESIS**.

## Start here

- [Program Charter v0.1](docs/program/PROGRAM_CHARTER_v0.1.md) defines the mission, constraints, workstreams, and reporting requirements.
- [M0 Foundation](docs/program/M0_FOUNDATION.md) records the completed infrastructure milestone, its exclusions and exit evidence, and the gate that opened M1.
- [M1 Foundation](docs/program/M1_FOUNDATION.md) defines the active Layer 1 taxonomy and formal-model milestone, its launch scope, and its still-open exit criteria.
- [Research Layers](docs/program/RESEARCH_LAYERS.md) defines how work is classified and kept product-independent.
- [Foundational Study Contract v0.1](docs/program/FOUNDATIONAL_STUDY_CONTRACT.md) defines mechanism-free Layer 1 study profiles and finding boundaries.
- [Evidence Label Normalization](docs/program/EVIDENCE_LABELS.md) maps Charter display labels to their machine-readable tokens without changing their meaning.
- [Evidence States](docs/program/EVIDENCE_STATES.md) defines maturity labels and the evidence required to advance them.
- [Governance](GOVERNANCE.md) defines authority, decisions, amendments, and research-integrity rules.
- [Contributing](CONTRIBUTING.md) defines the contribution and review workflow.
- [Security](SECURITY.md) defines vulnerability reporting and the initial research threat surface.
- [M0 Boundary Review](reviews/M0_BOUNDARY_REVIEW_2026-07-20.md) records the internal adversarial review and remaining completion blockers.
- [M0 Foundational Contract Review](reviews/M0_FOUNDATIONAL_CONTRACT_REVIEW_2026-07-21.md) records the mechanism-free Layer 1 contract judgment and testing results.
- [M0 Final Adversarial Review](reviews/M0_FINAL_ADVERSARIAL_REVIEW_2026-07-21.md) records the completion-focused negative tests and technical verdict.
- [M0 Completion Decision](reviews/M0_COMPLETION_DECISION_2026-07-21.md) records the exit-criterion evidence, governance acceptance, compatibility impact, and post-M0 limits.
- [M1 Prior-Art and Competing-Taxonomies Map](docs/taxonomy/M1_PRIOR_ART_AND_COMPETING_TAXONOMIES.md) records scoped research inputs and unresolved alternatives without adopting a taxonomy.
- [M1 Taxonomy-to-FMO Crosswalk Draft](docs/taxonomy/M1_TAXONOMY_TO_FMO_CROSSWALK_DRAFT_v0.1.md) preserves an unregistered mapping proposal outside the exact registered v1 subject bytes.
- [Memory Taxonomy v0.1 Candidate](docs/taxonomy/MEMORY_TAXONOMY_v0.1.md) defines falsifiable candidate terms, axes, distinctions, and edge cases.
- [Formal Memory Object Model v0.1 Candidate](docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md) defines the candidate objects, relations, operations, invariants, and open proof obligations.
- [M1 Synthetic Contract Dry Runs](examples/m1-dry-runs/) exercise the foundational subject-to-closeout record graph without registering a real study or producing evidence.
- [M1 Dry-Run Adversarial Review](reviews/M1_DRY_RUN_ADVERSARIAL_REVIEW_2026-07-21.md) records the separate mutation-test verdict and its limits.
- [M1 Dry-Run Decision](reviews/M1_DRY_RUN_DECISION_2026-07-21.md) records the steward-level acceptance boundary for this M1 increment.
- [M1 Taxonomy Subject Admission Dossier](reviews/M1_TAXONOMY_SUBJECT_ADMISSION_2026-07-21.md) reviews the exact taxonomy bytes for identity-only registration.
- [M1 Formal-Model Subject Admission Dossier](reviews/M1_FORMAL_MODEL_SUBJECT_ADMISSION_2026-07-21.md) reviews the exact formal-model bytes for identity-only registration.
- [M1 Subject-Admission Adversarial Review](reviews/M1_SUBJECT_ADMISSION_ADVERSARIAL_REVIEW_2026-07-21.md) records cross-binding and mutation-test results for the two real subject entries.
- [M1 Subject-Admission Decision](reviews/M1_SUBJECT_ADMISSION_DECISION_2026-07-21.md) records the final steward judgment and the limits of registration.
- [M1 Taxonomy Frozen Protocol](studies/foundational/m1-taxonomy-v1/protocol-v1.md) preregisters five structural/taxonomy analyses without executing them.
- [M1 Formal-Model Frozen Protocol](studies/foundational/m1-formal-model-v1/protocol-v1.md) preregisters seven bounded formal analyses while leaving the analyzer unexecuted.
- [M1 Study-Freeze Adversarial Review](reviews/M1_STUDY_FREEZE_ADVERSARIAL_REVIEW_2026-07-21.md) records exact-byte, mutation, output-absence, and registry-containment gates.
- [M1 Study-Freeze Decision](reviews/M1_STUDY_FREEZE_DECISION_2026-07-21.md) records the steward acceptance boundary and remaining execution obligations.
- [M1 Taxonomy Execution-Readiness Review](reviews/M1_TAXONOMY_EXECUTION_READINESS_2026-07-21.md) records the non-case preflight blockers that prevent taxonomy v1 execution.
- [M1 Formal Execution Preflight](studies/foundational/m1-formal-model-v1/execution/preflight-execution-attestation.json) records the fail-closed guard defect discovered before the configured analyzer command ran.
- [M1 Formal-Model Execution-Readiness Review](reviews/M1_FORMAL_MODEL_EXECUTION_READINESS_2026-07-21.md) records the formal v1 blocker, its non-result boundary, and the required governed supersession path.
- [M1 Study-Execution Adversarial Review](reviews/M1_STUDY_EXECUTION_ADVERSARIAL_REVIEW_2026-07-21.md) independently tests containment and the two truthful blocked-not-run states.
- [M1 Study-Execution Decision](reviews/M1_STUDY_EXECUTION_DECISION_2026-07-21.md) records the steward disposition and required versioned supersession work.
- [M1 Launch-Continuation Triage](reviews/M1_LAUNCH_CONTINUATION_TRIAGE_2026-07-21.md) is a historical consolidation of continuation prerequisites; later readiness records govern where its inventory has been superseded.
- [M1 Taxonomy Pre-Result Metadata and Intake-Contract Repair Package](reviews/M1_TAXONOMY_PRE_RESULT_REPAIR_PACKAGE_2026-07-22.md) records pre-result superseding obligations for taxonomy blockers B2–B6 without freeze, live intake, case access, or execution authority; residual human-contributor blocker B1 remains open.
- [M1 Formal Study-Record v2 Supersession](reviews/M1_FORMAL_STUDY_RECORD_V2_SUPERSESSION_2026-07-22.md) freezes the formal version-2 preregistration that supersedes the blocked version-1 tool binding without executing the analyzer or creating results.
- [M1 Taxonomy Study-Record v2 Freeze](reviews/M1_TAXONOMY_STUDY_RECORD_V2_FREEZE_2026-07-22.md) freezes taxonomy version-2 metadata repairs (B2–B6) while B1, case access, and execution remain closed.
- [Agent Instructions](AGENTS.md) applies the same boundary and evidence rules to automated contributors.

## Research contracts

- [`schemas/`](schemas/) contains versioned JSON Schema Draft 2020-12 contracts.
- [`examples/`](examples/) contains explicitly non-evidentiary example records.
- [`templates/`](templates/) contains proposal, protocol, report, foundational closeout, and threat-model structures.
- [`registry/`](registry/) contains mechanism, experiment, evidence, foundational-subject, foundational-study, research-finding, and foundational-closeout indexes. Two exact subjects and two frozen preregistrations are active; the five result/mechanism registries remain empty. Subject registration and study freeze are provenance and governance actions, not research evidence.
- [`records/`](records/) defines the immutable record layout used once experiments and evidence exist.
- [`references/`](references/) defines source-verification and citation-recording rules.

Repository validation is run with `python tools/validate_repository.py` after installing the pinned dependencies in `requirements-dev.lock`.

## Current phase

**M1 in progress — taxonomy v2 frozen with residual human-intake gate B1; formal v2 frozen but analysis not run**

The accepted M0 foundation establishes the rules and records needed to distinguish hypotheses, implementations, experiments, evidence, and maturity claims. M1 has two exact `ACTIVE` subjects. Taxonomy version-1 is retained as `SUPERSEDED` historical provenance after a digest-linked version-2 freeze that repairs metadata/intake-contract blockers B2–B6; residual human-contributor blocker **B1** remains open, so execution intake and case adjudication are not authorized. Formal version-1 is likewise `SUPERSEDED` after a digest-linked version-2 freeze that binds the corrected analyzer guard; the configured analyzer command, `main`, and `run_kernel` have still not been invoked for semantic analysis. All planned outputs remain absent, and no finding or closeout exists. These states do not adopt or validate either candidate, prove or disprove the formal model, award evidence, authorize product work, or complete M1. The mechanism, experiment, evidence, research-finding, and foundational-closeout registries remain empty.

## License

This repository is licensed under the [MIT License](LICENSE).

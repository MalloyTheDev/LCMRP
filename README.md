# Lifelong Cognitive Memory Research Program (LCMRP)

LCMRP is an independent research and engineering program investigating lifelong, human-inspired, machine-governed memory for artificial intelligence systems.

The program develops reproducible evidence, taxonomies, benchmarks, product-independent reference implementations, and security and governance analyses. Memory mechanisms remain research artifacts until their effectiveness, safety, and operational characteristics have been independently validated.

## Program boundary

LCMRP is not a CorpusStudio subsystem. CorpusStudio is a motivating use case and a possible future integration target, but it does not determine this program's research agenda, terminology, architecture, experiments, or implementation choices.

Any discussion of CorpusStudio is provisional, must be isolated under a section titled **Future CorpusStudio Integration Implications**, and must be labeled **RESEARCH-TO-PRODUCT HYPOTHESIS**.

## Start here

- [Program Charter v0.1](docs/program/PROGRAM_CHARTER_v0.1.md) defines the mission, constraints, workstreams, and reporting requirements.
- [M0 Foundation](docs/program/M0_FOUNDATION.md) defines the current milestone, exclusions, exit criteria, and M1 entry gate.
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
- [Memory Taxonomy v0.1 Candidate](docs/taxonomy/MEMORY_TAXONOMY_v0.1.md) defines falsifiable candidate terms, axes, distinctions, and edge cases.
- [Formal Memory Object Model v0.1 Candidate](docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md) defines the candidate objects, relations, operations, invariants, and open proof obligations.
- [M1 Synthetic Contract Dry Runs](examples/m1-dry-runs/) exercise the foundational subject-to-closeout record graph without registering a real study or producing evidence.
- [M1 Dry-Run Adversarial Review](reviews/M1_DRY_RUN_ADVERSARIAL_REVIEW_2026-07-21.md) records the separate mutation-test verdict and its limits.
- [M1 Dry-Run Decision](reviews/M1_DRY_RUN_DECISION_2026-07-21.md) records the steward-level acceptance boundary for this M1 increment.
- [Agent Instructions](AGENTS.md) applies the same boundary and evidence rules to automated contributors.

## Research contracts

- [`schemas/`](schemas/) contains versioned JSON Schema Draft 2020-12 contracts.
- [`examples/`](examples/) contains explicitly non-evidentiary example records.
- [`templates/`](templates/) contains proposal, protocol, report, foundational closeout, and threat-model structures.
- [`registry/`](registry/) contains mechanism, experiment, evidence, foundational-subject, foundational-study, research-finding, and foundational-closeout indexes. Empty registries mean that no research entries have yet been accepted.
- [`records/`](records/) defines the immutable record layout used once experiments and evidence exist.
- [`references/`](references/) defines source-verification and citation-recording rules.

Repository validation is run with `python tools/validate_repository.py` after installing the pinned dependencies in `requirements-dev.lock`.

## Current phase

**M1 launched — Layer 1 taxonomy and formal-model work in progress**

The accepted M0 foundation establishes the rules and records needed to distinguish hypotheses, implementations, experiments, evidence, and maturity claims. M1 has begun with product-independent candidate memory taxonomy and formal object-model artifacts. Two isolated synthetic dry runs now exercise the accepted Layer 1 record paths, but only as non-evidentiary fixtures. The candidates remain hypotheses and research inputs: they are not an adopted taxonomy, a validated formal model, a scientific finding, or evidence that any memory mechanism is ready for use. Production registries remain empty, and M1 remains incomplete.

## License

This repository is licensed under the [MIT License](LICENSE).

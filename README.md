# Lifelong Cognitive Memory Research Program (LCMRP)

LCMRP is an independent research and engineering program investigating lifelong, human-inspired, machine-governed memory for artificial intelligence systems.

The program develops reproducible evidence, taxonomies, benchmarks, product-independent reference implementations, and security and governance analyses. Memory mechanisms remain research artifacts until their effectiveness, safety, and operational characteristics have been independently validated.

## Program boundary

LCMRP is not a CorpusStudio subsystem. CorpusStudio is a motivating use case and a possible future integration target, but it does not determine this program's research agenda, terminology, architecture, experiments, or implementation choices.

Any discussion of CorpusStudio is provisional, must be isolated under a section titled **Future CorpusStudio Integration Implications**, and must be labeled **RESEARCH-TO-PRODUCT HYPOTHESIS**.

## Start here

- [Program Charter v0.1](docs/program/PROGRAM_CHARTER_v0.1.md) defines the mission, constraints, workstreams, and reporting requirements.
- [M0 Foundation](docs/program/M0_FOUNDATION.md) defines the current milestone, exclusions, exit criteria, and M1 entry gate.
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

**M0 complete — M1 entry gate open**

The accepted M0 foundation establishes the rules and records needed to distinguish hypotheses, implementations, experiments, evidence, and maturity claims. M1 may begin with product-independent memory taxonomy and formal-model work. M0 produced no scientific evidence and does not claim that any memory mechanism is validated or ready for product use.

## License

This repository is licensed under the [MIT License](LICENSE).

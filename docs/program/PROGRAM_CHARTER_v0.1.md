# Lifelong Cognitive Memory Research Program — LCMRP

## Program Charter v0.1

### Mission

LCMRP is an independent research and engineering program investigating lifelong, human-inspired, machine-governed memory for artificial intelligence systems.

Its purpose is to produce:

- Reproducible empirical evidence
- Clear memory-system taxonomies
- Representative benchmarks and evaluation protocols
- Product-independent reference implementations
- Security, privacy, and governance analyses
- Validated architectural mechanisms
- Documented failure modes and limitations

LCMRP will treat memory mechanisms as research artifacts until their effectiveness, safety, and operational characteristics have been independently validated.

### Program Status

LCMRP is not a CorpusStudio subsystem.

LCMRP is standalone and product-independent. Its research agenda, architecture, experiments, terminology, repositories, benchmarks, and implementation decisions must not be constrained by CorpusStudio’s:

- Current architecture
- Repository structure
- Product roadmap
- User interface
- Technology stack
- Existing implementation choices
- Near-term delivery requirements

CorpusStudio is a motivating use case and possible future integration target, not the organizing structure of the research program.

### Required Research Layers

Every LCMRP proposal, experiment, implementation, or report must identify its applicable layer.

#### Layer 1 — Foundational Research

This layer investigates underlying memory concepts and mechanisms without assuming a specific product environment.

Representative topics include:

- Memory types and functional taxonomies
- Encoding, consolidation, retrieval, reconsolidation, and forgetting
- Episodic, semantic, procedural, prospective, and working memory
- Temporal organization and event segmentation
- Salience and importance estimation
- Confidence, uncertainty, and provenance
- Contradiction detection and belief revision
- Memory interference and catastrophic accumulation
- Identity continuity and personalization
- Machine-controlled versus user-controlled memory
- Long-horizon evaluation
- Privacy, security, deletion, and governance
- Biological inspiration and its limits

Outputs should primarily consist of hypotheses, formal definitions, literature syntheses, datasets, benchmarks, experimental protocols, and empirical findings.

#### Layer 2 — Product-Independent Reference Implementations

This layer converts selected research hypotheses into minimal, reproducible technical systems.

Reference implementations must:

- Remain independent of CorpusStudio
- Expose clearly defined interfaces
- Minimize application-specific assumptions
- Include reproducible tests and experiments
- Distinguish experimental mechanisms from supporting infrastructure
- Record model, dataset, configuration, and environment provenance
- Include baseline comparisons
- Document known failure modes
- Avoid implying production readiness
- Support replacement of storage, retrieval, and model components where practical

A reference implementation demonstrates that a mechanism can be studied. It does not establish that the mechanism is appropriate for production integration.

#### Layer 3 — Future CorpusStudio Integration

This layer may evaluate how independently validated LCMRP results could apply to CorpusStudio workflows, such as:

- Dataset provenance
- Training-run continuity
- Project decisions
- Evaluation history
- Experiment lineage
- Local hardware constraints
- Long-running research context

This layer must remain separate from foundational research and reference implementation work.

No CorpusStudio-specific production code will be created during the foundational or product-independent phases.

### Evidence and Readiness States

LCMRP mechanisms should use explicit maturity labels.

| State | Meaning |
| --- | --- |
| HYPOTHESIS | A proposed mechanism with insufficient empirical support |
| PROTOTYPE | A runnable implementation intended for investigation |
| REPLICATED | Results reproduced across multiple controlled runs |
| BENCHMARKED | Evaluated against declared baselines and metrics |
| ROBUSTNESS-TESTED | Tested on adversarial, boundary, and distribution-shift cases |
| SECURITY-REVIEWED | Threat model and material security risks documented |
| INDEPENDENTLY VALIDATED | Evidence reproduced or reviewed outside the originating experiment |
| INTEGRATION CANDIDATE | Suitable for product-specific feasibility assessment |
| PRODUCTION-READY | Product validation, operational testing, and governance requirements satisfied |

Progress through these states is not automatic. A mechanism must not be described as production-ready merely because it performs well in a research benchmark.

### Research Standards

LCMRP work should include, where applicable:

1. A falsifiable hypothesis
2. A defined comparison baseline
3. Representative and held-out test cases
4. Quantitative and qualitative metrics
5. Reproducible configurations
6. Random-seed and model-version tracking
7. Ablation studies
8. Boundary and adversarial tests
9. Latency, storage, compute, and token-cost measurements
10. Security and privacy analysis
11. Failure categorization
12. Known limitations
13. Criteria for replication
14. Criteria for rejecting the mechanism

Negative results, null findings, and failed mechanisms are valid program outputs and should be retained.

### Initial Program Workstreams

#### Memory Taxonomy and Formal Model

Define a product-independent vocabulary for memory objects, processes, lifecycle states, authority, provenance, and confidence.

#### Benchmark and Evaluation Design

Create tasks that measure more than factual retrieval, including:

- Long-horizon continuity
- Selective retention
- Appropriate forgetting
- Contradiction handling
- Temporal reasoning
- Source-sensitive recall
- Preference evolution
- Cross-session task continuation
- Resistance to irrelevant-memory interference
- Safe deletion
- Recovery from corrupted memory

#### Memory Lifecycle Mechanisms

Investigate:

- Admission
- Encoding
- Deduplication
- Consolidation
- Abstraction
- Retrieval
- Updating
- Reconsolidation
- Decay
- Archival
- Deletion

#### Governance and Control

Study authority boundaries among:

- The user
- The AI system
- Application operators
- Model providers
- External tools and data sources

#### Security and Privacy

Analyze threats including:

- Memory poisoning
- Prompt-injection persistence
- Unauthorized inference
- Sensitive-data retention
- Cross-user leakage
- Provenance forgery
- Deletion failure
- Retrieval manipulation
- Malicious consolidation
- Identity and preference hijacking

#### Reference Architecture

Build modular experimental components for:

- Event ingestion
- Memory-object creation
- Provenance tracking
- Retrieval
- consolidation
- conflict detection
- policy enforcement
- deletion
- evaluation instrumentation

#### Longitudinal Experimentation

Develop simulations and controlled studies spanning many sessions, evolving facts, changing preferences, conflicting evidence, and delayed consequences.

### Architectural Independence Rules

LCMRP reference systems must not assume:

- A specific vector database
- A specific language model vendor
- A specific embedding model
- A particular application schema
- A CorpusStudio repository
- CorpusStudio domain entities
- CorpusStudio UI flows
- CorpusStudio release milestones
- Continuous cloud connectivity
- Unlimited compute or storage

CorpusStudio scenarios may later be introduced as evaluation cases, but they must not define the general memory architecture.

### Required Reporting Structure

Substantive LCMRP reports should use the following structure when applicable:

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

Any discussion of CorpusStudio must appear only in the following separately titled section.

### Future CorpusStudio Integration Implications

**RESEARCH-TO-PRODUCT HYPOTHESIS**

Content in this section is provisional and does not constitute an architectural decision, implementation commitment, roadmap recommendation, or claim of production readiness. Each implication must identify the independent validation still required before product adoption can be considered.

### Standing Constraints

The following constraints are now part of the LCMRP program baseline:

- LCMRP will not be described as part of CorpusStudio.
- Foundational research will not be routed into CorpusStudio product areas.
- CorpusStudio-specific production code will not be created.
- Product architecture will not be allowed to predetermine research conclusions.
- Reference implementations will remain product-independent.
- Successful experiments will not be treated as sufficient evidence for integration.
- CorpusStudio implications will be isolated in the required section.
- Every CorpusStudio recommendation will be labeled RESEARCH-TO-PRODUCT HYPOTHESIS until independently validated.

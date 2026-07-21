# M0 — Research Governance and Reproducibility Foundation

## Status

**Milestone state:** Complete  
**Accepted:** 2026-07-21 through the conditioned governance decision in [M0 Completion Decision](../../reviews/M0_COMPLETION_DECISION_2026-07-21.md)  
**Applicable layer:** Program infrastructure supporting all three research layers  
**Scientific evidence produced:** None

M0 establishes the contracts required to conduct and evaluate later LCMRP work. Completing M0 does not validate any memory mechanism.

## Objectives

M0 must make the program charter operational by establishing:

1. A canonical, versioned program charter.
2. Explicit research-layer and independence rules.
3. Defined evidence states and transition obligations.
4. Machine-readable mechanism experiments and evidence, mechanism-free foundational studies and findings, and immutable record indexes.
5. Human-facing proposal, protocol, report, and threat-model templates.
6. Empty registries that do not imply unperformed research.
7. Automated structural validation in continuous integration.
8. Contribution, governance, citation, and vulnerability-reporting procedures.

## In scope

- Research governance and terminology boundaries
- Reproducibility metadata contracts
- Method-specific applicability profiles for mechanism and mechanism-free research
- Claim and evidence discipline
- Security and privacy reporting structure
- Repository organization and automated contract checks
- Rules isolating future CorpusStudio implications

## Out of scope

- Implementing a memory engine or retrieval system
- Selecting a vector database, language model, embedding model, or model provider
- Producing benchmark scores or empirical conclusions
- Declaring any mechanism effective, novel, robust, secure, or production-ready
- Writing CorpusStudio-specific production code
- Treating a product workflow as the organizing architecture of LCMRP

## Exit criteria

M0 may be marked complete only when all of the following hold:

- [x] The full Program Charter v0.1 is canonical and discoverable.
- [x] Research layers and evidence-state semantics are documented.
- [x] All JSON Schemas pass Draft 2020-12 meta-schema validation.
- [x] Every example record validates against its declared schema.
- [x] Registries parse safely, declare a schema version, and contain no fabricated entries.
- [x] Templates include hypothesis, baselines, metrics, rejection criteria, failure analysis, reproducibility, limitations, and security/privacy obligations where applicable.
- [x] CorpusStudio implications are isolated and labeled **RESEARCH-TO-PRODUCT HYPOTHESIS**.
- [x] Duplicate JSON and YAML keys are rejected by repository validation.
- [x] Relative Markdown links resolve.
- [x] The continuous-integration validation job passes on a clean checkout.
- [x] A boundary review confirms that no memory implementation or product-specific architecture entered M0.

Completion evidence, compatibility impact, accepted limitations, and the exact governance condition are recorded in the [M0 Completion Decision](../../reviews/M0_COMPLETION_DECISION_2026-07-21.md). M0 completion establishes infrastructure only and awards no scientific evidence state.

## M1 entry gate

The M1 entry gate is open. M1 should begin with the product-independent memory taxonomy and formal object model. The accepted M0 foundation supplies stable artifact identifiers and requires charter or schema changes to be versioned without rewriting prior evidence records.

M1 must not begin by selecting storage infrastructure or coding a full memory service. Its first deliverables should be falsifiable definitions, competing taxonomies, representative edge cases, and unresolved formal obligations.

## Future CorpusStudio Integration Implications

**RESEARCH-TO-PRODUCT HYPOTHESIS**

M0 makes no CorpusStudio architectural recommendation. A future product-feasibility assessment may reuse independently validated LCMRP reporting and provenance contracts, but only after their usability, completeness, migration behavior, and governance properties have been evaluated outside a CorpusStudio-specific implementation.

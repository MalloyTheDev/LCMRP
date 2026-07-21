# Research Layers

## Purpose

Every LCMRP proposal, experiment, implementation, benchmark, and substantive report must declare exactly one applicable research layer. Work spanning layers must be split into separately reviewable artifacts whose claims and acceptance criteria remain independent.

Program infrastructure may explicitly state that it supports all three layers, but that classification does not make the infrastructure a research result or evidence for a memory mechanism.

Layer assignment describes the scope of the work. It does not imply evidence maturity or readiness.

## Canonical machine tokens

The Program Charter's layer titles remain the authoritative display labels. Schemas and registries use the following exact tokens:

| Charter display label | Canonical machine token |
| --- | --- |
| Layer 1 — Foundational Research | `LAYER_1_FOUNDATIONAL_RESEARCH` |
| Layer 2 — Product-Independent Reference Implementations | `LAYER_2_PRODUCT_INDEPENDENT_REFERENCE_IMPLEMENTATION` |
| Layer 3 — Future CorpusStudio Integration | `LAYER_3_FUTURE_CORPUSSTUDIO_INTEGRATION` |

These tokens are serialization aliases, not alternate layer definitions. Producers must emit the canonical token exactly; consumers may render its mapped Charter label. No normalization by punctuation removal, case folding, pluralization, or free-text matching is permitted.

## Layer 1 — Foundational Research

Layer 1 asks what memory concepts mean, how they may be modeled, and how competing mechanisms can be evaluated without assuming a particular product.

Typical outputs include:

- Falsifiable hypotheses and rejection criteria
- Formal or operational definitions
- Product-independent taxonomies
- Literature syntheses
- Datasets and scenario generators
- Benchmark specifications
- Experimental protocols
- Empirical findings, including null and negative results
- Threat models and governance analyses

Layer 1 work must not select a mechanism because it matches an existing product architecture. Biological analogy may motivate a hypothesis, but it is not evidence that the hypothesis is correct or desirable in a machine system.

## Layer 2 — Product-Independent Reference Implementations

Layer 2 implements a Layer 1 hypothesis as a minimal system that can be measured, replaced, and reproduced.

A Layer 2 contribution must:

- Identify the hypothesis or specification it instantiates
- Expose explicit component boundaries and interfaces
- Separate the experimental mechanism from test harnesses and supporting infrastructure
- Avoid application-specific domain entities and workflows
- Record code, model, dataset, configuration, seed, dependency, and environment provenance
- Include declared baselines and tests
- Measure relevant compute, storage, latency, and token costs
- Document failure modes and unsupported cases
- Permit replacement of storage, retrieval, embedding, and model components where practical
- Avoid claims of production readiness

Layer 2 establishes that a mechanism can be investigated as implemented. It does not establish general effectiveness, safe deployment, or product suitability.

## Layer 3 — Future CorpusStudio Integration

Layer 3 is limited to studying whether independently validated LCMRP results might apply to CorpusStudio-specific workflows and constraints.

Layer 3 may contain feasibility questions, evaluation scenarios, gap analyses, or provisional mappings. It must not:

- Redefine a Layer 1 concept to fit the current CorpusStudio architecture
- Add CorpusStudio assumptions to a Layer 2 interface
- Treat an encouraging experiment as an integration decision
- Create CorpusStudio-specific production code
- Create a CorpusStudio roadmap commitment
- Describe a mechanism as production-ready without product-specific validation and governance

Every permitted CorpusStudio discussion must appear under this exact heading:

## Future CorpusStudio Integration Implications

The first content under that heading must be the label:

**RESEARCH-TO-PRODUCT HYPOTHESIS**

The section must state what independent validation is still missing. If a contribution has no CorpusStudio implications, the section should be omitted rather than filled speculatively.

## Classification rules

Use the following decision test:

| Question | Applicable layer |
| --- | --- |
| Does the work define, compare, or test a general memory concept? | Layer 1 |
| Does the work implement a general mechanism so it can be reproduced experimentally? | Layer 2 |
| Does the work assess a validated mechanism against a CorpusStudio-specific use case or constraint? | Layer 3 |

When a contribution crosses layers, split it into independently reviewable artifacts. For example, define the general benchmark in Layer 1, implement its product-independent harness in Layer 2, and place any CorpusStudio feasibility analysis in a separately titled Layer 3 document.

Unclear classification defaults to the lower-numbered, more product-independent layer until reviewers resolve the boundary.

## Independence checks

A Layer 1 or Layer 2 contribution is noncompliant if its validity depends on any of the following:

- A particular vector database, language-model vendor, embedding model, or hosted service
- A CorpusStudio repository, domain entity, user-interface flow, release milestone, or implementation detail
- Continuous cloud access
- Unlimited compute or storage
- An undeclared application schema

Using one implementation as an experimental condition is permitted when the abstraction, reason for selection, provenance, alternatives, and limits on generalization are documented. The selected component must not become an undeclared architectural requirement.

## Review checklist

Reviewers must confirm:

1. The primary layer is declared and justified.
2. Claims do not exceed the layer's evidentiary scope.
3. Product assumptions have not leaked into foundational definitions or reference interfaces.
4. Cross-layer artifacts can be evaluated independently.
5. CorpusStudio discussion, if any, is isolated, labeled, and explicit about missing validation.
6. No CorpusStudio-specific production code is introduced.

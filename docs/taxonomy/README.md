# Memory Taxonomy and Formal Model

**Layer:** Layer 1 — Foundational Research  
**M0 status:** Structure established; no taxonomy has been validated or adopted.

This workstream will define a product-independent vocabulary for memory objects, processes, lifecycle states, authority, provenance, confidence, and uncertainty. Its purpose is to make hypotheses and experiments comparable without allowing a storage product, model vendor, application schema, or biological metaphor to dictate the definitions.

## Scope

Candidate areas include:

- Episodic, semantic, procedural, prospective, and working memory
- Encoding, consolidation, retrieval, reconsolidation, and forgetting
- Temporal organization and event segmentation
- Salience, confidence, uncertainty, provenance, and source authority
- Contradiction detection, belief revision, interference, and accumulation
- Identity continuity, personalization, and authority boundaries
- Admission, deduplication, abstraction, updating, decay, archival, and deletion

This list identifies charter-derived research areas. It does not assert that human memory categories transfer directly to machine systems or that the listed categories are mutually exclusive, exhaustive, or already operationally defined.

## Definition requirements

Every proposed term should state:

1. The term and any aliases
2. Whether it names an object, process, policy, state, capability, measurement, or system
3. A bounded natural-language definition
4. A formal or operational definition when one is available
5. Necessary and sufficient conditions, or an explicit statement that they remain unknown
6. Inputs, outputs, persistent state, and time assumptions
7. Authority and provenance semantics
8. Contrasting terms and known boundary cases
9. Observable tests that distinguish the term from adjacent concepts
10. Biological inspiration, if any, and the limits of that analogy
11. Evidence label, supporting sources, and unresolved conflicts
12. Version, author, review status, and superseded definitions

Definitions must not hide mechanism choices. For example, a memory category should not be defined by a particular vector database, embedding model, prompt format, or application entity unless the definition is explicitly limited to that implementation.

## Formalization discipline

For each formal claim, separate:

- **Claim:** what is being asserted
- **Assumptions:** conditions required for the claim
- **Model:** state, actors, operations, time, observations, and authority
- **Statement:** the precise proposition
- **Proof strategy:** the proposed derivation or experimental argument
- **Edge cases:** boundaries and counterexamples considered
- **Missing obligations:** unproved lemmas, untested assumptions, or unavailable evidence
- **Status:** hypothesis, proof sketch, proved under stated assumptions, empirically supported, contradicted, or unresolved

A proof sketch is not a proof. An operational definition that is useful for one benchmark is not automatically a general theory of memory.

## Review workflow

1. Propose a term with its evidence and competing definitions.
2. Search adjacent terminology across cognitive science, machine learning, information retrieval, databases, security, and human-computer interaction as applicable.
3. Identify ambiguity, category overlap, and counterexamples.
4. Define observable distinctions and candidate measurements.
5. Review for product and implementation assumptions.
6. Version the accepted definition; never silently rewrite a term used by a completed experiment.
7. Record unresolved alternatives and empirical tests needed to choose among them.

## M0 exit condition for this workstream

M0 establishes only the rules and location for future taxonomy work. A later milestone must define and review the initial terms, map their dependencies, and link each operational definition to candidate evaluation tasks before the taxonomy can guide experiments.

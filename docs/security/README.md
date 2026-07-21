# Security, Privacy, and Governance Research

**Layer rule:** Each security artifact declares exactly one applicable layer; foundational analysis and reference-implementation validation remain separate linked artifacts  
**M0 status:** Threat categories and review requirements established; no mechanism has completed a security review.

Persistent memory changes an AI system's security boundary: untrusted content can influence future sessions, derived state can outlive its source, retrieval can expose sensitive information, and a model may propose operations that it is not authorized to perform. LCMRP therefore treats security, privacy, deletion, provenance, and authority as properties to test rather than assurances inferred from task performance.

## Initial threat areas

Every relevant threat model must assess:

- Memory poisoning
- Persistent prompt injection
- Unauthorized inference
- Sensitive-data retention
- Cross-user leakage
- Provenance forgery
- Deletion failure
- Retrieval manipulation
- Malicious consolidation
- Identity or preference hijacking

The list is a minimum, not an exhaustive threat taxonomy. Rollback, replay, credential compromise, availability exhaustion, confused-deputy behavior, supply-chain compromise, unsafe recovery, and side channels should be added when applicable.

## Required security model

Before making a security claim, define:

1. The system boundary, lifecycle stages, components, and parameters
2. Protected assets and operational security properties
3. Actors, authority, ownership, and trust boundaries
4. The adversary's goals, capabilities, resources, persistence, and collusion
5. Oracle, model, storage, tool, administrative, and physical access
6. Explicit adversary non-capabilities
7. Direct leakage, observable outputs, and side channels
8. Trusted components and failure assumptions
9. A measurable success criterion for the adversary and for each defense
10. Residual risks and excluded threats

Claims apply only within that model. Passing a test against one injection strategy does not establish security against persistent injection in general.

## Authority principles

- The user, AI system, application operator, model provider, and external source are distinct principals.
- A model may propose a memory action; proposal alone does not authorize admission, disclosure, update, consolidation, archival, or deletion.
- Policy enforcement and audit evidence must reside in the declared trusted boundary.
- Provenance records must preserve who asserted information, who authorized a lifecycle action, and which transformation produced derived state.
- Confidence and salience do not confer authority.
- Cross-user and cross-scope access must be denied and tested explicitly rather than left to retrieval similarity.
- Privileged override, recovery, and revocation paths require their own controls and audit trail.

These are research constraints for evaluating mechanisms, not a claim that a trusted kernel or any particular implementation is already correct.

## Privacy and deletion

A data-lifecycle analysis must cover raw observations, normalized records, embeddings, summaries, consolidated memories, indexes, caches, logs, backups, exported artifacts, evaluation datasets, and any model updates derived from the data.

Deletion claims must state:

- The requesting principal and authorization rule
- The exact target and scope
- Whether deletion is logical, cryptographic, physical, or eventual
- Replica, cache, backup, log, and derived-state behavior
- How completion and failure are observed
- Retention exceptions and their authority
- Recovery and rollback implications
- Limits that prevent complete removal

The disappearance of an item from normal retrieval is not by itself evidence of deletion.

## Security evaluation

Security experiments should include:

- Positive and negative authorization tests
- Multi-user and multi-scope isolation tests
- Poisoning and persistent-injection sequences spanning sessions
- Provenance tampering and replay attempts
- Retrieval manipulation and denial-of-retrieval cases
- Malicious or erroneous consolidation and reconsolidation
- Correction, revocation, deletion, and derived-state verification
- Boundary values and resource exhaustion
- Distribution shifts and adaptive adversaries where justified
- Corruption detection, quarantine, and recovery
- False-positive and false-negative analysis

Record exact parameters, seeds, attacker knowledge, attempts, queries, successes, failures, and observables. Retain unsuccessful attacks; selectively reporting successful or unsuccessful attempts invalidates rate estimates.

## Review and evidence status

Use `templates/threat-model.md` for each mechanism or system revision. A security review should produce:

- A versioned threat model
- Traceable requirements and tests
- Findings ranked by evidence and impact
- Residual risks and explicit acceptance authority
- Reproducible attack and defense artifacts when release is safe
- Restricted handling for exploit or sensitive evidence when needed
- Review expiration triggers

`SECURITY_REVIEWED` means that the declared threat model and material risks were documented for a specific version. It does not mean vulnerability-free, independently validated, integration-ready, or production-ready. Architecture, policy, model, data-flow, dependency, and deployment changes can invalidate the review.

## Responsible handling

Potential vulnerabilities should be reported through the repository's documented security channel rather than published with unnecessary exploit detail. Preserve enough evidence for triage while minimizing exposure of secrets, personal data, attack payloads, and affected identities.

## M0 exit condition for this workstream

M0 establishes the threat-model template and baseline analysis requirements only. Later milestones must define scoped security hypotheses, build reproducible tests, document findings, and obtain the required review before any mechanism can be labeled `SECURITY_REVIEWED`.

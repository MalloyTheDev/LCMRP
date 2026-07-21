# Security Policy

## Supported research surface

LCMRP is currently establishing its M0 research governance and reproducibility foundation. During this phase, the latest revision of the default branch is the supported security-review surface. No mechanism is implied to be safe for production deployment.

Experimental artifacts may intentionally model hostile inputs and failure cases. Their presence does not make them safe to run on private data, privileged systems, or production infrastructure.

## Reporting a vulnerability

Do not open a public issue containing exploit details, secrets, personal data, or a method for persistently compromising a deployed memory system.

### Current private-reporting limitation

This policy does not claim that a private reporting channel is currently enabled or monitored. Before LCMRP solicits or accepts embargoed vulnerability details, active exploit material, durable prompt-injection payloads, sensitive samples, or other risky security artifacts, the repository owner must enable and verify GitHub private vulnerability reporting.

Until a verified private channel is available, do not submit risky details or artifacts through issues, pull requests, discussions, commit history, or other public repository surfaces. A contributor may open a minimal public issue asking the maintainer to enable a private channel, but that issue must contain no vulnerability details.

Use the repository's private **Report a vulnerability** or security-advisory interface only after it has been enabled and verified. Include:

- Affected file, component, version, or commit
- Vulnerability class and expected impact
- Preconditions and required attacker access
- Reproduction steps or a minimal proof of concept
- Persistence and cross-session behavior
- Data, user, tenant, tool, or authority boundaries crossed
- Whether deletion, revocation, or rollback succeeds
- Suggested mitigations, if known
- Disclosure constraints or active exploitation, if known

If no verified private reporting interface is available, the project is not ready to accept risky security artifacts. Maintainers must not ask a reporter to send sensitive details through an unverified channel.

Maintainers should acknowledge the report privately, reproduce and triage it, establish a coordinated disclosure plan, and preserve a non-sensitive decision record. Response and remediation timing depends on severity, reproducibility, maintainer availability, and whether downstream systems are affected.

## Initial threat surface

Security analysis should consider at least:

- Memory poisoning and durable prompt injection
- Cross-user, cross-session, cross-project, or cross-tenant leakage
- Unauthorized inference of sensitive or deleted information
- Provenance forgery and source-confusion attacks
- Retrieval ranking or filter manipulation
- Malicious consolidation, abstraction, or reconsolidation
- Identity, preference, authority, and policy hijacking
- Failure to delete derived copies, indexes, summaries, caches, backups, or model-visible state
- Corrupted-memory recovery and rollback failure
- Tool-output, model-output, and external-source trust confusion
- Resource-exhaustion attacks through unbounded accumulation or retrieval
- Integrity loss in experiment, benchmark, or evidence records
- Supply-chain compromise of models, datasets, dependencies, or stored artifacts

This list is a starting point, not a complete threat model.

## Security-model requirements

A security claim must define:

- Assets and protected properties
- Users, operators, providers, tools, and external sources
- Trust boundaries and authority boundaries
- Adversary capabilities, access, persistence, and collusion assumptions
- Available queries, oracles, side channels, and leakage
- Memory lifecycle stages in scope
- Success criterion and measurement method
- Recovery, revocation, deletion, and audit assumptions
- Residual risk and conditions outside the claim

A mechanism is not `SECURITY-REVIEWED` merely because it has security tests. The evidence gate in [Evidence and Readiness States](docs/program/EVIDENCE_STATES.md) requires a documented threat model, review, material findings, mitigations, and residual risks for the declared scope.

## Research-data safety

Use synthetic, consented, licensed, or appropriately governed data. Do not commit:

- Credentials, tokens, private keys, or connection strings
- Real personal conversations or memory exports without explicit authorization and governance
- Authentication artifacts or private system prompts
- Identifying data presented as anonymized without a documented re-identification assessment
- Malicious payloads that create unnecessary risk when a harmless reproducer is sufficient

Redact reports carefully. Memory vulnerabilities may remain exploitable even when the original triggering message is removed, so check summaries, embeddings, indexes, caches, derived records, logs, backups, and evaluation outputs.

## Deletion claims

A deletion test must define the target object, authority initiating deletion, derived artifacts in scope, storage and cache boundaries, time bound, backup assumptions, verification method, and acceptable residual evidence.

Removing a primary record is not sufficient evidence of deletion when retrievable derivatives, summaries, embeddings, indexes, logs, or replicas remain in scope.

## Coordinated disclosure and research publication

Security findings are valid research outputs, including findings that reject a proposed mechanism. Public reports should preserve scientific value while withholding operational details that would create avoidable harm before mitigation.

Security review is scoped evidence, not certification. Absence of a reported vulnerability is not evidence that a mechanism is secure.

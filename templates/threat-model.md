# Threat Model: `<system or mechanism>`

> This document defines the security model and its limits. Replace every angle-bracketed placeholder. Untested protections are design claims, not security findings.

## Document control

| Field | Value |
| --- | --- |
| Threat-model ID | `<stable identifier>` |
| Version | `<version>` |
| Status | `DRAFT`, `REVIEWED`, `SUPERSEDED`, or `RETIRED` |
| Scope revision | `<source revision or mechanism version>` |
| Applicable layer | `Layer 1`, `Layer 2`, or `Layer 3` |
| Authors | `<names or stable contributor identifiers>` |
| Security reviewers | `<names or stable contributor identifiers>` |
| Privacy reviewers | `<names or stable contributor identifiers>` |
| Created | `<YYYY-MM-DD>` |
| Last reviewed | `<YYYY-MM-DD>` |
| Next review trigger | `<date, architecture change, or evidence event>` |

## 1. Scope and security question

- System or mechanism under analysis: `<description>`
- Security question: `<falsifiable security question>`
- Included components and lifecycle stages: `<ingestion, creation, storage, retrieval, consolidation, updating, deletion, evaluation, or others>`
- Excluded components: `<components and rationale>`
- Deployment and operating assumptions: `<environment>`
- Parameters and resource bounds: `<model, data, session, storage, time, query, or compute bounds>`

## 2. Architecture and data flow

Describe each component, persistent store, model, external service, administrator surface, and user boundary. Attach a versioned data-flow diagram when the system has more than one trust boundary.

| Component | Responsibility | Inputs | Outputs | Persistent state | Trust level |
| --- | --- | --- | --- | --- | --- |
| `<component>` | `<responsibility>` | `<inputs>` | `<outputs>` | `<state>` | `<trusted, partially trusted, or untrusted>` |

## 3. Assets and security properties

| Asset | Owner or authority | Sensitivity | Required property | Failure impact |
| --- | --- | --- | --- | --- |
| `<memory content, provenance, policy, identity, model state, key, log, or other asset>` | `<principal>` | `<classification>` | `<confidentiality, integrity, availability, authenticity, isolation, deletion, or other property>` | `<impact>` |

Define each claimed property operationally. In particular, distinguish availability of the service from availability of a specific memory, and distinguish logical deletion from physical erasure and removal of derived state.

## 4. Actors, authority, and trust boundaries

| Actor | Authorized actions | Prohibited actions | Credentials or proof | Revocation path |
| --- | --- | --- | --- | --- |
| `<user, AI system, operator, model provider, external tool, data source, or attacker>` | `<actions>` | `<actions>` | `<mechanism>` | `<procedure>` |

### Trust boundaries

| Boundary ID | From | To | Data or control crossing | Enforcement | Failure consequence |
| --- | --- | --- | --- | --- | --- |
| `<TB-001>` | `<source>` | `<destination>` | `<flow>` | `<control>` | `<impact>` |

Do not treat the model's instruction following, confidence, or self-report as an authorization boundary.

## 5. Adversary model

Define the adversary before evaluating a defense. Include compromised insiders and external data sources when relevant.

| Adversary ID | Goal | Capabilities | Oracle, tool, and interface access | Persistence | Explicit non-capabilities | Success criterion |
| --- | --- | --- | --- | --- | --- | --- |
| `<A-001>` | `<goal>` | `<read, write, inject, observe, replay, collude, corrupt, or other powers>` | `<queries and controls available>` | `<duration and cross-session reach>` | `<bounds>` | `<observable condition>` |

### Leakage and side channels

- Direct outputs visible to the adversary: `<outputs>`
- Retrieval behavior and membership signals: `<signals>`
- Timing, size, frequency, and error channels: `<channels>`
- Embeddings, caches, logs, backups, and telemetry: `<channels>`
- Model-provider or external-tool exposure: `<exposure>`
- Physical or local-host side channels: `<scope or exclusion with rationale>`

## 6. Abuse cases and threat register

At minimum, assess every charter threat as applicable, not applicable with a reason, or unresolved.

| Threat ID | Threat | Preconditions and attack path | Assets and properties affected | Existing controls | Test or evidence | Residual risk | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<T-001>` | Memory poisoning | `<details>` | `<impact>` | `<controls>` | `<test or evidence record>` | `<risk>` | `<applicable, not applicable, or unresolved>` |
| `<T-002>` | Persistent prompt injection | `<details>` | `<impact>` | `<controls>` | `<test or evidence record>` | `<risk>` | `<status>` |
| `<T-003>` | Unauthorized inference | `<details>` | `<impact>` | `<controls>` | `<test or evidence record>` | `<risk>` | `<status>` |
| `<T-004>` | Sensitive-data retention | `<details>` | `<impact>` | `<controls>` | `<test or evidence record>` | `<risk>` | `<status>` |
| `<T-005>` | Cross-user leakage | `<details>` | `<impact>` | `<controls>` | `<test or evidence record>` | `<risk>` | `<status>` |
| `<T-006>` | Provenance forgery | `<details>` | `<impact>` | `<controls>` | `<test or evidence record>` | `<risk>` | `<status>` |
| `<T-007>` | Deletion failure | `<details>` | `<impact>` | `<controls>` | `<test or evidence record>` | `<risk>` | `<status>` |
| `<T-008>` | Retrieval manipulation | `<details>` | `<impact>` | `<controls>` | `<test or evidence record>` | `<risk>` | `<status>` |
| `<T-009>` | Malicious consolidation | `<details>` | `<impact>` | `<controls>` | `<test or evidence record>` | `<risk>` | `<status>` |
| `<T-010>` | Identity or preference hijacking | `<details>` | `<impact>` | `<controls>` | `<test or evidence record>` | `<risk>` | `<status>` |

Add threats involving rollback, replay, availability exhaustion, confused-deputy behavior, credential compromise, supply-chain compromise, corrupted-memory recovery, or policy bypass when they are within scope.

## 7. Privacy and data-lifecycle analysis

| Lifecycle stage | Data processed | Purpose and authority | Minimization | Retention | Deletion behavior | Derived or replicated state |
| --- | --- | --- | --- | --- | --- | --- |
| `<ingestion, encoding, storage, retrieval, consolidation, update, archival, deletion, or evaluation>` | `<data>` | `<purpose and authority>` | `<control>` | `<duration>` | `<semantics and verification>` | `<caches, embeddings, summaries, logs, backups, or model updates>` |

- Sensitive-data classes: `<classes>`
- Consent or lawful basis: `<basis>`
- Purpose limitation: `<limits>`
- User inspection, correction, export, and deletion rights: `<controls>`
- Data-controller and processor assumptions: `<roles>`
- Re-identification and linkage risks: `<risks>`
- Aggregate, derived, and model-state removal limits: `<limits>`

## 8. Security requirements and controls

| Requirement ID | Security statement | Assumptions | Control | Verification method | Failure response |
| --- | --- | --- | --- | --- | --- |
| `<R-001>` | `<testable requirement>` | `<assumptions>` | `<preventive, detective, or corrective control>` | `<test>` | `<response>` |

Separate controls enforced by trusted code from actions merely proposed by a model. Identify fail-open and fail-closed behavior, privileged override paths, key-management assumptions, and recovery dependencies.

## 9. Verification plan

| Test ID | Adversary and threat | Setup and parameters | Observable success criterion | Repetitions | Evidence retained |
| --- | --- | --- | --- | --- | --- |
| `<SEC-001>` | `<IDs>` | `<conditions>` | `<criterion>` | `<count and rationale>` | `<artifacts>` |

Include boundary, adversarial, distribution-shift, rollback, recovery, and deletion-verification tests where applicable. Document false-positive and false-negative costs. A passed test supports only the tested adversary, parameters, and environment.

## 10. Residual risk and failure handling

| Risk ID | Residual risk | Likelihood basis | Impact | Acceptance authority | Required follow-up |
| --- | --- | --- | --- | --- | --- |
| `<RR-001>` | `<risk>` | `<evidence or uncertainty>` | `<impact>` | `<principal>` | `<mitigation, test, transfer, or rejection>` |

- Detection and alerting: `<mechanisms>`
- Containment: `<procedure>`
- Revocation and quarantine: `<procedure>`
- Recovery from corrupted memory: `<procedure>`
- Evidence preservation: `<procedure>`
- User notification and remediation: `<procedure>`
- Conditions requiring the experiment or mechanism to stop: `<conditions>`

## 11. Claims, evidence, and review status

| Security claim | Evidence label | Supporting test or source | Missing obligation | Risk if false | Next check |
| --- | --- | --- | --- | --- | --- |
| `<bounded claim>` | `<[VERIFIED], [USER], [MEMORY], [VERIFY], or [CONFLICT]>` | `<locator>` | `<gap>` | `<impact>` | `<action>` |

- Security review status: `<not reviewed, reviewed with open findings, or reviewed>`
- Review scope: `<scope and exclusions>`
- Unresolved high-risk findings: `<findings, or None>`
- Prior awarded evidence profile: `<set of independently awarded labels and decision IDs>`
- State under review: `SECURITY_REVIEWED`
- Recommended action for that state: `<AWARD, RETAIN, WITHHOLD, REVOKE, or INCONCLUSIVE, with evidence records>`
- Independent validation: `<status and evidence, or Not performed>`

`SECURITY_REVIEWED` means the threat model and material risks have been documented; it does not mean the system is secure against undeclared adversaries or production-ready.

## 12. Reproducibility and limitations

- Source, configuration, model, and data revisions: `<identifiers>`
- Test harness and dependency lock: `<identifiers>`
- Random seeds and run artifacts: `<locations>`
- Restricted evidence and access procedure: `<details>`
- Assumptions not tested: `<assumptions>`
- Threats excluded: `<threats and rationale>`
- Environmental and parameter limits: `<limits>`
- Review expiration conditions: `<conditions>`

## Future CorpusStudio Integration Implications

**RESEARCH-TO-PRODUCT HYPOTHESIS**

`<Optional block: remove this heading, label, and placeholder when there is no CorpusStudio implication. Otherwise describe each provisional implication, the product-independent security evidence supporting it, the product-specific threats not covered here, and the independent validation still required. This section is not an architectural decision, implementation commitment, roadmap recommendation, or claim of production readiness.>`

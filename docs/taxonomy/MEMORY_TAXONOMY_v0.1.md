# Candidate Memory Taxonomy v0.1

Applicable layer: Layer 1 — Foundational Research  
Artifact status: LAUNCHED / IN PROGRESS candidate  
Mechanism evidence label: Not applicable  
Scientific findings asserted: None  
Artifact ID: `LCMRP-MEMORY-TAXONOMY`  
Artifact version: `0.1`

## Candidate status and use

This artifact proposes a product-independent vocabulary for studying lifelong machine memory. Its definitions are falsifiable candidates, not adopted terminology or findings. The categories are not presumed to be mutually exclusive, collectively exhaustive, biologically equivalent, or useful in an implementation.

The candidate taxonomy is intended to support later structural evaluation under the [Foundational Study Contract](../program/FOUNDATIONAL_STUDY_CONTRACT.md). Conformance to this document would mean only that a study or model uses the stated candidate definitions consistently. It would not establish that the definitions are correct, complete, externally valid, secure, or preferable to alternatives.

## Version and identifier rules

- A candidate term ID has the form `LCMRP-TAX-<CLASS>-<NUMBER>@<VERSION>`.
- The full ID, including version, identifies exactly one definition in this artifact.
- Rewording that changes a boundary, necessary condition, sufficient condition, observable distinction, or counterexample requires a new term version.
- A later artifact may retain the stable portion before `@`, but it must link the superseded exact version rather than silently rewriting it.
- Examples in this document are constructed cases. They are not observations, datasets, registrations, or evidence.
- “Proposed necessary” and “proposed sufficient” describe logical commitments to test. “Unknown” means this artifact intentionally makes no such commitment.

## Candidate term register

### Entities and informational objects

| Candidate ID | Term and kind | Bounded candidate definition | Necessary-condition status | Sufficient-condition status |
| --- | --- | --- | --- | --- |
| `LCMRP-TAX-ENT-001@0.1` | **Source event** — entity | A bounded occurrence, input, communication, observation, or system action presented as a possible origin of memory content. An event record can be inaccurate or malicious. | **Proposed necessary:** an event identity and at least one asserted event or receipt time. | **Unknown:** a timestamped input alone may be a static source rather than an event. |
| `LCMRP-TAX-ENT-002@0.1` | **Memory candidate** — entity/state bearer | A bounded representation proposed for possible admission but not yet accepted into the governed memory population. | **Proposed necessary:** content or a content reference, candidate identity, origin, and undecided admission status. | **Proposed sufficient within this artifact:** those conditions plus an applicable admission decision point. |
| `LCMRP-TAX-ENT-003@0.1` | **Memory object version** — entity | An immutable, identity-bearing representation admitted to a governed memory population, with an exact version, lifecycle state, provenance assertions, and scoped policy metadata. “Object” is abstract and does not imply object-oriented code or one stored record. | **Proposed necessary:** exact identity/version, admitted status, content or governed content reference, provenance, and lifecycle state. | **Unknown:** these structural features may not distinguish memory from ordinary governed records. |
| `LCMRP-TAX-ENT-004@0.1` | **Memory series** — relation-defined entity | The ordered set of exact memory object versions treated as continuity-preserving successors of one stable identity. Series continuity does not imply unchanged content or truth. | **Proposed necessary:** one stable series ID and at least one exact version; every successor names its predecessor. | **Proposed sufficient structurally:** a finite, acyclic successor chain with a common series ID. Semantic continuity remains unresolved. |
| `LCMRP-TAX-ENT-005@0.1` | **Claim** — informational entity | Proposition-like content that can be assessed for support, challenge, temporal validity, or incompatibility. A claim is distinct from the object that carries or refers to it. | **Proposed necessary:** an identity, interpretable assertion, and declared context or an explicit unknown context. | **Unknown:** not all memory content is propositional. |
| `LCMRP-TAX-ENT-006@0.1` | **Actor** — governance entity | An accountable person, system, organization, or external source that can be attributed an operation, assertion, request, grant, or obligation. Actor identity does not confer authority. | **Proposed necessary:** stable identity within an authority domain and declared actor type. | **Unknown:** group, delegated, and composite agency may require richer structures. |
| `LCMRP-TAX-ENT-007@0.1` | **Policy statement** — governance entity | A versioned, scoped rule that permits, denies, requires, or constrains an operation over identified objects, actors, purposes, or times. | **Proposed necessary:** rule effect, scope, authority source, version, and effective interval. | **Unknown:** policy conflicts and jurisdictional validity are not settled here. |
| `LCMRP-TAX-ENT-008@0.1` | **Provenance assertion** — informational entity | A claim that a named entity, activity, and actor participated in a source, derivation, transformation, or custody relationship at a stated time. It may itself be incomplete, mistaken, or forged. | **Proposed necessary:** assertion identity, relation type, endpoints, asserter, and time or explicit time uncertainty. | **Proposed sufficient syntactically:** those fields form an assertion; they do not make it authentic. |

### Functional-role candidates

These terms name possible roles. Whether roles should instead be stable object kinds is the central disagreement between the competing organizations below.

| Candidate ID | Term and kind | Bounded candidate definition | Necessary-condition status | Sufficient-condition status |
| --- | --- | --- | --- | --- |
| `LCMRP-TAX-ROL-001@0.1` | **Episodic role** — functional role | Use of an object to reconstruct or reason about a particular occurrence as situated by time, sequence, participants, or context. | **Proposed necessary:** reference to at least one particular source event and at least one contextual locator. | **Unknown:** event reference may be present without episodic use. |
| `LCMRP-TAX-ROL-002@0.1` | **Semantic role** — functional role | Use of an object as a general claim whose immediate task does not require reconstructing one particular source event, while its provenance remains separately traceable. | **Proposed necessary:** claim-like content and event-independent use in the current task. | **Unknown:** “general” and “event-independent” may be observer- or query-relative. |
| `LCMRP-TAX-ROL-003@0.1` | **Procedural role** — functional role | Use of an object to constrain how an action or decision is performed, such as an ordered procedure, conditional rule, or policy over steps. | **Proposed necessary:** an action class plus at least one ordering, condition, or selection constraint. | **Unknown:** a descriptive account of a procedure need not control action. |
| `LCMRP-TAX-ROL-004@0.1` | **Prospective role** — functional role | Use of an object to monitor a not-yet-satisfied condition or time and associate it with a future action, review, or obligation. | **Proposed necessary:** a future or unresolved trigger, an intended response, and completion state. | **Proposed sufficient within a task:** those conditions when the object participates in trigger monitoring. |
| `LCMRP-TAX-ROL-005@0.1` | **Working role** — functional role | Use of an object within a bounded active task context with explicit expiration, eviction, or handoff conditions. Persistence beyond the task is not required. | **Proposed necessary:** active task scope and an exit condition. | **Unknown:** high accessibility alone is not enough, and durable objects may temporarily play this role. |

### Lifecycle and transformation candidates

| Candidate ID | Term and kind | Bounded candidate definition | Necessary-condition status | Sufficient-condition status |
| --- | --- | --- | --- | --- |
| `LCMRP-TAX-OPS-001@0.1` | **Encoding** — process | A transformation from a source event or external representation into a memory candidate with explicit lineage. Encoding does not decide admission or truth. | **Proposed necessary:** source input, transformation identity, candidate output, and lineage assertion. | **Proposed sufficient structurally:** those features distinguish encoding from untracked copying; cognitive adequacy is unknown. |
| `LCMRP-TAX-OPS-002@0.1` | **Admission** — governed process | A policy-mediated decision to accept or reject a memory candidate for the governed memory population. | **Proposed necessary:** candidate, decision actor, applicable policy basis, decision time, and recorded outcome. | **Proposed sufficient structurally:** an authorized accept decision produces admitted status; usefulness is not implied. |
| `LCMRP-TAX-OPS-003@0.1` | **Retrieval** — process | Selection and exposure of zero or more eligible object versions in response to a query, task, actor, and time context. Retrieval does not imply relevance, truth, use, or successful recall. | **Proposed necessary:** request context, eligibility evaluation, and recorded zero-or-more result set. | **Unknown:** unsolicited activation and cached context challenge request-based sufficiency. |
| `LCMRP-TAX-OPS-004@0.1` | **Update** — process | Creation of a successor version that changes content, metadata, policy attachment, or epistemic assessment while preserving explicit predecessor lineage. | **Proposed necessary:** predecessor, successor, change description, authority, and transaction time. | **Proposed sufficient structurally:** those conditions; semantic continuity is unresolved. |
| `LCMRP-TAX-OPS-005@0.1` | **Consolidation** — process | Creation of a derived candidate or object from two or more inputs to reduce fragmentation or create a joint representation, with every contributing input retained in lineage. | **Proposed necessary:** at least two identified inputs, declared transformation, derived output, and contributor lineage. | **Unknown:** aggregation without information reduction may or may not count. |
| `LCMRP-TAX-OPS-006@0.1` | **Abstraction** — process | Creation of a derived representation that intentionally omits identified particulars to express a broader pattern, rule, or claim. | **Proposed necessary:** source representation, declared omitted particulars or abstraction rule, output, and lineage. | **Unknown:** compression and generalization may be observationally indistinguishable without declared intent. |
| `LCMRP-TAX-OPS-007@0.1` | **Reconsolidation** — process | Creation of a successor or derived version causally linked to prior retrieval or reactivation and new context. It is not in-place mutation. | **Proposed necessary:** prior object, recorded retrieval/reactivation, new context, changed output, and lineage to both. | **Unknown:** without causal evidence it collapses into update or consolidation. |
| `LCMRP-TAX-OPS-008@0.1` | **Deduplication** — process | Identification of exact or policy-relevant equivalence among candidates or objects and a recorded decision about retaining, linking, or suppressing them. It does not by itself merge or delete content. | **Proposed necessary:** comparison basis, equivalence criterion, compared identities, outcome, and disposition. | **Unknown:** approximate equivalence is task-dependent. |
| `LCMRP-TAX-OPS-009@0.1` | **Decay** — process/effect | A time- or use-conditioned change in accessibility, priority, confidence, or retention eligibility without necessarily changing asserted content. | **Proposed necessary:** prior value, later value, elapsed-time or use relation, and declared decay rule. | **Unknown:** an observed decrease may be policy change rather than decay. |
| `LCMRP-TAX-OPS-010@0.1` | **Forgetting** — governed process/effect | A reduction in an object's ordinary availability or influence under a declared policy and scope. Content may still exist and may remain recoverable. | **Proposed necessary:** target, prior and resulting availability conditions, scope, authority, and reason. | **Unknown:** forgetting may be an outcome composed from decay, suppression, archival, or deletion. |
| `LCMRP-TAX-OPS-011@0.1` | **Archival** — governed process | Retention of an object under a lower-default-access or differently controlled state, with a declared recovery path and policy. | **Proposed necessary:** retained target, archive state, access rule, recovery condition, authority, and time. | **Proposed sufficient structurally:** those conditions distinguish archival from deletion; operational durability is untested. |
| `LCMRP-TAX-OPS-012@0.1` | **Deletion** — governed process and scoped outcome | An authorized operation whose successful outcome makes content of every target in a declared deletion scope unavailable and non-reconstructable through governed interfaces, subject to explicitly recorded exceptions. | **Proposed necessary:** request, authority, target closure, exceptions, operation record, and verification outcome. | **Unknown:** completeness is not establishable when derivatives or external copies are unknown. |
| `LCMRP-TAX-OPS-013@0.1` | **Conflict detection** — analysis process | Identification of claims that cannot jointly hold under the same interpretation, validity interval, and context. Detection records the incompatibility but does not revise either claim. | **Proposed necessary:** at least two claims, shared comparison context, incompatibility rule, and result. | **Unknown:** semantic conflict may be undecidable or interpretation-dependent. |

### Epistemic and governance candidates

| Candidate ID | Term and kind | Bounded candidate definition | Necessary-condition status | Sufficient-condition status |
| --- | --- | --- | --- | --- |
| `LCMRP-TAX-EPI-001@0.1` | **Confidence assessment** — contextual assessment | An actor- or method-attributed assessment of support for a specified claim, source, classification, or operation outcome, expressed on a declared scale at a declared time. It is not truth or calibrated probability unless separately demonstrated. | **Proposed necessary:** target, assessor, scale, value or interval, context, method, and time. | **Proposed sufficient as an assessment record:** those fields; epistemic quality is unknown. |
| `LCMRP-TAX-EPI-002@0.1` | **Uncertainty description** — contextual assessment | An explicit representation of unresolved alternatives, missing information, ambiguity, variability, model limits, or imprecision concerning a target. | **Proposed necessary:** target, uncertainty kind, scope, and assessor or method. | **Unknown:** no single numeric form captures every listed uncertainty kind. |
| `LCMRP-TAX-EPI-003@0.1` | **Claim conflict** — contextual relation | A symmetric incompatibility relation between claims under a specified interpretation, context, and overlapping validity interval. | **Proposed necessary:** claim identities, context, temporal overlap, and incompatibility basis. | **Unknown:** formal contradiction is sufficient only when the representation semantics are complete enough. |
| `LCMRP-TAX-GOV-001@0.1` | **Authority grant** — governance relation | A scoped basis permitting an actor to attempt a named operation for a target, purpose, and interval. It is not a statement of trust, ownership, correctness, or unrestricted control. | **Proposed necessary:** grantor basis, grantee, operation, target scope, purpose or explicit absence, effective interval, and revocation rule. | **Unknown:** conflicting law, policy, delegation, and data-subject interests may defeat a grant. |
| `LCMRP-TAX-GOV-002@0.1` | **Provenance trace** — derived informational structure | A connected set of provenance assertions linking an object version to source entities, transformations, actors, and predecessor versions. Completeness and authenticity are separate assessments. | **Proposed necessary:** at least one source or predecessor path plus attributed transformation steps. | **Unknown:** a connected trace may omit material contributors or contain forged assertions. |
| `LCMRP-TAX-GOV-003@0.1` | **Deletion scope** — governance structure | The declared closure of versions, derivatives, replicas, caches, indexes, backups, reconstructions, and audit residues targeted by a deletion request, including explicit exclusions and retention exceptions. | **Proposed necessary:** root target, closure rule, system boundary, exceptions, and verification rule. | **Unknown:** no finite declaration guarantees discovery of unknown or external copies. |
| `LCMRP-TAX-GOV-004@0.1` | **Retention obligation** — governance constraint | A scoped rule requiring identified content or audit information to remain available until a condition or time, with its authority basis recorded. | **Proposed necessary:** target, authority basis, required duration or condition, and permitted access scope. | **Unknown:** competing deletion rights and jurisdictions require adjudication outside this taxonomy. |

## Orthogonal classification axes

No axis is asserted to be primary. Except where a candidate definition states otherwise, an item can take multiple values on an axis, and values may vary by actor, query, purpose, or time.

| Axis | Candidate values or questions | Why it is not reducible to another axis |
| --- | --- | --- |
| **A1 — Representational kind** | event trace, claim, procedure-like constraint, policy, provenance assertion, composite, opaque content | What content is represented does not determine why or when it is used. |
| **A2 — Functional role** | episodic, semantic, procedural, prospective, working, none declared, multiple | The same representation may play different roles for different tasks. |
| **A3 — Temporal orientation** | retrospective, presently active, prospective, atemporal/unknown; event time, validity time, transaction time | A future-oriented claim can be archived; a past event can be in working context. |
| **A4 — Lifecycle state** | candidate, rejected, admitted/active, superseded, archived, deletion pending, deleted | State does not reveal content kind, truth, or role. |
| **A5 — Epistemic posture** | asserted, supported, challenged, unresolved, conflicted, withdrawn; confidence and uncertainty separately scoped | Governance acceptance and high availability do not establish support. |
| **A6 — Provenance condition** | source-linked, derived, consolidated, provenance incomplete, provenance disputed, provenance unavailable | Detailed lineage does not imply authenticity or authority. |
| **A7 — Authority relation** | permitted, denied, obligated, contested, expired, unknown for a named actor/operation/purpose | Authority is operation- and context-specific, not an intrinsic object property. |
| **A8 — Availability and persistence** | active, suppressed, low-priority, archived, externally retained, deletion pending, inaccessible, verified within scope | Availability can change without changing the claim or role. |
| **A9 — Derivation form** | direct encoding, successor update, consolidation, abstraction, reconsolidation, imported copy, unknown | Derivation describes lineage, not semantic quality. |
| **A10 — Sensitivity and handling** | public, restricted, sensitive, disputed, unknown under a declared policy vocabulary | Sensitivity affects handling but does not determine memory function. |

**Constructed cross-axis case:** an uncertain, source-linked appointment claim could play a prospective role for one task, an episodic role after the event, remain active, and be subject to a user-scoped deletion obligation. No one axis determines the other values. This example illustrates the proposed independence; it does not demonstrate it.

## Competing primary organizations

The taxonomy intentionally retains two incompatible ways to make functional categories primary. They share term definitions so their different commitments can be tested rather than hidden by vocabulary changes.

### Organization K — Stable kind-first partition

**Candidate rule:** Every admitted memory series receives exactly one primary functional kind—`EPISODIC`, `SEMANTIC`, `PROCEDURAL`, or `PROSPECTIVE`—at admission. The primary kind remains stable for the series. `WORKING` is an availability tier rather than a primary kind. Mixed inputs must be split into distinct series or assigned one declared primary kind with secondary annotations.

**Commitments that could fail:**

- Primary kind is an intrinsic, series-stable classification rather than a query-relative relation.
- Each series has exactly one primary kind.
- A role change that crosses primary kinds requires a new series or a separately admitted derivative.
- Stable partitions improve definition clarity enough to justify forced splits and primary-kind adjudication.

**Predicted difficult cases:** a reminder after its trigger occurs, a recipe recalled as a learning episode, a personal event generalized into a claim, and a durable object temporarily used in active task context.

### Organization R — Contextual role-first relation

**Candidate rule:** Functional categories are not intrinsic object kinds. A role is a relation among object version, query or task, actor, purpose, and time. One object may play zero, one, or several roles, and its roles may change without creating a new object version. Representational kind and lifecycle state remain separate axes.

**Commitments that could fail:**

- Role membership is contextual and many-valued rather than series-stable.
- A change in use alone does not create a new memory identity or version.
- Classification must record the context tuple needed to reproduce the role assignment.
- Contextual flexibility improves boundary handling enough to justify weaker global partitions.

**Predicted difficult cases:** determining when two contexts are equivalent, comparing studies that omit task context, deciding when a functional change is actually a content update, and producing aggregate counts without arbitrary context sampling.

### Why the organizations genuinely compete

| Shared constructed case | Organization K commitment | Organization R commitment | Incompatibility to evaluate |
| --- | --- | --- | --- |
| “Call the clinic at 09:00”; after the call, a later query asks what happened. | Prospective series must remain prospective; episodic use requires a new or derived episodic series. | One object may first play prospective and later episodic roles without a version change if content is unchanged. | Whether role change alone requires identity multiplication. |
| A recipe includes steps and the story of where it was learned. | Assign one primary kind or split procedural and episodic series. | Retain one composite object and classify each use context. | Whether every admitted series must have one primary function. |
| “The office closes at 17:00,” learned during a visit; a query asks where that belief came from. | The primary semantic series remains semantic; source episode is separate provenance or series. | The same object can play semantic and episodic roles in different queries. | Whether source-sensitive recall changes functional membership. |
| A durable policy is loaded into a short task context. | Primary procedural kind plus non-kind working tier. | Procedural and working are simultaneous contextual roles. | Whether working memory is a tier or a role comparable to the others. |

If later evaluation finds no case for which the organizations require different identity, cardinality, or classification outcomes, M1-O2 must be rejected and the organizations collapsed or reformulated.

## Necessary and sufficient condition discipline

The register uses three statuses:

- **Proposed:** the condition is a falsifiable commitment of this version.
- **Unknown:** this version makes no adequacy claim and requires counterexamples or further definition.
- **Structurally sufficient within this artifact:** the condition is enough only to classify a record under this candidate vocabulary; it is not sufficient for external validity, usefulness, safety, or biological similarity.

No candidate functional role has both general necessary and sufficient conditions in v0.1. That absence is deliberate. A later study must not convert a convenient benchmark rule into a general definition without versioned scope and counterexample analysis.

## Observable distinctions

These are proposed observations for later preregistration, not completed tests. An observation distinguishes two record descriptions under stated conditions; it does not prove that the corresponding natural category exists.

| Candidate distinction | Controlled observation or record inspection | Result that would challenge the distinction |
| --- | --- | --- |
| Encoding vs. admission | Hold one encoded candidate constant and vary the recorded admission decision and authority basis. | The system description cannot represent an encoded-but-rejected candidate. |
| Admission vs. truth assessment | Admit a claim while recording epistemic status as unresolved or challenged. | Admission structurally forces the claim to supported or true. |
| Retrieval vs. use | Record a returned set and a separately observed set of objects actually used in a task. | The model defines every returned item as used or successful recall. |
| Retrieval vs. relevance | Include an eligible but irrelevant object in a constructed result set. | Retrieval entails relevance by definition. |
| Update vs. in-place mutation | Inspect whether predecessor bytes and identity remain referencable after change. | The predecessor silently changes or disappears. |
| Consolidation vs. abstraction | Compare a multi-input joint representation that retains particulars with one declaring omitted particulars. | No observable or declared omission criterion separates them. |
| Update vs. reconsolidation | Compare equal content changes with and without a recorded causal retrieval/reactivation event. | Reconsolidation classification ignores the causal record. |
| Deduplication vs. deletion | Mark two objects equivalent while retaining both and recording no deletion. | Equivalence automatically destroys an object. |
| Decay vs. policy change | Hold elapsed time constant while changing policy, then hold policy constant while applying the declared decay rule. | Both produce indistinguishable records with no causal attribution. |
| Forgetting vs. archival | Test ordinary availability and the separately declared recovery route. | Forgetting always supplies an archive recovery path or archival always reduces influence identically. |
| Forgetting vs. deletion | Attempt an authorized recovery within the declared scope. | “Forgotten” content is defined as destroyed, or “deleted” content remains ordinarily recoverable. |
| Archival vs. deletion | Inspect retained payload and recovery policy after transition. | Archived payload is absent, or deleted payload remains within governed recovery. |
| Confidence vs. correctness | Construct a high-confidence false claim and a low-confidence true claim. | The vocabulary prohibits either structure. |
| Uncertainty vs. low confidence | Represent precise low support separately from a wide unresolved range or competing alternatives. | Both must collapse to one scalar. |
| Provenance vs. authenticity | Construct a complete-looking trace containing a forged assertion. | Trace completeness entails authenticity. |
| Conflict vs. temporal succession | Compare incompatible claims with overlapping and non-overlapping validity intervals. | Non-overlapping claims are always classified as conflict. |
| Authority vs. actor identity | Hold actor constant and vary operation, purpose, target, and effective interval. | Actor type alone grants every operation. |
| Prospective vs. procedural role | Compare a future trigger-response obligation with an atemporal action sequence having no unresolved trigger. | Every conditional procedure becomes prospective. |
| Episodic vs. semantic role | Ask first for a general answer, then for reconstruction of the particular learning event using the same content. | The selected organization cannot state whether context changes the classification. |
| Working role vs. persistence | Compare one durable object temporarily used in a task with one task-local object subject to expiry. | Working classification is defined only by storage duration. |

## Counterexamples and edge cases

| Edge case | Candidate terms stressed | Required treatment in later evaluation |
| --- | --- | --- |
| A source truthfully reports that it is lying. | source event, claim, provenance, confidence | Separate event receipt, claim semantics, source assessment, and paradox handling. |
| Two claims differ only because one was valid last year and one is valid now. | conflict, validity time, update | Do not infer conflict without temporal overlap. |
| A reminder is completed but retained to explain a later decision. | prospective and episodic roles, archival | Test stable-kind splitting against contextual role change. |
| A procedure is quoted as a historical fact but never used to act. | procedural role, semantic role | Distinguish procedural-shaped content from procedural use. |
| A source event contains a general rule and detailed episode in one indivisible signed document. | kind-first partition, composite content | Preserve the forced-split cost and signature/provenance implications. |
| Two byte-identical claims have different sources, consent, or deletion obligations. | deduplication, provenance, authority, deletion scope | Equivalence must not erase governance differences. |
| Two differently worded claims are semantically equivalent only for one task. | deduplication, abstraction, semantic role | Record the task-scoped equivalence rule rather than global identity. |
| A high-confidence object comes from a forged but internally consistent provenance chain. | confidence, provenance authenticity | Keep structural trace, authenticity, and claim support separate. |
| A user requests deletion while an independently authorized retention rule applies. | authority, deletion, retention obligation | Record conflict, scope, authority bases, and unresolved disposition; do not silently pick a winner. |
| A deletion succeeds in an active index but a derivative summary and backup remain. | deletion scope, consolidation, deletion failure | Classify the operation as incomplete within any scope containing those copies. |
| A tombstone reveals that a sensitive event occurred. | deletion, provenance, audit residue | Treat metadata leakage and minimum audit content as an open obligation. |
| An object is archived but a privileged actor retrieves it routinely. | archival, availability, authority | Evaluate “lower-default-access” relative to actor and purpose. |
| A retrieval returns no object because policy denies access, not because no object exists. | retrieval, authority, uncertainty | Preserve non-disclosure and distinguish absence from denied or unknown where policy permits. |
| A reconsolidation incorporates malicious query context into a trusted object. | reconsolidation, poisoning, provenance | Require separate lineage and authority; do not inherit trust automatically. |
| An object is deleted and identical content later arrives from an independent source. | deletion, identity, admission | Use a new identity and provenance; do not call it resurrection of the deleted version. |
| A group preference conflicts with one member's current preference. | actor, authority, claim conflict, time | Avoid treating identity continuity or group aggregation as already solved. |

## Authority, provenance, deletion, confidence, and uncertainty

### Authority

Authority is proposed as a relation over actor, operation, target, purpose, time, and policy basis. It is not a global actor ranking. Originating content, being described by content, operating infrastructure, supplying a model, and requesting an action are distinct relations and do not automatically imply one another's permissions.

Open authority conflicts include grant versus later revocation, deletion request versus retention obligation, individual versus group control, delegated versus original authority, emergency override, and incompatible jurisdictions. This taxonomy records such conflicts; it does not resolve them.

### Provenance

Provenance assertions are themselves claims requiring identity, attribution, protection, and possible challenge. A trace can be structurally connected yet incomplete or forged. Consolidation, abstraction, update, and reconsolidation must add derivation assertions rather than replace source history. Whether cryptographic, institutional, or observational evidence authenticates those assertions is outside this candidate taxonomy.

### Deletion

Deletion is always scoped. A success statement must identify the governed boundary, derivative-closure rule, replicas and backups considered, permitted audit residue, external copies excluded, verification method, and exceptions. Index removal, retrieval suppression, archival, expiry, and ordinary forgetting are not sufficient deletion outcomes under this definition.

The candidate definition may prove too strong when reconstruction cannot be bounded or external actors retain lawful copies. Such cases should narrow the declared scope or produce an incomplete/failed disposition, not a universal deletion claim.

### Confidence and uncertainty

Confidence requires an assessor, target, context, method, scale, and time. Confidence in source authenticity, classification, claim support, retrieval relevance, or deletion verification are different assessments and must not be combined silently.

Uncertainty can concern missing facts, alternative interpretations, measurement variability, model limits, identity resolution, temporal bounds, provenance completeness, or policy applicability. A single confidence score is not presumed to encode all these forms. High confidence and high residual uncertainty can coexist when they target different questions.

## Biological analogy limits

The labels episodic, semantic, procedural, prospective, working, consolidation, reconsolidation, decay, and forgetting are research vocabulary candidates. Their use here asserts no shared substrate, causal process, capacity limit, subjective experience, neural organization, developmental pathway, or behavioral equivalence with biological memory.

In particular:

- a database or model state is not an autobiographical episode merely because it has a timestamp;
- generated text about an action is not a learned motor skill;
- a context window is not presumed equivalent to biological working memory;
- batch summarization is not presumed equivalent to biological consolidation;
- rewriting a record after retrieval is not sufficient to establish reconsolidation;
- time-based expiry is not presumed to model biological decay; and
- deletion or access suppression is not presumed equivalent to human forgetting.

Biological literature may later motivate hypotheses or counterexamples, but any transfer requires explicit mapping assumptions and tests. Analogy cannot supply a missing operational definition or validity result.

## Candidate competency questions

A future structural study should determine whether the exact taxonomy version can answer, at minimum:

1. Can one representation play episodic and semantic roles at different times without changing content?
2. What record distinguishes encoding from admission and rejection?
3. Can a retrieved object remain unused, irrelevant, false, or policy-ineligible for another actor?
4. When does a changed representation count as update, abstraction, consolidation, or reconsolidation?
5. Can byte-identical objects remain distinct because provenance or governance differs?
6. Can two claims disagree without conflicting because their validity intervals do not overlap?
7. What must be recorded before a confidence value is interpretable?
8. Can uncertainty be represented without forcing it into one scalar?
9. Which actor is authorized for one operation, target, purpose, and time, and what happens when authorities conflict?
10. What exact closure and exceptions are covered by a deletion-success claim?
11. Does a complete-looking provenance trace remain challengeable as forged or incomplete?
12. Which constructed cases force Organization K and Organization R to different identity or cardinality decisions?

Answerability is only a structural property. It does not establish that an answer is correct or useful.

## Rejection conditions for this candidate

Reject or supersede all or part of v0.1 if a governed analysis shows any of the following:

- a term cannot be distinguished even in principle from every adjacent term it claims to differ from;
- a necessary condition excludes a declared positive case without a justified scope change;
- a proposed sufficient condition admits a declared negative case;
- the functional organizations do not make genuinely different commitments;
- one axis logically determines another despite the claimed orthogonality;
- a category depends on a storage, model, vendor, application, or product assumption represented as general;
- provenance structure entails provenance authenticity, or confidence entails correctness;
- admission or retrieval entails truth, relevance, consent, or authority;
- forgetting, archival, and deletion cannot represent their declared differences;
- deletion can be reported successful without scope and verification;
- authority collapses to actor identity or an unrestricted global ranking;
- the vocabulary requires a biological equivalence claim; or
- ambiguous, negative, null, or contradictory cases cannot be retained without forced classification.

## Companion formal-model crosswalk

This Layer 1 crosswalk compares each v0.1 candidate taxonomy term to the companion [FMO-0.1 candidate formal model](FORMAL_MEMORY_OBJECT_MODEL_v0.1.md). It is a structural analysis aid only. A `direct` entry records an apparent named counterpart in FMO-0.1; a `partial` entry records overlap with unresolved definition or coverage obligations; an `absent` entry records no explicit counterpart identified in FMO-0.1; and a `conflict` entry would record an apparent incompatibility requiring versioned resolution. `partial`, `absent`, and `conflict` entries are analysis inputs, not automatic overrides, validation outcomes, evidence-state changes, or adoption decisions.

| Taxonomy term ID | Natural-language term | FMO-0.1 symbol/relation/state/operation | Mapping status | Open obligation |
| --- | --- | --- | --- | --- |
| `LCMRP-TAX-ENT-001@0.1` | Source event | `E`; `event`; `sourceOf` | direct | Test whether static sources need a separate formal type. |
| `LCMRP-TAX-ENT-002@0.1` | Memory candidate | `N`; `candidate`; `candidateState` with `PENDING`, `REJECTED`, `ADMITTED` | direct | Verify that candidate identity and undecided admission state cover all proposed positive cases. |
| `LCMRP-TAX-ENT-003@0.1` | Memory object version | `O`; `object`; `objectState`; `contentID`; `provenance` relations | direct | Determine whether these structures distinguish memory objects from ordinary governed records. |
| `LCMRP-TAX-ENT-004@0.1` | Memory series | `S`; `seriesOf`; `predecessor`; `supersedes` | direct | Define semantic continuity beyond structural successor chains. |
| `LCMRP-TAX-ENT-005@0.1` | Claim | `K`; `asserts`; `about`; `validDuring`; `assessment` | direct | Bound claim interpretation for non-propositional or mixed content. |
| `LCMRP-TAX-ENT-006@0.1` | Actor | `A`; `actorRole`; `attributedTo`; `authz` actor parameter | direct | Model group, delegated, composite, and unresolved agency without collapsing identity into authority. |
| `LCMRP-TAX-ENT-007@0.1` | Policy statement | `P`; `governs`; `policyEffect`; `policyDomain`; `effectiveFor`; `issuedBy` | direct | Define conflict handling, jurisdiction, and validity semantics. |
| `LCMRP-TAX-ENT-008@0.1` | Provenance assertion | `PT`; `prov`; provenance relation kinds | direct | Define authenticity evidence separately from structural provenance. |
| `LCMRP-TAX-ROL-001@0.1` | Episodic role | `FR=EPISODIC`; `playsRole`; optional `primaryKind` extension | partial | Formalize necessary and sufficient role conditions without biological equivalence assumptions. |
| `LCMRP-TAX-ROL-002@0.1` | Semantic role | `FR=SEMANTIC`; `playsRole`; optional `primaryKind` extension | partial | Define event-independent use and observer/query relativity. |
| `LCMRP-TAX-ROL-003@0.1` | Procedural role | `FR=PROCEDURAL`; `playsRole`; optional `primaryKind` extension | partial | Distinguish procedure-shaped content from action-controlling use. |
| `LCMRP-TAX-ROL-004@0.1` | Prospective role | `FR=PROSPECTIVE`; `playsRole`; optional `primaryKind` extension | partial | Decide whether autonomous monitoring is required or query-time matching can suffice. |
| `LCMRP-TAX-ROL-005@0.1` | Working role | `FR=WORKING`; `playsRole` | partial | Determine whether working status is a role, resource limit, access tier, temporal scope, or process state. |
| `LCMRP-TAX-OPS-001@0.1` | Encoding | `encode`; `WAS_ENCODED_FROM`; `candidate` output | direct | Test whether untracked copying and encoding remain distinguishable. |
| `LCMRP-TAX-OPS-002@0.1` | Admission | `admit`; `CandidateState=ADMITTED`; `ObjectState=ACTIVE`; `WAS_ADMITTED_FROM` | direct | Verify separation of acceptance, belief, truth, and usefulness. |
| `LCMRP-TAX-OPS-003@0.1` | Retrieval | `retrieve`; `accessible`; `WAS_RETRIEVED_IN` | direct | Address unsolicited activation, cached context, and non-disclosure cases. |
| `LCMRP-TAX-OPS-004@0.1` | Update | `update`; `WAS_UPDATED_FROM`; `predecessor`; `supersedes` | direct | Define when a changed version preserves series continuity. |
| `LCMRP-TAX-OPS-005@0.1` | Consolidation | `consolidate`; `WAS_CONSOLIDATED_FROM`; `usedInput` | direct | Distinguish consolidation from aggregation without assuming improvement. |
| `LCMRP-TAX-OPS-006@0.1` | Abstraction | `abstract`; `WAS_ABSTRACTED_FROM`; abstraction rule in operation inputs | direct | Distinguish abstraction from compression or undeclared omission. |
| `LCMRP-TAX-OPS-007@0.1` | Reconsolidation | `reconsolidate`; `WAS_RECONSOLIDATED_FROM`; retrieval/reactivation precondition | direct | State the causal evidence needed beyond update after retrieval. |
| `LCMRP-TAX-OPS-008@0.1` | Deduplication | `deduplicate`; equivalence assessment operation | direct | Define task-scoped equivalence without erasing governance differences. |
| `LCMRP-TAX-OPS-009@0.1` | Decay | No dedicated operation; represented only through changed accessibility, priority, confidence, or retention-related values when declared | partial | Decide whether decay is a mechanism, policy, observed effect, or family of processes. |
| `LCMRP-TAX-OPS-010@0.1` | Forgetting | `forget`; `ObjectState=SUPPRESSED`; `accessible` changes | direct | Define ordinary availability independently of a retrieval mechanism. |
| `LCMRP-TAX-OPS-011@0.1` | Archival | `archive`; `restore`; `ObjectState=ARCHIVED` | direct | Specify lower-default-access and recovery conditions relative to actors and purposes. |
| `LCMRP-TAX-OPS-012@0.1` | Deletion | `requestDelete`; `executeDelete`; `DS`; `DeletionResult`; `DeletionSuccess`; `ObjectState=DELETE_PENDING/DELETED` | direct | Formalize closure, verification, external copies, and audit residue leakage. |
| `LCMRP-TAX-OPS-013@0.1` | Conflict detection | `detectConflict`; `conflicts`; `CX` | direct | Bound interpretation semantics and decidability. |
| `LCMRP-TAX-EPI-001@0.1` | Confidence assessment | `CA`; `confidence`; `numericValue` optional projection | direct | Define scale compatibility, calibration claims, and aggregation rules. |
| `LCMRP-TAX-EPI-002@0.1` | Uncertainty description | `UA`; `uncertainty`; candidate uncertainty kinds | direct | Determine which uncertainty kinds are comparable or must remain separate. |
| `LCMRP-TAX-EPI-003@0.1` | Claim conflict | `conflicts`; `detectConflict`; `validDuring`; `CX` | direct | Distinguish contradiction, ambiguity, temporal succession, and unknown compatibility. |
| `LCMRP-TAX-GOV-001@0.1` | Authority grant | `authz`; `AuthzDecision`; `actorRole`; `governs`; `policyEffect` | partial | Add a policy calculus for grants, denials, obligations, delegation, revocation, and jurisdiction. |
| `LCMRP-TAX-GOV-002@0.1` | Provenance trace | `trace(x)`; `prov`; `sourceOf`; `derivedFrom`; `generatedBy`; `usedInput`; `attributedTo` | direct | Specify completeness criteria and forgery assessment. |
| `LCMRP-TAX-GOV-003@0.1` | Deletion scope | `DS`; `scope`; `Targets`; `DeletionSuccess` | direct | Establish when closure is finite, discoverable, and stable. |
| `LCMRP-TAX-GOV-004@0.1` | Retention obligation | `P` with `policyEffect=REQUIRE`; `governs`; `authz=UNRESOLVED` for contested operations | partial | Formalize retention duties and adjudication against deletion requests. |

## Unresolved questions and obligations

- Is “memory object” distinguishable from a governed information record by structural conditions alone?
- Should functional categories be kinds, roles, capabilities, task-relative observations, or some combination?
- Is working memory best represented as a role, resource limit, access tier, temporal scope, or process state?
- What makes a series successor semantically continuous rather than merely sharing an identifier?
- Can episodic context be operationalized without assuming a human-like self or experience?
- When is a procedure representation causally controlling action rather than merely descriptive?
- Does prospective memory require autonomous monitoring, or is later query-time matching enough?
- Can consolidation be distinguished from aggregation without a measurable information-loss or integration criterion?
- Can abstraction be distinguished from compression using only artifacts and declared intent?
- What causal evidence is sufficient to distinguish reconsolidation from ordinary update?
- What equivalence relation is safe for deduplication when provenance and deletion duties differ?
- Is decay a mechanism, a policy, an observed effect, or a family of unrelated processes?
- Can ordinary forgetting be defined independently of a particular retrieval mechanism?
- What constitutes non-reconstructability, and under which adversary and system boundary?
- How should audit tombstones balance deletion verification against metadata leakage?
- How are conflicting authorities compared without assuming one universal legal or moral ordering?
- How should confidence assessments from different actors, scales, or targets be compared?
- Which uncertainty types require intervals, sets of alternatives, distributions, or qualitative descriptions?
- What representation semantics make conflict detection decidable for a bounded study?
- What source collection and coverage rule could test the taxonomy without circularly favoring it?
- Which observations would justify retaining one competing organization, both, or neither?

## Known limitations

- No candidate term has been evaluated through a frozen foundational study.
- No claim of inter-rater reliability, external coverage, biological validity, or implementation usefulness is made.
- The examples were constructed to stress boundaries and may omit important domains or cultures.
- Natural-language definitions remain vulnerable to interpretation differences.
- The candidate taxonomy has no accepted measurement scale for salience, importance, relevance, interference, or identity continuity.
- Governance concepts may require jurisdiction- and community-specific extensions that this product-independent artifact does not model.
- No human-subject, controlled empirical, computational, or evidence-synthesis work is authorized by this artifact.
- The relationship between this vocabulary and the companion formal model remains a candidate mapping with open proof obligations.

## Recommended next falsification step

Create a frozen structural/taxonomy protocol that compares Organizations K and R against a preregistered, versioned set of positive, negative, ambiguous, and adversarial constructed cases. Require term-by-term necessary-condition and negative-case checks, an explicit coverage rule, independent adjudication, and atomic reporting of every retained, narrowed, superseded, rejected, null, or invalid outcome.

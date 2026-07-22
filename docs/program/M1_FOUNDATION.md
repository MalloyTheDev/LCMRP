# M1 — Candidate Memory Taxonomy and Formal Object Model

## Status

**Milestone state:** In progress — two frozen v1 studies blocked at execution preflight; neither study executed  
Applicable layer: Layer 1 — Foundational Research  
**Mechanism evidence label:** Not applicable  
**Scientific findings asserted:** None  
**Version:** 0.1-execution-readiness  
**Launch date:** 2026-07-21

M1 begins the governed investigation of a product-independent vocabulary and formal object model for lifelong machine memory. This document authorizes candidate-definition, structural-evaluation, and formal-analysis work only. It does not adopt a taxonomy, establish that the formal model is sound, validate a memory mechanism, or authorize an implementation.

M1 is governed by the [Program Charter v0.1](PROGRAM_CHARTER_v0.1.md) and the [Foundational Study Contract v0.1](FOUNDATIONAL_STUDY_CONTRACT.md). The accepted [M0 Foundation](M0_FOUNDATION.md) supplies the record and review contracts; it does not supply evidence for any M1 claim.

## Research question

Can a versioned, product-independent set of candidate definitions and a corresponding formal object model distinguish memory objects, functional roles, lifecycle operations, epistemic properties, and authority boundaries well enough to support falsifiable later studies without embedding a storage architecture, model provider, application schema, or biological equivalence claim?

## Mission

M1 will produce a launch-quality candidate vocabulary and formal system that make disagreements inspectable. The work should expose, rather than prematurely resolve:

- competing ways to organize memory categories;
- necessary and sufficient conditions that remain unknown;
- observable distinctions and counterexamples;
- authority, provenance, confidence, uncertainty, conflict, and deletion semantics;
- intended entailments and explicit non-entailments; and
- proof, evaluation, security, and governance obligations that remain open.

The milestone succeeds only if later governed analyses can reject or revise its candidates. Editorial consistency or schema conformance alone is not success.

## Launch artifacts

| Artifact | Purpose | Launch status | What the artifact cannot establish |
| --- | --- | --- | --- |
| [Candidate Memory Taxonomy v0.1](../taxonomy/MEMORY_TAXONOMY_v0.1.md) | Define versioned candidate terms, orthogonal axes, competing organizations, observable distinctions, and boundary cases. | Exact bytes registered as `LCMRP-FSUBJ-0001-MEMORY-TAXONOMY` v1; still a candidate | Completeness, external validity, biological fidelity, validation, or adoption. |
| [Candidate Formal Memory Object Model v0.1](../taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md) | State typed entities, relations, operations, invariants, conjectures, countermodels, and missing proof obligations. | Exact bytes registered as `LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL` v1; still a candidate | Consistency, soundness, realizability, mechanism effectiveness, validation, or security. |
| [Prior Art and Competing Taxonomies](../taxonomy/M1_PRIOR_ART_AND_COMPETING_TAXONOMIES.md) | Map candidate definitions to relevant research traditions and expose competing organizations and unresolved transfer assumptions. | Scoped research input; not a systematic evidence synthesis | Novelty, exhaustive coverage, or adoption of a source taxonomy. |
| [Taxonomy-to-FMO Crosswalk Draft v0.1](../taxonomy/M1_TAXONOMY_TO_FMO_CROSSWALK_DRAFT_v0.1.md) | Preserve proposed term-to-formal-surface mappings outside the immutable registered v1 candidate bytes. | `DRAFT CONTINUATION PROPOSAL`; unregistered and not frozen | A valid or complete mapping, amendment or supersession of either subject, a study result, or evidence. |
| [Structural/taxonomy study protocol](../../studies/foundational/m1-taxonomy-v1/protocol-v1.md) | Preregister an evaluation under the accepted `STRUCTURAL_OR_TAXONOMY_EVALUATION` profile. | `FROZEN`; five planned analyses; no output or finding | A scientific result before atomic findings and closeout. |
| [Formal-analysis study protocol](../../studies/foundational/m1-formal-model-v1/protocol-v1.md) | Preregister an evaluation under the accepted `FORMAL_ANALYSIS` profile. | `FROZEN`; seven planned analyses; analyzer not executed | A proof or validity result before the declared verification work. |
| [Taxonomy execution-readiness review](../../reviews/M1_TAXONOMY_EXECUTION_READINESS_2026-07-21.md) | Check contributor, source, environment, intake, and output gates without reading case contents. | `BLOCKED`; taxonomy v1 not run; five outputs absent | A case disposition, finding, candidate evaluation, or substitute for eligible human adjudicators. |
| [Formal execution preflight](../../studies/foundational/m1-formal-model-v1/execution/preflight-execution-attestation.json) | Resolve exact bytes and exercise the frozen provenance guard before machine analysis. | `BLOCKED_NOT_RUN`; configured command, `main`, and `run_kernel` not invoked; seven outputs absent | Satisfiability, consistency, entailment, proof, or any semantic result. |
| [Formal-model execution-readiness review](../../reviews/M1_FORMAL_MODEL_EXECUTION_READINESS_2026-07-21.md) | Record the fail-closed formal v1 guard blocker and bound the only permissible supersession path. | `BLOCKED`; formal v1 not run; no result or disposition | A repaired study, executable v2 freeze, semantic result, proof, or validation. |
| [Study-execution adversarial review](../../reviews/M1_STUDY_EXECUTION_ADVERSARIAL_REVIEW_2026-07-21.md) | Test the truthfulness and containment of both pre-execution failures. | Internal pass for fail-closed blockage only; both studies not run | Independent scientific validation, an atomic disposition, or M1 completion. |
| [Launch-continuation triage](../../reviews/M1_LAUNCH_CONTINUATION_TRIAGE_2026-07-21.md) | Preserve a historical consolidation of continuation prerequisites and unresolved review needs. | Non-evidentiary historical review; later readiness records supersede parts of its inventory | Current execution authority, a finding, closeout, candidate disposition, or completion decision. |
| [Non-evidentiary contract dry runs](../../examples/m1-dry-runs/) | Exercise subject, study, finding, and closeout paths using synthetic inputs before a real study is accepted. | Two isolated fixture families prepared and internally adversarially reviewed | Registration, replication, scientific validity, candidate adoption, or evidence. |
| [Dry-run adversarial review](../../reviews/M1_DRY_RUN_ADVERSARIAL_REVIEW_2026-07-21.md) | Test digest, identity, lifecycle, closeout, production-registry, and claim-boundary failures. | Conditional internal pass; external reproduction not performed | Independent scientific validation or M1 completion. |
| Independent boundary review of later substantive findings | Assess product independence, claim discipline, ambiguity, and untested obligations after real governed analyses exist. | Not started | Scientific validation by itself. |

The two candidate documents are inputs to future studies, not outputs of completed studies. Their foundational-subject entries and verified raw-byte digests identify the exact reviewed versions. Registry presence creates stable identity and provenance only; it does not adopt a candidate or report a result.

## In scope

- Candidate definitions for memory objects, content and functional roles, lifecycle processes, temporal semantics, and governance concepts.
- Multiple orthogonal classification axes rather than a single assumed partition.
- At least two genuinely competing primary organizations of the same candidate domain.
- Formal representation of identities, versions, actors, sources, provenance, authority, confidence, uncertainty, conflicts, policies, and deletion scope.
- Preconditions, postconditions, and non-entailments for admission, encoding, retrieval, update, consolidation, reconsolidation, forgetting, archival, and deletion.
- Constructed positive, negative, ambiguous, adversarial, and boundary cases suitable for later preregistered analysis.
- Structural integrity questions, satisfiability questions, countermodel search, and missing proof obligations.
- Threat analysis for poisoning, provenance forgery, authority confusion, sensitive retention, retrieval manipulation, malicious consolidation, and deletion failure at the conceptual-model level.
- Versioning and supersession rules for candidate definitions.

## Out of scope

- Selecting or evaluating a vector database, graph database, relational database, file format, or other storage implementation.
- Selecting a language model, embedding model, reranker, model provider, or prompting strategy.
- Building an ingestion pipeline, retriever, memory service, agent framework, user interface, or production integration.
- Defining an application-specific entity model or treating any product workflow as the organizing architecture.
- Producing benchmark scores, latency measurements, model comparisons, or claims of mechanism effectiveness.
- Human-subject or participant-data studies; the accepted foundational-study contract does not yet support them.
- Treating biological categories as implementation requirements or claiming functional equivalence with human memory.
- Awarding, changing, or implying a mechanism evidence state.
- Declaring any candidate complete, canonical, validated, adopted, novel, safe, secure, or production-ready.

## Falsifiable launch objectives

These are objectives to be tested by future frozen studies. They are not results.

### M1-O1 — Bounded term discrimination

**Candidate hypothesis:** Each in-scope candidate term can state a bounded definition, proposed necessary conditions, the status of sufficiency, at least one observable distinction from an adjacent term, and at least one counterexample or boundary case.

**Proposed baseline:** The unstructured list of memory topics in the Program Charter.

**Rejection rule:** Reject the candidate vocabulary if any term used by the formal model lacks a stable versioned identifier, has only implementation-specific criteria, cannot be distinguished from every declared adjacent term even in principle, or is presented as exhaustive without a coverage argument.

### M1-O2 — Genuine organizational competition

**Candidate hypothesis:** An intrinsic-kind organization and a contextual-role organization make different, inspectable classification commitments for at least one shared case while remaining internally expressible over the same candidate terms.

**Proposed baseline:** A single unchallenged episodic/semantic/procedural partition.

**Rejection rule:** Reject the claim of genuine competition if the organizations are merely renamed views with identical classifications, or reject one organization if it cannot state how mixed-role, role-changing, and ambiguous cases are handled.

### M1-O3 — Product-independent formal expressiveness

**Candidate hypothesis:** The formal object model can represent the declared lifecycle, epistemic, provenance, conflict, authority, and deletion distinctions without referring to a storage engine, model vendor, embedding representation, application schema, or continuous cloud service.

**Proposed baseline:** A record definition consisting only of payload, embedding, and timestamp.

**Rejection rule:** Reject or narrow the model if a required distinction can be expressed only by assuming a named implementation class, or if removing such an assumption changes a claimed invariant.

### M1-O4 — Non-entailment discipline

**Candidate hypothesis:** The formal model permits countermodels showing that retrieval does not imply truth, confidence does not imply correctness, provenance does not imply authenticity, forgetting does not imply deletion, and conflict detection does not select a winning belief.

**Proposed baseline:** Informal lifecycle language with no explicit semantics.

**Rejection rule:** Reject the relevant axiom or relation if it accidentally entails any prohibited implication, or reject the formalization if the declared countermodels cannot be constructed under its assumptions.

### M1-O5 — Governed lifecycle safety obligations

**Candidate hypothesis:** Every state-changing operation can declare an actor, authority basis, input versions, event or transaction time, provenance effect, and an auditable success or failure postcondition.

**Proposed baseline:** Unversioned in-place mutation with implicit operator authority.

**Rejection rule:** Reject an operation definition if it permits silent mutation, provenance erasure, authority-free state change, resurrection of a deleted payload under the same identity, or a deletion-success claim with an unspecified target scope.

### M1-O6 — Formal analyzability

**Candidate hypothesis:** The candidate invariants and operation rules can be translated into a declared verification formalism that supports consistency or satisfiability checking, intended-entailment checks, and countermodel search.

**Proposed baseline:** Syntax validation alone.

**Rejection rule:** Reject the formal-analysis plan if it reports syntactic well-formedness as semantic validity, cannot enumerate its assumptions, or cannot preserve a counterexample that challenges an intended proposition.

## Planned evaluation sequence

1. Stabilize candidate artifact identifiers and explicit version boundaries without calling the candidates adopted.
2. Assemble constructed case sources that include positive, negative, ambiguous, cross-axis, temporal, authority-conflict, provenance-forgery, and deletion-scope cases.
3. Run the two synthetic, non-evidentiary contract dry runs recommended by the Foundational Study Contract. **Prepared and internally reviewed; acceptance remains infrastructure-only.**
4. Resolve any contract defects by versioned supersession; do not rewrite frozen records.
5. Register the exact candidate taxonomy and formal model as separate foundational subjects if the dry runs show the record path is usable. **Completed for identity and provenance only; no study or evidence effect.**
6. Freeze one structural/taxonomy protocol and one formal-analysis protocol with explicit analyses, baselines, rejection criteria, tools, and immutable artifacts. **Completed as preregistration only; all outputs remain absent.**
   A later execution-readiness review found that both frozen version-1 records fail their own pre-execution gates. Taxonomy v1 lacks valid contributor intake and consistent immutable source/environment bindings; formal v1's digest-bound tool rejects the schema-valid canonical index before analysis. Preserve both records and supersede them before execution.
7. Publish one atomic finding or terminal disposition per planned analysis, including null, halted, invalid, and contradictory outcomes.
8. Close each study only when its immutable all-analysis ledger is complete.
9. Commission an independent review of claims, counterexamples, product independence, and unresolved risks.
10. Decide whether to reject, supersede, narrow, or retain each candidate. No outcome is promoted automatically to a mechanism evidence state.

## M1 exit criteria

M1 is not complete. The two protocol-definition criteria are satisfied by exact frozen preregistrations, but the subsequent readiness increment found both version-1 records unexecutable as frozen. Neither study has been executed and no candidate has received a disposition. All result, closeout, independent-review, and completion criteria remain unchecked. Freeze conformance is not an execution-readiness claim.

- [ ] The exact taxonomy and formal-model subject versions evaluated in M1 are immutable and digest-bound in the foundational-subject registry.
- [x] A frozen `STRUCTURAL_OR_TAXONOMY_EVALUATION` study tests the declared competency questions, integrity constraints, positive and negative cases, adjudication method, and coverage rule.
- [x] A frozen `FORMAL_ANALYSIS` study declares its formal system, assumptions, propositions, consistency method, intended entailments, non-entailments, countermodel search, and immutable tool provenance.
- [ ] Both studies publish exactly one active atomic finding or terminal disposition for every planned analysis and have valid immutable closeouts.
- [ ] M1-O1 through M1-O6 each receive an explicit retain, narrow, supersede, or reject disposition linked to the applicable findings.
- [ ] The competing taxonomy organizations are evaluated as genuinely competing, with mixed-role and role-changing counterexamples preserved.
- [ ] Candidate necessary and sufficient conditions are either supported within the declared structural scope or remain explicitly unresolved.
- [ ] Formal consistency or satisfiability, intended entailments, and declared non-entailments are checked by the preregistered method; syntax checks alone do not satisfy this criterion.
- [ ] Security, privacy, authority, provenance-forgery, and deletion-failure cases receive explicit dispositions and residual risks.
- [ ] An independent reviewer confirms that reported conclusions do not exceed the frozen analyses or imply mechanism maturity.
- [ ] Relative links, exact artifact digests, examples, registries, and repository validation pass on the exact reviewed revision.
- [ ] A boundary review confirms that M1 selected no storage system, model, vendor, application schema, or product architecture and built no memory service.
- [ ] A versioned M1 completion decision records negative and null findings, rejected candidates, accepted limitations, open proof obligations, and the next falsification step.

## Stop, rejection, and reset criteria

Pause new M1 findings and return to candidate design or governance review if any of the following occurs:

- The work requires an unsupported controlled empirical, computational, evidence-synthesis, or human-subject method profile.
- A candidate term or axiom embeds a vendor, storage, embedding, model, product, or application assumption that is represented as general.
- A study accesses its planned results before freeze or changes a confirmatory analysis after result access without disclosed supersession and exploratory reclassification.
- The exact subject, study, profile, finding, or artifact digest cannot be resolved through the accepted contracts.
- A frozen protocol and manifest disagree on their complete source set, or freeze-required environment and intake bindings are absent or self-referential.
- A digest-bound execution guard rejects the schema-valid canonical registry before the declared analysis can begin.
- A taxonomy organization is described as exhaustive without a coverage rule, or alternatives and counterexamples are suppressed.
- A formal claim rests only on a successful parse, type check, example execution, or absence of a found counterexample.
- A deletion claim omits derivatives, replicas, backups, audit residue, or a declared exception scope.
- An authority rule allows the system, operator, provider, source, or user to acquire undeclared universal authority.
- A result is translated into a mechanism maturity label or product recommendation.
- Material contradictory, null, negative, invalid, or halted outcomes are omitted from the record.

If a stop condition exposes a defect in the accepted M0 contracts, M1 must not silently weaken those contracts. The defect should be reported for separately reviewed, versioned governance work.

## Threats and limitations at launch

- **Construct validity:** Candidate terms may create neat labels that do not correspond to distinct observable capabilities.
- **Category leakage:** Functional roles may overlap, change over time, or depend on the query and actor, defeating stable partitions.
- **Biological overreach:** Familiar human-memory labels may conceal different machine processes or encourage unsupported equivalence claims.
- **Formalization loss:** A compact model may omit social, legal, contextual, or probabilistic features that matter to governance.
- **Authority ambiguity:** Authority can be scoped by operation, subject, jurisdiction, time, and policy; a single ordering may be inadequate.
- **Provenance illusion:** Detailed lineage can still be false, incomplete, forged, or derived from compromised sources.
- **Confidence misuse:** Numeric confidence can be uncalibrated, actor-dependent, or mistaken for truth probability.
- **Deletion incompleteness:** Derivative discovery and deletion verification may be impossible under incomplete lineage or external retention obligations.
- **Adversarial definitions:** An attacker may exploit ambiguity among admission, retrieval, reconsolidation, archival, forgetting, and deletion.
- **Evaluation circularity:** Competency questions written from the candidate taxonomy may favor the candidate taxonomy.
- **Method limits:** The accepted v0.1 foundational profiles do not support controlled empirical, computational, evidence-synthesis, or human-subject work.
- **No implementation evidence:** M1 launch documents provide no latency, storage, token-cost, robustness, usability, or operational measurements.

## Architectural and implementation boundary

M1 selects and builds none of the following: a storage engine, vector index, graph store, embedding model, language model, model provider, retriever, reranker, consolidation engine, agent framework, user interface, application schema, full memory service, or production integration.

Mathematical entities such as sets, relations, operations, payloads, scores, and clocks are abstract research constructs. They do not prescribe serialization, database layout, API shape, hosting model, or runtime component. A later Layer 2 proposal would require separate authorization, a replaceable reference architecture, declared baselines, reproducible experiments, and its own evidence discipline.

## Evidence and reporting boundary

M1 launch artifacts are candidate research inputs. They carry no Charter mechanism evidence label, make no empirical finding, and confer no maturity state. The words “defined,” “modeled,” and “represented” in these documents describe the contents of a proposal, not demonstrated properties of a running system or the world.

The synthetic dry runs created no production registry entry; their bundle-local lifecycle records and indexes remain examples only. Separate reviewed increments registered the exact taxonomy and formal-model bytes as two `ACTIVE` Layer 1 subjects and froze two `ACTIVE` study preregistrations. Those actions are not derived from a dry-run outcome and create no adoption, finding, closeout, experiment, mechanism, evidence, or maturity effect. The mechanism, experiment, evidence, research-finding, and foundational-closeout registries remain empty.

Negative, null, contradictory, invalid, and halted analyses are acceptable outcomes and must be retained. Completion of every checkbox would establish only the bounded M1 study dispositions actually reported; it would not establish production readiness or automatic readiness for Layer 2.

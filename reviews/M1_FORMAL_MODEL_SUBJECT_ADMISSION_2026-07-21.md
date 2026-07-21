# M1 Formal-Model Foundational-Subject Admission Dossier — 2026-07-21

## Dossier status

- **Applicable layer:** Layer 1 — Foundational Research
- **Artifact role:** Subject-admission review; not a finding, study, closeout, or evidence decision
- **Candidate subject:** Exact current bytes of `docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md`
- **Admission recommendation:** **ADMIT AS AN ACTIVE FOUNDATIONAL SUBJECT ONLY AFTER EXACT-BYTE AND SCHEMA RECHECK ON THE REGISTRY PR HEAD**
- **Mechanism maturity applicability:** Not applicable
- **Scientific findings asserted:** None
- **Novelty asserted:** No
- **Independent validation established:** No
- **Implementation or adoption authority created:** None

This dossier evaluates whether one exact candidate document can receive a stable Layer 1 subject identity under the Foundational Study Contract. Registration would make the document addressable by a later frozen `FORMAL_ANALYSIS` study. It would not make the document correct, adopted, proved, validated, useful, secure, or ready for implementation.

## Admission question

Can the exact raw bytes currently stored at `docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md` be registered as version 1 of a product-independent `FORMAL_MEMORY_MODEL` subject without converting candidate statements, proof targets, countermodels, or open obligations into findings or mechanism evidence?

## Governing basis and authority

The Program Charter places formal definitions and formal-model work in Layer 1. The M1 Foundation explicitly sequences real registration after synthetic contract dry runs and before a frozen formal-analysis protocol. The accepted synthetic dry-run decision confirms only that the record path is suitable as regression infrastructure; it creates no real subject or evidence.

Admission authority belongs to the LCMRP repository steward acting through a reviewed registry pull request. This originating, agent-assisted dossier may recommend field values, but it cannot activate a registry entry or supply independent scientific review. The effective authority event is the steward-approved merge of an exact-head pull request containing the registry change after required validation.

## Exact artifact examination

The candidate document declares itself to be the Layer 1, launched/in-progress candidate **FMO-0.1**. It describes an abstract typed transition system covering memory candidates and exact versions, lifecycle, time, provenance, authority, epistemic assessments, conflict, operations, and bounded deletion. It explicitly disclaims consistency, satisfiability, completeness, soundness, realizability, security, usefulness, biological equivalence, and implementation status.

The reviewed byte binding is:

| Property | Exact reviewed value |
| --- | --- |
| Locator | `docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md` |
| Raw-byte length | `48995` bytes |
| Digest algorithm | `SHA-256` |
| Digest scope | `RAW_FILE_BYTES` |
| Digest status in the final reviewed registry binding | `VERIFIED` |
| Digest value | `82052e424c01d3204828472ef569f74f7c0aad418f827cffda92400562bbfaf3` |
| Media type | `text/markdown` |

The digest binds raw repository bytes, including whitespace and line endings. Rendering equivalence, normalized text, a copied excerpt, a later edit at the same path, or a semantically similar document is not the registered subject version. Any byte change before registration invalidates this recommendation until the digest and dossier are re-reviewed. Any accepted change after registration requires a new subject version with digest-linked supersession; version 1 must not be rewritten in place.

## Final reviewed registry binding

The following object is the final reviewed publication binding for `registry/foundational-subjects.yaml`. It supersedes the earlier proposed specimen in this dossier. Reviewers and tests must compare the production entry to this object, not reconstruct values from earlier drafting history. Its presence in this dossier records the exact admission recommendation; the registry becomes authoritative only through the steward-approved merge.

```json
{
  "target_type": "FOUNDATIONAL_SUBJECT",
  "subject_kind": "FORMAL_MEMORY_MODEL",
  "subject_id": "LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL",
  "subject_series": "LCMRP-FORMAL-MEMORY-OBJECT-MODEL",
  "subject_version": 1,
  "supersedes_subject_version": null,
  "supersedes_definition_digest": null,
  "entry_status": "ACTIVE",
  "name": "Candidate Formal Memory Object Model v0.1",
  "definition": "A product-independent candidate formal memory object model comprising typed entities, relations, lifecycle operations, temporal and authority semantics, candidate invariants, intended non-entailments, countermodels, and open proof obligations.",
  "boundary": "Registry presence fixes the exact candidate bytes for future Layer 1 formal analysis. It is not a proof of consistency, satisfiability, soundness, or realizability, and it does not establish adoption, scientific evidence, mechanism validation, security assurance, or implementation authorization.",
  "definition_artifact": {
    "artifact_id": "LCMRP-FORMAL-MEMORY-OBJECT-MODEL",
    "artifact_version": 1,
    "schema_id": "urn:lcmrp:artifact-schema:markdown:1",
    "locator": "docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md",
    "digest": {
      "algorithm": "SHA-256",
      "status": "VERIFIED",
      "value": "82052e424c01d3204828472ef569f74f7c0aad418f827cffda92400562bbfaf3",
      "scope": "RAW_FILE_BYTES"
    },
    "media_type": "text/markdown"
  },
  "research_layer": "LAYER_1_FOUNDATIONAL_RESEARCH",
  "mechanism_maturity_applicability": "NOT_APPLICABLE",
  "registered_at": "2026-07-21T20:45:22Z"
}
```

### Field rationale and compatibility

| Field group | Rationale and contract compatibility |
| --- | --- |
| Subject ID | `LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL` satisfies the subject-ID pattern and reserves one stable identity for this version lineage. It must be reused, not replaced, for a future superseding version of the same series. |
| Series and kind | `LCMRP-FORMAL-MEMORY-OBJECT-MODEL` and `FORMAL_MEMORY_MODEL` match the document's declared artifact identity and the registry's bounded kind enum. Both must remain stable across versions. |
| Version | Registry `subject_version: 1` is the first immutable registered version. The source document's human-facing `Artifact version: 0.1` remains unchanged. This explicit mapping is necessary because the registry schema requires integer versions. It does not relabel the document as version 1.0. |
| Supersession | Both supersession fields are `null`, as required for initial version 1. No predecessor is claimed. |
| Status | `ACTIVE` makes the exact subject resolvable for a future frozen study; it does not mean accepted, correct, or validated. Only one active version may exist for this subject ID. |
| Definition and boundary | The final definition identifies the product-independent formal-model contents and explicitly retains open proof obligations. The boundary denies proof, adoption, evidence, mechanism validation, security assurance, and implementation authorization. Neither text substitutes for the exact artifact binding. |
| Artifact identity | The artifact ID is copied from the candidate document. `artifact_version: 1` equals `subject_version: 1`, as required by repository semantic validation. |
| Schema ID | `urn:lcmrp:artifact-schema:markdown:1` denotes the byte artifact's Markdown format contract. It does not assert validation against a content schema and cannot establish the document's structure, meaning, or semantic validity. |
| Locator and digest | The repository-relative locator satisfies traversal restrictions. The verified SHA-256 binds exact raw bytes at that locator. |
| Layer and maturity | The schema-required Layer 1 value is exact. `NOT_APPLICABLE` prevents a foundational subject from receiving a Charter mechanism maturity label. |
| Registration time | `2026-07-21T20:45:22Z` is the stable RFC 3339 registry timestamp selected for both initial M1 subject admissions. It is registry provenance metadata, not a scientific event or evidence claim. |

## Admission rationale

Admission is warranted as an identity and provenance action because:

1. The accepted Foundational Study Contract requires an exact active subject to resolve through the production subject registry before a frozen study can become active.
2. The synthetic taxonomy and formal-analysis dry runs exercised the registry-to-closeout graph and were accepted only as non-evidentiary infrastructure. They exposed no accepted contract defect that blocks a real initial subject entry.
3. The candidate artifact has an explicit ID, human-facing version, research layer, scope boundary, falsifiable statements, rejection criteria, limitations, and a next falsification step.
4. The artifact remains abstract and product-independent. It selects no storage engine, index, model, embedding, application schema, service topology, or implementation.
5. The final reviewed registry binding preserves the document's candidate status, exact bytes, and negative boundaries instead of treating registration as endorsement.
6. Registration is a necessary provenance prerequisite for study freeze, not a sufficient reason to freeze a weak protocol or publish a result.

## Conditions that block or reverse admission

Do not merge the reviewed registry entry, or withdraw/supersede it through a separately reviewed record if already admitted, when any of the following holds:

- The exact PR-head bytes do not hash to `82052e424c01d3204828472ef569f74f7c0aad418f827cffda92400562bbfaf3`.
- The artifact cannot be resolved at the exact repository-relative locator or its artifact ID and declared human-facing version no longer match this dossier.
- The reviewed entry fails JSON Schema Draft 2020-12 validation or repository semantic validation.
- The subject ID or series collides with another subject, the kind or series is unstable, another version is already active, or version 1 is given non-null supersession fields.
- `artifact_version` differs from `subject_version`, the digest is not raw-byte SHA-256, or the status is asserted as verified without recomputation.
- Registration wording is changed to imply adoption, proof, evidence, novelty, mechanism maturity, implementation authorization, or product readiness.
- Candidate limitations, rejection criteria, intended non-entailments, countermodels, or open proof obligations are removed from the exact artifact before registration without a fresh review and binding.
- A later study cannot bind the same subject ID, series, version, definition, boundary, artifact coordinates, and raw-byte digest exactly.
- The formal-analysis plan relies on parsing, typing, example execution, or failure to find a counterexample as semantic validation.
- Contradictory, negative, null, invalid, halted, or not-run outcomes cannot be retained as atomic dispositions under the accepted contract.

Withdrawal would terminate active use of the exact registered version; it would not erase its history. Correction or material revision must use versioned, digest-linked supersession rather than mutating this entry or its bound artifact.

## Open proof and definition obligations preserved

Admission closes none of the candidate document's 25 obligations. Every item below remains **OPEN** and must be carried into the study design where applicable:

1. **Satisfiability:** construct a nontrivial model satisfying all candidate invariants and lifecycle rules.
2. **Invariant independence:** test redundancy and contradiction among invariants.
3. **Transition completeness:** resolve quarantine, expiry, legal hold, migration, corruption, and recovery as states or orthogonal relations.
4. **Distributed time:** replace or justify strict total transaction order for concurrent and imported operations.
5. **Semantic continuity:** distinguish same-series updates from new-series creation.
6. **Content identity:** define equality and equivalence without selecting a representation or leaking deleted content.
7. **Provenance completeness:** define required direct and indirect inputs and omission detection.
8. **Provenance authenticity:** define trust evidence without conflating signatures, custody, source authority, or truth.
9. **Policy calculus:** formalize delegation, revocation, denial, obligation, jurisdiction, purpose limitation, and contested authority.
10. **Authority liveness:** test whether conservative `UNRESOLVED` can indefinitely block legitimate safety or deletion operations.
11. **Access noninterference:** formalize protection against inference through outputs, errors, timing, scores, tombstones, or aggregates.
12. **Confidence semantics:** define scale compatibility, calibration claims, assessor dependence, and aggregation constraints.
13. **Uncertainty algebra:** determine which uncertainty kinds compose and which remain incomparable.
14. **Conflict semantics:** distinguish contradiction, inconsistency, temporal change, ambiguity, and difference under a bounded interpretation language.
15. **Revision semantics:** if added, show that conflict resolution preserves contrary evidence and authority checks.
16. **Role semantics:** define necessary and sufficient conditions for functional roles under both competing organizations.
17. **Deletion closure:** establish when target closure is finite, discoverable, and stable during execution.
18. **Deletion verification:** define the observation model and adversary for non-materialization and non-reconstructability.
19. **External copies:** constrain deletion-result wording under partial authority and unreachable systems.
20. **Audit residue:** define the minimum accountability record and maximum leakage compatible with deletion scope.
21. **No resurrection:** model rollback, restore, replication lag, replay, and independent reacquisition.
22. **Failure atomicity:** define the effects of partial transforms and deletion failures on lifecycle and provenance.
23. **Countermodel validity:** machine-check CM-01 through CM-10 against the exact formal encoding.
24. **Biological independence:** verify that no axiom depends on unstated biological equivalence.
25. **Implementation independence:** verify that primitives admit multiple realizations, or no realization, without changing meaning.

In addition, all four propositions, four conjectures, ten intended entailments, every explicit non-entailment, all ten candidate countermodels, and the security/privacy falsification questions remain unproved and unevaluated. Their presence in registered bytes does not create a result. A later frozen manifest must select explicit atomic analyses and cannot silently mark unselected obligations complete.

## Accepted limitations of this admission review

- The artifact is natural-language mathematics, not a machine-checked formal encoding.
- The digest establishes byte identity, not authorship, provenance authenticity, meaning, correctness, or tamper resistance after an authorized replacement.
- Schema conformance establishes entry shape only. It does not establish subject quality or formal validity.
- The review is originating, agent-assisted, repository-local, and not independent scientific validation.
- The prior-art work is bounded and non-systematic, so no novelty conclusion is available.
- The selected artifact-format `schema_id` is not a machine proof of the Markdown document's internal structure or semantics.
- The model retains unresolved assumptions about time, content identity, authority, provenance, confidence, uncertainty, conflict, deletion, accessibility, reconstruction, and lifecycle dimensionality.
- Registration supplies no participant, runtime, model, dataset, latency, storage, compute, token-cost, information-leakage, security-control, or deletion-effectiveness measurement.
- A future machine encoding may expose ambiguity or contradiction requiring narrowing, rejection, or supersession of FMO-0.1.

## Required checks on the registry pull request

The final reviewer must, on the exact publication head:

1. recompute the raw-byte SHA-256 and byte length of the candidate document;
2. validate the complete production registry against `schemas/foundational-subject-registry.schema.json` using Draft 2020-12;
3. run repository semantic validation to confirm ID/version uniqueness, stable series/kind, one active version, and artifact-version equality;
4. confirm that the registry entry reproduces every field in the final reviewed registry binding exactly, including its name, definition, boundary, artifact-format `schema_id`, and `registered_at` value;
5. run the full repository validator and unit/adversarial suite;
6. confirm that no study, finding, closeout, experiment, evidence, or mechanism registry entry is created by this admission lane; and
7. reject the PR if its prose or metadata overstates registration as adoption, validation, evidence, proof, or readiness.

## Recommended next falsification step

After, and only after, the exact subject is active and resolvable, prepare a separate frozen `FORMAL_ANALYSIS` study against this exact subject identity and digest. Preregister a declared formalism, explicit assumptions and propositions, a nontrivial satisfiability or consistency method, all intended entailment queries, every explicit non-entailment, CM-01 through CM-10, invariant-independence probes, authority and deletion boundary cases, immutable tool provenance, counterexample search, semantic-validity criteria, and terminal rejection conditions. Preserve every counterexample, null result, contradiction, invalid analysis, halted run, and missing proof as its own atomic finding or disposition.

## Final recommendation

**ADMIT AS AN ACTIVE FOUNDATIONAL SUBJECT ONLY AFTER EXACT-BYTE AND SCHEMA RECHECK ON THE REGISTRY PR HEAD.** The exact candidate is sufficiently bounded and addressable to serve as the subject of a later formal study. This recommendation is limited to identity and provenance registration. It is not proof, adoption, a scientific finding, a mechanism evidence award, independent validation, implementation authorization, or M1 completion.

# M1 Taxonomy Foundational-Subject Admission Dossier — 2026-07-21

## Admission status

- **Applicable layer:** Layer 1 — Foundational Research
- **Target:** Exact current bytes of `docs/taxonomy/MEMORY_TAXONOMY_v0.1.md`
- **Reviewed disposition:** **PASS — FINAL EXACT-BYTE REGISTRY BINDING RECONCILED**
- **Registration effect:** One active foundational-subject identity, version 1
- **Scientific finding asserted:** None
- **Taxonomy adoption or validation asserted:** None
- **Mechanism maturity applicability:** `NOT_APPLICABLE`
- **M1 completion asserted:** No

This dossier reviews whether the exact candidate document can be bound as a real foundational subject under the accepted Foundational Study Contract. The final binding below reproduces the separately prepared registry entry exactly and supersedes the earlier admission-preflight specimen. This dossier does not freeze a study, publish a finding, or accept any candidate definition as correct.

## Admission question

Can the exact current bytes of Candidate Memory Taxonomy v0.1 be assigned a stable Layer 1 subject identity and immutable definition-artifact binding without converting registration into adoption, research evidence, scientific validation, implementation authority, or a mechanism maturity decision?

## Governing basis

The Program Charter places memory types, functional taxonomies, lifecycle operations, authority, provenance, confidence, uncertainty, deletion, and governance in Layer 1. The Foundational Study Contract requires a real foundational study to resolve one exact, versioned, digest-bound subject through the production foundational-subject registry. The M1 Foundation schedules separate registration of the exact taxonomy and formal-model candidates after synthetic dry runs establish that the record path is usable.

The accepted dry-run decision supports this next governance step only as internal contract and regression evidence. It did not register a subject, validate the taxonomy, or produce a scientific result. This admission therefore depends on the candidate document's bounded status and exact identity, not on any dry-run fixture outcome being reused as research evidence.

## Exact artifact binding

| Property | Exact reviewed value |
| --- | --- |
| Repository-relative locator | `docs/taxonomy/MEMORY_TAXONOMY_v0.1.md` |
| Raw byte length | `41584` bytes |
| Line-feed count | `314` |
| Digest algorithm | `SHA-256` |
| Digest scope | `RAW_FILE_BYTES` |
| Digest status at admission | `VERIFIED` |
| Raw-byte SHA-256 | `dbdc96095ae90549132e50cbb8759bc45f228cae7d8fcb9a107b95d33647ba70` |
| Media type | `text/markdown` |
| Self-declared artifact ID | `LCMRP-MEMORY-TAXONOMY` |
| Self-declared document version | `0.1` |

`sha256sum`, OpenSSL, and Python `hashlib.sha256` independently returned the same digest during this review. The byte and line-feed counts are descriptive audit aids; the SHA-256 over raw bytes is the binding value. A line-ending conversion, whitespace edit, link edit, or any other byte change creates a different artifact and must not retain this digest.

## Final reviewed registry identity and fields

| Registry field | Final value | Admission rationale |
| --- | --- | --- |
| `target_type` | `FOUNDATIONAL_SUBJECT` | The object is a mechanism-free Layer 1 research subject. |
| `subject_kind` | `MEMORY_TAXONOMY` | Matches the candidate's declared scope. |
| `subject_id` | `LCMRP-FSUBJ-0001-MEMORY-TAXONOMY` | Stable identity reserved for this subject series. |
| `subject_series` | `LCMRP-MEMORY-TAXONOMY` | Matches the document's stable artifact identity and must remain stable across successors. |
| `subject_version` | `1` | First registry version of the subject. |
| `supersedes_subject_version` | `null` | Version 1 has no predecessor. |
| `supersedes_definition_digest` | `null` | Version 1 has no predecessor digest. |
| `entry_status` | `ACTIVE` | Makes this exact identity resolvable for a future study; it does not mean adopted or validated. |
| `name` | `Candidate Memory Taxonomy v0.1` | Preserves candidate status in the human-readable name. |
| `definition_artifact.artifact_id` | `LCMRP-MEMORY-TAXONOMY` | Uses the exact self-declared artifact ID. |
| `definition_artifact.artifact_version` | `1` | Required to equal `subject_version`; it serializes document version `0.1` as the first registry version. |
| `definition_artifact.schema_id` | `urn:lcmrp:artifact-schema:markdown:1` | Identifies the byte artifact format; it does not assert a successful taxonomy content assessment. |
| `definition_artifact.locator` | `docs/taxonomy/MEMORY_TAXONOMY_v0.1.md` | Exact repository-relative path with no traversal. |
| `definition_artifact.media_type` | `text/markdown` | Matches the bound artifact. |
| `research_layer` | `LAYER_1_FOUNDATIONAL_RESEARCH` | Exactly one applicable research layer. |
| `mechanism_maturity_applicability` | `NOT_APPLICABLE` | The subject is not a mechanism version. |
| `registered_at` | `2026-07-21T20:45:22Z` | Exact reviewed registry admission timestamp. |

Final `definition` value:

> A product-independent candidate memory taxonomy comprising versioned terms, orthogonal classification axes, competing kind-first and role-first organizations, observable distinctions, boundary cases, lifecycle concepts, and explicit unresolved obligations.

Final `boundary` value:

> Registry presence fixes the exact candidate bytes for governed Layer 1 evaluation. It does not adopt or validate the taxonomy, establish completeness, novelty, biological fidelity, external validity, mechanism effectiveness, safety, or suitability for implementation.

The following serialization is the final reviewed taxonomy entry and is publication-authoritative for this dossier. It supersedes the earlier preflight specimen. Every field must remain byte-for-byte equivalent in value to the corresponding registry field; no older proposed definition, boundary, schema coordinate, or timestamp should be reproduced in publication.

```yaml
target_type: FOUNDATIONAL_SUBJECT
subject_kind: MEMORY_TAXONOMY
subject_id: LCMRP-FSUBJ-0001-MEMORY-TAXONOMY
subject_series: LCMRP-MEMORY-TAXONOMY
subject_version: 1
supersedes_subject_version: null
supersedes_definition_digest: null
entry_status: ACTIVE
name: Candidate Memory Taxonomy v0.1
definition: >-
  A product-independent candidate memory taxonomy comprising versioned terms,
  orthogonal classification axes, competing kind-first and role-first
  organizations, observable distinctions, boundary cases, lifecycle concepts,
  and explicit unresolved obligations.
boundary: >-
  Registry presence fixes the exact candidate bytes for governed Layer 1
  evaluation. It does not adopt or validate the taxonomy, establish
  completeness, novelty, biological fidelity, external validity, mechanism
  effectiveness, safety, or suitability for implementation.
definition_artifact:
  artifact_id: LCMRP-MEMORY-TAXONOMY
  artifact_version: 1
  schema_id: urn:lcmrp:artifact-schema:markdown:1
  locator: docs/taxonomy/MEMORY_TAXONOMY_v0.1.md
  digest:
    algorithm: SHA-256
    status: VERIFIED
    value: dbdc96095ae90549132e50cbb8759bc45f228cae7d8fcb9a107b95d33647ba70
    scope: RAW_FILE_BYTES
  media_type: text/markdown
research_layer: LAYER_1_FOUNDATIONAL_RESEARCH
mechanism_maturity_applicability: NOT_APPLICABLE
registered_at: "2026-07-21T20:45:22Z"
```

## Compatibility assessment

The final reviewed entry is structurally compatible with `schemas/foundational-subject-registry.schema.json` and the repository's additional registry semantics:

- the subject ID matches the required foundational-subject pattern;
- the artifact ID matches the local-ID pattern;
- the locator is repository-relative and contains no traversal segment;
- version 1 correctly has null supersession fields;
- the artifact version equals the subject version;
- the research layer and mechanism-maturity fields use their required constants;
- the digest uses the required algorithm, scope, lowercase value form, and an allowed verification status;
- the complete reviewed registry assigns the proposed ID and series to exactly this taxonomy subject without colliding with the separately identified formal-model subject; and
- a future successor must retain `subject_id`, `subject_series`, and `subject_kind`, use a higher integer version, identify a lower registered predecessor, bind that predecessor's exact definition digest, and leave at most one version active.

The mapping from document version `0.1` to registry integer version `1` is deliberate because the accepted subject schema uses integer versions. The document's semantic version remains visible in its filename, heading, and name. This mapping must be stated consistently in every future subject reference.

The final `schema_id`, `urn:lcmrp:artifact-schema:markdown:1`, denotes the byte artifact format used for the definition artifact. It supplies no evidence of taxonomy content-schema assessment. No dedicated taxonomy content schema is present. Repository validation can verify the registry structure, locator, raw-byte digest, identity, and lineage, but it cannot establish the semantic quality of the candidate definitions.

## Registration, adoption, evidence, and validation boundary

Registration would establish only the following:

1. A stable subject identity exists.
2. Subject version 1 refers to one exact byte sequence.
3. A future frozen study can resolve that exact identity and artifact through the production registry.
4. Later byte-changing revisions require explicit versioned lineage rather than silent replacement.

Registration would not establish that the taxonomy is correct, complete, useful, representative, novel, internally consistent, biologically faithful, secure, externally valid, preferred over a baseline, or suitable for implementation. It would not make any term canonical or adopted. It would not freeze a study, establish prior-result separation, publish a finding, close an analysis ledger, award a mechanism label, or complete M1.

`ACTIVE` means active as a resolvable registry identity. It must never be paraphrased as scientifically accepted. `VERIFIED` means only that the recorded hash was recomputed over the current raw file bytes. It does not authenticate authorship, provenance, review independence, or truth.

## Authority and change control

This dossier records an internal review of the separately prepared registry change. Final publication authority belongs to the repository steward. The final reviewer must recompute the digest from the exact candidate-tree bytes, confirm that the ID and series still resolve uniquely, verify the exact registered timestamp and every other stable field against the publication candidate, validate the complete registry, and review the resulting diff before acceptance.

Once admitted, the exact v1 entry and bound bytes must be treated as immutable historical inputs. Any semantic or editorial byte change intended to replace the subject requires a new registered subject version. The prior version should become `SUPERSEDED`, the successor must point to version 1 and its exact digest, and the registry must retain the historical entry. Withdrawal may change lifecycle status through reviewed history, but it must not erase the old definition or claim it never existed.

## Admission rationale

The candidate is suitable to become a study target because it already declares Layer 1, candidate status, no mechanism evidence, no scientific findings, explicit version rules, bounded definitions, competing organizations, competency questions, rejection conditions, unresolved obligations, biological-analogy limits, and known limitations. These properties make disagreement and falsification addressable without asserting that the proposed vocabulary has passed such evaluation.

Admission is also sequenced correctly: the synthetic dry runs exercised the subject-to-closeout record path and were accepted only as non-evidentiary infrastructure. Registration now supplies the exact real subject identity required before a substantive frozen taxonomy study can become active. The dry runs do not support the taxonomy and are not a baseline result.

## Rejection and stop conditions

Reject or pause the registry mutation if any of the following is true at final review:

1. The candidate bytes no longer hash to `dbdc96095ae90549132e50cbb8759bc45f228cae7d8fcb9a107b95d33647ba70`.
2. The locator does not resolve to a regular repository file or resolves through traversal, aliasing, or an unintended generated artifact.
3. The proposed subject ID or series collides with another subject, or the complete registry would violate one-active-version, stable-series, stable-kind, or lineage rules.
4. The artifact version differs from the subject version, or version 1 is given non-null supersession data.
5. The final entry weakens the candidate, non-evidence, non-adoption, or no-maturity boundary.
6. The entry implies validation by a content schema, registrar, reviewer, or scientific process that did not occur.
7. A general definition has been changed so that an implementation, vendor, application, or product architecture becomes a general prerequisite without an explicit bounded scope and separate review.
8. Registration is bundled with a frozen-study, finding, closeout, evidence, implementation, or completion claim that has not independently satisfied its own contract.
9. The steward cannot preserve the exact prior bytes and entry through future append-oriented supersession.
10. Repository validation, relative-link checks, registry semantics, or the exact-head test suite fails.

These are admission controls. The candidate document's own scientific rejection conditions remain unresolved questions for a governed study; they are not silently converted into admission results.

## Security, privacy, and governance considerations

The target is a public conceptual document and contains no authorized participant study or participant dataset. Registration does not authorize collection of human data. A future study must independently declare its sources, assets, threats, controls, retention and deletion behavior, and residual risks under an accepted method profile.

SHA-256 detects accidental or adversarial byte substitution only when a trusted reviewer recomputes it against an independently obtained expected value. It does not prevent an authorized actor from changing both an artifact and every digest reference, prove that provenance assertions are authentic, or establish authorship. Reviewable version-control history, protected merge authority, exact-head checks, and append-oriented lineage remain necessary controls.

The Markdown locator is readable and replaceable across environments, but byte identity is sensitive to newline normalization and text transformations. Consumers must hash repository raw bytes rather than rendered text, decoded text, or copied excerpts.

## Limitations and open obligations

- No candidate term has been evaluated through a real frozen foundational study.
- No inter-rater reliability, coverage, construct-validity, external-validity, biological-validity, or implementation-utility result exists.
- The cases were constructed with the candidate and may favor its distinctions.
- Natural-language definitions remain interpretation-sensitive.
- The Markdown byte-format coordinate has no dedicated machine-enforced taxonomy content schema.
- Hash equality establishes byte identity, not provenance authenticity or scientific merit.
- This internal admission review is not independent scientific validation.
- Registration alone satisfies neither a substantive study obligation nor the first M1 exit criterion, whose wording applies to subject versions actually evaluated in M1; no required frozen study has yet bound or evaluated this subject.
- A later study must preserve negative, null, ambiguous, contradictory, halted, invalid, and not-run outcomes rather than forcing every case into the taxonomy.

## Next falsification step

After exact-byte registration, prepare and independently review a frozen `STRUCTURAL_OR_TAXONOMY_EVALUATION` study that binds this subject ID, version, locator, and digest exactly. The protocol should compare the kind-first and role-first organizations against preregistered positive, negative, ambiguous, boundary, temporal, authority-conflict, provenance-forgery, and deletion-scope cases. It should require term-by-term necessary-condition and negative-case checks, a declared coverage rule, held-out cases, independent adjudication, explicit rejection thresholds, and one atomic finding or terminal disposition per planned analysis.

Any mismatch between the frozen study and this subject reference must fail closed. Any byte change needed before freeze must create and register a successor subject version rather than update version 1 in place.

## Final recommendation

**PASS — FINAL EXACT-BYTE REGISTRY BINDING RECONCILED.** The reviewed identity and artifact reference represent the exact current candidate as a real Layer 1 foundational subject while preserving the distinction among identity registration, taxonomy adoption, scientific evidence, validation, mechanism maturity, and milestone completion.

The final reviewer should publish only the exact digest-bound bytes and stable registry values reproduced above, run the complete registry and repository gates, and reject the change if any admission condition fails or either side of the dossier-to-registry binding changes.

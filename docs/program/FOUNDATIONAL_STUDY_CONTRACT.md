# Foundational Study Contract v0.1

## Status and scope

- **Applicable layer:** Layer 1 — Foundational Research
- **Contract status:** Draft M0 infrastructure for investigation
- **Mechanism evidence labels:** Not applicable
- **Empirical findings asserted:** None

This contract defines how LCMRP may preregister and report a mechanism-free foundational study without inventing a dummy mechanism or weakening the separate mechanism evidence-state gates.

The v0.1 contract supports two bounded method profiles:

1. `STRUCTURAL_OR_TAXONOMY_EVALUATION`
2. `FORMAL_ANALYSIS`

Controlled computational or empirical evaluation and evidence synthesis are not yet supported by this contract. They require separately versioned profiles with their own enforceable obligations.

## Research question

How can LCMRP represent taxonomy, formal-model, concept, and evaluation-construct studies while preserving immutable provenance, preregistration discipline, negative and null dispositions, and the rule that Charter maturity labels apply only to exact mechanism versions?

## Design hypothesis

A parallel foundational-study and finding contract is easier to audit than making `mechanism_versions` optional inside the existing experiment and evidence schemas. The parallel contract should be rejected if it permits a non-mechanism finding to award or imply a mechanism evidence label.

## Artifact model

| Artifact | Responsibility | Explicitly cannot do |
| --- | --- | --- |
| `foundational-study-manifest` | Bind an exact non-mechanism subject, one versioned method profile, preregistration state, per-analysis modes, sources, rejection criteria, and reproducibility plan. | Evaluate a mechanism or target a mechanism maturity label. |
| `research-finding-record` | Preserve one analysis finding or terminal disposition against an exact study, subject, profile, and analysis. | Award or change a mechanism evidence profile. |
| `foundational-record-index` | Define append-oriented entries for immutable study and finding records. | Establish that a study occurred or that a finding is valid merely because an entry exists. |

The existing `experiment-manifest`, `evidence-record`, mechanism registry, and evidence-decision gates remain unchanged.

## Contract requirements

### Typed, immutable subject identity

Every study has exactly one `FOUNDATIONAL_SUBJECT` with a stable subject ID, series, exact version, bounded definition, and artifact reference. Frozen records require a recorded or verified SHA-256 digest over raw bytes. A missing subject or a fake placeholder mechanism is invalid.

This entity/activity/agent separation and derivation discipline follows the general provenance model in [W3C PROV-DM](https://www.w3.org/TR/prov-dm/). The distinction between a stable series and an exact version is also consistent with [DataCite relation metadata](https://datacite-metadata-schema.readthedocs.io/en/4.7/properties/relatedidentifier/) and the ontology-series/version distinction in the [OWL 2 structural specification](https://www.w3.org/TR/owl2-syntax/#Ontology_IRI_and_Version_IRI). Raw-byte digests follow the content-identification rationale in [RFC 6920](https://www.rfc-editor.org/info/rfc6920/).

### One versioned primary method profile

Every manifest selects exactly one primary profile with its own stable ID, series, version, and definition artifact. Profile obligations are machine-enforced; unrestricted free-text `NOT_APPLICABLE` is not a substitute for them.

This design follows the profile model described by [RO-Crate 1.3](https://www.researchobject.org/ro-crate/specification/1.3/profiles.html), where a profile has a persistent identifier and declares additional expected constraints. The [W3C Profiles Vocabulary](https://www.w3.org/TR/dx-prof/) is supporting guidance; it is a Working Group Note rather than a W3C Recommendation.

### Preregistration and amendments

A draft has no freeze timestamp or freeze artifact. A frozen manifest must state that results were not accessed before freeze and must record the freeze time, authority, and immutable freeze artifact. Any post-result change requires a superseding record, an exact prior digest, a disclosure, and exploratory classification for amended analyses.

This is aligned with the timestamped, read-only registration behavior documented by [OSF Registrations](https://help.osf.io/article/330-welcome-to-registrations) and the prediction-versus-postdiction distinction described by [Nosek et al.](https://www.pnas.org/doi/10.1073/pnas.1708274114). LCMRP's exact schema fields are a program design choice, not a claim that those sources define this schema.

### Per-analysis classification and terminal disposition

Analysis mode belongs to each planned analysis so a study may transparently contain both confirmatory and exploratory work. A finding binds one exact analysis and records one of `COMPLETED`, `NOT_RUN`, `HALTED`, or `INVALID`.

Result classification and claim assessment are intentionally independent. For example, a `NULL` observation can support a claim that predicts equivalence, while a positive measurement can fail to support an overbroad claim. No automatic result-to-claim inference is allowed.

Mandatory terminal dispositions and preservation of null or failed work respond to documented publication and write-up bias against null findings, including [Franco, Malhotra, and Simonovits](https://pubmed.ncbi.nlm.nih.gov/25170047/). Claim-scoped findings with explicit supporting or challenging relations are also compatible with the [Micropublications model](https://pmc.ncbi.nlm.nih.gov/articles/PMC4530550/); separating a finding from a maturity decision is an LCMRP design inference.

## Profile obligations

### Structural or taxonomy evaluation

The profile requires:

- competency questions;
- explicit integrity constraints;
- versioned category definitions;
- positive and negative case sources;
- an adjudication method; and
- an explicit coverage rule.

Structural conformance cannot be described as biological truth, external validity, usefulness, or mechanism effectiveness. The distinction between concept schemes and formal ontologies follows the [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/). Individual validation outcomes and explicit conformance are informed by [W3C SHACL](https://www.w3.org/TR/shacl/). Competency questions as evaluation requirements are supported by [Grüninger and Fox](https://www.eil.utoronto.ca/wp-content/uploads/enterprise-modelling/papers/gruninger-ijcai95.pdf).

### Formal analysis

The profile requires:

- a versioned formal-system artifact;
- explicit assumptions and propositions;
- consistency or satisfiability checks;
- intended entailments;
- non-entailments or countermodels;
- immutable tool provenance;
- a proof or verification method; and
- separate semantic-validity and counterexample-search descriptions.

Syntax checking alone cannot support a validity claim.

## Security and privacy boundary

The v0.1 source kinds prohibit human-subject studies and participant data. A foundational manifest must still identify assets, threats, controls, retention/deletion behavior, and residual risk. A future human-subject profile requires a separate governance contract before it can be represented.

## Rejection conditions

Reject a proposed record when any of the following holds:

- The subject is absent, mutable, unversioned, or represented by a dummy mechanism.
- No primary profile or more than one primary profile is declared.
- A profile-required obligation is removed or replaced by unsupported free text.
- A frozen manifest lacks a freeze time, authority, immutable artifact, or no-prior-result-access assertion.
- A post-result change is not represented by a disclosed superseding record.
- A finding's study, subject, profile, or analysis binding does not match the referenced manifest.
- A non-mechanism finding contains an evidence decision, a non-empty awarded-label set, or any mechanism maturity effect.
- A result class is automatically translated into claim support or refutation.
- A taxonomy evaluation omits positive or negative cases.
- A formal analysis relies on syntax checking without consistency, intended-inference, and countermodel obligations.

## Reproducibility and validation

Schema conformance is structural only. It does not establish that a taxonomy is complete, a formal model is sound, a result is true, or an evaluator is independent.

The synthetic `9999` examples are fixtures. They are not registrations, experiments, findings, replications, or evidence. Their pending inputs must not be cited as if they exist.

## Known limitations

- Repository validation checks finding-to-study record IDs and versions, subject identity and version, profile identity and version, and analysis ID and mode. It does not yet resolve the embedded subject definition through a standalone subject registry.
- A terminal study does not yet have a machine-enforced completeness rule requiring one finding or disposition for every planned analysis.
- A standalone foundational-subject registry and subject supersession validator do not yet exist.
- External registration-service verification is not implemented; the contract records an authority and immutable freeze artifact only.
- Controlled computational/empirical and evidence-synthesis profiles remain to be designed and adversarially tested.
- The parallel schemas duplicate some amendment and artifact-reference definitions. A shared base schema may be considered only after interoperability and auditability are tested.

These are open M0 obligations. The new contract must remain draft until they are resolved or explicitly accepted through governance.

## Recommended next experiment

Create two frozen synthetic protocol families—one taxonomy evaluation and one formal analysis—then attempt adversarial cross-record substitutions, missing terminal dispositions, profile switching, null-result interpretation, and subject supersession. Use the results to decide whether the shared identity/provenance layer should be extracted before any real Layer 1 study is registered.

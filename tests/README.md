# Research contract and M1 launch tests

**Artifact classification:** program infrastructure supporting all three research layers; this document and the test suite are not research evidence.

The tests check whether repository artifacts satisfy declared structural and governance contracts, including the M1 launch boundaries. A passing test suite does not establish that a memory mechanism works, validate a taxonomy or formal model, validate a research finding, award an evidence label, or demonstrate product readiness.

## Run the suite

After installing [`requirements-dev.txt`](../requirements-dev.txt), run:

```text
python tools/validate_repository.py
python -m unittest discover --start-directory tests --verbose
```

Both commands must pass. The repository validator exercises whole-tree discovery, JSON/YAML parsing, schemas, examples, registries, local artifact digests, governance invariants, and relative links. Unit tests add targeted positive and adversarial cases.

## Foundational-study boundary expectations

The mechanism-free Layer 1 contracts are tested as a separate artifact family. The tests require:

- a valid foundational study manifest and research finding with no mechanism under evaluation;
- exact, immutable study, subject, and method-profile identity and artifact bindings in a finding;
- foundational-subject registry uniqueness, stable-series, supersession, and exact active-study resolution;
- exactly one immutable, versioned primary method profile, with its method-specific obligations enforced;
- explicit applicability values and internally consistent applicable/not-applicable payloads;
- per-analysis confirmatory or exploratory classification and transparent post-result profile/amendment changes;
- retained terminal dispositions including null, invalid, halted, and not-run work;
- an immutable closeout that set-equals every frozen planned analysis to exactly one active published finding, while allowing partial studies to remain open;
- canonical, path-safe subject, study, finding, and closeout registry entries with digest-linked lineage;
- no mechanism maturity award, evidence decision, or implied evidence-profile effect from a general finding;
- rejection of human-subject work until a separately approved governance contract exists;
- rejection of Layer 3 or CorpusStudio integration fields in Layer 1 artifacts;
- preservation of preregistration, result-access, and post-result amendment rules;
- orthogonality between result class and claim assessment;
- dynamic discovery and validation of new schema/example pairs; and
- continued validity of the existing mechanism-oriented example family.

Negative fixtures mutate synthetic examples in memory. They are deliberately non-evidence and must not be registered as research records.

## M1 launch boundary expectations

The M1 launch tests treat the taxonomy, prior-art map, and formal object model as unvalidated Layer 1 candidates. They require:

- exactly one Layer 1 declaration per substantive launch artifact;
- an in-progress milestone with unchecked exit criteria and explicit stop or rejection rules;
- competing taxonomy organizations, observable distinctions, edge cases, and unresolved obligations;
- product-independent authority, provenance, confidence, uncertainty, deletion, time, and lifecycle semantics;
- a typed formal model with declared operations, invariants, intended non-entailments, countermodels, and missing proof obligations;
- no mechanism maturity award, adoption claim, novelty claim, or fabricated finding;
- no product, model-provider, storage-provider, or CorpusStudio architecture assumption; and
- unchanged empty production registries.

These are launch-contract checks, not validation of the candidate definitions or their supporting sources.

## M1 dry-run boundary expectations

The M1 dry-run tests treat both bundles as isolated, synthetic program-infrastructure fixtures. They require:

- Draft 2020-12 validation for every schema-backed bundle record and index;
- exact raw-byte SHA-256, subject, profile, study, finding, and closeout bindings;
- one terminal atomic record per planned analysis and set-equal closeout ledgers;
- disjoint bundle identities and one active version per governed record;
- explicit non-evidentiary markers, no human data, and no mechanism maturity effect;
- empty production registries; and
- rejection of digest substitution, cross-bundle identity substitution, missing, duplicate, or extra closeout rows, profile swaps, false completion rhetoric, production-registry contamination, and multiple active versions.

Bundle-native semantic replay and serialization checks supplement these tests. They do not prove taxonomy quality, formal soundness, external validity, independent validation, or M1 completion.

## Interpretation limits

These checks establish only that encoded cases are accepted or rejected as intended by the current contracts. They do not prove that free-form prose is truthful, that a study is scientifically sound, that identities are controlled by real independent parties, or that every future bypass has been anticipated. Human review and independent scientific validation remain necessary.

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
- no registry effect from the historical launch package itself; a later, separately reviewed admission may populate only the foundational-subject registry without changing the launch artifacts into evidence.

These are launch-contract checks, not validation of the candidate definitions or their supporting sources.

## M1 dry-run boundary expectations

The M1 dry-run tests treat both bundles as isolated, synthetic program-infrastructure fixtures. They require:

- Draft 2020-12 validation for every schema-backed bundle record and index;
- exact raw-byte SHA-256, subject, profile, study, finding, and closeout bindings;
- one terminal atomic record per planned analysis and set-equal closeout ledgers;
- disjoint bundle identities and one active version per governed record;
- explicit non-evidentiary markers, no human data, and no mechanism maturity effect;
- no dry-run-derived production entry: only the two separately admitted exact subjects and the two separately frozen exact real studies may appear in their production registries, while the five result/mechanism registries remain empty; and
- rejection of digest substitution, cross-bundle identity substitution, missing, duplicate, or extra closeout rows, profile swaps, false completion rhetoric, production-registry contamination, and multiple active versions.

Bundle-native semantic replay and serialization checks supplement these tests. They do not prove taxonomy quality, formal soundness, external validity, independent validation, or M1 completion.

## M1 subject-admission boundary expectations

The subject-admission tests treat registration as an identity and provenance action supporting Layer 1. They require:

- exactly two `ACTIVE` version-1 subjects with unique IDs, stable series, correct kinds, null supersession, safe locators, and exact verified raw-byte digests;
- exact agreement among the registry, candidate bytes, and final reviewed dossier bindings;
- `NOT_APPLICABLE` mechanism maturity and no adoption, validation, study-completion, evidence, or product-readiness claim;
- exactly the two reviewed frozen studies may follow the subject registrations, while research-finding, foundational-closeout, experiment, mechanism, and evidence registries remain empty; and
- rejection of digest substitution, kind or locator swaps, duplicate active lineage, false validation or completion rhetoric, and accidental study or evidence entries.

These checks show that the two candidates are addressable for later governed studies. They do not establish taxonomy quality, formal consistency, scientific validity, adoption, independent validation, or M1 completion.

## M1 study-freeze boundary expectations

The study-freeze tests treat both real studies as unexecuted Layer 1 preregistrations. They require:

- exactly two `ACTIVE`, `FROZEN`, version-1 studies, each resolving one exact registered subject and its declared method profile;
- immutable raw-byte bindings for the subject, method profile, protocol, freeze attestation, sources, configurations, environment, and profile-specific formal or category artifacts;
- five distinct planned taxonomy outputs and seven distinct planned formal-analysis outputs, all retaining `PENDING` null digests and absent paths;
- `results_accessed_before_freeze: false`, an exact common freeze authority and timestamp, and no execution-result fields in either manifest;
- no taxonomy execution intake and no formal analyzer execution before a separately governed execution increment;
- empty research-finding, foundational-closeout, experiment, mechanism, and evidence registries and record areas; and
- rejection of digest substitution, identity cross-binding, path escape, duplicate outputs, result leakage, false completion or evidence claims, and product-specific contamination.

These checks establish preregistration integrity and containment only. They do not evaluate the taxonomy, prove the formal model, publish a finding, close either study, award mechanism maturity, or complete M1.

## M1 study-execution readiness expectations

The execution-readiness tests accept only truthful fail-closed blockage. They require:

- exact preservation of both frozen version-1 manifests and their non-result artifact bindings;
- taxonomy execution to remain blocked without a valid immutable intake, two eligible primary human adjudicators, a distinct eligible human tie adjudicator, consistent source bindings, complete freeze-environment provenance, and a non-self-referential intake digest contract;
- no taxonomy case access, coding, output, finding, or closeout created by the readiness lane;
- formal preflight metadata to bind the exact study, tool, inputs, runtime, public snapshot, configured command, and absent result path;
- configured formal analyzer, `main`, and `run_kernel` invocation counts of zero;
- reproducible failure of the frozen canonical-index guard before analysis and continued absence of all seven formal result paths;
- rejection of substituted paths, digest mismatch, fabricated contributors, premature downstream analyses, false proof or validation language, product coupling, and suppressed negative, null, contradictory, counterexample, or invariant-omission rows; and
- empty research-finding and foundational-closeout registries, with both studies still open and M1 still in progress.

These checks do not show that a repaired intake, superseding analyzer, future result, or human semantic mapping is correct. A blocked preflight is program-engineering evidence about execution readiness, not a research finding about either candidate.

## Interpretation limits

These checks establish only that encoded cases are accepted or rejected as intended by the current contracts. They do not prove that free-form prose is truthful, that a study is scientifically sound, that identities are controlled by real independent parties, or that every future bypass has been anticipated. Human review and independent scientific validation remain necessary.

# M0 contract tests

**Artifact classification:** program infrastructure supporting all three research layers; this document and the test suite are not research evidence.

The M0 tests check whether repository artifacts satisfy declared structural and governance contracts. A passing test suite does not establish that a memory mechanism works, validate a research finding, award an evidence label, or demonstrate product readiness.

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
- exact, immutable study and subject identity bindings in a finding;
- exactly one immutable, versioned primary method profile, with its method-specific obligations enforced;
- explicit applicability values and internally consistent applicable/not-applicable payloads;
- per-analysis confirmatory or exploratory classification and transparent post-result profile/amendment changes;
- retained terminal dispositions for every planned analysis, including null, invalid, halted, and not-run work;
- no mechanism maturity award, evidence decision, or implied evidence-profile effect from a general finding;
- rejection of human-subject work until a separately approved governance contract exists;
- rejection of Layer 3 or CorpusStudio integration fields in Layer 1 artifacts;
- preservation of preregistration, result-access, and post-result amendment rules;
- orthogonality between result class and claim assessment;
- dynamic discovery and validation of new schema/example pairs; and
- continued validity of the existing mechanism-oriented example family.

Negative fixtures mutate synthetic examples in memory. They are deliberately non-evidence and must not be registered as research records.

## Interpretation limits

These checks establish only that encoded cases are accepted or rejected as intended by the current contracts. They do not prove that free-form prose is truthful, that a study is scientifically sound, that identities are controlled by real independent parties, or that every future bypass has been anticipated. Human review and independent scientific validation remain necessary.

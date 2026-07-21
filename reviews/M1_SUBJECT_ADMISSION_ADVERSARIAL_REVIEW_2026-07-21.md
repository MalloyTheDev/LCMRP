# M1 Foundational-Subject Admission Adversarial Review — 2026-07-21

## Review classification

- **Applicable layer:** Layer 1 — Foundational Research
- **Artifact role:** Program verification infrastructure; not a research finding or evidence record
- **Review scope:** Exactly two real M1 candidate-subject registrations, their definition artifacts, and their admission dossiers
- **Verdict:** **CONDITIONAL PASS — IDENTITY AND PROVENANCE REGISTRATION ONLY**
- **Research evidence created:** None
- **Independent scientific validation established:** No
- **Mechanism evidence labels awarded or changed:** None
- **Study, finding, or closeout created:** No
- **M1 completion established:** No

This is an internal adversarial review of subject identity, exact-byte provenance, registry containment, and claim boundaries. It is not a foundational study, research finding, proof, taxonomy evaluation, replication, external review, or scientific validation. The conditional pass applies only if the same exact publication head passes repository validation, the full test suite, and required continuous integration before steward acceptance.

## Independence and write boundary

The taxonomy-admission and formal-model-admission dossiers were authored in separate work areas. The verification lane treated both candidate documents, both dossiers, all registries, schemas, navigation files, prior decisions, and existing tests as read-only. It wrote only this review and `tests/test_m1_subject_admission.py`; it did not repair originating work.

During verification, the first integrated draft was rejected because the dossier specimens and production registry disagreed on artifact `schema_id`, name, definition, and boundary fields. The authoring lanes corrected only their own dossiers, and the final gate now parses each dossier's single authoritative registry specimen and requires complete structured equality with its production entry. This detected correction is an internal process observation, not evidence that every possible defect has been found.

## Exact objects reviewed

| Subject ID | Kind | Series | Version and state | Definition artifact | Raw-byte SHA-256 |
| --- | --- | --- | --- | --- | --- |
| `LCMRP-FSUBJ-0001-MEMORY-TAXONOMY` | `MEMORY_TAXONOMY` | `LCMRP-MEMORY-TAXONOMY` | v1, `ACTIVE` | `docs/taxonomy/MEMORY_TAXONOMY_v0.1.md` | `dbdc96095ae90549132e50cbb8759bc45f228cae7d8fcb9a107b95d33647ba70` |
| `LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL` | `FORMAL_MEMORY_MODEL` | `LCMRP-FORMAL-MEMORY-OBJECT-MODEL` | v1, `ACTIVE` | `docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md` | `82052e424c01d3204828472ef569f74f7c0aad418f827cffda92400562bbfaf3` |

Both entries declare `FOUNDATIONAL_SUBJECT`, `LAYER_1_FOUNDATIONAL_RESEARCH`, and `NOT_APPLICABLE` mechanism maturity. Both are initial versions with null supersession fields. Their `ACTIVE` state means only that the exact identities are resolvable for later study.

## Positive admission gates

The dedicated suite requires:

- exactly the reviewed two-subject ID set, with unique IDs, series, and ID/version pairs;
- the expected taxonomy and formal-model kinds without cross-substitution;
- initial version 1, `ACTIVE` state, null predecessor fields, and matching artifact version;
- complete Draft 2020-12 validation and repository subject-lineage semantics;
- repository-relative, traversal-free locators bound to the intended candidate document;
- `VERIFIED` SHA-256 values recomputed over exact `RAW_FILE_BYTES`;
- the final Markdown artifact-format coordinate and `text/markdown` media type;
- exact structured equality between each dossier's final registry specimen and the corresponding production entry;
- explicit Layer 1, no-finding, no-independent-validation, and no-mechanism-maturity boundaries;
- product-independent candidate and admission material without a named technology dependency;
- no evidence-decision or mechanism-label fields in the subject registry;
- empty mechanism, experiment, evidence, foundational-study, research-finding, and foundational-closeout registries; and
- no JSON record in any canonical real study, finding, closeout, experiment, or evidence record area.

## Adversarial mutations

| Attack | Mutation | Required rejection |
| --- | --- | --- |
| Raw-byte digest substitution | Replaced the taxonomy digest with a different valid-length lowercase value | Rejected because it differs from the separately recomputed reviewed digest |
| Subject-kind swap | Exchanged `MEMORY_TAXONOMY` and `FORMAL_MEMORY_MODEL` while preserving schema-valid values | Rejected because each exact subject ID and locator has one reviewed kind |
| Definition substitution | Pointed the taxonomy entry at the formal-model path | Rejected as an exact locator and artifact-binding mismatch |
| Path escape | Replaced a locator with `../outside.md` | Rejected by the admission path gate and Draft 2020-12 locator pattern |
| Duplicate active identity/version | Appended the first active entry again | Rejected for wrong cardinality and duplicate ID/version and series |
| Duplicate series | Assigned the taxonomy series to the formal-model subject | Rejected because a stable series cannot identify two subject IDs |
| Validation laundering | Replaced a boundary with an affirmative scientific-validation claim | Rejected by the claim-boundary gate |
| Adoption laundering | Replaced a boundary with an affirmative taxonomy-adoption claim | Rejected by the claim-boundary gate |
| Premature completion | Replaced a boundary with an affirmative M1-completion claim | Rejected by the claim-boundary gate |
| Registry side effect | Inserted an entry into each non-subject production registry in turn | Rejected because this admission may affect only the subject registry |
| Dossier/registry divergence | Earlier dossier specimens used coordinates and descriptions different from production | Rejected until each final specimen became exactly equal to its registry entry |

## Validation results

All commands ran from the repository root with the pinned development packages made available through `PYTHONPATH=.venv/lib/python3.12/site-packages`.

| Check | Result |
| --- | --- |
| Dedicated subject-admission suite | **12/12 passed** |
| Complete unit and adversarial suite | **130/130 passed** |
| Repository validator | Passed |
| Exact candidate SHA-256 recomputation | Passed for both definition artifacts |
| Dossier-to-registry structured equality | Passed for both subjects |
| Production-registry containment | Passed; two subject entries only, all other registries empty |

An initial full-suite run correctly exposed a stale dry-run regression gate that still required every production registry to be empty. The integration reviewer updated that existing gate to distinguish the two admitted real subjects from forbidden synthetic dry-run contamination while retaining emptiness requirements for the other six registries. The final results above must reflect a clean re-run after that correction.

## Security, privacy, and governance observations

- SHA-256 detects byte divergence when a reviewer retains and recomputes an expected value. It does not authenticate authorship, prove semantic correctness, or prevent consistent replacement of an artifact and every digest before review.
- Repository-relative path and traversal gates constrain the referenced artifact to the reviewed tree. They do not establish that the content itself is safe or correct.
- The registered targets are public conceptual documents. Registration creates no authority to collect participant data or execute a human-subject study.
- Stable initial identities improve later auditability, but a byte-changing correction must use a successor version and digest-linked lineage rather than modifying the registered v1 artifact in place.
- The claim checks cover explicit structured and dossier statements. They are paired with human review because indirect or euphemistic overclaims may evade text gates.

## Limitations and open obligations

1. This review is internal, agent-assisted, and repository-local. Separate agent lanes do not constitute independent scientific validation.
2. Registry and schema validity establish identity and contract shape only. They do not establish taxonomy completeness, category utility, formal consistency, satisfiability, soundness, realizability, security, or novelty.
3. The candidate taxonomy has not undergone its required frozen structural/taxonomy evaluation.
4. The formal model remains natural-language mathematics and has not undergone its required frozen formal analysis or machine-checked proof.
5. No study was frozen, no result was accessed, no analysis was run, and no atomic finding or closeout was published by this increment.
6. The mutation set is representative rather than exhaustive. Multi-field coordinated substitutions and future schema extensions may require additional gates.
7. `VERIFIED` describes digest recomputation only. `ACTIVE` describes registry resolution only. Neither word is scientific acceptance.
8. M1 remains in progress. Subject registration enables the next governed work but does not satisfy the substantive exit criteria.

## Recommended next falsification step

Prepare two separately reviewed protocols against these exact subject IDs, versions, locators, and digests: one `STRUCTURAL_OR_TAXONOMY_EVALUATION` and one `FORMAL_ANALYSIS`. Freeze each protocol before result access, preserve every negative, null, invalid, halted, contradictory, and not-run disposition, and reject any later study whose subject binding differs by even one governed identity or raw byte.

## Decision

**CONDITIONAL PASS — IDENTITY AND PROVENANCE REGISTRATION ONLY.** The reviewed production registry contains exactly the two intended real Layer 1 candidate subjects, binds their current raw bytes exactly, keeps the subject kinds and lineages distinct, preserves product independence and no-maturity boundaries, and creates no study, finding, closeout, experiment, mechanism, or evidence effect. Acceptance remains conditional on clean final local validation, exact-head continuous integration, and steward review. This decision must not be restated as candidate adoption, scientific validation, proof, evidence, implementation readiness, or M1 completion.

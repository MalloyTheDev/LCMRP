# M1 Foundational-Subject Admission Decision — 2026-07-21

## Decision status

- **Applicable layer:** Layer 1 — Foundational Research
- **Artifact role:** Program governance decision; not a research finding or evidence record
- **Decision:** **ACCEPT EXACTLY TWO FOUNDATIONAL-SUBJECT REGISTRATIONS**
- **Mechanism evidence label:** Not applicable
- **Scientific findings asserted:** None
- **Independent validation established:** No
- **M1 completion effect:** None; M1 remains in progress
- **Product or implementation authority created:** None

This decision accepts two exact candidate-document identities and their provenance bindings. It does not adopt or validate a taxonomy, prove or validate a formal model, freeze or complete a study, publish a finding, award mechanism evidence, authorize implementation, or establish integration or production readiness.

## Admission scope

The accepted registry effect is limited to these two `ACTIVE`, version-1 Layer 1 subjects:

| Subject | Kind | Exact raw-byte SHA-256 |
| --- | --- | --- |
| `LCMRP-FSUBJ-0001-MEMORY-TAXONOMY` | `MEMORY_TAXONOMY` | `dbdc96095ae90549132e50cbb8759bc45f228cae7d8fcb9a107b95d33647ba70` |
| `LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL` | `FORMAL_MEMORY_MODEL` | `82052e424c01d3204828472ef569f74f7c0aad418f827cffda92400562bbfaf3` |

Both entries bind repository-relative Markdown artifacts using verified SHA-256 over `RAW_FILE_BYTES`, carry `NOT_APPLICABLE` mechanism-maturity applicability, and have null supersession because each is the initial registered version. The schema identifier describes the registered byte-artifact format; it does not assert that either candidate's content has passed a semantic content schema.

The foundational-study, research-finding, foundational-study-closeout, experiment, mechanism, and evidence registries must remain empty on the accepted head. No synthetic dry-run identity or result may enter a production registry.

## Review inputs

The steward reviewed:

- the exact candidate taxonomy and formal-model bytes;
- the two isolated subject-admission dossiers;
- the accepted non-evidentiary dry-run decision and its stated limits;
- the subject-registry Draft 2020-12 schema and repository semantic validation;
- a separate in-process adversarial review covering exact bindings, lineage, registry containment, claims, and product independence; and
- the repository validator and complete unit/adversarial suite on the proposed integration head.

The work was split into three non-overlapping lanes: taxonomy admission, formal-model admission, and independent verification. Each agent wrote only its assigned files. The repository steward reconciled the registry, navigation, legacy regression expectations, and this decision, then served as final reviewer, coder, and tester.

## Findings of the admission review

1. The two candidate locators resolve within the repository and their raw bytes match the admitted digests.
2. Each entry has a unique subject ID and series/version identity, the correct bounded subject kind, one active initial version, and no false supersession claim.
3. The candidates remain product-independent Layer 1 artifacts. Registration introduces no storage, retrieval, model, embedding, vendor, application, service, or product architecture.
4. The registry and dossier boundaries explicitly deny adoption, proof, validation, scientific evidence, mechanism maturity, implementation authority, and M1 completion.
5. The formal-model registration preserves every declared open proof obligation; it closes none of them.
6. Registration supplies the stable identity required to prepare later frozen studies but supplies no outcome from such a study.

## Fail-closed correction during review

The separate verification lane initially rejected the integration draft because the two dossier specimens and registry draft used different `schema_id`, name, definition, and boundary values. That was a real cross-binding defect. The originating agents revised only their own dossiers to add an explicit final reviewed binding, and the steward required exact agreement before acceptance. The earlier proposals remain visible as review history but are expressly superseded by each dossier's final binding for this admission.

This correction documents that the review gates detected one integration defect. It is not research evidence and does not show that every possible registry, scientific, security, or governance defect has been detected.

## Validation disposition

Publication is conditional on all of the following passing on the exact final pull-request head:

- `python tools/validate_repository.py`;
- `python -m unittest discover --start-directory tests --verbose`;
- JSON Schema Draft 2020-12 validation of the complete foundational-subject registry;
- exact digest, locator, identity, kind, series/version, status, and dossier cross-binding checks;
- adversarial mutations for digest substitution, kind swap, path escape, duplicate active lineage, false validation/adoption/completion claims, and accidental study or evidence entries; and
- GitHub Actions for the exact reviewed commit.

Exact command results, test counts, pull-request identities, commit hashes, and completed Actions runs are bound below where they can be known without self-reference. The final integration head and its Actions run are pinned in pull request #12 and in the merge operation's expected-head check: embedding the commit that contains this paragraph, or the workflow run created by that commit, inside the same commit would be self-referential.

## Publication record

- Taxonomy admission: [pull request #10](https://github.com/MalloyTheDev/LCMRP/pull/10), reviewed head `755c88026dce50f469abaa9cdfbc21286ecd64b7`, [Actions run 29867620226](https://github.com/MalloyTheDev/LCMRP/actions/runs/29867620226) passed, squash merge `ac6b805c07931e6526926a3a54f73606c684c715`.
- Formal-model admission: [pull request #11](https://github.com/MalloyTheDev/LCMRP/pull/11), reviewed head `ca47a3633edefc0a2a93314ceddafbe7bcbb0f65`, [Actions run 29867754846](https://github.com/MalloyTheDev/LCMRP/actions/runs/29867754846) passed, squash merge `a9ed9d988f32a9fa60c6995c8100b9399c787db1`.
- Subject-admission integration: [pull request #12](https://github.com/MalloyTheDev/LCMRP/pull/12), branch `agent/m1-subject-admission-integration`, base `a9ed9d988f32a9fa60c6995c8100b9399c787db1`, initial reviewed integration commit `9f5cdf84acce85cffebfffddf8afe72cc7b96fcc`. The final binding commit, exact-head Actions run, and merge result are recorded in the pull request and merge history under an expected-head check.
- Exact local validation on the publication content: repository validator passed; complete unit/adversarial suite passed 130/130; dedicated subject-admission suite passed 12/12; Python compilation passed; `python -m pip check` reported no broken requirements; both candidate SHA-256 values matched the registry.

## Limitations and open obligations

- These are originating, agent-assisted, repository-local reviews, not independent scientific validation.
- A cryptographic digest establishes byte identity, not truth, authorship, semantic quality, completeness, safety, security, or usefulness.
- Draft 2020-12 and semantic registry validation establish contract conformance only.
- The taxonomy's competing organizations, boundary cases, necessary conditions, sufficiency claims, and coverage remain unevaluated by a frozen study.
- The formal model is not machine-checked and retains every declared consistency, satisfiability, entailment, authority, provenance, time, conflict, deletion, and realizability obligation.
- No empirical, computational, human-subject, latency, storage, compute, token-cost, robustness, security-effectiveness, or deletion-effectiveness result is created.
- The subject-registration prerequisite alone does not satisfy the first M1 exit criterion because no required frozen study has yet evaluated and bound these versions.

## Remaining M1 work

The next authorized increment is to prepare and separately review one structural/taxonomy protocol and one formal-analysis protocol against these exact registered subject versions. Each protocol must be frozen before result access, declare all planned atomic analyses and rejection rules, preserve negative and null outcomes, and create no claim beyond the applicable Foundational Study Contract profile.

## Final judgment

**Accept exactly the two bounded foundational-subject registrations, conditional on the exact-head validation and publication record above.** The admission makes two candidate artifacts addressable for governed Layer 1 study. Nothing in this decision adopts a candidate, resolves a scientific question, awards evidence, authorizes implementation, changes product architecture, or completes M1.

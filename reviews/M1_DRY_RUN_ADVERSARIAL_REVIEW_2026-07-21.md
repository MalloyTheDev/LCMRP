# M1 Dry-Run Adversarial Review — 2026-07-21

## Review classification

- **Applicable layer:** Program infrastructure supporting Layer 1 — Foundational Research
- **Review scope:** The isolated synthetic dry-run bundles under `examples/m1-dry-runs/taxonomy/` and `examples/m1-dry-runs/formal-analysis/`
- **Verdict:** **CONDITIONAL PASS**
- **Research evidence created:** None
- **Independent validation established:** No
- **Mechanism evidence labels awarded or changed:** None
- **M1 completion established:** No

This is an internal adversarial review of serialization and governance behavior. It is not a research finding, replication, scientific validation, external review, or acceptance of either candidate subject. The pass is conditioned on the same exact bytes passing repository validation and exact-head continuous integration before steward acceptance.

## Independence and write boundary

The taxonomy and formal-analysis bundles were authored in separate work areas. The verification arm treated both authored directories as read-only and wrote only this review and `tests/test_m1_dry_runs.py`. It did not repair either bundle. No external product repository was inspected or modified, and no product-specific content appears in either dry-run tree.

## Objects reviewed

| Bundle | Exact governed subject | Method profile | Planned analyses | Published atomic records | Closeout rows |
| --- | --- | --- | ---: | ---: | ---: |
| `taxonomy/` | `MEMORY_TAXONOMY` synthetic dry-run subject 9901 | `STRUCTURAL_OR_TAXONOMY_EVALUATION` | 2 | 2 | 2 |
| `formal-analysis/` | `FORMAL_MEMORY_MODEL` synthetic dry-run subject 9902 | `FORMAL_ANALYSIS` | 2 | 2 | 2 |

Each bundle contains one local active subject version, one active frozen study version, exactly one active published atomic record for each planned analysis, and one active published closeout. The local closeout analysis-ID set equals the frozen manifest analysis-ID set. All eight schema-backed records and indexes in each bundle validate against the applicable JSON Schema Draft 2020-12 contract.

The `ACTIVE`, `FROZEN`, `PUBLISHED`, and `COMPLETED` values occur only inside isolated synthetic fixture lifecycles. They do not populate production registries or assert that a real study, scientific claim, candidate taxonomy, or formal memory model has been completed or validated.

## Adversarial attacks

`tests/test_m1_dry_runs.py` applies graph-level checks and then proves that representative corruptions are rejected. No test relies on word count.

| Attack | Mutation | Required rejection |
| --- | --- | --- |
| Raw-byte digest substitution | Replaced a finding's frozen-manifest SHA-256 value while retaining the referenced locator | Rejected as a raw-byte SHA-256 mismatch and exact binding mismatch |
| Cross-bundle identity substitution | Inserted the formal subject reference into a taxonomy finding | Rejected as an exact subject identity and definition-artifact mismatch |
| Missing disposition | Removed one closeout row | Rejected because the closeout set no longer equals the planned analysis set |
| Duplicate disposition | Reused one closeout analysis row and finding | Rejected for duplicate analysis disposition and terminal-finding reuse |
| Extra disposition | Added an unplanned synthetic analysis row | Rejected because the closeout contains an analysis absent from the frozen plan |
| Profile-kind substitution | Changed a finding from its selected profile to the other accepted profile kind | Rejected as an exact profile binding mismatch |
| False completion rhetoric | Replaced a bounded finding statement with a claim that the research study was successfully completed and established a real finding | Rejected as a false completed-study claim |
| Production-registry contamination | Inserted a dry-run entry into the in-memory production foundational-study registry | Rejected because dry runs must leave all production registries empty |
| Multiple active versions | Added a second active study-index entry for the same record identity | Rejected by the one-active-version gate |

Positive gates additionally verify:

- every schema-backed record against its existing Draft 2020-12 schema;
- every populated local `RECORDED` or `VERIFIED` SHA-256 reference against exact raw file bytes;
- index registry type, artifact type, schema ID, normalized bundle-local target path, target identity, target version, lifecycle state, and raw-byte digest;
- exact study, subject, profile artifact, analysis ID/mode, finding, and closeout bindings;
- one and only one terminal atomic record for each planned analysis;
- closeout set equality and unique finding use;
- one active version for each indexed record and foundational subject;
- explicit synthetic and non-evidentiary boundaries for records and claims;
- false human-subject and participant-data flags, no mechanism maturity effect, and empty awarded-label lists;
- no named-product, vendor, model, storage, application, or product-architecture binding; and
- unchanged empty production mechanism, experiment, evidence, foundational-subject, foundational-study, finding, and closeout registries.

## Validation results

All commands ran from the repository root with the pinned development packages made available through `PYTHONPATH=.venv/lib/python3.12/site-packages`.

| Check | Result |
| --- | --- |
| Dedicated adversarial dry-run suite | **13/13 passed** |
| Full unit and adversarial suite | **118/118 passed** |
| Repository validator | Passed |
| Taxonomy bundle-native verifier | Passed; 8 schema-backed objects, 23 recorded local digests, 2/2 terminal ledger rows, zero mechanism labels |
| Formal-analysis bundle-native verifier | Passed; 8 schema-backed objects, all recorded local digests, complete four-valuation replay, 2/2 terminal ledger rows, zero mechanism labels |
| Python compilation check | Passed |
| Installed-package consistency (`pip check`) | Passed |
| Targeted credential-pattern scan | No match |

No blocker remained after distinguishing two intentional bundle conventions from defects: isolated record-index paths resolve relative to their bundle roots, while immutable artifact locators resolve from the repository root; and each bundle's local Python verifier is audit support, not a memory mechanism or product dependency.

## Security, privacy, and governance observations

- Both manifests declare no human subjects and no human participant data; all source records repeat the non-human boundary.
- No model, embedding provider, vendor service, vector database, continuous network access, product schema, or application workflow is required.
- Local SHA-256 binding detects byte replacement but does not authenticate authorship or prevent an authorized actor from consistently replacing an artifact and every downstream digest before review.
- Synthetic authority names and deterministic timestamps exercise the record contract only. They are not an external registrar attestation.
- The formal outputs and taxonomy cases are constructed fixtures. Their retention is useful for regression testing but creates no scientific claim about memory, cognition, taxonomy quality, or formal-model correctness.

## False-positive and false-negative limits

- The topology gate requires one isolated subject registry and one study, finding, and closeout index per bundle. An equivalent differently packaged fixture could be rejected until its normalization rule is made explicit.
- Text checks detect direct completion rhetoric and named technology coupling. They may miss indirect or euphemistic claims and therefore remain paired with human review.
- Obvious structured human-data flags are enforced, but the tests are not a general privacy or personally identifiable information classifier.
- Schema conformance can accept a semantically wrong proposition, category definition, or manually encoded result if it remains internally consistent.
- SHA-256 equality proves byte identity only. It does not prove truth, provenance authority, novelty, correctness, or independent replication.
- The formal semantic replay is deterministic and complete for its four frozen valuations, but it is not an independently developed theorem prover. The taxonomy verifier checks its constructed serialization rules, not biological validity or external category utility.
- Mutation coverage is representative rather than exhaustive. Untried multi-field attacks or future schema extensions may require new gates.

## Limitations and open validation obligations

1. Neither dry run is a real registration, study, experiment, finding, replication, or independent validation.
2. The taxonomy dry run includes a tautological synthetic serialization outcome and an explicit `NOT_RUN` disposition; neither can support the candidate taxonomy.
3. The formal dry run establishes only relations inside its deliberately trivial two-atom fixture. It does not test FMO-0.1 or a memory model.
4. No external registration authority independently attested the freeze artifacts.
5. No external reviewer reproduced the record graph, semantic replay, or mutation suite.
6. Production registries must remain empty until a separately reviewed real Layer 1 proposal satisfies the accepted entry gates.
7. M1 remains in progress; this review satisfies a dry-run governance exercise only and does not satisfy all M1 exit criteria.

## Recommended next falsification step

Have a reviewer outside the originating workflow independently rebuild both record graphs from raw bytes and reimplement the formal four-valuation replay and taxonomy case adjudication without using either bundle-local verifier. Require that reviewer to introduce digest, identity, ledger-cardinality, countermodel, and claim-boundary corruptions and publish discrepancies, including null results. Until that succeeds, describe these bundles only as non-evidentiary synthetic contract dry runs.

## Decision

**CONDITIONAL PASS:** the two isolated M1 dry runs are internally coherent, fail closed under the declared adversarial mutations, preserve the program's Layer 1 and product-independence boundaries, and leave all production registries empty. Acceptance remains conditional on exact-head continuous integration and steward review. This decision creates no research evidence, mechanism maturity, independent-validation status, product recommendation, or M1 completion claim.

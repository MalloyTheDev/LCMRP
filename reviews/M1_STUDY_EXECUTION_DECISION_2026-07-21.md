# M1 Study-Execution Readiness Decision — 2026-07-21

## Decision classification

- **Applicable layer:** Layer 1 — Foundational Research
- **Artifact role:** Steward governance decision; not a study result, research finding, closeout, evidence record, or maturity decision
- **Decision:** **ACCEPT FAIL-CLOSED BLOCKAGE; DO NOT EXECUTE EITHER VERSION-1 STUDY**
- **Taxonomy study executed:** No
- **Formal configured command, `main`, or `run_kernel` invoked:** No
- **Planned outputs present:** 0 of 12
- **Findings or terminal dispositions published:** None
- **Closeouts published:** None
- **Mechanism evidence effect:** None
- **M1 completion effect:** None; M1 remains in progress

## Steward judgment

The repository may preserve and publish the taxonomy readiness review, formal preflight metadata, adversarial gates, and this decision as program-engineering records of execution readiness. It may not interpret either blocked preflight as a scientific observation about the candidate taxonomy or formal object model.

Both active version-1 preregistrations remain immutable historical records. They were frozen before result access, but later pre-execution checks established that neither can be executed under its exact commitments. The only accepted action is to stop, preserve the defects, and prepare separately reviewed digest-linked superseding records while every planned result remains absent.

## Taxonomy disposition

`LCMRP-FSTUDY-0001-M1-TAXONOMY` version 1 is `BLOCKED_NOT_RUN` for execution-readiness purposes. No taxonomy case packet, case content, peer code, planned output, or result was accessed by either the taxonomy readiness lane or the verification lane.

Execution is prohibited because:

1. the protocol and canonical manifest do not bind the same complete source-ID set;
2. the protocol pins an obsolete raw-byte digest for `docs/program/M1_FOUNDATION.md`;
3. freeze-required repository, dependency, platform, and environment identity is incomplete in the manifest or attestation;
4. the immutable execution-intake raw-byte digest lacks a defined non-self-referential scope and external binding contract;
5. no immutable intake identifies two eligible primary human adjudicators and a separate eligible human tie adjudicator with attributable eligibility, isolation, conflict, and no-prior-result-access declarations; and
6. the package's attestation and lifecycle descriptions do not fully match the bound artifact contents.

Agents must not be substituted for the required human adjudicators. Taxonomy execution may be reconsidered only after a version-2 study record corrects the immutable metadata and intake contract and three eligible people are assigned under a reviewed intake. The version-1 protocol, manifest, and bound inputs must not be rewritten.

## Formal-model disposition

`LCMRP-FSTUDY-0002-M1-FORMAL-MODEL` version 1 is `BLOCKED_NOT_RUN` for execution-readiness purposes. The formal lane resolved the exact public snapshot, manifest, inputs, tool, runtime, and absent output path. Before invoking the configured analyzer command, it found that the frozen `verify_manifest_index` helper requires eight leading spaces before `artifact_digest.value`, while the accepted schema-valid canonical registry uses six. A direct guard-only probe raised:

```text
StudyGuardError: canonical index entry lacks artifact_digest.value
```

The configured command, `main`, `run_kernel`, model enumeration, and result serialization were never invoked. The error is a provenance-guard implementation defect, not a satisfiability, consistency, entailment, non-entailment, invariant, authority, deletion, or semantic result.

The analyzer's bytes are digest-bound by the frozen version-1 manifest. Repair therefore requires a version-2 tool and study record linked by supersession, an independent freeze review, and a fresh preflight while all seven result paths remain absent. Editing the frozen tool in place is prohibited.

## Three-lane separation and review scope

The increment was intentionally divided into non-overlapping work products:

| Lane | Exclusive output | Scope limit |
| --- | --- | --- |
| Taxonomy readiness | `M1_TAXONOMY_EXECUTION_READINESS_2026-07-21.md` | Non-case metadata only; no intake, case access, output, or registry edit |
| Formal preflight | Two files under `m1-formal-model-v1/execution/` | Guard preflight only; no configured analyzer or result |
| Adversarial verification | `test_m1_study_execution.py` and `M1_STUDY_EXECUTION_ADVERSARIAL_REVIEW_2026-07-21.md` | Tests and review only; no study-package repair |

The root steward alone reconciled navigation, validator requirements, milestone status, and this decision. That role separation is an internal engineering control, not independent scientific validation.

## Validation accepted

- repository validator: passed;
- dedicated execution-readiness suite: 24/24 passed;
- complete repository suite: 168/168 passed;
- dependency consistency: passed, with no broken requirements;
- syntax compilation: passed for the repository validator, frozen formal analyzer, and execution-readiness tests without invoking the analyzer;
- all five taxonomy outputs and all seven formal outputs: absent;
- research-finding and foundational-closeout registries: empty; and
- frozen version-1 manifest digests: unchanged.

These checks establish truthful containment and repository conformance only. They do not establish scientific correctness, contributor independence, result validity, candidate adoption, formal proof, replication, external validation, mechanism maturity, or product readiness.

## Publication record

1. Taxonomy readiness: PR [#16](https://github.com/MalloyTheDev/LCMRP/pull/16), exact reviewed head `b4a6269c5da4eefcfb91e0e00af94a8717909cef`, successful Actions run [29873632380](https://github.com/MalloyTheDev/LCMRP/actions/runs/29873632380), squash merge `bfa1216694b16a888ca515f0701b2addcae09396`.
2. Formal preflight: PR [#17](https://github.com/MalloyTheDev/LCMRP/pull/17), exact reviewed head `14a3052f7d78c79f7769895325d32d9f519ca9b1`, successful Actions run [29873774211](https://github.com/MalloyTheDev/LCMRP/actions/runs/29873774211), squash merge `ebaee2ce50093f27395f15850a973aaf9d0af2b9`.
3. Verification, integration, and this decision: PR [#18](https://github.com/MalloyTheDev/LCMRP/pull/18), initial byte-checked head `db6aa97b9d14366c7d81c6068e2ed1becf64a835`. Clean-checkout run `29874337035` exposed a verifier portability defect and failed; the correction is preserved in the adversarial review. The final decision-bound head and exact-head Actions run are recorded in that pull request because embedding a commit hash in the commit itself would be self-referential.

## Next governed work

1. Publish a taxonomy version-2 repair package and a formal version-2 repair package through separate review boundaries; do not combine repair with execution.
2. Create superseding canonical records and registry entries that preserve active-version uniqueness and exact version-1 lineage.
3. Re-run all freeze and execution-readiness gates with every planned output still absent.
4. For taxonomy only, recruit the three eligible human contributors and create the reviewed immutable intake after metadata repair.
5. Authorize execution, if at all, in a later explicit increment. Preserve negative, null, contradictory, halted, invalid, and not-run outcomes as required by the Foundational Study Contract.

## Boundary confirmation

No storage system, model provider, embedding provider, vector database, application schema, memory service, or product architecture was selected or implemented. CorpusStudio was not inspected or modified.

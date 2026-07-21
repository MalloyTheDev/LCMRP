# M1 Study-Execution Adversarial Review — 2026-07-21

## Review classification

- **Applicable layer:** Layer 1 — Foundational Research
- **Artifact role:** Program verification infrastructure; not a research finding, execution result, evidence record, or closeout
- **Reviewed increment:** Taxonomy execution readiness and formal Analysis 01 machine-execution preflight
- **Verdict:** **PASS FOR FAIL-CLOSED BLOCKAGE ONLY — BOTH STUDIES NOT RUN**
- **Taxonomy analysis executed:** No
- **Formal `main` or `run_kernel` invoked:** No
- **Planned result artifacts created:** None
- **Atomic findings or terminal dispositions published:** None
- **Mechanism evidence or maturity effect:** None
- **M1 completion effect:** None; M1 remains in progress

This review accepts the truthfulness and containment of two blocked pre-execution
states. It does not accept either study as execution-ready, treat a preflight
failure as a scientific result, prove that either candidate is valid, or convert
`BLOCKED_NOT_RUN` into an immutable `NOT_RUN` or `HALTED` finding. The frozen
study manifests remain unchanged and active; their newly discovered execution
blockers require separately governed supersession rather than in-place repair.

## Independence and write boundary

The verification lane wrote only this review and
`tests/test_m1_study_execution.py`. It did not edit either study package, frozen
manifest, registry, readiness artifact, runtime artifact, finding, closeout,
milestone document, or navigation file. Defects were reported to the root
steward rather than repaired across lane boundaries.

The taxonomy authoring lane wrote only its readiness review. The formal lane
wrote only its preflight attestation and runtime-provenance record. Publication
and any shared integration changes remain the root steward's responsibility.

## Access boundary

### Taxonomy cases

This verification lane did not open, parse, search, hash, render, summarize, or
pass to another process any file under
`studies/foundational/m1-taxonomy-v1/cases/`. Its tests deliberately skip those
bytes. Only case locators, declared artifact identities, manifest-held digests,
counts, and path absence were observed in non-case metadata.

The taxonomy readiness lane likewise reports that it did not access case
contents. Separately, the root steward ran the repository-wide suite, whose
legacy freeze tests read and hash the already frozen case artifacts. The root
steward is the freeze authority and is explicitly ineligible to adjudicate this
study. That verification access therefore does not fabricate an eligible
adjudicator, satisfy the missing intake, or create an eligible-adjudicator
exposure. It must not be restated as blinded case adjudication.

### Formal analysis

The verification lane inspected only the two stable formal execution metadata
artifacts, the already frozen formal metadata/tool inputs, and result-path
absence. To reproduce the blocker, it imported the frozen analyzer and invoked
only `verify_manifest_index`. It did not invoke `main`, `run_kernel`, valuation
enumeration, result serialization, or the configured analyzer command. All
seven planned formal result paths remained absent before and after the probe.

## Exact reviewed artifacts

| Artifact | Role | Raw-byte SHA-256 at review |
| --- | --- | --- |
| `reviews/M1_TAXONOMY_EXECUTION_READINESS_2026-07-21.md` | Taxonomy non-case readiness review | `8ba23de9f72fc2bf33f1402f87d14479e4b9c0212ff3792a58060df6c82101ce` |
| `studies/foundational/m1-formal-model-v1/execution/preflight-execution-attestation.json` | Formal guard-preflight attestation | `c3dcbf87d8c23a28ebbe377c3fe2300b9110bf17136c09f1855a8be380f62fc5` |
| `studies/foundational/m1-formal-model-v1/execution/runtime-provenance.json` | Formal no-run runtime provenance | `2063dee7d84f800310536d379985833aa2d64e3d612658cb18e2ddf812fba6cf` |
| `tests/test_m1_study_execution.py` | Independent execution/adversarial gate | `3d08d79781e82bf73a39e01e2cd5094bda2f19ae98255f59fa2f19f27d94420d` |

The frozen taxonomy and formal manifest digests remain respectively
`01640e8dae3836874b2b39fe3ea2a8f9c090374508aa69b31adf06fea9272139`
and
`b99da2d9cfa34d659416fe30cc1d3fa731425d1fcfb8b6c9422cd9b5add2707e`.
No frozen v1 byte was changed by this increment.

The three new readiness/runtime artifacts are not scientific records and are
not indexed as findings or closeouts. Their table digests support this review's
local byte identification only; repository history and the final reviewed pull
request must provide publication immutability.

## Taxonomy readiness judgment

### Confirmed safe state

- The canonical study remains `ACTIVE` and `FROZEN`.
- `execution/execution-intake.json` is absent.
- No stable contributor assignment exists.
- All five planned output paths are absent.
- The research-finding and foundational-closeout registries remain empty.
- No taxonomy case coding, packet generation, agreement calculation, finding,
  closeout, or result interpretation occurred.
- The readiness review says `BLOCKED — DO NOT START TAXONOMY EXECUTION` and
  makes no affirmative validation, proof, maturity, product, or M1-completion
  claim.

### Independently reproduced hard blockers

| ID | Observation | Classification and required treatment |
| --- | --- | --- |
| B1 | No two eligible primary human adjudicators, separate eligible human tie adjudicator, attributable declarations, or immutable intake exist. | **Hard execution blocker.** Do not substitute agent IDs or bare strings. Recruit eligible contributors only after the frozen metadata is repaired. |
| B2 | The frozen protocol declares seven source IDs, while the canonical manifest declares five. `SOURCE-M1-FOUNDATIONAL-CONTRACT` and `SOURCE-M1-MILESTONE` are protocol-only. | **Hard execution blocker.** The protocol requires set equality before coding. Preserve v1 and create a disclosed superseding record. |
| B3 | The protocol pins `docs/program/M1_FOUNDATION.md` at `473ea1b4…8654b6`; the mutable current-status document is recomputed at validation time and does not match that frozen digest. | **Hard execution blocker.** Do not select convenient current bytes or rewrite the frozen protocol. Preserve or supersede the exact source binding. |
| B4 | The bound environment requires an exact repository revision, dependency-file digest, platform details, and environment digest in the manifest or attestation. The lockfile digest, concrete platform details, and exact freeze-integration revision are absent there. | **Hard execution blocker under the frozen environment requirement.** A later intake cannot retroactively satisfy a freeze-location obligation. |
| B6 | The configuration requires a raw-byte SHA-256 over the immutable intake but defines no external receipt/index or non-self-referential digest scope and supplies no schema/template. | **Hard intake-creation blocker.** Define and review a separate immutable binding before an intake can be valid. |

The tests reject fabricated and placeholder contributor IDs, repeated role
identities, missing eligibility/isolation declarations, unverified contributor
provenance, case/output access without an intake, and premature findings or
closeout records.

### Documentation and lifecycle inconsistencies

These discrepancies require explicit steward disposition and should be repaired
through supersession, but this review distinguishes them from the independently
sufficient actor, source-set, stale-digest, freeze-metadata, and intake-contract
hard blockers above:

1. The package README says the freeze attestation contains an artifact
   inventory and raw-byte digest ledger. The attestation contains identity,
   authority, counts, absence, and claim-boundary metadata, while the actual
   artifact/digest bindings reside in the canonical manifest.
2. The exact method profile, category rules, configuration, and environment
   bytes bound by the frozen manifest each self-declare
   `artifact_status: DRAFT_FREEZE_INTENT`. External manifest binding makes the
   bytes immutable, but their lifecycle wording conflicts with an unqualified
   description of finalized operational inputs.

These are not scientific findings about the taxonomy. They are contract and
documentation defects that reinforce the decision not to execute the current
record.

## Formal execution judgment

### Confirmed preflight state

The two formal execution metadata files agree on the exact study, record,
analysis, frozen manifest, tool, input digests, CPython 3.12.13 runtime,
configured command, result locator, and public-snapshot identifiers. The
verification lane recomputed the registry, manifest, eleven immutable-reference,
configuration, analyzer, and formal input digests against local bytes. It also
confirmed the following:

- status is `BLOCKED_NOT_RUN` / `NOT_RUN_BLOCKED_DURING_GUARD_PREFLIGHT`;
- configured analyzer invocation count is zero;
- `run_kernel` invocation count is zero;
- no model, dataset, external solver, network call, cloud call, or storage
  service was used by the analyzer;
- no output was copied into the shared workspace;
- analysis duration, compute, and output digest correctly remain null/not
  measured; and
- all seven planned output paths are absent.

The public commit, Git tree, and tracked-inventory values are internally
consistent across the two records. This lane did not have Git metadata in the
shared checkout and therefore did not independently reconstruct the claimed
170-entry public tree or repeat the remote lookup. Those snapshot claims remain
formal-lane provenance, not independently authenticated facts in this review.

### Independently reproduced guard failure

An independent YAML parse resolves exactly one active formal study entry and
its manifest digest matches the canonical manifest bytes. The canonical YAML
line containing `artifact_digest.value` has six leading spaces, consistent with
its nesting:

```text
      value: b99da2d9cfa34d659416fe30cc1d3fa731425d1fcfb8b6c9422cd9b5add2707e
```

The frozen analyzer's `verify_manifest_index` helper searches the entry body
with a regular expression requiring eight leading spaces before `value`.
Calling that guard directly produced exactly:

```text
StudyGuardError: canonical index entry lacks artifact_digest.value
```

The failure occurs before the analyzer can reach `run_kernel`. It is therefore
a fail-closed provenance-guard defect, not an observation that any module is
satisfiable or unsatisfiable and not evidence about an entailment,
non-entailment, invariant, authority rule, deletion rule, or semantic mapping.

The frozen analyzer is digest-bound through the active v1 manifest. Editing its
regex in place would violate the exact preregistration. The required treatment
is a pre-result, digest-linked superseding study/tool record, independent
review, a new freeze, and a complete preflight with all outputs still absent.

### Downstream containment

Analyses 02 through 07 remain absent. Even after a future corrected machine
run, no analysis-scoped interpretation may be published without the protocol's
two independently fixed source-to-encoding mappings, retained disagreement,
and adjudication. Tests reject substituted result paths, overwrites, mismatched
input provenance, missing semantic-review blockers, false proof/validation or
maturity language, product coupling, and missing/duplicate negative, null,
counterexample, invariant-omission, or named-countermodel rows.

Because no raw output exists, the row-retention gates were exercised against
adversarial structural fixtures, not against observed study values. No result
value or scientific disposition is asserted by those mutation tests.

## Adversarial test coverage

The 24-test execution suite covers:

1. exact frozen manifest, non-case taxonomy input, formal input, tool, and
   analyzer byte bindings;
2. truthful taxonomy blockage with no intake, output, finding, or closeout;
3. fabricated/placeholder contributor IDs and unverified identity provenance;
4. case or output access without a valid intake;
5. protocol/manifest source-set divergence;
6. the stale M1 milestone digest;
7. environment-mandated freeze metadata gaps;
8. attestation-inventory and bound-component lifecycle inconsistencies;
9. non-self-referential intake digest requirements;
10. formal result absence or exact-path containment;
11. substituted paths, overwrite attempts, and digest/provenance mismatch;
12. prohibition of analyses 02–07 before two independent semantic mappings;
13. false proof, validation, maturity, completion, production-readiness, and
    product-coupling claims;
14. mandatory retention of every module, entailment, non-entailment,
    invariant-omission, named-countermodel, null, negative, and contradictory
    row shape;
15. exact formal preflight/runtime consistency and runtime/service boundaries;
16. direct reproduction of the frozen index-guard failure without executing
    the analysis; and
17. absence of all seven formal results after the failure.

The mutation set is representative, not exhaustive. It does not prove that a
future intake schema, superseding tool, semantic mapping, scientific result, or
human declaration is correct.

## Validation evidence

| Check | Result |
| --- | --- |
| Dedicated `tests.test_m1_study_execution` suite after both lanes stabilized | **24/24 passed** |
| Syntax compilation of `tools/validate_repository.py`, the frozen formal analyzer, and `tests/test_m1_study_execution.py` | Passed |
| Dependency consistency (`python -m pip check`) | Passed; no broken requirements |
| Root repository-wide suite before the latest ten taxonomy/formal gates | **158/158 passed** |
| Final repository validator | Passed |
| Final repository-wide rerun including all 24 execution gates | **168/168 passed in 2.946 seconds** |

The verification lane intentionally did not run the repository-wide suite
after the explicit no-taxonomy-case-access instruction because legacy freeze
tests read/hash those case bytes. The root steward's prior 158-test run did so
under the access distinction documented above, and the root steward performed
the final 168-test rerun under the same distinction. These passing repository
checks establish contract and integration conformance only; they do not create
an eligible taxonomy adjudicator or a scientific result.

`docs/program/M1_FOUNDATION.md` is mutable milestone-status navigation. Test 16
therefore pins only the exact digest declared by the frozen protocol, recomputes
the current file digest on every run, validates its lowercase 64-hex form, and
requires inequality. It deliberately does not hard-code the mutable current
digest. The taxonomy readiness review's earlier current-digest value remains a
time-bounded observation from that lane, not a permanent identity claim.

## Limitations and open obligations

1. Neither study executed. There is no scientific result, finding, closeout,
   replication, evidence state, adoption decision, or M1 completion basis.
2. Taxonomy v1 cannot proceed without metadata supersession and three eligible,
   attributable human contributors under a reviewed immutable intake contract.
3. Formal v1 cannot proceed without a digest-linked superseding tool/study
   record that corrects the fail-closed index guard before any result access.
4. Two independent formal semantic mappings and adjudication remain absent.
5. Taxonomy case bytes were not independently inspected or hashed by this lane;
   their scientific content and present digest correctness are not conclusions
   of this review.
6. Formal runtime snapshot/remote claims were cross-record checked but not
   independently reconstructed from Git by this lane.
7. The new preflight/runtime JSON artifacts have no dedicated JSON Schema or
   production registry. Tests constrain their current shape, but they are
   governance metadata rather than immutable scientific findings.
8. SHA-256 comparison detects byte substitution relative to a recorded digest;
   it does not authenticate authorship, establish semantic correctness, or
   prove contributor independence.
9. Internal agent-assisted review is not independent scientific validation.
10. Final exact-head CI and three-PR publication remain external obligations.
11. Mutable milestone-status navigation can change during integration; only the
    frozen protocol's declared digest is stable, while current bytes must be
    recomputed rather than pinned by the execution test.

## Recommended next governed increments

1. Publish the taxonomy readiness review alone and preserve the blocked state.
2. Publish the formal preflight/runtime provenance alone and preserve every
   absent result path.
3. Publish this verification suite/review and a root steward decision in a
   third PR after final full-suite and exact-head validation.
4. Design a taxonomy v2 supersession that reconciles source identity, stale
   source bytes, freeze metadata, inventory/lifecycle wording, and an external
   intake digest receipt before recruiting adjudicators or opening cases.
5. Design a formal v2 supersession that binds a corrected parser-based or
   indentation-correct guard, then replay the complete preflight before one
   exact analyzer invocation.

Do not combine either repair with result production. Pre-result supersession,
review, freeze, and output-absence confirmation must finish first.

## Final judgment

**PASS FOR FAIL-CLOSED BLOCKAGE ONLY — BOTH STUDIES NOT RUN.** The taxonomy lane
correctly refused to invent contributors or access cases in the presence of
actor, source, digest, freeze-metadata, lifecycle, and intake-contract blockers.
The formal lane correctly stopped at a reproducible frozen index-guard defect
before invoking the analyzer or creating a result. The reviewed state preserves
all frozen bytes, all twelve planned outputs remain absent, result/finding and
closeout registries remain empty, mechanism maturity remains not applicable,
and M1 remains in progress.

This verdict must not be restated as successful taxonomy execution, a formal
`NOT_RUN`/`HALTED` finding, a satisfiability result, proof, validation, evidence,
product integration authority, production readiness, or M1 completion.

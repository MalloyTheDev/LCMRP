# M1 taxonomy structural-study package v1

Applicable layer: Layer 1 — Foundational Research  
Package status: `FROZEN PREREGISTRATION` / `BLOCKED_NOT_RUN` / `REQUIRES_SUPERSESSION`  
Study: `LCMRP-FSTUDY-0001-M1-TAXONOMY`  
Study record: `LCMRP-FSTUDYREC-0001-M1-TAXONOMY@1`  
Primary profile: `LCMRP-MPROF-0001-M1-STRUCTURAL-TAXONOMY@1`  
Subject: `LCMRP-FSUBJ-0001-MEMORY-TAXONOMY@1`  
Mechanism evidence labels: Not applicable

This directory retains the reviewed draft history and the separately frozen preregistration for a mechanism-free structural evaluation of the exact registered Candidate Memory Taxonomy v0.1. It contains the immutable protocol and freeze attestation alongside the non-authoritative draft manifest, operational method profile, category-evaluation rules, constructed case sources, and reproducibility declarations.

The frozen protocol and attestation establish preregistration only. Nothing in this directory is an execution record, finding, closeout, validation, adoption decision, evidence award, or implementation recommendation. No planned analysis has been run. No result or expected favorable outcome is encoded in the case artifacts. The words `positive`, `negative`, and `held-out` identify source roles required by the study contract; they do not state how a case will be classified.

## Exact subject binding

The only subject under study is:

- subject ID: `LCMRP-FSUBJ-0001-MEMORY-TAXONOMY`;
- subject series: `LCMRP-MEMORY-TAXONOMY`;
- subject version: `1`;
- locator: `docs/taxonomy/MEMORY_TAXONOMY_v0.1.md`;
- raw-byte SHA-256: `dbdc96095ae90549132e50cbb8759bc45f228cae7d8fcb9a107b95d33647ba70`; and
- digest scope: `RAW_FILE_BYTES`.

Registration fixes identity and provenance only. This package does not adopt the registered candidate.

## Contents

- `protocol-draft.md` — complete DRAFT protocol using the Foundational Study Contract reporting structure.
- `manifest-draft.json` — non-authoritative DRAFT study manifest; local freeze-intent artifacts deliberately retain `PENDING` digests until final review. It is neither a canonical record nor eligible for the production study index.
- `protocol-v1.md` — immutable `FROZEN` protocol derived from the reviewed draft without rewriting draft history.
- `freeze-attestation.json` — authority, timestamp, author-package revision, no-prior-result-access assertion, and absent-output inventory.
- `definitions/method-profile.json` — versioned structural/taxonomy method definition and adjudication contract.
- `definitions/category-evaluation-rules.json` — exact term scope, competency questions, organizations, distinctions, integrity constraints, and coding semantics.
- `cases/positive-cases.json` — constructed development cases that expose declared distinctions without expected dispositions.
- `cases/negative-cases.json` — constructed constraint-challenge cases without expected dispositions.
- `cases/held-out-cases.json` — constructed held-out and adversarial cases that must not be used to amend rules after freeze.
- `reproducibility/environment.json` — runtime, dependency, locale, network, and human-analysis environment requirements.
- `reproducibility/configuration.json` — evaluator isolation, deterministic case ordering, metrics, output, and retention configuration.

The five planned output locators under `outputs/` do not exist. Creating an output outside a separately governed execution increment is an integrity failure, not progress.

## Execution-readiness disposition

The [non-case execution-readiness review](../../../reviews/M1_TAXONOMY_EXECUTION_READINESS_2026-07-21.md) blocked version-1 execution before any taxonomy case packet or case content was accessed. It identified independently sufficient blockers: the protocol and manifest source sets disagree; the protocol's M1 milestone digest is stale; freeze-required repository, dependency, platform, and environment bindings are incomplete; the intake digest contract is undefined; and no immutable intake names two eligible primary human adjudicators plus a separate eligible human tie adjudicator.

The review also found that the freeze attestation does not itself contain the artifact/digest inventory described below and that several bound operational inputs retain `DRAFT_FREEZE_INTENT` lifecycle wording. The active frozen record remains an immutable provenance object, but it is not execution-ready. No agent identity may substitute for the required humans. Repair requires a separately reviewed, digest-linked version-2 study record before contributor assignment, case access, coding, or output creation.

A pre-result repair package under [`superseding/pre-result-metadata-intake-v2/`](superseding/pre-result-metadata-intake-v2/) records version-2 obligations for blockers B2–B6 and the external intake-digest contract. That package is **not frozen**, **not registered**, and **not execution authority**. Residual human-contributor blocker B1 remains open. See also [M1 taxonomy pre-result repair package review](../../../reviews/M1_TAXONOMY_PRE_RESULT_REPAIR_PACKAGE_2026-07-22.md).

## Originally recorded freeze boundary

The freeze action was intended to perform all of the following in order. The later execution-readiness review found that items 4, 6, and 7 were not fully represented in the frozen metadata and that the protocol/manifest source sets diverge. This historical checklist therefore does not authorize execution:

1. confirm that the subject registry resolves the exact subject ID, series, version, locator, and digest above;
2. assign a named freeze authority and bind the exact eligibility, isolation, and conflict criteria for later adjudicators; adjudicator identities need not and must not be invented to complete freeze;
3. confirm that no planned output exists and no result has been accessed;
4. approve the protocol, profile, category rules, cases, environment, and configuration without an unresolved placeholder;
5. compute SHA-256 directly over the raw bytes of every frozen input and replace each local `PENDING` digest in a new frozen manifest;
6. bind the exact repository revision containing those bytes;
7. create an immutable freeze-attestation artifact containing the artifact inventory, raw-byte digests, authority, timestamp, and no-prior-result-access assertion;
8. change the manifest and protocol status to `FROZEN` without altering their substantive commitments; and
9. validate the frozen manifest against JSON Schema Draft 2020-12 and independently recompute every digest.

The draft files preserve the authoring state. Any change to the frozen protocol or bound inputs requires a superseding study-record version linked to the prior raw-byte digest. Confirmatory analysis may begin only after a corrected version is independently reviewed and frozen and its execution-intake requirements are satisfied.

## Execution boundary

After a valid freeze, evaluators may execute only the five predeclared analysis IDs. Each analysis must eventually receive exactly one active atomic finding or terminal disposition: `COMPLETED`, `NOT_RUN`, `HALTED`, or `INVALID`. A closeout may be published only when its analysis-ID set is exactly equal to the frozen manifest's set.

Before any case packet, peer code, planned output, or result is accessed, an immutable execution-intake artifact must bind the exact frozen study record and digest; name two primary adjudicators and one tie adjudicator using stable contributor IDs; record each role's eligibility, isolation, and conflict declarations; assert no prior result access; and receive a raw-byte digest and timestamp. The assigned contributors must remain traceable in the later finding provenance. Protocol authors and the freeze authority are ineligible to adjudicate.

Case-set roles, selection rationales, and file paths are hidden from primary adjudicators during initial coding. A deterministic pseudonym and ordering procedure is declared in the configuration. Independent codes and rationales are locked before reconciliation. Disagreements, ambiguity, null outcomes, protocol deviations, invalid work, and non-execution are retained.

## Integrity checks that are not analyses

The following checks are design-time integrity checks, not planned analyses or findings:

```bash
python -m json.tool studies/foundational/m1-taxonomy-v1/manifest-draft.json
python -m json.tool studies/foundational/m1-taxonomy-v1/definitions/method-profile.json
python -m json.tool studies/foundational/m1-taxonomy-v1/definitions/category-evaluation-rules.json
python -m json.tool studies/foundational/m1-taxonomy-v1/cases/positive-cases.json
python -m json.tool studies/foundational/m1-taxonomy-v1/cases/negative-cases.json
python -m json.tool studies/foundational/m1-taxonomy-v1/cases/held-out-cases.json
python -m json.tool studies/foundational/m1-taxonomy-v1/reproducibility/environment.json
python -m json.tool studies/foundational/m1-taxonomy-v1/reproducibility/configuration.json
```

Schema conformance, successful parsing, complete files, and matching digests establish only package integrity.

## Known limitations

- Every case is synthetic and was authored from the candidate's declared distinctions and open obligations; construction and evaluation circularity remain material threats.
- The held-out set is held out from post-freeze rule development, not secret, statistically sampled, natural, representative, or externally sourced.
- Structural answerability and internally consistent coding do not establish semantic truth, completeness, usefulness, biological fidelity, safety, privacy effectiveness, or external validity.
- Human adjudication is interpretive. Blinding case roles cannot blind evaluators to the candidate or hypotheses they must apply.
- The v0.1 contract does not support human-subject, participant-data, controlled computational, empirical, or evidence-synthesis work.
- Raw-byte digests detect substitution but do not prove authorship, independence, provenance authenticity, or scientific merit.

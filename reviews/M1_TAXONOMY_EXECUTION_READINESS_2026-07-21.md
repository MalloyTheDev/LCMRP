# M1 Taxonomy Execution-Readiness Review — 2026-07-21

## Decision status

- **Applicable layer:** Layer 1 — Foundational Research
- **Artifact role:** Internal execution-readiness review; not a research finding, execution record, evidence record, or closeout
- **Decision:** **BLOCKED — DO NOT START TAXONOMY EXECUTION**
- **Study:** `LCMRP-FSTUDY-0001-M1-TAXONOMY`
- **Canonical study record:** `LCMRP-FSTUDYREC-0001-M1-TAXONOMY@1`
- **Mechanism evidence labels:** Not applicable
- **Scientific findings asserted:** None
- **Independent scientific validation established:** No
- **M1 completion effect:** None; M1 remains in progress

The taxonomy study is registered and its canonical manifest is `FROZEN`, but it is not execution-ready. No eligible adjudicators are appointed, the required post-freeze/pre-coding execution intake is absent, and the currently available agent workers cannot be substituted for the human research contributors required by the frozen environment and protocol. Independent metadata review also found source-binding and freeze-metadata inconsistencies that would make the protocol's mandatory pre-coding checks fail even if eligible personnel were later supplied.

This is a fail-closed readiness decision. It does not invalidate or reinterpret a scientific result because no taxonomy analysis has run and no result exists.

## 1. Scope and access boundary

This review was restricted to non-case metadata and procedure. It examined:

- the [Program Charter](../docs/program/PROGRAM_CHARTER_v0.1.md) and [Foundational Study Contract](../docs/program/FOUNDATIONAL_STUDY_CONTRACT.md);
- the [canonical frozen study manifest](../records/foundational/studies/LCMRP-FSTUDYREC-0001-M1-TAXONOMY-v1.json);
- the active [foundational-study registry](../registry/foundational-studies.yaml) and [foundational-subject registry](../registry/foundational-subjects.yaml);
- the frozen [taxonomy protocol](../studies/foundational/m1-taxonomy-v1/protocol-v1.md), [method profile](../studies/foundational/m1-taxonomy-v1/definitions/method-profile.json), [configuration](../studies/foundational/m1-taxonomy-v1/reproducibility/configuration.json), [environment](../studies/foundational/m1-taxonomy-v1/reproducibility/environment.json), and [freeze attestation](../studies/foundational/m1-taxonomy-v1/freeze-attestation.json);
- the exact registered [taxonomy subject](../docs/taxonomy/MEMORY_TAXONOMY_v0.1.md); and
- registry state and path existence for the planned intake, outputs, findings, and closeout.

The contents of all files below `studies/foundational/m1-taxonomy-v1/cases/` were deliberately not opened, parsed, searched, hashed, rendered, summarized, or passed to another process. Case paths, declared counts, artifact IDs, and manifest-recorded digests were observed only where they appeared in non-case metadata. The three case digests therefore were not independently recomputed by this review.

No packet-generation command, evaluator workflow, repository-wide validator, test suite, metric calculation, model inference, or analysis command was run. Path-existence checks confirmed that the future intake and all five planned outputs are absent; no result content was accessed. This access discipline preserves the frozen requirement that intake precede case-packet, planned-output, and result access.

## 2. Checks performed

### 2.1 Layer, status, and identity

| Check | Observation | Readiness effect |
| --- | --- | --- |
| Research layer | Manifest, protocol, profile, environment, and attestation identify Layer 1 foundational work. | Pass for identity; no Layer 2 or Layer 3 authority created. |
| Study state | Canonical record is `FROZEN`; study registry entry is `ACTIVE`. | Pass for preregistration identity only. |
| Subject state | `LCMRP-FSUBJ-0001-MEMORY-TAXONOMY@1` is the sole active matching subject entry. | Pass for exact subject identity only. |
| Mechanism boundary | No mechanism is under evaluation and mechanism maturity applicability is `NOT_APPLICABLE`. | Pass; no maturity label may be awarded. |
| Findings and closeout | Research-finding and foundational-closeout registries are empty. | Confirms non-execution; supplies no scientific evidence. |
| Intake and outputs | `execution/execution-intake.json`, the `execution/` directory, and all five planned output files are absent. | Correct pre-execution state, but intake absence blocks coding. |

### 2.2 Exact non-case byte bindings

Raw-byte SHA-256 was independently recomputed only for non-case artifacts. The following bindings match their authoritative registry, manifest, or protocol references:

| Artifact | Recomputed SHA-256 | Binding result |
| --- | --- | --- |
| Canonical study manifest | `01640e8dae3836874b2b39fe3ea2a8f9c090374508aa69b31adf06fea9272139` | Matches active study-registry entry. |
| Taxonomy subject | `dbdc96095ae90549132e50cbb8759bc45f228cae7d8fcb9a107b95d33647ba70` | Matches subject registry and manifest. |
| Frozen protocol v1 | `667f01d88287f04418b04ca7e549b8e13a48725f7b30262f21ce47f53e4dcb1c` | Matches manifest. |
| Freeze attestation | `fbfa5b94cc940af1ccf5e38ddf763ef93982463ca0bd8f5fb0325d4bf6e843a9` | Matches manifest. |
| Method profile | `f87a1cac0d9ad1b1bd81b53acaaea10e9320932cec4201184cbb5b6c8f3e95e0` | Matches manifest. |
| Category-evaluation rules | `391f1e6857f5c802f1ec46f74c15b583780bf11d586fd8f5b99f8b110560c282` | Matches manifest. |
| Environment | `36d7abee18605177ac8e092a4733526f8ac3fbeb0ff2918638b6e9b2fe8ae56f` | Matches manifest. |
| Configuration | `23d61b1a7a45f9239e9ee329af44455096d3c81deabc440754516e01bffdc5ac` | Matches manifest. |
| Program Charter | `bea7433324a3d5fc5b4b640bfd95840b58f3663d5b89e08f6f93714512cc9882` | Matches protocol and manifest. |
| Prior-art map | `9f9c6393d5e972c23ced935b29854581ac39bd4932361540034f482796156b4c` | Matches protocol and manifest. |
| Foundational Study Contract | `8334432023815c153879cbdeccb09df39ffe035b1c6fc9244f341ac153a3de61` | Matches the protocol-only declaration. |

These matches establish current byte identity for the reviewed non-case files. They do not establish semantic correctness, adjudicator independence, scientific validity, or readiness to execute.

### 2.3 Procedure and actor requirements

The frozen materials agree on the following execution gate:

1. execution uses **local human structural adjudication** and no language-model inference;
2. two eligible primary adjudicators independently code all required cells;
3. one separate eligible tie adjudicator receives only unresolved disagreements after both primary ledgers are locked;
4. protocol, profile, rule, or case authors and the freeze authority are ineligible for all three adjudicator roles;
5. the three role assignments, stable contributor IDs, declarations, exact manifest binding, execution authority, timestamp, and no-prior-result-access assertion must be captured in an immutable intake before any case packet, output, or result access; and
6. every later finding or terminal disposition must preserve the intake and contributor provenance.

The frozen protocol explicitly records `Adjudicators: None appointed at freeze`. No later intake or role-assignment record exists. The agent workers available in the present workflow are not eligible substitutes: the environment requires human adjudication and explicitly states that no language model participates. This review does not invent human identities, equate agent IDs with contributor IDs, or infer that the user or any other person satisfies authorship, conflict, isolation, or prior-access requirements.

## 3. Blocking findings

### B1 — Required human adjudicators and immutable intake are absent

**Status:** Blocking.

There is no evidence of two eligible primary human adjudicators and one distinct eligible human tie adjudicator. There are no stable contributor IDs, attributable eligibility declarations, conflict disclosures, isolation commitments, or prior-access declarations. The required intake path is absent.

The study cannot truthfully start with the actors currently represented in the repository or this agent workflow. Creating case packets, opening case content for adjudication, creating a planned output, or beginning coding before a valid intake would violate the frozen sequence.

### B2 — Protocol and canonical manifest declare different source-ID sets

**Status:** Blocking.

The frozen protocol declares seven source IDs across its related-work and case-source sections:

- `SOURCE-M1-FOUNDATIONAL-CONTRACT`
- `SOURCE-M1-MILESTONE`
- `SOURCE-M1-PRIOR-ART`
- `SOURCE-M1-PROGRAM-CHARTER`
- `SOURCE-M1-TAXONOMY-POSITIVE`
- `SOURCE-M1-TAXONOMY-NEGATIVE`
- `SOURCE-M1-TAXONOMY-HELD-OUT`

The canonical manifest contains only the final five; it omits `SOURCE-M1-FOUNDATIONAL-CONTRACT` and `SOURCE-M1-MILESTONE`. Protocol procedure step 3 requires set comparison of all declared source IDs before coding, and the invalid-coverage rule rejects a missing or extra source. That check cannot currently pass.

This is not repairable by silently adding sources to the frozen v1 manifest. The immutable-record rule requires a disclosed superseding record.

### B3 — The frozen protocol's M1 milestone digest no longer resolves

**Status:** Blocking.

The protocol binds `SOURCE-M1-MILESTONE` to `docs/program/M1_FOUNDATION.md` with SHA-256:

`473ea1b43eeac3661491d85008c898f2bd27b2c539bae4b901222563cc8654b6`

The current raw bytes at that locator hash to:

`829307e4ebb128d3bcd95d110d93b37c38eaabab84d17f26939ccc7a0f757880`

The protocol's own consequence for an incorrect milestone source is to revise questions and thresholds before freeze. Because v1 is already frozen, execution must not select whichever bytes are convenient. A superseding study record must either bind a preserved exact copy of the originally reviewed bytes or transparently bind the current version and disclose the effect of the change.

### B4 — Frozen environment requirements are not fully recorded at the required location

**Status:** Blocking pending governed resolution.

The bound environment says that the exact repository revision, dependency-file digest, platform details, and the environment artifact digest **must be recorded in the frozen manifest or freeze attestation**. The environment artifact digest is present. The following required metadata are not fully present in either location:

- the dependency lockfile's raw-byte digest; the current `requirements-dev.lock` digest is `cd65f68d7665b69512bd7be8843727bf565e0aebc229f4d76666edb308571fca`, but neither the manifest nor attestation records it;
- concrete platform details for the frozen execution environment; and
- an exact canonical freeze-integration revision. The files record author-package revision `ee7d6a089dc05ab2cdad7726a930ee722a904100`, while the manifest describes the later freeze integration only as exact-head reviewed on a date.

A future intake may record the actual execution host, but it cannot retroactively satisfy an explicit requirement that freeze metadata reside in the immutable manifest or attestation. Any repair must preserve the v1 record and use disclosed supersession.

### B5 — The attestation and component lifecycle metadata do not match their documented freeze description

**Status:** Blocking pending steward disposition; do not rewrite in place.

The package README says the freeze attestation contains an artifact inventory and raw-byte digests. The actual attestation contains study identity, authority, timestamp, counts, output absence, and claim boundaries, but no artifact inventory or per-artifact digest values. Those values exist in the canonical manifest, not in the attestation described by that requirement.

In addition, the exact profile, category rules, configuration, and environment bytes bound by the frozen manifest each still self-declare `artifact_status: DRAFT_FREEZE_INTENT`. The canonical manifest can externally make exact bytes immutable, so this review does not automatically declare those artifacts scientifically invalid. However, the unresolved lifecycle wording is inconsistent with describing them as unambiguously finalized operational inputs. It must be resolved explicitly in a superseding freeze package rather than ignored or edited in place.

### B6 — Intake digest semantics and validation shape are undefined

**Status:** Blocking for intake creation, not a scientific finding.

The configuration lists a raw-byte SHA-256 over the immutable intake among the intake's required fields, but the repository supplies no execution-intake schema or template and does not say where that digest is stored. A file cannot straightforwardly contain a digest over all of its own final raw bytes. Before intake publication, governance must define an external digest receipt/index or a precise non-self-referential digest scope. It must also define how required fields, role distinctness, declarations, and locator safety are validated.

Guessing a one-off JSON shape or embedding an unverifiable self-digest would weaken the frozen provenance gate.

## 4. Minimum truthful intake and role-assignment evidence

This section identifies the minimum semantic obligations already required by the frozen materials. It is not an intake schema and does not authorize creation of the intake before the blockers above are resolved.

### 4.1 Exact study binding

The finalized intake must identify:

- intake artifact ID and version;
- `LCMRP-FSTUDY-0001-M1-TAXONOMY`;
- `LCMRP-FSTUDYREC-0001-M1-TAXONOMY`, record version `1` or an explicitly superseding accepted record version;
- canonical manifest locator, digest algorithm, digest value, and `RAW_FILE_BYTES` scope;
- the accepted protocol/profile/configuration versions; and
- a UTC intake timestamp and named execution authority with the authority basis recorded.

### 4.2 Three pairwise-distinct eligible human contributors

For each of `PRIMARY_1`, `PRIMARY_2`, and `TIE`, the record needs a stable contributor ID and attributable declarations establishing that the contributor:

- is a human research contributor under the frozen execution model, not an AI agent or model inference;
- did not author or change the protocol, method profile, category rules, case sources, or planned analyses;
- is not the freeze authority;
- has disclosed relevant conflicts and has a recorded eligibility determination;
- did not access case packets, source-role metadata, planned outputs, provisional scores, peer codes, or results before the permitted stage;
- accepts offline execution and the frozen retention/deviation rules; and
- can remain traceable in every applicable finding or terminal disposition without being treated as a study participant.

The two primary contributors must separately commit not to access each other's codes or rationales until both raw ledgers are locked. The tie contributor must commit to remain separate from primary coding and to receive only unresolved cells after lock and reconciliation.

Repository-verifiable attribution may use signatures, protected identity records, or another approved mechanism, but a bare unverified string is not evidence that the declaration came from the contributor.

### 4.3 No-prior-access and absence state

Before the intake is finalized, the execution authority must record:

- `results_accessed_before_intake=false`;
- that no planned output or provisional result exists;
- that each prospective adjudicator satisfies the case-access and conflict boundary; and
- any prior exposure or uncertainty rather than forcing a favorable declaration.

If a contributor previously accessed a prohibited packet, source role, rationale, or peer code, the record must not conceal that fact. The contributor must be replaced or the affected work halted/invalidated according to the frozen compromise rule.

### 4.4 Immutable digest binding

After the intake payload is final, its raw bytes must be hashed and the digest recorded in a separately defined, non-self-referential immutable binding. Later findings must cite the intake artifact ID, version, digest, and applicable contributor IDs.

## 5. Safe next action

1. **Keep execution stopped.** Do not open taxonomy case contents, generate evaluator packets, appoint agents as adjudicators, create the intake, or create any planned output.
2. **Publish a separately reviewed repair/supersession increment.** Preserve v1 unchanged; reconcile the protocol/manifest source sets, restore or supersede the stale M1 milestone binding, satisfy the environment freeze requirements, add a complete freeze inventory, resolve component lifecycle labels, and define a non-self-referential intake contract.
3. **Recruit or identify three eligible humans.** Obtain stable contributor IDs and attributable eligibility, conflict, isolation, and prior-access declarations. Do not assume that the user, a reviewer, an authoring lane, a root agent, or any other actor is eligible without evidence.
4. **Freeze and validate the superseding record before case access.** Recompute all frozen bindings under the repaired contract. Case-byte verification belongs to that authorized pre-coding process and was intentionally not performed here.
5. **Create the immutable intake only after the repaired freeze passes.** Then generate blinded packets and begin the two-primary/one-tie process exactly as declared.

If three eligible humans cannot be supplied, preserve a truthful `NOT_RUN` disposition only through the later governed finding workflow. Do not fabricate adjudication or agreement values. Using AI adjudicators would require a separately approved method profile and superseding preregistration; it is not authorized by the current frozen human-adjudication protocol.

## 6. Claim and evidence boundary

### Observation

The reviewed non-case bytes largely retain their registered identities, the canonical study and subject entries are active, the intake and outputs are absent, no findings or closeout are registered, and the blockers above are present in current metadata.

### Inference

Because actor eligibility and intake are mandatory preconditions, and because the frozen source/binding checks cannot currently pass, starting taxonomy execution would violate the preregistration. The defensible readiness disposition is `BLOCKED`.

### Not established

This review does not establish or challenge:

- whether any taxonomy term, distinction, organization, competency question, or integrity constraint succeeds;
- the content, quality, completeness, sensitivity, or digest correctness of any case file;
- adjudicator agreement, Cohen's kappa, support, rejection, ambiguity, invalidity, or a null result;
- taxonomy correctness, novelty, completeness, usefulness, external validity, biological fidelity, safety, privacy effectiveness, or implementation suitability;
- independent replication or scientific validation; or
- any Charter mechanism evidence or readiness state.

No result-to-claim inference is permitted. Repairing readiness metadata would authorize only a controlled attempt to execute the bounded Layer 1 study; it would not predetermine a favorable result or complete M1.

## Final judgment

**Do not start `LCMRP-FSTUDY-0001-M1-TAXONOMY` execution from the current record.** The minimum honest next increment is metadata repair through immutable supersession plus verified assignment of two independent primary human adjudicators and one separate human tie adjudicator. Until both conditions are satisfied, absence of execution is the correct research outcome.

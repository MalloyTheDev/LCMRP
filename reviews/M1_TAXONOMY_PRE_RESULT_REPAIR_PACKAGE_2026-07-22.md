# M1 Taxonomy Pre-Result Metadata and Intake-Contract Repair Package — 2026-07-22

## Classification

- **Applicable layer:** Layer 1 — Foundational Research
- **Artifact role:** Program-engineering pre-result repair package review surface
- **Slice ID:** `M1-TAX-PRE-RESULT-METADATA-INTAKE-V2-001`
- **Package ID:** `M1-TAX-PRE-RESULT-METADATA-INTAKE-V2`
- **Study:** `LCMRP-FSTUDY-0001-M1-TAXONOMY`
- **Historical record:** `LCMRP-FSTUDYREC-0001-M1-TAXONOMY@1` digest `01640e8dae3836874b2b39fe3ea2a8f9c090374508aa69b31adf06fea9272139`
- **Package status:** `PRE_RESULT_REPAIR_PACKAGE_NOT_FROZEN`
- **Research finding created:** No
- **Closeout created:** No
- **Evidence effect:** None
- **Execution authorized:** No
- **M1 completion effect:** None

## Decision status for this increment

**ACCEPT AS PRE-RESULT REPAIR MATERIALS ONLY — DO NOT EXECUTE; DO NOT TREAT AS FREEZE OR INTAKE**

This increment publishes superseding **draft** obligations and contracts that address taxonomy readiness blockers **B2–B6** without rewriting version-1 frozen bytes, without registering a version-2 study record, without creating a live intake, and without appointing adjudicators. Residual blocker **B1** remains open.

## Authority

- [M1 Taxonomy Execution-Readiness Review](M1_TAXONOMY_EXECUTION_READINESS_2026-07-21.md) — blockers and safe next action item 2
- [M1 Study-Execution Decision](M1_STUDY_EXECUTION_DECISION_2026-07-21.md) — separate taxonomy v2 repair package; preserve v1
- [Foundational Study Contract](../docs/program/FOUNDATIONAL_STUDY_CONTRACT.md) — immutable records; digest-linked supersession
- [Automated case-access correction](M1_TAXONOMY_AUTOMATED_CASE_ACCESS_CORRECTION_2026-07-22.md) — containment remains in force; this package does not reopen case bodies

## What was published

Under `studies/foundational/m1-taxonomy-v1/superseding/pre-result-metadata-intake-v2/`:

| Artifact | Blockers |
| --- | --- |
| `source-binding-reconciliation.json` | B2, B3 |
| `environment-freeze-obligations.json` | B4, B5 |
| `intake-binding-contract.md` | B6 (+ sequence for B1) |
| `residual-human-contributor-gate.md` | B1 residual open |
| `package-manifest.json` / `README.md` | Package identity and claim boundary |

Shared contracts:

| Artifact | Role |
| --- | --- |
| `schemas/foundational-execution-intake.schema.json` | Intake **payload** shape without full-file self-digest |
| `schemas/foundational-execution-intake-receipt.schema.json` | External raw-byte digest receipt |
| `templates/foundational-execution-intake.md` | Human template |
| `examples/foundational-execution-intake*.example.json` | Synthetic non-evidence fixtures |

## Milestone binding policy (B3)

Version-1 protocol bound `docs/program/M1_FOUNDATION.md` at digest `473ea1b4…654b6`. Repository history shows later digests `829307e4…7880` and current tip `2e5a62ff…242d`. This package selects **transparent rebind of the current milestone document with mandatory freeze-time recomputation and amendment disclosure**. It rejects silent convenience selection and rejects in-place v1 protocol edits.

## Intake digest policy (B6)

Accepted binding is **payload file + external receipt**. Full-file self-digest inside the payload is forbidden as the sole binding. Synthetic examples demonstrate shape only; their receipt digests are placeholders.

## Explicit non-actions

1. No edit to version-1 protocol, freeze attestation, definitions, reproducibility files, cases, or canonical study record.
2. No registry history change.
3. No live `execution/execution-intake.json`.
4. No adjudicator appointment or agent substitution.
5. No planned output creation.
6. No formal-model lane changes.
7. No scientific taxonomy claim.

## CLAIMS_MADE

- Pre-result repair materials for B2–B6 exist and are digest-linked to the v1 study record identity.
- Intake self-digest is rejected; external receipt is specified.
- B1 remains an open human gate.

## CLAIMS_EXPLICITLY_NOT_MADE

- Taxonomy execution readiness or authorization
- Version-2 freeze or ACTIVE registry supersession
- Correctness or adoption of the candidate taxonomy
- M1 completion, findings, closeouts, or mechanism evidence
- Eligibility of any real person as adjudicator

## Residual risks

- A reader may over-interpret package presence as freeze or execution readiness.
- A future freeze may still choose the alternative historical-byte milestone binding; this package documents the selected default policy only.
- Human recruitment (B1) can still block all later taxonomy execution indefinitely.

## Next valid gates

1. Independent engineering review and human merge decision for this package.
2. Separate taxonomy v2 freeze + registry supersession (not this PR).
3. Human recruitment and live intake with external receipt after freeze.
4. Separate execution authorization only after intake.

## Formal lane note

The formal pre-result guard package under `m1-formal-model-v1/superseding/pre-result-guard-v2/` is intentionally untouched. Formal v2 study-record supersession remains a separate review boundary.

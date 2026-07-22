# M1 Formal Study-Record v2 Supersession — 2026-07-22

## Classification

- **Applicable layer:** Layer 1 — Foundational Research
- **Artifact role:** Steward freeze / registry supersession for pre-result tool correction
- **Slice ID:** `M1-FMO-STUDY-RECORD-V2-001`
- **Study:** `LCMRP-FSTUDY-0002-M1-FORMAL-MODEL`
- **Prior record:** `LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL@1` digest `b99da2d9…707e` → registry `SUPERSEDED`
- **New record:** `LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL@2` → registry `ACTIVE`
- **Blocker addressed:** `FMO-EXEC-PREFLIGHT-BLOCK-001`
- **Analyzer executed:** No (`main` / `run_kernel` not invoked)
- **Planned outputs present:** 0 of 7
- **Findings / closeouts:** None
- **M1 completion effect:** None

## Decision

**ACCEPT VERSION-2 FROZEN SUPERSEDING PREREGISTRATION — DO NOT TREAT FREEZE AS EXECUTION OR PROOF**

## What changed

1. New corrected analyzer under `studies/foundational/m1-formal-model-v1/superseding/study-record-v2/` that:
   - preserves the guard-v2 indentation-safe index parse; and
   - resolves the unique **ACTIVE** registry entry for the study record (version 2), allowing SUPERSEDED historical entries for the same `record_id`.
2. Version-2 tool provenance and freeze attestation.
3. Canonical study record v2 with `amendment.kind = SUPERSEDING_RECORD` and exact prior digest.
4. Registry history: v1 `SUPERSEDED`, v2 `ACTIVE` (active-version uniqueness preserved).

## What did not change

- Version-1 study record, protocol, analyzer, and blocked preflight files (immutable)
- Subject definition bytes
- Planned analysis IDs and output locators (still PENDING / absent)
- Result, finding, closeout, evidence, experiment, and mechanism registries (empty)

## Claim boundary

### CLAIMS_MADE

- Digest-linked supersession of the formal preregistration for the documented pre-result guard defect
- Guard-only index verification succeeds for ACTIVE v2
- No semantic analysis result was produced at freeze

### CLAIMS_EXPLICITLY_NOT_MADE

- Scientific formal-model validity, proof, or replication
- Authorization of production execution beyond a later governed execution increment
- M1 completion or mechanism maturity

## Next gates

1. Human merge review for this registry/freeze change — **completed** on `main` via PR #29
2. Optional fresh preflight attestation under v2 (still without analysis) — recorded in `M1_FORMAL_V2_GUARD_PREFLIGHT_2026-07-22.md` / `superseding/study-record-v2/execution/preflight-attestation.json` (engineering only)
3. Separate execution authorization only if later explicitly approved
4. Taxonomy residual B1 (humans + intake) remains an independent lane

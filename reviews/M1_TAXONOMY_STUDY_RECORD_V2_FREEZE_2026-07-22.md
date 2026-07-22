# M1 Taxonomy Study-Record v2 Freeze — 2026-07-22

## Classification

- **Applicable layer:** Layer 1 — Foundational Research
- **Artifact role:** Steward freeze / registry supersession for pre-result metadata repair
- **Slice ID:** `M1-TAX-STUDY-RECORD-V2-001`
- **Study:** `LCMRP-FSTUDY-0001-M1-TAXONOMY`
- **Prior record:** `@1` digest `01640e8d…2139` → registry `SUPERSEDED`
- **New record:** `@2` → registry `ACTIVE`
- **Blockers addressed:** B2, B3, B4, B5, B6
- **Residual blocker:** **B1** (human adjudicators / live intake)
- **Case contents accessed:** No
- **Live intake created:** No
- **Planned outputs present:** 0 of 5
- **Findings / closeouts:** None
- **M1 completion effect:** None

## Decision

**ACCEPT VERSION-2 FROZEN SUPERSEDING PREREGISTRATION — DO NOT EXECUTE; B1 REMAINS OPEN**

## What changed

1. Protocol v2 with protocol/manifest-identical seven-source set (adds foundational contract and milestone).
2. Transparent milestone rebind to current `docs/program/M1_FOUNDATION.md` with disclosure policy.
3. Freeze attestation inventory, lockfile digest, platform declaration, and lifecycle resolution for local `DRAFT_FREEZE_INTENT` wording without rewriting v1 operational files.
4. Intake binding remains the external payload+receipt contract; no live intake.
5. Registry: taxonomy v1 `SUPERSEDED`, taxonomy v2 `ACTIVE`. Formal lane unchanged on this branch.

## What did not change

- Version-1 study record, protocol, cases, definitions, and freeze attestation bytes
- Case body access discipline
- Empty finding/closeout/evidence registries
- Residual requirement for three eligible human adjudicators before coding

## Next gates

1. Human merge of this freeze PR (depends on pre-result repair package PR #28 stack)
2. Recruit eligible humans and publish payload+receipt intake (B1)
3. Separate execution authorization only after intake

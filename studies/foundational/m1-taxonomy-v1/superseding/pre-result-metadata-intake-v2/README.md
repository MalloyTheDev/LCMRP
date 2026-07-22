# M1 Taxonomy Pre-Result Metadata and Intake-Contract Package v2

Applicable layer: Layer 1 — Foundational Research  
Package role: Pre-result repair / supersession **draft materials only**  
Package status: `PRE_RESULT_REPAIR_PACKAGE` / `NOT_FROZEN` / `NOT_REGISTERED` / `NOT_EXECUTABLE`  
Study: `LCMRP-FSTUDY-0001-M1-TAXONOMY`  
Supersedes lineage target: `LCMRP-FSTUDYREC-0001-M1-TAXONOMY@1`  
Mechanism evidence labels: Not applicable  
Scientific findings asserted: None

## Boundary

This package is a **pre-result** engineering and governance repair surface for documented taxonomy version-1 execution-readiness blockers **B2–B6**. It does **not**:

- freeze or register a version-2 study record;
- rewrite version-1 frozen bytes;
- create a live execution intake with real people;
- appoint adjudicators or substitute agents for humans;
- open taxonomy case contents;
- create planned outputs, findings, closeouts, or evidence records;
- authorize taxonomy execution; or
- complete M1.

Version-1 remains the sole ACTIVE frozen preregistration until a later, separately reviewed freeze and registry supersession.

## Authority

- [M1 Taxonomy Execution-Readiness Review](../../../../../reviews/M1_TAXONOMY_EXECUTION_READINESS_2026-07-21.md) — blockers B1–B6 and safe next action item 2
- [M1 Study-Execution Decision](../../../../../reviews/M1_STUDY_EXECUTION_DECISION_2026-07-21.md) — preserve v1; separate taxonomy v2 repair package
- [Foundational Study Contract](../../../../../docs/program/FOUNDATIONAL_STUDY_CONTRACT.md) — immutable records; supersession by new version

## Package contents

| Path | Addresses | Role |
| --- | --- | --- |
| `package-manifest.json` | Package identity | Digest-bound inventory and claim boundary |
| `source-binding-reconciliation.json` | B2, B3 | Protocol vs manifest source-ID sets; milestone digest policy |
| `environment-freeze-obligations.json` | B4, B5 | Lockfile, platform, freeze inventory, lifecycle labels |
| `intake-binding-contract.md` | B6 (+ residual B1) | Non-self-referential intake digest contract; human residual gate |
| `residual-human-contributor-gate.md` | B1 | Explicit human-only residual obligations |

Shared contracts introduced with this package (repository root):

| Path | Role |
| --- | --- |
| `schemas/foundational-execution-intake.schema.json` | Machine shape for a future intake **payload** (no full-file self-digest) |
| `schemas/foundational-execution-intake-receipt.schema.json` | External raw-byte digest receipt for an intake payload |
| `templates/foundational-execution-intake.md` | Human template for future intake authoring |
| `examples/foundational-execution-intake.example.json` | Synthetic non-evidence payload example |
| `examples/foundational-execution-intake-receipt.example.json` | Synthetic non-evidence external receipt example |

## Residual blocker B1

No eligible human adjudicators are appointed here. Three pairwise-distinct eligible humans with attributable declarations remain a hard pre-coding gate after a later freeze. Agents must not be substituted.

## Claims

### CLAIMS_MADE

- Version-1 taxonomy study bytes are preserved as historical inputs for this package.
- Documented metadata blockers B2–B6 are expressed as explicit superseding obligations and contracts.
- Intake full-file self-digest is rejected as the sole binding; external receipt is required.
- Planned taxonomy outputs and live study intake remain absent after this package.

### CLAIMS_EXPLICITLY_NOT_MADE

- Taxonomy execution readiness or authorization
- Correctness, completeness, or adoption of the candidate taxonomy
- Scientific findings, closeouts, evidence labels, or M1 completion
- That any person named in repository history is an eligible adjudicator
- That a version-2 freeze or registry supersession has occurred

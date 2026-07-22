# Taxonomy Execution-Intake Binding Contract (Pre-Result v2)

Applicable layer: Layer 1 — Foundational Research  
Package: `M1-TAX-PRE-RESULT-METADATA-INTAKE-V2`  
Blocker addressed: **B6** (intake digest semantics); residual obligations for **B1**  
Status: **Contract definition only** — not a live intake, not a freeze, not execution authority

## Purpose

The version-1 configuration requires a raw-byte SHA-256 over the immutable execution intake among the intake's required fields, but the repository previously supplied no intake schema and did not define a non-self-referential binding. A file cannot truthfully contain a digest over **all of its own final raw bytes** as a field inside those same bytes.

This contract defines the accepted binding shape for any future taxonomy intake. It does **not** create `studies/foundational/m1-taxonomy-v1/execution/execution-intake.json`, does **not** appoint people, and does **not** authorize case access.

## Two-artifact binding model

A future governed intake uses **two** artifacts:

1. **Intake payload** — human and machine fields about study binding, roles, declarations, timestamps, and authority. The payload **must not** contain a field whose value is the SHA-256 of the complete final payload file that includes that field.
2. **External digest receipt** — a separate artifact that records the payload locator and the SHA-256 over the payload's raw file bytes (`RAW_FILE_BYTES`).

Machine contracts:

- `schemas/foundational-execution-intake.schema.json`
- `schemas/foundational-execution-intake-receipt.schema.json`

Synthetic non-evidence examples:

- `examples/foundational-execution-intake.example.json`
- `examples/foundational-execution-intake-receipt.example.json`

Human authoring aid:

- `templates/foundational-execution-intake.md`

## Required payload content (semantic obligations)

Derived from the frozen protocol, configuration, and readiness review §4 without inventing identities:

1. Intake `artifact_id` and `artifact_version`
2. `study_id` = `LCMRP-FSTUDY-0001-M1-TAXONOMY` (or a later authorized superseding study identity that retains the same study_id series rules)
3. Exact study record identity: `study_record_id`, `record_version` of the **accepted frozen** superseding record (not v1 if v1 remains blocked), canonical manifest locator, digest algorithm, digest value, `RAW_FILE_BYTES`
4. Protocol / profile / configuration versions bound by that freeze
5. Three pairwise-distinct roles: `PRIMARY_1`, `PRIMARY_2`, `TIE`
6. For each role: stable contributor ID and attributable eligibility, isolation, conflict, and no-prior-prohibited-access declarations establishing a **human** research contributor (not an AI agent or model inference)
7. Confirmation that protocol/profile/rule/case authors and the freeze authority are ineligible and not assigned
8. `results_accessed_before_intake` = `false` with supporting absence assertions for planned outputs
9. UTC intake timestamp and named execution authority with authority basis
10. Explicit statement that case packets, peer codes, and planned outputs were not accessed before intake finalization

## Required receipt content

1. Receipt `artifact_id` and `artifact_version`
2. Payload locator (repository-relative)
3. Payload digest: algorithm `SHA-256`, scope `RAW_FILE_BYTES`, status `VERIFIED` or `RECORDED` as appropriate after independent recomputation
4. Optional receipt-of-receipt is **not** required; do not create infinite digest chains

## Explicitly invalid patterns

| Pattern | Why invalid |
| --- | --- |
| Single JSON file contains `raw_byte_sha256` equal to SHA-256 of that entire file including the field | Self-referential; not computable for the final byte sequence that includes its own hash |
| Bare contributor string without attributable declaration mechanism | Does not evidence eligibility |
| Agent, model, or orchestrator ID as adjudicator under the current human-adjudication profile | Forbidden substitution |
| Intake created while planned outputs exist or cases already coded | Violates pre-coding sequence |
| Intake bound only to blocked version-1 record after a superseding freeze exists | Stale identity |

## Sequence relative to freeze and case access

1. Accept metadata repair package (this package class).
2. Separately freeze and register a superseding study record while all planned outputs remain absent.
3. Re-run freeze and execution-readiness checks.
4. Recruit three eligible humans with attributable declarations (**B1**).
5. Publish payload + external receipt under the freeze-declared intake locator family.
6. Only then generate blinded packets and begin coding.

## Claims

### CLAIMS_MADE

- Full-file self-digest is not an accepted sole binding for intake.
- External receipt over payload raw bytes is the accepted digest binding.

### CLAIMS_EXPLICITLY_NOT_MADE

- That an intake exists
- That any adjudicator is eligible or appointed
- That taxonomy execution may begin
- Any scientific result about the candidate taxonomy

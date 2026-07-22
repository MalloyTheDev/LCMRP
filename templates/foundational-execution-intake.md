# Foundational Execution Intake (template)

Applicable layer: Layer 1 — Foundational Research  
Template status: Non-evidentiary authoring aid  
Binding model: **External digest receipt** (see `schemas/foundational-execution-intake.schema.json` and `schemas/foundational-execution-intake-receipt.schema.json`)

Do not invent people. Do not use agent or model identities as adjudicators under a human-adjudication profile. Do not embed the SHA-256 of this file's final raw bytes inside the payload.

## 1. Study binding

- Intake artifact ID / version:
- Study ID:
- Study record ID / record version:
- Canonical manifest locator:
- Manifest raw-byte SHA-256:
- Protocol / profile / configuration versions:

## 2. Roles (exactly three pairwise-distinct humans)

### PRIMARY_1

- Contributor ID:
- Eligibility declaration:
- Isolation declaration:
- Conflict declaration:
- No-prior-prohibited-access declaration:
- Not protocol/profile/rule/case author: yes/no (must be yes)
- Not freeze authority: yes/no (must be yes)

### PRIMARY_2

- Contributor ID:
- Eligibility declaration:
- Isolation declaration:
- Conflict declaration:
- No-prior-prohibited-access declaration:
- Not protocol/profile/rule/case author: yes/no (must be yes)
- Not freeze authority: yes/no (must be yes)

### TIE

- Contributor ID:
- Eligibility declaration:
- Isolation declaration:
- Conflict declaration:
- No-prior-prohibited-access declaration:
- Not protocol/profile/rule/case author: yes/no (must be yes)
- Not freeze authority: yes/no (must be yes)
- Receives only unresolved cells after both primary ledgers are locked: yes/no (must be yes)

## 3. Absence and access assertions

- `results_accessed_before_intake`: false
- Planned outputs absent: true
- Case packets accessed before intake: false
- Peer codes accessed before intake: false

## 4. Authority and time

- UTC intake timestamp:
- Execution authority name:
- Authority basis:

## 5. External receipt (separate file)

After the payload bytes are final:

1. Write the payload JSON without any full-file self-digest field.
2. Compute SHA-256 over the payload raw bytes.
3. Write a separate receipt JSON with payload locator + digest.
4. Cite both artifacts from later findings.

## Claim boundary

Completing this template does not freeze a study, create a scientific result, or authorize product integration.

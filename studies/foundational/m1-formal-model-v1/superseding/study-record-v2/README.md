# M1 Formal-Model Study Record v2 (Pre-Result Supersession)

Applicable layer: Layer 1 — Foundational Research  
Package status: `FROZEN SUPERSEDING PREREGISTRATION` / `ANALYSIS_NOT_RUN`  
Study: `LCMRP-FSTUDY-0002-M1-FORMAL-MODEL`  
Study record: `LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL@2`  
Supersedes: version 1 digest `b99da2d9cfa34d659416fe30cc1d3fa731425d1fcfb8b6c9422cd9b5add2707e`  
Blocker corrected: `FMO-EXEC-PREFLIGHT-BLOCK-001`  
Mechanism evidence labels: Not applicable  
Scientific findings asserted: None

## Boundary

This package freezes a digest-linked version-2 preregistration that binds the corrected analyzer guard. It does **not**:

- execute `main`, `run_kernel`, or the configured analyzer command for semantic analysis;
- create any of the seven planned result files;
- publish findings or closeouts;
- rewrite version-1 study, analyzer, or blocked preflight bytes; or
- complete M1.

Version-1 remains in the study registry as `SUPERSEDED` historical provenance. Version-2 is the sole `ACTIVE` formal study record.

## Why version 2 exists

The frozen version-1 analyzer guard rejected the schema-valid ACTIVE registry entry because it required a fixed indentation depth for `artifact_digest.value`. Guard preflight stopped before analysis. Editing the version-1 analyzer in place is forbidden because it is digest-bound by the version-1 record.

## Contents

| Path | Role |
| --- | --- |
| `analyze_fmo_kernel.py` | Corrected analyzer; resolves unique ACTIVE registry entry for this record_id at version 2 |
| `artifacts/tool-provenance.json` | Version-2 tool provenance binding the corrected analyzer digest |
| `freeze-attestation.json` | Version-2 freeze attestation |
| `package-manifest.json` | Package inventory and claim boundary |

Canonical record: `records/foundational/studies/LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL-v2.json`

## Claims

### CLAIMS_MADE

- Version-2 is a frozen superseding preregistration linked to the exact version-1 digest.
- Guard-only index verification succeeds against the ACTIVE version-2 registry entry.
- All seven planned formal outputs remain absent after freeze.

### CLAIMS_EXPLICITLY_NOT_MADE

- Satisfiability, consistency, entailment, non-entailment, proof, or scientific validity of FMO-0.1
- Execution authorization for semantic analysis
- M1 completion or mechanism evidence

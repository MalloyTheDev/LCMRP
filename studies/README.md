# Foundational studies

**Artifact classification:** program navigation supporting Layer 1 — Foundational Research; this index is not a research finding or evidence record.

This directory retains study-local author packages separately from canonical immutable records. Draft artifacts preserve the reviewed authoring history. A study becomes an active preregistration only when a distinct `FROZEN` manifest is present under `records/foundational/studies/` and its exact raw-byte digest is active in `registry/foundational-studies.yaml`.

## Active M1 preregistrations

- [M1 taxonomy study](foundational/m1-taxonomy-v1/) binds `LCMRP-FSTUDY-0001-M1-TAXONOMY` to the exact registered taxonomy subject. Its [frozen protocol](foundational/m1-taxonomy-v1/protocol-v1.md) declares five analyses and 48 synthetic cases. The [execution-readiness review](../reviews/M1_TAXONOMY_EXECUTION_READINESS_2026-07-21.md) found source, environment, contributor-intake, and intake-digest blockers. No case adjudication occurred and all five planned outputs are absent.
- [M1 formal-model study](foundational/m1-formal-model-v1/) binds `LCMRP-FSTUDY-0002-M1-FORMAL-MODEL` to the exact registered formal-model subject. Its [frozen protocol](foundational/m1-formal-model-v1/protocol-v1.md) declares seven analyses and a bounded offline analyzer. The digest-bound provenance guard rejected the schema-valid canonical index before the configured command, `main`, or `run_kernel` ran, as recorded by the [formal execution-readiness review](../reviews/M1_FORMAL_MODEL_EXECUTION_READINESS_2026-07-21.md). All seven planned outputs are absent.

`FROZEN` means that the preregistration inputs are immutable. It does not mean that a record is executable, an analysis ran, a result exists, a candidate is valid or adopted, a study is closed, or any mechanism evidence label applies. Both version-1 studies now require separately reviewed, digest-linked supersession before execution. Atomic findings and closeouts remain later governed work.

The formal package also contains a `superseding/pre-result-guard-v2/` corrected-tool proposal whose metadata claims a non-authorizing, guard-only preflight pass with no analysis executed. It is not a canonical version-2 study record, active registry entry, complete freeze, execution authorization, result, finding, or closeout. Its unresolved provenance and full-guard obligations must be corrected under a governed supersession before it can support a canonical execution-authorizing preflight.

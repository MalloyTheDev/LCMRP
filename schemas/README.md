# Research artifact schemas

These JSON Schema Draft 2020-12 contracts define the minimum machine-readable structure for LCMRP mechanism experiment manifests, mechanism evidence records, mechanism-registry entries, foundational subjects, foundational-study manifests, mechanism-independent research findings, immutable foundational-study closeouts, and record indexes.

The mechanism contracts and foundational contracts are deliberately parallel. A foundational finding cannot award a Charter mechanism evidence label, and a mechanism evidence decision cannot omit its exact mechanism version.

See [Foundational Study Contract v0.1](../docs/program/FOUNDATIONAL_STUDY_CONTRACT.md) for the supported profiles, subject-registry and closeout rules, rejection conditions, source rationale, and known limitations.

Schema validity establishes structural conformance only. It does not establish that a hypothesis is sound, a protocol is adequate, a result is true, an evaluator is independent, or an evidence state has been earned.

Schema versions and `$id` values are part of research provenance. A semantic change requires a new schema version. Existing evidence should continue to reference the schema under which it was recorded.

`foundational-execution-intake.schema.json` and `foundational-execution-intake-receipt.schema.json` define a multi-human pre-coding intake **payload** and a separate external raw-byte digest **receipt**. `foundational-execution-intake-solo.schema.json` defines the solo-human + optional non-adjudicative AI tooling intake shape used only after a disclosed solo-method freeze. Payloads must not use a full-file self-digest as their sole binding. Schema presence does not create a live intake, appoint adjudicators, or authorize study execution.

# Immutable research records

This directory is reserved for registered mechanism experiment manifests, mechanism evidence records, foundational-study manifests, mechanism-independent research-finding records, and foundational-study closeouts:

- `records/experiments/` for JSON experiment manifests
- `records/evidence/` for JSON evidence records
- `records/foundational/studies/` for JSON foundational-study manifests
- `records/foundational/findings/` for JSON research-finding records
- `records/foundational/closeouts/` for immutable all-analysis closeout records

M0 created no registered records. M1 currently contains exactly two canonical foundational-study manifests, each frozen before result access and indexed by an exact raw-byte SHA-256 digest. These are preregistrations, not findings. No experiment manifest, evidence record, foundational finding, or foundational closeout has been registered. Foundational subject definitions remain separate immutable artifacts indexed by `registry/foundational-subjects.yaml`.

Future records must validate against their declared schema and be indexed in the corresponding YAML registry with a SHA-256 digest over the exact raw file bytes.

Frozen or published records are append-only. Corrections create a new version with explicit supersession lineage; they do not replace bytes referenced by an existing registry entry.

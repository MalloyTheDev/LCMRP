# Immutable research records

This directory is reserved for registered experiment manifests and evidence records:

- `records/experiments/` for JSON experiment manifests
- `records/evidence/` for JSON evidence records

M0 contains no registered records and therefore does not create synthetic files in these locations. Future records must validate against their declared schema and be indexed in the corresponding YAML registry with a SHA-256 digest over the exact raw file bytes.

Frozen or published records are append-only. Corrections create a new version with explicit supersession lineage; they do not replace bytes referenced by an existing registry entry.

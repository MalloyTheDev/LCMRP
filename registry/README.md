# Research registries

The registries are append-oriented indexes of accepted mechanism, experiment, and evidence records. An empty `entries` list means that no entries of that class have been accepted; it must not be interpreted as missing or hidden positive results.

Registry entries should identify immutable or content-addressed artifacts. Corrections, withdrawals, and superseding interpretations must remain traceable rather than erasing earlier records.

The M0 registries intentionally contain no mechanism or experiment claims.

## Experiment and evidence index entries

`experiments.yaml` and `evidence.yaml` use [`record-index.schema.json`](../schemas/record-index.schema.json). Each future entry must identify an immutable JSON record by stable record ID, independent record version, schema ID, repository-relative path, registration status, and a SHA-256 digest over the exact raw file bytes.

The digest is external to the referenced record, so it is not self-referential. Any byte-level change creates a different digest. A semantic correction to a frozen or published record requires a new record version and index entry rather than rewriting the registered file.

Repository validation checks the entry shape, safe path resolution, file existence, raw-byte digest, declared artifact identity, and conformance to the declared schema.

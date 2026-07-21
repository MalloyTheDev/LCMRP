# Research registries

The registries are append-oriented indexes of accepted mechanism, experiment, and evidence records. An empty `entries` list means that no entries of that class have been accepted; it must not be interpreted as missing or hidden positive results.

Registry entries should identify immutable or content-addressed artifacts. Corrections, withdrawals, and superseding interpretations must remain traceable rather than erasing earlier records.

The M0 registries intentionally contain no mechanism or experiment claims.

## Experiment and evidence index entries

`experiments.yaml` and `evidence.yaml` use [`record-index.schema.json`](../schemas/record-index.schema.json). Each future entry must identify an immutable JSON record by stable record ID, independent record version, schema ID, repository-relative path, registration status, and a SHA-256 digest over the exact raw file bytes.

The digest is external to the referenced record, so it is not self-referential. Any byte-level change creates a different digest. A semantic correction to a frozen or published record requires a new record version and index entry rather than rewriting the registered file.

Repository validation checks the entry shape, safe path resolution, file existence, raw-byte digest, declared artifact identity, and conformance to the declared schema.

## Foundational subjects, studies, findings, and closeouts

[`foundational-subject-registry.schema.json`](../schemas/foundational-subject-registry.schema.json) defines `foundational-subjects.yaml`. Subject versions retain exact identity, immutable definition artifacts, and digest-linked supersession. Registry presence establishes identity and provenance only; it is not evidence that a subject is correct, useful, or validated.

[`foundational-record-index.schema.json`](../schemas/foundational-record-index.schema.json) defines the append-oriented indexes in `foundational-studies.yaml`, `research-findings.yaml`, and `foundational-study-closeouts.yaml`. The foundational-subject registry contains exactly two `ACTIVE` M1 candidate identities: the exact candidate taxonomy and formal-model bytes. The foundational-study, research-finding, and foundational-closeout registries remain empty. Registration makes a subject resolvable for a later frozen study; it does not adopt or validate the subject and is not a finding or evidence award.

Repository validation requires active studies to be frozen and resolve an exact registered subject, active findings to be published and bind the exact study/subject/profile/analysis artifacts, and active closeouts to be published and set-complete over every planned analysis. A frozen study remains a valid preregistration while work is partial; only a separate immutable closeout can assert terminal completeness.

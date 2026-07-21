# M1 taxonomy contract synthetic dry run

Applicable layer: Layer 1 — Foundational Research  
Bundle status: `SYNTHETIC-DRY-RUN` / `NON-EVIDENTIARY`  
Subject: `LCMRP-FSUBJ-9901-SYNTHETIC-DRY-RUN-TAXONOMY@1`  
Method profile: `LCMRP-MPROF-9901-SYNTHETIC-DRY-RUN-STRUCTURAL@1`  
Mechanism evidence labels: Not applicable; none awarded

This isolated family exercises the accepted `STRUCTURAL_OR_TAXONOMY_EVALUATION` contract from subject registration through immutable closeout. It compares the candidate stable kind-first and contextual role-first organizations using artificial positive, negative, and boundary cases. Every apparent outcome is pre-authored fixture behavior. Nothing in this directory is a registered production study, research finding, validation, adoption decision, novelty claim, implementation recommendation, or mechanism evidence state.

## Bundle contents

- `definitions/`: exact synthetic subject, method-profile, and category-rule bytes.
- `cases/`: two positive, two negative, and four boundary constructions.
- `protocol/`: the frozen protocol, configuration, environment declaration, and synthetic freeze receipt.
- `reports/`: one completed serialization output and report, one explicit not-run narrative, and the closeout report.
- `records/foundational/`: one `FROZEN` study manifest, two `PUBLISHED` atomic records, and one immutable `PUBLISHED` closeout.
- `indexes/`: isolated subject, study, finding, and closeout indexes.
- `verify_bundle.py`: bundle-local Draft 2020-12, digest, binding, index, and set-equality checks.

The first analysis is `COMPLETED` only because its deterministic serialization steps emitted all pre-authored rows. Its result is `MIXED` and its claim assessment is `INCONCLUSIVE`. The second planned analysis is explicitly `NOT_RUN`; no agreement value or raw result was invented. The closeout ledger contains exactly these two analysis IDs, once each.

## Construction and digest order

The logical record order is deliberately acyclic:

1. Freeze exact subject, profile, category rules, cases, environment, configuration, protocol, and receipt bytes.
2. Compute SHA-256 directly over each file's raw bytes; record no normalized-text or parsed-object digest.
3. Write the `FROZEN` manifest with those immutable input digests. Planned outputs remain `PENDING` in the frozen plan because their bytes are not preregistration inputs.
4. Compute the manifest raw-byte digest.
5. Produce the synthetic serialization output and companion report, compute their raw-byte digests, and publish one atomic finding for the completed fixture execution. Publish the second atomic record as `NOT_RUN` with no raw output.
6. Compute both finding-record digests, bind them into the all-analysis closeout, then compute the closeout digest.
7. Populate the four isolated indexes and run the local verifier.

Changing any referenced byte invalidates its digest and every downstream reference. A correction should regenerate a new versioned fixture family rather than overwrite a purportedly frozen or published record.

The foundational-record-index schema requires `artifact_path` values beginning with `records/foundational/...`. In these isolated examples that namespace is rooted at this bundle directory, so `records/foundational/studies/study-manifest.json` resolves to the file beside this README, not to a production record area. `verify_bundle.py` makes that isolation rule explicit and verifies the resulting raw bytes. Production registries remain untouched.

## Verification

From the repository root, with the pinned development dependencies available:

```bash
PYTHONPATH=.venv/lib/python3.12/site-packages python examples/m1-dry-runs/taxonomy/verify_bundle.py
```

The verifier:

- rejects duplicate JSON keys;
- validates eight schema-backed documents against the existing Draft 2020-12 schemas;
- resolves and recomputes every recorded local raw-byte SHA-256 reference;
- verifies the isolated indexes against their actual local records;
- binds the exact subject, method profile, frozen study record, analysis identities, published findings, and closeout;
- requires set equality between the two planned analyses and two closeout dispositions; and
- requires zero awarded mechanism evidence labels.

A passing check means only that the synthetic contract family is internally consistent.

## Limitations

- Cases and expected commitment strings were authored together, creating complete construction bias.
- There are no natural, representative, statistically sampled, or independently authored cases.
- There is no external source corpus, participant data, human-subject work, independent adjudicator, or independent replication.
- No biological equivalence, semantic adequacy, completeness, usability, safety, privacy effectiveness, or external validity is tested.
- Recorded SHA-256 values protect byte identity but do not establish authorship, provenance authenticity, semantic correctness, or scientific merit.
- No storage, retrieval, model, embedding, database, cloud, or implementation vendor is selected.
- The bundle must not be used to prefer, adopt, or validate either candidate organization.

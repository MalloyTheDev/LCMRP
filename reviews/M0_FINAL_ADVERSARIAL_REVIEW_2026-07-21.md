# M0 Final Adversarial Review — 2026-07-21

## Review status

- **Artifact classification:** Program infrastructure supporting all three research layers
- **Review type:** Internal adversarial contract and repository review conducted as a separate testing arm
- **Disposition:** **PASS** for M0 technical-infrastructure acceptance
- **Completion condition outside this review:** The exact candidate revision must pass GitHub Actions from a clean checkout, and the program steward must record the governance acceptance decision
- **Independent scientific validation:** None claimed
- **Scientific evidence or mechanism maturity awarded:** None

This disposition applies only to the research-governance, reproducibility, and record-integrity foundation. It does not validate a taxonomy, formal model, benchmark, memory mechanism, scientific finding, security property, product integration, or production-readiness claim.

## Scope and boundary

The review covered the current M0 charter and governance documents, research-layer and evidence semantics, JSON Schemas, synthetic examples, empty registries, human-facing templates, repository validator, and automated tests. The final pass focused on the previously open mechanism-free Layer 1 contract obligations:

- stable foundational-subject identity, registration, and digest-linked supersession;
- exact study, subject, method-profile, finding, and artifact binding;
- immutable terminal closeout with complete planned-analysis accounting;
- canonical record discovery, path safety, active-version uniqueness, and amendment lineage;
- dedicated foundational protocol, finding-report, and closeout templates; and
- rejection of unsupported method profiles, human-subject work, mechanism maturity effects, and Layer 3 field leakage.

CorpusStudio was not inspected or modified. No CorpusStudio repository, training setup, schema, or implementation assumption was needed for this product-independent review.

## Method

The testing arm constructed a complete synthetic, non-evidentiary lifecycle from a registered subject through a frozen study, published findings, and a published closeout. It then mutated individual records, indexes, paths, digests, statuses, versions, and lineage links to look for false acceptance. Each discovered bypass was converted into a regression test after the implementation arm corrected the validator or schema.

The final local gate ran:

```text
python tools/validate_repository.py
python -m unittest discover --start-directory tests --verbose
python -m compileall -q tools tests
python -m pip check
```

The review also checked that every registry remained an empty versioned container, scanned repository text for common credential and private-key patterns, and audited CorpusStudio references for boundary-only or explicitly provisional usage.

## False accepts found and corrected

The following weaknesses were observable during the adversarial pass. The disposition column describes the final candidate, not the earlier state.

| False-accept path | Final disposition |
| --- | --- |
| A finding could name the expected subject or method profile while its artifact reference pointed to unrelated, correctly hashed bytes. | Rejected by exact identity and local raw-byte artifact binding. |
| A foundational index path could contain dot segments and escape its canonical record family. | Rejected by canonical path normalization and family containment checks. |
| A frozen study had no immutable terminal object proving that all planned analyses received exactly one retained disposition. | Corrected with a separate closeout record whose published analysis ledger must set-equal the frozen plan and resolve one active published finding per analysis. |
| An active finding could bind a substituted, correctly hashed study manifest while the active study index pointed to different bytes. | Rejected; active findings must bind the exact active indexed study artifact. |
| Canonical mechanism experiment or evidence records could exist without their required index entries. | Rejected by whole-tree canonical-record discovery. |
| Experiment and evidence indexes could expose more than one active version of the same logical record. | Rejected by active-version uniqueness checks across record registries. |
| A mechanism record-index path could use a dot-segment traversal form. | Rejected by the same canonical family-containment rule. |
| A superseding foundational study or finding could change its logical identity or target. | Rejected by amendment-lineage identity preservation. |
| Subject and method-profile consistency checks could be bypassed by moving a frozen study out of active status. | Rejected; every indexed frozen study remains auditable, including superseded versions. |
| A closeout could omit or duplicate analyses, reuse one finding, cite an inactive finding, substitute the index path or digest, or alter the human report bytes. | Rejected by ledger equality, one-to-one finding use, active-index resolution, exact artifact matching, and raw-byte SHA-256 verification. |

The artifact-identity comparison deliberately excludes digest verification status. Changing the same digest from `RECORDED` to `VERIFIED` adds verification metadata without creating different artifact bytes; changing the identifier, version, schema, locator, media type, digest algorithm, digest value, or digest scope does change the bound identity.

## Final validation results

- Structural repository validation: passed
- Draft 2020-12 schema meta-validation and example validation: passed through the repository validator
- Unit and adversarial tests: **86/86 passed**, including 24 completion-focused adversarial cases
- Python compilation: passed
- Dependency consistency: passed; no broken requirements reported
- Registry audit: seven registries parsed successfully and contained zero research entries
- Credential and private-key pattern scan: no findings
- Relative Markdown-link validation: passed through the repository validator
- Boundary audit: no memory implementation or product-specific architecture entered M0

The clean local result supports the technical exit criteria, but it is not a substitute for a successful workflow attached to the exact public candidate revision.

## Exit-criterion assessment

The final candidate makes the Charter discoverable, documents layers and evidence semantics, validates all schemas and examples, preserves empty versioned registries, supplies the required human-facing obligations, isolates provisional product implications, rejects duplicate serialization keys, validates relative links, and contains no memory implementation or product-specific architecture.

The testing arm found no remaining technical M0 blocker. Two publication-governance actions are intentionally outside this review's authority:

1. Confirm the GitHub Actions validation job passes on a clean checkout of the exact candidate revision.
2. Record the steward's explicit M0 completion decision without treating this internal review as independent scientific validation.

## Limitations and post-M0 obligations

- Structural conformance cannot establish that free-form claims are true or that a research design is scientifically adequate.
- No real foundational study, research finding, closeout, experiment, or evidence record has been registered or independently reproduced.
- External registration-service verification is not automated. M0 binds repository-local immutable bytes and records the authority; a future registrar adapter may add external verification.
- The foundational v0.1 profiles cover structural or taxonomy evaluation and formal analysis. Controlled empirical, computational, and evidence-synthesis profiles remain future versioned work; unsupported profiles are rejected rather than weakly accepted.
- Human-subject research remains prohibited until separately approved governance and method contracts exist.
- Usability, inter-reviewer agreement, migration behavior, long-horizon operation, security efficacy, and scientific completeness remain to be evaluated.
- Passing these tests does not award any Charter evidence label or support a product-integration decision.

These limitations do not block M0 because M0 establishes the governed infrastructure for later research; it does not perform or validate that research.

## Final judgment

No remaining technical M0 blocker was found in the reviewed candidate. The repository is **PASS** for M0 technical-infrastructure acceptance, contingent only on exact-head clean-checkout GitHub Actions and the steward's explicit completion record.

After those two actions, M1 may begin with product-independent memory taxonomy and formal-model work. This verdict does not authorize a memory implementation, CorpusStudio integration, maturity promotion, or production claim.

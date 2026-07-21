# M1 `FORMAL_ANALYSIS` Synthetic Dry Run 9902

> **SYNTHETIC-DRY-RUN — NON-EVIDENTIARY.** This self-contained fixture family exercises the accepted foundational-study contract. It is not a production registration, real experiment, research finding, replication, independent validation, or evidence award. Its lifecycle words (`ACTIVE`, `FROZEN`, and `PUBLISHED`) describe isolated example records only.

## Scope and layer

- **Applicable layer:** Layer 1 — Foundational Research
- **Method profile exercised:** `FORMAL_ANALYSIS`
- **Subject:** a deliberately tiny two-valued propositional system over `A` and `B` with theory `{A}`
- **Mechanism evidence labels:** not applicable; none may be awarded
- **Humans, participant data, datasets, model calls, solver calls, and network calls:** none

The subject is not FMO-0.1 and does not model memory or cognition. The retained truth-table outcomes establish only internal relations in the exact synthetic two-atom system. They must not be cited as proof, validation, or evaluation of FMO-0.1 or any other architecture.

## Bundle contents

| Path | Role |
| --- | --- |
| `artifacts/subject-definition.json` | Exact formal-model subject definition/version |
| `artifacts/method-profile-definition.json` | Exact local profile definition selecting the accepted `FORMAL_ANALYSIS` path |
| `artifacts/formal-system.json` | Frozen vocabulary, semantics, theory, propositions, and obligations |
| `artifacts/assumptions.json` | Exact assumption ledger |
| `artifacts/propositions.json` | Exact proposition ledger |
| `artifacts/tool-provenance.json` | Local semantic-check, schema-validation, and digest-tool provenance |
| `artifacts/environment.json` | Reproducibility and no-external-dependency boundary |
| `artifacts/configuration.json` | Enumeration order and preregistered decision rules |
| `artifacts/freeze-attestation.json` | Synthetic local freeze serialization |
| `protocol.md` | Human-facing frozen protocol |
| `outputs/satisfiability-result.json` | Retained complete valuation table and satisfiability witness |
| `outputs/entailment-countermodel-result.json` | Retained theory models, intended entailment, and non-entailment countermodel |
| `reports/*-finding.md` | Human-facing atomic finding reports |
| `reports/study-closeout.md` | Human-facing closeout report |
| `records/foundational/studies/*.json` | One schema-valid `FROZEN` study manifest |
| `records/foundational/findings/*.json` | Two schema-valid atomic `PUBLISHED` finding records |
| `records/foundational/closeouts/*.json` | One schema-valid immutable `PUBLISHED` closeout |
| `indexes/*.example.json` | Isolated subject, study, finding, and closeout example indexes |
| `validate_bundle.py` | Bundle-local schema, digest, binding, and set-equality checker |

The three foundational record indexes use schema-required paths beginning with `records/foundational/`. For this isolated bundle, those paths are resolved relative to this directory, where the corresponding files exist. They are example indexes only and are not included in the repository's production registries.

## Artifact and binding order

The dependency order encoded by the fixture is:

1. Bind the exact subject definition, local method-profile definition, formal system, assumptions, propositions, environment, configuration, tool provenance, freeze attestation, and protocol.
2. Serialize the `FROZEN` manifest with immutable digests for every pre-freeze input. Its planned-output references intentionally remain `PENDING`; a frozen preregistration cannot know post-freeze result bytes.
3. Retain the two output artifacts and their human-facing atomic reports.
4. Serialize one `PUBLISHED` finding per planned analysis, each binding the exact frozen-manifest bytes, exact subject/profile artifacts, exact analysis ID/mode, and actual output/report bytes.
5. Serialize the closeout report, then the immutable `PUBLISHED` closeout whose ledger binds both exact finding records and is set-equal to the manifest's analysis IDs.
6. Create isolated example indexes over the exact subject, study, findings, and closeout.

The ISO timestamps are deterministic fixture values used to exercise ordering constraints; they do not attest that a real registration or study occurred at those times. The chain's audit property comes from exact identifiers, versions, locators, and raw-byte digests, not from the synthetic timestamps.

## Digest generation

All populated digest values are SHA-256 over the referenced file's raw bytes (`RAW_FILE_BYTES`). They were generated with GNU coreutils 9.4:

```bash
sha256sum path/to/artifact
```

Digests were inserted only downstream: leaf artifacts → manifest → findings → closeout → indexes. No artifact embeds its own digest, so the bundle has no self-referential digest cycle. The `PENDING` planned-output references contain `null` rather than pretending that post-freeze bytes were known.

The bundle validator recomputes populated digests with Python `hashlib.sha256(path.read_bytes())`, validates schema-backed records with `jsonschema` Draft 2020-12, checks exact subject/study/finding bindings, and checks the closeout ledger for exact set equality and uniqueness.

Run from the repository root with the development dependencies installed:

```bash
PYTHONPATH=.venv/lib/python3.12/site-packages \
  python examples/m1-dry-runs/formal-analysis/validate_bundle.py
```

The recorded fixture environment used Python 3.12.13, `jsonschema` 4.25.1, `referencing` 0.37.0, and GNU coreutils 9.4. Those versions are provenance for this dry run, not general architecture requirements. Another Draft 2020-12 implementation and SHA-256 implementation may be substituted if they produce the same validations and raw-byte digests.

## Expected bounded serialization outcomes

- `ANALYSIS-9902-SATISFIABILITY`: `COMPLETED`; two retained valuations satisfy `{A}` and `A=true,B=false` is a witness.
- `ANALYSIS-9902-ENTAILMENT-COUNTERMODEL`: `COMPLETED`; every theory model satisfies `PROP-9902-A`, while `A=true,B=false` is a countermodel to entailment of `PROP-9902-B`.
- Closeout: exactly two unique ledger rows whose analysis-ID set equals the two planned IDs.
- Mechanism maturity effect: `NOT_APPLICABLE`, with an empty awarded-label list in every finding and the closeout.

These are fixture serialization outcomes, not program evidence.

## Limitations

- The formal system is intentionally trivial and has no demonstrated scientific, biological, or engineering relevance.
- The retained outputs were manually encoded; the validator checks internal determinism and completeness, not an independently implemented theorem prover.
- No novelty search, substantive formal soundness review, independent replication, adversarial formalization review, or external registration occurred.
- Schema validity cannot establish that a proposition, proof, interpretation, or research claim is scientifically correct.
- The synthetic authority names and lifecycle states confer no program acceptance.
- The bundle tests only the currently accepted `FORMAL_ANALYSIS` serialization path and does not justify a new method profile or tool dependency.

## Next falsification step

Commission an independent reviewer to mutate subject/profile digests, omit or duplicate a valuation, reverse a proposition relation, reuse a finding, and add or remove a closeout ledger row. The path should be accepted only if every mutation is rejected for the intended reason before a real Layer 1 formal study is proposed.

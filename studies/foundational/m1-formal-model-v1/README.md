# M1 Formal-Model Study Draft Package

Applicable layer: Layer 1 — Foundational Research  
Package state: `DRAFT` / not frozen  
Mechanism under evaluation: None  
Mechanism maturity labels: Not applicable  
Scientific findings asserted: None

This directory prepares, but does not activate, a product-independent `FORMAL_ANALYSIS` study of the exact registered Candidate Formal Memory Object Model v0.1.

- Study: `LCMRP-FSTUDY-0002-M1-FORMAL-MODEL`
- Record: `LCMRP-FSTUDYREC-0002-M1-FORMAL-MODEL`, version 1
- Profile: `LCMRP-MPROF-0002-M1-FORMAL-ANALYSIS`, version 1
- Subject: `LCMRP-FSUBJ-0002-FORMAL-MEMORY-OBJECT-MODEL`, version 1
- Subject raw-byte SHA-256: `82052e424c01d3204828472ef569f74f7c0aad418f827cffda92400562bbfaf3`

## No-freeze and no-result boundary

`manifest-draft.json` is a non-authoritative draft. It is not a canonical study record and must not be entered into the active foundational-study index as though it were frozen. `protocol-draft.md` is also non-authoritative. Neither file supplies a freeze timestamp, registration authority, freeze attestation, finding, disposition, or closeout.

The analyzer must not be executed and none of the seven planned `results/` locators may be created or inspected before a separately reviewed final protocol, authority-bound freeze attestation, immutable `FROZEN` manifest, exact canonical index digest, and no-prior-result-access assertion exist. The script enforces that boundary and refuses this draft.

Compilation, JSON parsing, JSON Schema validation, raw-byte digest verification, and static source inspection are allowed draft-integrity checks. They are not formal-analysis results and cannot establish that the bounded kernel—or FMO-0.1—is consistent, satisfiable, sound, complete, realizable, secure, or useful.

## Package contents

| Path | Purpose | Draft boundary |
| --- | --- | --- |
| `manifest-draft.json` | Schema-valid planned foundational-study manifest | `DRAFT`; null freeze fields; no result digest |
| `protocol-draft.md` | Complete human protocol following the foundational-study template | Prepared for independent review, not frozen |
| `artifacts/method-profile-definition.json` | Study-local `FORMAL_ANALYSIS` obligations, baselines, stops, and proof boundary | Does not register a program-wide profile |
| `artifacts/formal-system.json` | Finite Boolean modules, variables, constraints, bounds, and exclusions | Does not encode or validate all FMO-0.1 |
| `artifacts/assumptions.json` | Stable FMO-A01 through FMO-A12 assumptions and checks | Assumptions remain contestable |
| `artifacts/propositions.json` | Stable source propositions, entailment/non-entailment queries, invariant targets, and FMO-CM-01 through CM-10 assignments | Entries are planned obligations, not results |
| `artifacts/configuration.json` | Exact offline execution plan and seven unique analysis-result locators | Execution remains forbidden while draft |
| `artifacts/environment.json` | Planned CPython 3.12.13 standard-library environment | Study-local reproducibility target only |
| `artifacts/tool-provenance.json` | Exact analyzer digest, toolchain, integrity, and semantic boundary | Must be immutable in a frozen manifest |
| `analyze_fmo_kernel.py` | Guarded deterministic finite-model enumerator | Compile/static-check only before freeze |

## Planned analysis outputs

Each analysis has one unique planned output. None exists in this draft package.

| Analysis | Planned locator |
| --- | --- |
| `ANALYSIS-FMO-01-SATISFIABILITY` | `results/analysis-01-bounded-kernel-raw.json` |
| `ANALYSIS-FMO-02-ENTAILMENT` | `results/analysis-02-entailment.json` |
| `ANALYSIS-FMO-03-NONENTAILMENT` | `results/analysis-03-nonentailment.json` |
| `ANALYSIS-FMO-04-INVARIANT-INDEPENDENCE` | `results/analysis-04-invariant-independence.json` |
| `ANALYSIS-FMO-05-AUTHORITY` | `results/analysis-05-authority.json` |
| `ANALYSIS-FMO-06-DELETION` | `results/analysis-06-deletion.json` |
| `ANALYSIS-FMO-07-SEMANTIC-VALIDITY` | `results/analysis-07-semantic-validity.json` |

The Analysis 01 raw machine bundle is a supporting input to later interpretations, but it is not reused as another analysis's planned output. Each later analysis must publish its own atomic interpretation or adjudication artifact and terminal disposition.

## Bounded formal-system warning

The kernel enumerates independent finite Boolean modules. It does not construct a cross-module, quantified, temporal, or executable model of the complete subject. It omits natural-language truth, policy composition, distributed concurrency, liveness, probability, information flow, physical erasure, external copies, and implementation behavior.

Therefore:

- a module model does not establish full FMO-0.1 satisfiability;
- absence of a bounded counterexample does not prove a source proposition;
- a retained witness establishes only freedom in the encoded module;
- an invariant-omission witness establishes only module-local independence;
- authority facts do not establish legitimacy or a policy calculus; and
- deletion facts do not establish physical, external, legal, or operational deletion.

Two independent source-to-encoding mappings and retained adjudication are mandatory. A broader, circular, or unsupported mapping invalidates affected machine analyses.

## Required freeze handoff

A freeze authority must perform a separately reviewed action outside this authoring package:

1. resolve every independent review finding without running the analyzer;
2. derive a final protocol and schema-valid `FROZEN` canonical record;
3. record an exact repository revision and immutable raw-byte digests;
4. create an authority-bound freeze attestation with `results_accessed_before_freeze=false`;
5. register exactly the canonical record and digest through the foundational-study index;
6. verify every planned result path is absent; and
7. only then authorize the exact guarded invocation.

Any post-freeze change requires the contract's digest-linked supersession process. Negative, null, contradictory, failed, halted, invalid, and not-run outcomes must be preserved, and the study cannot close until all seven analysis IDs have exactly one active atomic disposition.

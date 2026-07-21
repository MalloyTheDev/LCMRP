# Evidence Label Normalization

## Purpose

The Program Charter defines evidence and readiness states with human-readable display labels. JSON schemas, registries, and other machine-readable artifacts require stable tokens that do not contain spaces or hyphens.

This document is the authoritative, lossless mapping between those representations. It does not amend the Charter, define additional states, impose an ordering, or change any evidence gate.

## Canonical mapping

| Charter display label | Canonical machine token |
| --- | --- |
| `HYPOTHESIS` | `HYPOTHESIS` |
| `PROTOTYPE` | `PROTOTYPE` |
| `REPLICATED` | `REPLICATED` |
| `BENCHMARKED` | `BENCHMARKED` |
| `ROBUSTNESS-TESTED` | `ROBUSTNESS_TESTED` |
| `SECURITY-REVIEWED` | `SECURITY_REVIEWED` |
| `INDEPENDENTLY VALIDATED` | `INDEPENDENTLY_VALIDATED` |
| `INTEGRATION CANDIDATE` | `INTEGRATION_CANDIDATE` |
| `PRODUCTION-READY` | `PRODUCTION_READY` |

## Serialization rules

- Human-facing prose should use the Charter display label.
- Machine-readable fields governed by an LCMRP schema must use the canonical machine token exactly.
- Producers must not derive tokens by applying an ad hoc punctuation or whitespace transformation. They must use this table.
- Consumers may render a machine token as its mapped display label, but must preserve the original token in stored and exchanged artifacts.
- An unknown display label or token is invalid. It must not be silently coerced to the nearest known value.
- A mapping change is a governance and schema-compatibility change requiring explicit review. It must not rewrite or reinterpret historical artifacts.

Evidence-state meanings and minimum gates remain defined by the [Program Charter](PROGRAM_CHARTER_v0.1.md) and [Evidence and Readiness States](EVIDENCE_STATES.md).

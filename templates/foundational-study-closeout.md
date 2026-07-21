# Foundational Study Closeout: `<descriptive title>`

> Publish this immutable Layer 1 closeout only after every analysis in the exact frozen foundational-study manifest has one active, published finding or terminal disposition. Replace every angle-bracketed placeholder. Do not rewrite the frozen study or omit negative, null, halted, invalid, or not-run work.

## Document control

| Field | Value |
| --- | --- |
| Closeout ID | `<LCMRP-FCLOSE-...>` |
| Closeout record ID and version | `<LCMRP-FCLOSEREC-... and integer version>` |
| Record status | `DRAFT`, `PUBLISHED`, `SUPERSEDED`, or `RETRACTED` |
| Applicable layer | `Layer 1 — Foundational Research` |
| Exact study ID, record ID, and version | `<identifiers>` |
| Frozen study-manifest locator and raw-byte SHA-256 | `<locator and digest>` |
| Closeout authority | `<stable person or governance identifier>` |
| Closeout timestamp | `<ISO 8601 timestamp>` |
| Supersession lineage | `<prior closeout version and raw-byte SHA-256, or None>` |
| Closeout report locator and raw-byte SHA-256 | `<immutable rendered report artifact>` |

## Completeness assertion

`EXACTLY_ONE_PUBLISHED_FINDING_PER_PLANNED_ANALYSIS`

- Frozen study analysis IDs: `<complete set>`
- Closeout disposition analysis IDs: `<complete set>`
- Set-equality check: `<passed or failed; a failed check prohibits publication>`
- Duplicate analysis or active-finding check: `<passed or failed; a failed check prohibits publication>`

Registry activation of this closeout must independently resolve the exact active frozen study, each exact active published finding, and all raw-byte digests. The closeout does not mutate the study protocol; it is a separately versioned, immutable completion assertion.

## All-analysis disposition ledger

| Planned analysis ID | Mode | Finding ID | Finding record ID and version | Finding locator and raw-byte SHA-256 | Terminal disposition | Finding status | Binding check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<ANALYSIS-...>` | `CONFIRMATORY` or `EXPLORATORY` | `<LCMRP-FIND-...>` | `<LCMRP-FINDREC-... and version>` | `<locator and digest>` | `COMPLETED`, `NOT_RUN`, `HALTED`, or `INVALID` | `PUBLISHED` | `<passed>` |

Include exactly one row for every analysis in the frozen manifest. A study may remain open with partial findings, but it cannot publish a closeout until this ledger is complete and exact.

## Failures, deviations, and unresolved conflicts

- Study-level failures or aborts: `<items, or None>`
- Protocol deviations represented in findings: `<items, or None>`
- Retracted or superseded findings excluded from the active ledger: `<identifiers and lineage, or None>`
- Unresolved conflicts: `<items, or None>`

## Security and privacy closeout

- Provenance and artifact-integrity checks: `<outcomes>`
- Retention and deletion obligations: `<outcomes and open work>`
- Incidents or unresolved risks: `<items, or None>`
- Human subjects or participant data: `None under the v0.1 foundational profiles`

## Limitations

- `<limits on completeness verification, findings, profile, sources, tools, independent review, or interpretation>`

Closeout completeness does not establish that any finding is true, externally valid, replicated, or independently validated.

## Mechanism maturity boundary

- Mechanism under evaluation: `None`
- Mechanism maturity applicability: `Not applicable`
- Awarded mechanism evidence labels: `None`
- Mechanism evidence profile changes: `None`

## Recommended next work

- Independent review or replication: `<needed work>`
- Next falsifiable question: `<question>`
- Required correction or supersession: `<None, or exact action>`


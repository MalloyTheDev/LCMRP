# M0 Completion Decision — 2026-07-21

## Decision status

- **Decision class:** Program-infrastructure, schema, and registry-semantics acceptance
- **Applicable layer:** Program infrastructure supporting all three research layers; not a research artifact
- **Decision:** **ACCEPT M0 — Research Governance and Reproducibility Foundation**
- **Effective condition:** Satisfied. Pull request [#4](https://github.com/MalloyTheDev/LCMRP/pull/4) was merged by the repository steward at `0c9165587bdc50325522c7fbbf28e36eefc9eb23` after GitHub Actions [run 29853876546](https://github.com/MalloyTheDev/LCMRP/actions/runs/29853876546) passed on exact head `233b788ae567a8d9df2cf85d1132b66b649a0662`
- **Scientific evidence produced or awarded:** None
- **Independent scientific validation:** None claimed
- **Mechanism maturity effect:** None

M0 establishes the governed infrastructure needed to begin later LCMRP research. It does not validate a taxonomy, formal model, benchmark, memory mechanism, security property, product integration, or production-readiness claim.

## Authority and reviewer relationship

Under [LCMRP Governance](../GOVERNANCE.md), the public repository owner is the initial program steward and sole maintainer until a superseding appointment is recorded. Schema and registry-history changes may be approved by that steward-maintainer through a public pull request containing rationale, compatibility impact, and validation.

This decision records the final internal judgment prepared through separate research, implementation, and adversarial-testing arms. The work is originating, agent-assisted review and is not independent scientific validation. The steward account's merge of pull request #4 supplies the required public governance acceptance; merge authority does not award a scientific evidence state.

## Governance objective

Accept the smallest product-independent foundation that makes the Program Charter operational and opens the M1 entry gate without:

- implementing a memory system;
- fabricating research records or results;
- weakening mechanism evidence gates;
- treating a frozen preregistration as a completed study;
- requiring future research methods or scientific validation inside an infrastructure milestone; or
- introducing product-specific architecture.

## Reviewed change

The accepted candidate combines the initial M0 governance foundation, the mechanism-free Layer 1 contract completed in pull request #3, and the terminal-completeness and subject-registry delta accepted in pull request #4. It adds or completes:

- a versioned foundational-subject registry with immutable definition identity and digest-linked supersession;
- exact subject and method-profile artifact binding across studies and findings;
- a separate immutable study-closeout record whose published ledger set-equals every planned analysis to exactly one active published terminal finding;
- canonical, path-safe, append-oriented study, finding, closeout, experiment, and evidence indexes;
- one-active-version and historical-provenance checks;
- human-facing foundational protocol, atomic finding-report, and study-closeout templates; and
- adversarial coverage for substitution, traversal, missing/duplicate/extra dispositions, inactive records, lineage drift, unindexed canonical records, and maturity-boundary leakage.

The real registries remain empty. Synthetic `9999` examples and fixtures are non-evidentiary contract tests.

## Alternatives considered

| Alternative | Decision and rationale |
| --- | --- |
| Make `mechanism_versions` optional in the existing experiment schema. | Rejected because mechanism-only baseline, metric, ablation, and evidence assumptions would remain hidden. |
| Treat a `FROZEN` study manifest as terminal. | Rejected because preregistration precedes execution and partial work must remain valid. A separate immutable closeout preserves that distinction. |
| Put terminal state only in mutable registry metadata. | Rejected because discoverability metadata must not become the scientific closure assertion. |
| Require computational, empirical, evidence-synthesis, or human-subject profiles before M0 completion. | Deferred because M0 is infrastructure, M1 begins with the two supported taxonomy/formal profiles, and unsupported methods are rejected rather than weakly represented. |
| Require an external registration service or independent scientific study before M0 completion. | Deferred because neither is an M0 exit criterion. Repository-local immutable bytes are sufficient for v0.1 provenance; independent scientific validation belongs to later research. |

## Compatibility and migration impact

- No real foundational subject, study, finding, closeout, experiment, evidence, or mechanism record exists, so there is no accepted research history to migrate or reinterpret.
- The foundational schemas are first-publication contracts within pull request #3; their `0.1.0` identifiers do not rewrite an earlier accepted foundational record.
- Existing mechanism experiment and evidence semantics remain separate. Symmetric path, indexing, and active-version checks strengthen their declared registry contract without awarding or removing evidence.
- Future semantic schema changes require new versions and must preserve the exact schema identifiers referenced by historical records.

## Exit-criterion evidence

| M0 exit criterion | Disposition | Evidence |
| --- | --- | --- |
| Full Program Charter v0.1 is canonical and discoverable. | Pass | Charter is linked from the repository start page and enforced as a required path. |
| Research layers and evidence-state semantics are documented. | Pass | Layer, normalization, evidence-state, governance, and contribution policies are present and cross-linked. |
| All JSON Schemas pass Draft 2020-12 meta-validation. | Pass | Repository validator and adversarial review. |
| Every example validates against its declared schema. | Pass | Dynamic schema/example discovery in the repository validator. |
| Registries parse safely, are versioned, and contain no fabricated entries. | Pass | Seven registries parse with zero entries; duplicate keys and invalid lineage are rejected. |
| Human templates expose applicable research obligations. | Pass | Proposal, experiment protocol/report, threat model, foundational protocol/finding/closeout templates. |
| Product implications are isolated and labeled. | Pass | Charter and template invariants plus boundary tests. |
| Duplicate JSON and YAML keys are rejected. | Pass | Parser tests and whole-tree validation. |
| Relative Markdown links resolve. | Pass | Whole-tree link validation. |
| Clean-checkout continuous integration passes. | Pass | GitHub Actions run 29853876546 passed on pull request #4 exact head `233b788ae567a8d9df2cf85d1132b66b649a0662` before steward merge. |
| Boundary review finds no memory implementation or product architecture in M0. | Pass | Initial boundary review and final adversarial review. |

The final local gate passed structural validation, all **86/86** unit and adversarial tests, Python compilation, and dependency consistency. The [M0 Final Adversarial Review](M0_FINAL_ADVERSARIAL_REVIEW_2026-07-21.md) records the false accepts found and corrected, test scope, limitations, and conditional technical PASS.

## Accepted limitations and post-M0 obligations

- No scientific result has been produced, reproduced, benchmarked, robustness-tested, security-reviewed, or independently validated.
- External registration-service verification is not automated.
- Controlled computational/empirical, evidence-synthesis, and human-subject profiles are unsupported until separately versioned contracts are reviewed.
- The two supported foundational profiles still require real dry runs, usability assessment, inter-reviewer testing, and later independent scientific review.
- Shared schema refactoring, migration behavior, private vulnerability-reporting enablement, and long-horizon operational testing remain future work.

These limitations constrain what may be registered or claimed; they do not prevent the governed taxonomy and formal-model work that M1 is intended to begin.

## Final decision

The candidate satisfies every applicable M0 exit criterion without crossing the Program Charter's product-independence or evidence boundaries. The condition was satisfied by the exact-head validation and steward merge of pull request #4 on 2026-07-21. M0 is accepted, and the M1 entry gate is open for product-independent memory-taxonomy and formal-model work.

This decision does not authorize a memory implementation, product integration, maturity promotion, or production claim.

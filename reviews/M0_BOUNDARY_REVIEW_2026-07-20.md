# M0 Boundary Review — 2026-07-20

## Review status

- **Review type:** Internal adversarial program-boundary and contract review
- **Disposition:** Suitable for a draft pull request; not sufficient to mark M0 complete
- **Independence:** Originating-work review; not independent validation
- **Scientific evidence reviewed or awarded:** None

This review evaluates whether the proposed M0 repository foundation enforces the Program Charter's boundaries and prevents unsupported evidence claims. It does not evaluate a memory mechanism, reproduce an experiment, award an evidence label, or establish product readiness.

> **Follow-up — 2026-07-21:** The mechanism-free foundational-study gap identified below was addressed by a parallel draft contract and reviewed in [M0 Foundational Contract Review](M0_FOUNDATIONAL_CONTRACT_REVIEW_2026-07-21.md). That follow-up retains additional blockers before M0 completion or real record registration; it does not retroactively change this review's original scope.

## Scope

The review covers the candidate M0 charter, governance policies, research-layer and evidence-label rules, JSON Schemas, synthetic examples, empty registries, templates, repository validator, tests, and continuous-integration workflow.

It asks whether the candidate foundation:

1. Keeps LCMRP independent and product-neutral.
2. Separates hypotheses, experiments, evidence decisions, and readiness claims.
3. Preserves provenance, immutable-version, and supersession obligations.
4. Rejects common schema and governance paths to overstated evidence.
5. Makes unfinished work and operational limitations visible.

## Method

- Inspected all proposed repository files for product-specific code, implementation commitments, benchmark results, real research entries, and unsupported readiness language.
- Checked every JSON Schema with the Draft 2020-12 meta-schema and every synthetic example against its matching schema.
- Exercised mutation tests for duplicate serialization keys, stale or unverifiable digests, duplicate registry identities, layer violations, invalid evidence decisions, incomplete runs, planned-only robustness claims, reviewer conflicts, and missing integration or production obligations.
- Checked relative Markdown links, dependency pins, required paths, empty registries, Charter invariants, and local artifact digests.
- Scanned the candidate file set for common credential and private-key patterns.

## Findings

### Program boundary

- No memory engine, retrieval implementation, vector-store selection, model-vendor dependency, embedding selection, application schema, or CorpusStudio production code is present.
- CorpusStudio references state the research boundary or appear in the required, explicitly provisional integration-implications section.
- The repository remains program infrastructure. It does not classify M0 itself as Layer 1, Layer 2, or Layer 3 research evidence.

### Claim and evidence discipline

- Registries are empty. Synthetic examples use conspicuous `9999` identifiers, remain draft or pending, and award no evidence label.
- Evidence labels are independent obligations represented as an awarded profile, not an automatic ladder or a single "highest" state.
- Final decisions require an action, effect, claim scope, gate assessments, attributed reviewers, authority, and supporting artifacts.
- `INDEPENDENTLY_VALIDATED` requires an eligible external evaluator. An originator or solo maintainer cannot self-award it.
- Integration and production labels require their own governance, cost, monitoring, rollback, incident-response, deletion, and operational evidence; benchmark success cannot imply them.

### Provenance and lifecycle controls

- Recorded or verified local artifacts are content-addressed and checked against raw bytes.
- Supersession references require an existing prior version and a recorded or verified digest; pending or null supersession digests are rejected.
- Confirmatory and exploratory analyses are distinct. Draft preregistrations cannot claim result access, and post-result amendments are forced to disclosed exploratory analysis.
- Human-subject sources are prohibited by the v0.1 experiment contract until a dedicated human-subject governance contract exists.

### Security and reporting

- The security policy does not claim that private vulnerability reporting is enabled.
- Risky payloads and sensitive vulnerability artifacts are prohibited until a private channel is enabled and verified.
- No credential-like values or private keys were found in the candidate file set.

## Adversarial findings and disposition

| Finding | Disposition in this candidate |
| --- | --- |
| A final evidence decision could omit its exact action, effect, gate results, or reviewer relationship. | Resolved in schema requirements and negative tests. |
| `BENCHMARKED` could be awarded with no completed run, held-out evaluation, measured resources, or failure analysis. | Resolved with accepted-decision gates and mutation tests. |
| Planned robustness work could satisfy `ROBUSTNESS-TESTED`. | Resolved; completed boundary, adversarial, and distribution-shift cases are required. |
| Documentation-only or originating-author review could satisfy `INDEPENDENTLY_VALIDATED`. | Resolved through evaluator-role, relationship, mode, materials, deviation, and outcome gates. |
| Integration or production labels could inherit scientific evidence without operational obligations. | Resolved through distinct prerequisite-evidence gates. |
| Supersession could point to mutable or unidentified prior material. | Resolved through version resolution and digest enforcement. |
| Charter display labels and machine tokens could drift into two taxonomies. | Resolved through an explicit, lossless normalization table. |
| Governance did not say who can appoint reviewers or how a solo maintainer handles independence. | Resolved through appointment, quorum, recusal, and external-evaluator rules. |
| Security guidance could imply a private reporting channel existed. | Resolved; the current limitation and enablement gate are explicit. |

## Open obligations and limitations

- The GitHub Actions job must pass on the published draft pull request before CI-related M0 exit criteria can be considered satisfied.
- Human maintainer review and an explicit M0 acceptance decision are still required. This internal review cannot supply independent validation.
- The initial experiment and evidence contracts center versioned mechanisms. Before using them for a foundational study with no mechanism under test, LCMRP must add a generic research-subject profile or explicitly version and document the narrower applicability.
- Private vulnerability reporting must be enabled and verified before the project accepts embargoed details, active exploit material, durable injection payloads, or sensitive samples.
- The schemas and examples establish contract structure only. Usability, inter-reviewer agreement, migration behavior, and completeness still require real, independently reviewed use cases.

## Conclusion

The candidate is appropriately scoped for public draft review as an M0 starting point. It contains no empirical result and supports no maturity award. M0 must remain **In progress** until its published CI run passes, the open applicability question is resolved or explicitly accepted through governance, and a maintainer records completion of every exit criterion.

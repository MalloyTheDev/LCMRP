# M1 Taxonomy-to-FMO Crosswalk Draft v0.1

Status: draft proposal · Version 0.1

## Status

This is a draft, mutable research proposal. It maps terms from the [Candidate Memory Taxonomy v0.1](MEMORY_TAXONOMY_v0.1.md) to the [Candidate Formal Memory Object Model v0.1](FORMAL_MEMORY_OBJECT_MODEL_v0.1.md). It does not validate the mapping, establish completeness, or assert any finding.

The mappings below compare the two candidate documents. A `direct` entry records an apparent named counterpart in FMO-0.1; a `partial` entry records overlap with unresolved definition or coverage obligations; an `absent` entry records no explicit counterpart identified in FMO-0.1; and a `conflict` entry records an apparent incompatibility requiring resolution. Every status remains a hypothesis pending line-level source verification.

## Proposed crosswalk

| Taxonomy term ID | Natural-language term | FMO-0.1 symbol/relation/state/operation | Mapping status | Open obligation |
| --- | --- | --- | --- | --- |
| `LCMRP-TAX-ENT-001@0.1` | Source event | `E`; `event`; `sourceOf` | direct | Test whether static sources need a separate formal type. |
| `LCMRP-TAX-ENT-002@0.1` | Memory candidate | `N`; `candidate`; `candidateState` with `PENDING`, `REJECTED`, `ADMITTED` | direct | Verify that candidate identity and undecided admission state cover all proposed positive cases. |
| `LCMRP-TAX-ENT-003@0.1` | Memory object version | `O`; `object`; `objectState`; `contentID`; `provenance` relations | direct | Determine whether these structures distinguish memory objects from ordinary governed records. |
| `LCMRP-TAX-ENT-004@0.1` | Memory series | `S`; `seriesOf`; `predecessor`; `supersedes` | direct | Define semantic continuity beyond structural successor chains. |
| `LCMRP-TAX-ENT-005@0.1` | Claim | `K`; `asserts`; `about`; `validDuring`; `assessment` | direct | Bound claim interpretation for non-propositional or mixed content. |
| `LCMRP-TAX-ENT-006@0.1` | Actor | `A`; `actorRole`; `attributedTo`; `authz` actor parameter | direct | Model group, delegated, composite, and unresolved agency without collapsing identity into authority. |
| `LCMRP-TAX-ENT-007@0.1` | Policy statement | `P`; `governs`; `policyEffect`; `policyDomain`; `effectiveFor`; `issuedBy` | direct | Define conflict handling, jurisdiction, and validity semantics. |
| `LCMRP-TAX-ENT-008@0.1` | Provenance assertion | `PT`; `prov`; provenance relation kinds | direct | Define authenticity evidence separately from structural provenance. |
| `LCMRP-TAX-ROL-001@0.1` | Episodic role | `FR=EPISODIC`; `playsRole`; optional `primaryKind` extension | partial | Formalize necessary and sufficient role conditions without biological equivalence assumptions. |
| `LCMRP-TAX-ROL-002@0.1` | Semantic role | `FR=SEMANTIC`; `playsRole`; optional `primaryKind` extension | partial | Define event-independent use and observer/query relativity. |
| `LCMRP-TAX-ROL-003@0.1` | Procedural role | `FR=PROCEDURAL`; `playsRole`; optional `primaryKind` extension | partial | Distinguish procedure-shaped content from action-controlling use. |
| `LCMRP-TAX-ROL-004@0.1` | Prospective role | `FR=PROSPECTIVE`; `playsRole`; optional `primaryKind` extension | partial | Decide whether autonomous monitoring is required or query-time matching can suffice. |
| `LCMRP-TAX-ROL-005@0.1` | Working role | `FR=WORKING`; `playsRole` | partial | Determine whether working status is a role, resource limit, access tier, temporal scope, or process state. |
| `LCMRP-TAX-OPS-001@0.1` | Encoding | `encode`; `WAS_ENCODED_FROM`; `candidate` output | direct | Test whether untracked copying and encoding remain distinguishable. |
| `LCMRP-TAX-OPS-002@0.1` | Admission | `admit`; `CandidateState=ADMITTED`; `ObjectState=ACTIVE`; `WAS_ADMITTED_FROM` | direct | Verify separation of acceptance, belief, truth, and usefulness. |
| `LCMRP-TAX-OPS-003@0.1` | Retrieval | `retrieve`; `accessible`; `WAS_RETRIEVED_IN` | direct | Address unsolicited activation, cached context, and non-disclosure cases. |
| `LCMRP-TAX-OPS-004@0.1` | Update | `update`; `WAS_UPDATED_FROM`; `predecessor`; `supersedes` | direct | Define when a changed version preserves series continuity. |
| `LCMRP-TAX-OPS-005@0.1` | Consolidation | `consolidate`; `WAS_CONSOLIDATED_FROM`; `usedInput` | direct | Distinguish consolidation from aggregation without assuming improvement. |
| `LCMRP-TAX-OPS-006@0.1` | Abstraction | `abstract`; `WAS_ABSTRACTED_FROM`; abstraction rule in operation inputs | direct | Distinguish abstraction from compression or undeclared omission. |
| `LCMRP-TAX-OPS-007@0.1` | Reconsolidation | `reconsolidate`; `WAS_RECONSOLIDATED_FROM`; retrieval/reactivation precondition | direct | State the causal evidence needed beyond update after retrieval. |
| `LCMRP-TAX-OPS-008@0.1` | Deduplication | `deduplicate`; equivalence assessment operation | direct | Define task-scoped equivalence without erasing governance differences. |
| `LCMRP-TAX-OPS-009@0.1` | Decay | No dedicated operation; represented only through changed accessibility, priority, confidence, or retention-related values when declared | partial | Decide whether decay is a mechanism, policy, observed effect, or family of processes. |
| `LCMRP-TAX-OPS-010@0.1` | Forgetting | `forget`; `ObjectState=SUPPRESSED`; `accessible` changes | direct | Define ordinary availability independently of a retrieval mechanism. |
| `LCMRP-TAX-OPS-011@0.1` | Archival | `archive`; `restore`; `ObjectState=ARCHIVED` | direct | Specify lower-default-access and recovery conditions relative to actors and purposes. |
| `LCMRP-TAX-OPS-012@0.1` | Deletion | `requestDelete`; `executeDelete`; `DS`; `DeletionResult`; `DeletionSuccess`; `ObjectState=DELETE_PENDING/DELETED` | direct | Formalize closure, verification, external copies, and audit residue leakage. |
| `LCMRP-TAX-OPS-013@0.1` | Conflict detection | `detectConflict`; `conflicts`; `CX` | direct | Bound interpretation semantics and decidability. |
| `LCMRP-TAX-EPI-001@0.1` | Confidence assessment | `CA`; `confidence`; `numericValue` optional projection | direct | Define scale compatibility, calibration claims, and aggregation rules. |
| `LCMRP-TAX-EPI-002@0.1` | Uncertainty description | `UA`; `uncertainty`; candidate uncertainty kinds | direct | Determine which uncertainty kinds are comparable or must remain separate. |
| `LCMRP-TAX-EPI-003@0.1` | Claim conflict | `conflicts`; `detectConflict`; `validDuring`; `CX` | direct | Distinguish contradiction, ambiguity, temporal succession, and unknown compatibility. |
| `LCMRP-TAX-GOV-001@0.1` | Authority grant | `authz`; `AuthzDecision`; `actorRole`; `governs`; `policyEffect` | partial | Add a policy calculus for grants, denials, obligations, delegation, revocation, and jurisdiction. |
| `LCMRP-TAX-GOV-002@0.1` | Provenance trace | `trace(x)`; `prov`; `sourceOf`; `derivedFrom`; `generatedBy`; `usedInput`; `attributedTo` | direct | Specify completeness criteria and forgery assessment. |
| `LCMRP-TAX-GOV-003@0.1` | Deletion scope | `DS`; `scope`; `Targets`; `DeletionSuccess` | direct | Establish when closure is finite, discoverable, and stable. |
| `LCMRP-TAX-GOV-004@0.1` | Retention obligation | `P` with `policyEffect=REQUIRE`; `governs`; `authz=UNRESOLVED` for contested operations | partial | Formalize retention duties and adjudication against deletion requests. |

## Known limitations

- No mapping row has been independently reviewed or established as a finding.
- Apparent symbol-name correspondence can conceal weaker, broader, circular, or conflicting semantics.
- The table supplies no line-level citation ledger, completeness proof, counterexample search, or treatment of concepts outside the 33 taxonomy term IDs.
- Both mapped artifacts are candidates with unresolved obligations; a mapping cannot validate either one through mutual reference.
- The labels `direct` and `partial` are provisional coding values, not evidence-backed dispositions.

## Next falsification step

Create a separately versioned analysis plan that binds the exact registered subject digests, maps every row to exact source locations in both candidates, permits `absent` and `conflict` outcomes, requires two independent semantic mappings plus retained disagreement, and rejects any row whose apparent correspondence is broader, circular, unsupported, or dependent on an undeclared implementation assumption. Do not add the result to either registered v1 subject in place.

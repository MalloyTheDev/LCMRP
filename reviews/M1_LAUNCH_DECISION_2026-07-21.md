# M1 Launch Decision — 2026-07-21

## Decision status

- **Decision class:** Program-governance acceptance supporting Layer 1 work; not a research artifact
- **Milestone:** M1 — Candidate Memory Taxonomy and Formal Object Model
- **Decision:** **ACCEPT M1 LAUNCH CANDIDATE — EFFECTIVE ON CONDITIONED MERGE**
- **M1 state after the condition:** Launched and in progress; not complete
- **Effective condition:** The exact head of pull request [#6](https://github.com/MalloyTheDev/LCMRP/pull/6) must pass the required GitHub Actions workflow and then be merged by the repository steward
- **Scientific evidence produced or awarded:** None
- **Mechanism maturity effect:** None
- **Production registry effect:** None; all production registries remain empty

This decision authorizes publication of falsifiable Layer 1 candidates and a governed M1 research agenda. It does not adopt the taxonomy, establish the formal model's consistency, report a foundational finding, validate a memory mechanism, authorize an implementation, or complete M1.

## Launch question

Does the initial M1 package establish a product-independent, falsifiable basis for studying memory terminology and a formal memory-object model without presenting candidate definitions as findings, selecting implementation infrastructure, or crossing into product integration?

## Applicable layer and artifact relationship

The taxonomy, formal object model, and prior-art map each declare exactly **Layer 1 — Foundational Research**. This launch decision and its automated tests are program-governance infrastructure supporting that layer; they are not research findings.

The launch package contains:

- [M1 Foundation](../docs/program/M1_FOUNDATION.md), which declares the active scope, six falsifiable objectives, stop rules, and thirteen still-unchecked exit criteria;
- [M1 Prior Art and Competing Memory Taxonomies](../docs/taxonomy/M1_PRIOR_ART_AND_COMPETING_TAXONOMIES.md), an unregistered and non-systematic research input;
- [Candidate Memory Taxonomy v0.1](../docs/taxonomy/MEMORY_TAXONOMY_v0.1.md), which proposes versioned terms, axes, competing organizations, observable distinctions, and rejection conditions;
- [Candidate Formal Memory Object Model v0.1](../docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md), which proposes typed entities, transitions, operations, invariants, countermodels, and missing proof obligations;
- [M1 launch adversarial tests](../tests/test_m1_launch.py); and
- [M1 Launch Adversarial Review](M1_LAUNCH_ADVERSARIAL_REVIEW_2026-07-21.md).

No artifact above is an active foundational-subject registry entry, frozen study, published finding, immutable closeout, experiment, evidence decision, or mechanism maturity award.

## Isolated three-arm process

| Arm | Scope | Exclusive writable paths | Final output |
| --- | --- | --- | --- |
| Deep research | Primary and authoritative prior art, competing organizations, transfer limits, operational distinctions, and falsifiable comparison questions | `docs/taxonomy/M1_PRIOR_ART_AND_COMPETING_TAXONOMIES.md` | Seven competing organization schemes, fourteen observable distinctions, fifteen adversarial edge cases, twelve falsifiable questions, and a bounded source index |
| Specification | Milestone definition, candidate taxonomy, and candidate formal object model | `docs/program/M1_FOUNDATION.md`; `docs/taxonomy/MEMORY_TAXONOMY_v0.1.md`; `docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md` | Six objectives, thirty-three candidate terms, two competing primary organizations, sixteen invariants, ten countermodels, and explicit open proof obligations |
| Adversarial verification | Negative launch gates and independent-in-process boundary review | `tests/test_m1_launch.py`; `reviews/M1_LAUNCH_ADVERSARIAL_REVIEW_2026-07-21.md` | Seventeen M1 gates and a conditional launch-only PASS |

The arms had disjoint writable paths. The verification arm read the completed research package but did not edit it. Root integration was limited to navigation, continuous-integration naming, required-path registration, this decision, final validation, and publication.

The process is originating and agent-assisted. File isolation reduces self-review coupling, but it is not independent scientific validation.

## Final-judge reconciliation

The package passes the launch threshold for the following reasons:

1. **Claim discipline:** Every research artifact is labeled as a candidate or research input, disclaims scientific findings and mechanism evidence, and preserves explicit unknowns, counterexamples, and rejection rules.
2. **Competing explanations:** The prior-art map compares multiple organizing principles, while the candidate taxonomy forces stable kind-first and contextual role-first organizations to make different identity and cardinality commitments.
3. **Operational distinctions:** The taxonomy separates representation, role, lifecycle, time, epistemic posture, provenance, authority, availability, derivation, and sensitivity rather than overloading one biological or storage hierarchy.
4. **Formal falsifiability:** FMO-0.1 names intended entailments and non-entailments, proposes countermodels, and states that no consistency, satisfiability, or proof result has been obtained.
5. **Governance and safety surface:** Authority, provenance, confidence, uncertainty, conflict, failure retention, deletion scope, derivative closure, and verification limits are first-class candidate semantics.
6. **Architectural independence:** No storage engine, vector database, model, embedding provider, application schema, cloud assumption, user interface, or full memory service is selected or built.
7. **Evidence boundary:** The launch creates no registry entries, studies, findings, closeouts, benchmarks, implementation measurements, or evidence-state transitions.

Representative source spot checks confirmed that the cited source pages support the map's use of CoALA as a modular language-agent architecture, W3C PROV as a domain-agnostic provenance model, NIST ABAC as operation- and attribute-scoped access-control guidance, and AgentPoison as primary memory/knowledge-base poisoning work. This limited check is not a reproduction of the full prior-art search and cannot establish completeness or novelty.

## Adversarial result and validation

The separate internal review found no local launch blocker and issued **CONDITIONAL PASS — M1 launch only**. It tested premature completion, maturity and novelty laundering, vendor coupling, hidden product assumptions, unobservable categories, false provenance or confidence entailments, lifecycle collapse, authority-free mutation, deletion overclaiming, fabricated registry effects, and broken package links.

The reconciled local tree passed:

- repository structural validation;
- all **17/17** dedicated M1 launch tests;
- all **103/103** repository unit and adversarial tests;
- Python compilation for tools and tests; and
- dependency consistency.

These checks establish repository and claim-boundary consistency only. The exact public pull-request head must independently pass GitHub Actions before the decision becomes effective.

## Rejected launch alternatives

| Alternative | Decision and rationale |
| --- | --- |
| Select the faceted taxonomy as canonical at launch. | Rejected. Its apparent coverage is a design hypothesis that must compete against simpler organizations under frozen cases. |
| Treat functional labels as mutually exclusive intrinsic kinds. | Not adopted. The role-first alternative must remain available because mixed and changing uses create different observable commitments. |
| Register the candidate subjects immediately. | Deferred. The accepted sequence first exercises non-evidentiary contract dry runs and stabilizes exact artifacts before any registry activation. |
| Encode FMO-0.1 in a solver during launch. | Deferred to governed formal analysis. A rushed encoding could hide unresolved semantics and would not itself establish semantic validity. |
| Begin a storage or retrieval implementation. | Rejected as outside M1 launch and contrary to the M1 entry boundary. |

## Open M1 completion obligations

M1 remains incomplete until its foundation's exit criteria are satisfied. Material blockers include:

- exact taxonomy and formal-model subject versions registered with immutable digests after contract dry runs;
- one frozen structural/taxonomy study and one frozen formal-analysis study;
- preregistered positive, negative, ambiguous, adversarial, and held-out cases;
- exactly one published atomic finding or terminal disposition per planned analysis and immutable study closeouts;
- explicit retain, narrow, supersede, or reject dispositions for M1-O1 through M1-O6;
- machine-checked satisfiability, entailment, non-entailment, and countermodel work under declared assumptions;
- security, privacy, authority, provenance-forgery, and deletion-failure dispositions;
- independent claim review; and
- a versioned M1 completion decision preserving negative, null, contradictory, invalid, and halted outcomes.

## Accepted launch limitations

- The prior-art map is bounded, English-language, and non-systematic; absence from it is not evidence of novelty.
- Candidate terms have not been tested for inter-rater agreement, coverage, construct validity, or operational usefulness.
- FMO-0.1 is natural-language mathematics with no solver or proof-assistant encoding.
- The total transaction order, deletion closure, authority composition, confidence scales, and conflict semantics may require rejection or material revision.
- Constructed examples and countermodels are non-evidentiary until evaluated through frozen methods.
- No runtime, model, dataset, participant, latency, storage, compute, token-cost, security-control, privacy-control, or deletion-effectiveness measurement exists.
- The internal adversarial arm is not an independent scientific reviewer.

## Final disposition

**CONDITIONAL ACCEPT — M1 LAUNCH ONLY.** The package is suitable for publication as an in-progress Layer 1 research agenda and set of candidate artifacts. This decision becomes effective only after exact-head GitHub Actions succeeds and the steward merges pull request [#6](https://github.com/MalloyTheDev/LCMRP/pull/6).

The decision must not be restated as taxonomy adoption, formal-model correctness, research evidence, mechanism validation, implementation readiness, an integration recommendation, or M1 completion.

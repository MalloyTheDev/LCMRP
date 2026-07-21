# Evidence and Readiness States

## Purpose

Evidence states communicate what has actually been established for a specific mechanism version. They are controlled research claims, not promotional labels, implementation milestones, or automatic consequences of passing tests.

A state applies only to the mechanism, version, configuration range, datasets or scenarios, threat model, and evaluation conditions named by its supporting evidence.

The Program Charter's labels are the authoritative human-readable display labels. Machine-readable artifacts use canonical underscore tokens. The exact, lossless mapping is defined in [Evidence Label Normalization](EVIDENCE_LABELS.md). The machine tokens are serialization aliases; they do not create different states or weaken the Charter definitions.

## State definitions and minimum gates

| State | Minimum evidence gate |
| --- | --- |
| `HYPOTHESIS` | A precise mechanism claim, assumptions, scope, predicted outcome, comparison target, and falsification or rejection criterion are recorded. |
| `PROTOTYPE` | A runnable investigative implementation exists with a stable identifier, documented interfaces, provenance, reproducible configuration, and basic correctness tests. |
| `REPLICATED` | The declared result has been reproduced across multiple controlled runs; seeds, run conditions, variance, deviations, and failed replications are retained. |
| `BENCHMARKED` | The mechanism has been evaluated against declared baselines on representative and held-out cases with predefined metrics, costs, and failure analysis. |
| `ROBUSTNESS-TESTED` | Boundary, adversarial, corrupted-input, and relevant distribution-shift tests have been run, with residual failure modes and the tested envelope documented. |
| `SECURITY-REVIEWED` | Assets, actors, trust boundaries, adversary capabilities, abuse cases, privacy risks, mitigations, residual risks, and deletion behavior have been documented and reviewed. |
| `INDEPENDENTLY VALIDATED` | Evidence has been reproduced or substantively reviewed outside the originating experiment, with evaluator independence, materials used, deviations, and outcome recorded. |
| `INTEGRATION CANDIDATE` | Independent evidence supports a product-specific feasibility assessment, and benchmark, robustness, security, operational-cost, and governance prerequisites are explicitly satisfied for the claimed scope. |
| `PRODUCTION-READY` | Product-specific validation, operational testing, security review, privacy review, governance approval, monitoring, rollback, deletion, and incident-response requirements are satisfied for a defined deployment. |

## State semantics

The states express distinct evidence obligations, not a single total ordering. An accepted evidence decision awards one bounded label. The set of labels currently supported for an exact mechanism version and claim scope is its **awarded evidence profile**.

Reports and registries must display the relevant profile rather than collapsing it into a highest state. Some investigations may satisfy gates in a different chronological order, but no evidence obligation is inherited merely because a later-sounding label has been assigned. `INTEGRATION CANDIDATE` and `PRODUCTION-READY` are convergence gates with explicit prerequisites; they do not turn the remaining labels into an automatic sequence.

In particular:

- `PROTOTYPE` means runnable, not effective.
- `REPLICATED` means a result repeated under declared conditions, not generalized.
- `BENCHMARKED` means compared within the declared benchmark scope, not robust or secure.
- `ROBUSTNESS-TESTED` applies only to the tested attacks, boundaries, and shifts.
- `SECURITY-REVIEWED` means risks were systematically analyzed; it does not mean risk-free.
- `INDEPENDENTLY VALIDATED` must state exactly which claims were independently supported.
- `INTEGRATION CANDIDATE` authorizes feasibility assessment, not product adoption.
- `PRODUCTION-READY` cannot be inferred from LCMRP research evidence alone. It requires a named product and deployment context outside the foundational and reference-implementation phases.

## Evidence-state decision record

Every award, denial, qualification, demotion, or withdrawal must be supported by an immutable decision record containing:

- Mechanism identifier and exact version or digest
- Previous awarded evidence profile and the single state under decision
- Claim and scope to which the state applies
- Evidence-record identifiers
- Protocol, benchmark, dataset, model, configuration, seed, code, and environment identifiers where applicable
- Gate-by-gate assessment
- Reviewer identity and relationship to the originating experiment
- Known failures, limitations, uncertainty, and unresolved risks
- Decision and rationale
- Decision date

Continuous integration, a passing test suite, an author's assertion, or completion of a planned milestone must not award an evidence state automatically.

## Versioning and inheritance

Evidence attaches to an immutable mechanism version. A changed mechanism receives a new version or digest.

Prior evidence may be referenced only when an explicit equivalence assessment shows why the change cannot affect the supported claim. Otherwise, the relevant evidence gate must be rerun. Changes to retrieval policy, lifecycle behavior, provenance handling, trust boundaries, data transformations, model components, or default configuration are presumed material until shown otherwise.

## Demotion and withdrawal

A mechanism must be demoted, qualified, or marked withdrawn when later evidence invalidates a gate, reveals an unmodeled threat, exposes irreproducibility, or shows that the recorded scope was materially overstated.

The original record must remain available. Corrections are appended through a new evidence decision so that negative results and changes in understanding are auditable.

## Independent validation

An independent validation record must disclose:

- Whether the evaluator contributed to the mechanism or originating experiment
- Which artifacts and instructions were available
- Whether results were reproduced, reanalyzed, or reviewed
- Any protocol deviations or unavailable dependencies
- The claims supported, contradicted, or left unresolved
- Conflicts of interest or organizational relationships

Independent review of documentation alone must not be represented as experimental reproduction.

## Evidence claim checklist

Before displaying an evidence state, verify that:

1. The mechanism version and claim scope are unambiguous.
2. All required evidence records exist and are traceable.
3. Baselines and rejection criteria were declared before interpreting results, or the analysis is clearly labeled exploratory.
4. Failed, null, and contradictory results are retained.
5. Costs, limitations, uncertainty, and material security or privacy risks are visible.
6. The state does not imply untested generalization or product readiness.
7. Any CorpusStudio implication is isolated and labeled `RESEARCH-TO-PRODUCT HYPOTHESIS`.

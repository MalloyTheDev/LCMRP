# Benchmark and Evaluation Design

**Applicable layer:** Layer 1 — Foundational Research  
**M0 status:** Evaluation requirements established; no benchmark, dataset, baseline result, or leaderboard has been released.

LCMRP benchmarks must evaluate memory behavior over time, not merely whether a system can retrieve a fact from a store. They must distinguish useful retention from indiscriminate accumulation and measure whether authority, provenance, privacy, and deletion constraints are respected.

## Charter-derived capability targets

| Capability | Evaluation question |
| --- | --- |
| Long-horizon continuity | Can relevant state support a task after many intervening sessions and events? |
| Selective retention | Does the system preserve information that remains useful while excluding irrelevant or unauthorized material? |
| Appropriate forgetting | Does information become unavailable when policy, expiry, correction, or task relevance requires it? |
| Contradiction handling | Does the system detect and respond appropriately to incompatible observations or claims? |
| Temporal reasoning | Can it distinguish event time, observation time, update order, and current validity? |
| Source-sensitive recall | Does retrieval and response behavior account for provenance, authority, and confidence? |
| Preference evolution | Can preferences change without treating an old preference as an immutable identity fact? |
| Cross-session task continuation | Can work resume with the necessary state while preserving scope and user boundaries? |
| Interference resistance | Does unrelated or adversarial memory degrade relevant retrieval or decision quality? |
| Safe deletion | Are targeted records and covered derivatives removed according to declared semantics? |
| Corruption recovery | Can the system identify, quarantine, and recover from damaged or poisoned memory state? |

These are evaluation targets, not claims that a benchmark design or memory mechanism already satisfies them.

## Required benchmark artifacts

Every benchmark release should include:

- A versioned task specification and explicit construct definition
- Falsifiable capability claims and known non-claims
- Scenario or dataset provenance, licenses, and data-governance record
- Immutable generation and split procedures
- Development, validation, and access-controlled held-out test separation where appropriate
- Contamination, memorization, and benchmark-gaming analysis
- Baseline definitions and executable configurations
- Metric definitions, units, directionality, uncertainty, and failure handling
- Random seeds and nondeterminism documentation
- Scoring and evaluation code with integrity checks
- Latency, storage, compute, and token-cost measurements
- Boundary, adversarial, and distribution-shift cases
- Security, privacy, deletion, and cross-user isolation tests where applicable
- A threat model for benchmark infrastructure and hidden test assets
- Known limitations, invalid uses, and retirement criteria
- A result format that retains negative, failed, invalid, and aborted runs

## Baseline discipline

Use multiple baselines when they isolate different causal questions. Candidate baseline families may include:

- No persistent memory
- Fixed recent-context or bounded transcript
- Simple exact-match or structured lookup
- A minimal retrieval system without consolidation or updating
- A stronger published or independently implemented method, when licensing and reproducibility permit

The final choice belongs in a versioned proposal and protocol. Baselines must receive comparable data, context, tool access, time, compute, and tuning opportunity. Report every material mismatch.

## Measurement principles

- Report capability components separately before considering a composite score.
- Distinguish memory admission, storage, retrieval, use, update, and deletion failures.
- Separate task success from policy compliance and security outcomes.
- Treat abstention as its own behavior rather than automatically correct or incorrect.
- Include uncertainty across scenarios, seeds, models, and time horizons.
- Predeclare missing-data, invalid-run, and early-stopping rules.
- Prevent evaluation answers and future events from entering the system's observable state.
- Evaluate both helpful memory and the cost of irrelevant, stale, contradictory, or malicious memory.
- Avoid interpreting benchmark performance as human-like cognition, general intelligence, or production readiness.

## Longitudinal split integrity

Long-horizon evaluations require stronger isolation than a random row split. A specification should define:

- Which events are visible at each simulated time
- Which facts, preferences, permissions, and sources can change
- Which queries may reveal future labels or hidden state
- How identities and users remain isolated
- How generator templates are separated across splits
- Whether models or operators can inspect held-out scenarios
- How reruns avoid adapting to the held-out set

## Benchmark acceptance and rejection

A benchmark should be revised or rejected when it cannot distinguish the target capability from prompt length, model knowledge, evaluator leakage, or application-specific assumptions; when its labels are not reproducible; when its privacy or licensing basis is inadequate; or when a trivial shortcut dominates the intended task.

Benchmark publication does not imply that any evaluated mechanism is `BENCHMARKED`. That state requires declared baseline results, metrics, configurations, and evidence records for the specific mechanism version.

## M0 exit condition for this workstream

M0 creates the evaluation-design boundary and quality requirements only. Subsequent work must propose benchmark constructs, test them for validity and leakage, implement baseline harnesses, and publish reproducible evidence before reporting comparative performance.

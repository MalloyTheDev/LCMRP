# Experimental Practice

**Layer rule:** Each experiment declares exactly one applicable layer; cross-layer work uses separate linked artifacts  
**M0 status:** Workflow and templates established; no experiment has been registered or executed.

LCMRP experiments test bounded hypotheses under versioned conditions. They do not promote a mechanism automatically, and they retain negative, null, failed, invalid, and aborted outcomes as program evidence.

## Artifact sequence

1. **Research proposal:** defines the question, hypothesis, comparison, rejection criteria, risks, and intended evidence decision.
2. **Frozen protocol:** fixes variables, assets, run matrix, metrics, analysis, security controls, and deviation rules before confirmatory execution.
3. **Run artifacts:** preserve exact configuration, provenance, logs, measurements, failures, and environment identity for every run.
4. **Experiment report:** accounts for all runs and separates predeclared results from post-hoc exploration.
5. **Evidence record:** states the bounded claim, supporting and conflicting artifacts, limitations, and review status.
6. **Registry update:** indexes the immutable versions without replacing prior evidence.

Use the files in `templates/` as the human-facing starting point. Machine-readable schemas and registry entries supplement these documents; neither form replaces the other.

## Mechanism-free foundational studies

Taxonomy, formal-model, concept, and evaluation-construct studies must not invent a dummy mechanism or borrow a mechanism maturity label. Use the parallel [Foundational Study Contract v0.1](../program/FOUNDATIONAL_STUDY_CONTRACT.md), its study manifest, and its atomic research-finding record.

The v0.1 foundational path supports structural/taxonomy evaluation and formal analysis only. Its findings cannot award or change a mechanism evidence profile. Controlled computational/empirical and evidence-synthesis profiles remain open contract work.

## Before execution

An experiment is ready to run only when:

- Its applicable layer and system boundary are explicit.
- The hypothesis, competing explanation, and falsifier are testable.
- Baselines are versioned and comparison budgets are fair.
- Representative and held-out cases are defined without future-event leakage.
- Metrics, uncertainty, missing-data handling, and decision thresholds are predeclared.
- Seeds, model versions, datasets, prompts, policies, dependencies, hardware, and external services can be recorded exactly.
- Ablation, boundary, adversarial, and distribution-shift coverage is proportionate to the claim.
- Required privacy, security, and governance review is complete.
- Stop conditions and rejection criteria cannot be confused with successful completion.

Exploratory work may begin with an explicitly exploratory protocol, but it must not be relabeled confirmatory after results are known.

## During execution

- Assign every run a stable identifier.
- Capture start and end times, configuration and artifact digests, seeds, environment identity, resource measurements, and exit status.
- Preserve raw observations before transformation or aggregation.
- Log operator interventions and external-service changes.
- Quarantine corrupted or security-relevant artifacts without destroying their evidentiary record.
- Do not rerun selectively only because a result is unfavorable.
- Do not overwrite a frozen protocol, dataset version, configuration, or completed report.

Any protocol deviation must identify when it occurred, why, which runs it affected, who authorized it, and how it changes interpretation.

## Failure classification

Classify at least the following separately:

| Category | Meaning |
| --- | --- |
| Mechanism failure | The tested mechanism behaved contrary to its declared requirements under a valid test. |
| Implementation defect | Code or configuration did not implement the intended mechanism. |
| Infrastructure failure | Hardware, runtime, network, storage, or provider behavior prevented a valid observation. |
| Evaluation invalidity | Leakage, contamination, scoring error, protocol violation, or insufficient coverage invalidated the inference. |
| Security or privacy failure | A declared security property, authority boundary, isolation rule, or data-lifecycle requirement failed. |
| Inconclusive outcome | The observation cannot distinguish the hypothesis from its alternatives under the declared decision rule. |

Root cause may remain `unknown`; do not convert uncertainty into a mechanism conclusion.

## Evidence-profile decisions

An experiment report recommends an action for one evidence state; the relevant review process decides it. Independently awarded labels form an evidence profile, not a single current state or a linear checklist:

- `REPLICATED` requires controlled reproduction, not repeated trials hidden within one run.
- `BENCHMARKED` requires declared baselines, metrics, and comparable conditions.
- `ROBUSTNESS_TESTED` requires adversarial, boundary, and distribution-shift evidence.
- `SECURITY_REVIEWED` requires a scoped threat model and documented material risks.
- `INDEPENDENTLY_VALIDATED` requires review or reproduction outside the originating experiment.
- `INTEGRATION_CANDIDATE` and `PRODUCTION_READY` require separate product-specific evidence and governance.

Contradictory evidence remains linked to the mechanism. Superseding a report does not erase the earlier result.

## Reproducibility minimum

A report should enable an independent party to reconstruct:

- The exact source tree and uncommitted-state policy
- Models, datasets, prompts, policies, and configurations by immutable version or digest
- Seeds and seed derivation
- Hardware, firmware, operating system, drivers, runtime, and locked dependencies
- Storage, retrieval, embedding, and policy components
- Run order, interventions, timeouts, retries, and invalidation rules
- Raw and derived result provenance
- Compute, latency, storage, energy when available, and token-cost accounting

Any artifact that cannot be shared must be identified together with the access constraint and the resulting limit on replication.

## Layer separation

Layer 1 experiments investigate general concepts. Layer 2 experiments may evaluate replaceable reference components but must remain product-independent. Layer 3 may assess feasibility for a named product only after independent evidence exists. Any CorpusStudio discussion belongs exclusively in the required `Future CorpusStudio Integration Implications` section and remains a `RESEARCH-TO-PRODUCT HYPOTHESIS` until independently validated.

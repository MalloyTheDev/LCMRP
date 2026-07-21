# LCMRP Agent Instructions

These instructions apply to the entire repository.

## Program identity

LCMRP is a standalone, product-independent research and engineering program. It is not a CorpusStudio subsystem. CorpusStudio may appear only as a future integration target under the boundary defined in the Program Charter.

The canonical governing document is [`docs/program/PROGRAM_CHARTER_v0.1.md`](docs/program/PROGRAM_CHARTER_v0.1.md). If a task conflicts with that charter, stop and surface the conflict instead of silently weakening the charter.

## Research layers

Every substantive artifact must declare exactly one applicable layer:

1. Foundational Research
2. Product-Independent Reference Implementations
3. Future CorpusStudio Integration

Program infrastructure may explicitly state that it supports all layers without constituting research evidence.

Do not place CorpusStudio-specific production code, schemas, or architecture in Layer 1 or Layer 2 work. Any permitted CorpusStudio discussion must be isolated under **Future CorpusStudio Integration Implications** and labeled **RESEARCH-TO-PRODUCT HYPOTHESIS**.

## Claim discipline

- Distinguish hypotheses, implementations, observations, and conclusions.
- Do not invent citations, identifiers, measurements, benchmark outcomes, or replication claims.
- Do not call a mechanism novel without a documented prior-art search.
- Do not promote an evidence state automatically. Record the evidence satisfying each transition obligation.
- Preserve negative, null, contradictory, and failed results.
- Treat examples and fixtures as non-evidence unless an experiment record explicitly establishes otherwise.
- Separate reproduced facts from inference and unresolved assumptions.

## Experiment obligations

Use the repository schemas and templates for substantive work. An experiment should declare, where applicable:

- a falsifiable hypothesis;
- comparison baselines;
- held-out and adversarial cases;
- metrics and success thresholds;
- rejection or stop criteria;
- seeds, model versions, dataset identities, configuration, environment, and artifact digests;
- latency, storage, compute, and token-cost measurements;
- security, privacy, deletion, and governance considerations;
- limitations, failure categories, and the next falsification step.

Raw results are immutable evidence inputs. Corrections or reinterpretations should create a new record linked to the superseded record rather than rewriting history.

Mechanism-free Layer 1 taxonomy, formal-model, concept, and evaluation-construct studies use the parallel [Foundational Study Contract](docs/program/FOUNDATIONAL_STUDY_CONTRACT.md). Resolve an active frozen study through the versioned subject registry, publish one atomic finding or disposition per analysis, and use an immutable closeout for terminal completeness. Do not invent a dummy mechanism, make `mechanism_versions` optional, or assign a Charter mechanism evidence label to a foundational subject, finding, or closeout.

## Implementation boundaries

- Keep reference implementations replaceable at storage, retrieval, model, and embedding boundaries where practical.
- Do not assume continuous cloud access, unlimited compute, a model vendor, an embedding provider, or a vector database.
- Keep experimental mechanisms distinguishable from supporting infrastructure.
- Do not describe a runnable prototype as production-ready.
- Do not begin product integration merely because a benchmark improved.

## Repository workflow

Before submitting changes:

1. Run `python tools/validate_repository.py` after installing `requirements-dev.txt`.
2. Run `python -m unittest discover --start-directory tests --verbose`.
3. Confirm relative links resolve and examples validate against JSON Schema Draft 2020-12.
4. State the research layer, evidence status, limitations, and any open validation obligations in the pull request.

Changes to the charter, schemas, evidence-state semantics, or registry history require explicit review because they can alter the interpretation of existing research artifacts.

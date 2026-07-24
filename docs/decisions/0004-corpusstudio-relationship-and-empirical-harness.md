# 0004. Relationship to CorpusStudio, and adopting its harness for empirical work

- **Status:** Accepted
- **Date:** 2026-07-24
- **Deciders:** Maintainer
- **Affects:** `README.md`, `studies/h4-longmemeval-oracle/`, empirical roadmap

## Context

LCMRP began while building CorpusStudio's training/evaluation harness: managing
memory in a real system surfaced the questions about identity, provenance,
supersession, authority, and deletion that this project now formalizes. Both
repositories are maintained by the same person. An earlier AI-generated
governance layer had declared LCMRP "not a CorpusStudio subsystem" and required
every mention of CorpusStudio to be quarantined — a firewall that misstated the
real lineage and has since been removed with the rest of that apparatus.

Separately, hypothesis H4 needs an empirical harness (serve a model, run a
long-memory benchmark, score it). CorpusStudio already has one: a torch-optional
evaluation path (`eval-run` → `run_evaluation` → a scorer), model backends
(vLLM/ollama/openai-compatible and in-process 4-bit), per-example honesty
(null-with-reason, measured-vs-unavailable), and hash-bound provenance.

## Decision

**1. State the true relationship.** LCMRP is the **research arm of
CorpusStudio**: it investigates the lifelong-memory questions that arose while
building CorpusStudio's harness, and its findings feed back into the product.
The README says this plainly. No quarantine, no "not a subsystem" firewall.

**2. Keep independence of *evidence*, not of *purpose*.** Because findings are
meant to inform a product the maintainer also owns, the honesty rules in
`METHOD.md` (preregister before analysis, report nulls, cap solo work at E2,
mark confirmatory vs exploratory) are what keep a finding trustworthy enough to
rely on. Independence here means the evidence is judged on its merits — not a
wall between the projects.

**3. Use the CorpusStudio harness for empirical studies.** H4 and its scoped
first step (H4-Oracle) run on CorpusStudio's eval path. Runs disclose the local
model (Qwen2.5-7B), decode settings, and hardware, and stay E2 (single-analyst,
not independently replicated) until someone else replicates.

Alternatives considered: build a separate eval stack in LCMRP (rejected —
duplicates a working, honesty-aligned harness the maintainer already owns);
keep the firewall (rejected — it misstates the lineage and blocks the obvious
empirical path).

## Consequences

The empirical roadmap has a concrete home. `studies/h4-longmemeval-oracle/`
holds the preregistered plan and a LongMemEval→instruction converter, runnable
on the local GPU. A small deterministic QA scorer will be added to CorpusStudio
(a separate PR) so H4 can report a reproducible metric alongside the LLM judge.
The two projects share tooling openly while LCMRP's evidence stays method-first.

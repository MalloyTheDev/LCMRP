# Testable Hypotheses

Falsifiable propositions this project can test, drawn from the candidate
taxonomy and formal model. Each states what it predicts, how to test it, what
would confirm or refute it, and whether one person can run it. All are **E1
(candidate)** until a preregistered study moves them (see [`METHOD.md`](../METHOD.md)).

Most of the field proposes a memory system and reports a benchmark win; almost
none state a falsifiable structural hypothesis with rejection conditions. That
gap is where this project sits — so the hypotheses below are framed to be
*refutable*, not just demonstrable.

Sequence recommendation: **H1 (paper) → H3 (formal) → H4/H5 (code)**.

## H1 — Organizations K and R genuinely diverge

- **Prediction:** There is at least one constructed case where the two candidate
  organizations — **K** (stable-kind-first) and **R** (contextual-role-first) —
  require *different* outcomes on identity, cardinality, or classification. The
  four "genuinely compete" cases (reminder-after-trigger, signed composite,
  source-sensitive claim, durable-policy-in-active-task) should force K to
  multiply identity while R keeps one object with contextual roles.
- **Test:** Blind adjudication of the frozen `positive`/`held-out` cases under
  each organization's coding rule; record identity count and kind/role
  assignment per case per organization.
- **Confirms:** ≥1 case with a forced divergence that isn't an artifact of
  wording → K and R are distinct hypotheses worth carrying.
- **Refutes:** Zero forced divergences → **reject the two-organization claim**;
  collapse or reformulate (the taxonomy's own rejection condition).
- **Solo?** Yes to **E2** — paper adjudication, no code. Single-adjudicator bias
  is the main risk, and a time-separated second pass only partly mitigates it
  (an author who built the cases can't truly blind themselves to their
  `stress_targets`). Genuine blinding — and the move to **E3** — needs one
  recruited second coder.

## H2 — The classification axes are non-redundant

- **Prediction:** For each axis A1–A10, at least one case pair varies that axis
  while holding the others fixed — no axis is derivable from the rest.
- **Test:** Axis-ablation over the case set: try to predict each axis's value
  from the other nine; an axis is redundant if perfectly predictable.
- **Confirms:** Every axis has ≥1 independent-variation witness.
- **Refutes:** An axis is fully determined by others under all cases → drop or
  merge it.
- **Solo?** Yes — paper exercise, partly scriptable as a table check.

## H3 — FMO-0.1 is satisfiable and its non-entailments hold

- **Prediction:** A finite model satisfying all 16 invariants exists, and each
  `⇏` non-entailment (e.g. `retrieved ⇏ relevant`, `hasProvenance ⇏ authentic`,
  `forgotten ⇏ deleted`) admits a countermodel — the `CM-01…CM-10` witnesses
  hold under a real encoding.
- **Test:** Encode the FMO core in [Alloy](https://alloytools.org/) or
  [TLA+](https://lamport.azurewebsites.net/tla/tla.html); ask the solver for (a)
  one satisfying instance, (b) a witness for each countermodel, (c) whether any
  intended non-entailment is forced.
- **Confirms:** A satisfying instance + all 10 countermodels realized + no
  non-entailment forced.
- **Refutes:** Unsatisfiable core, or an intended non-entailment provably
  entailed → narrow or supersede the FMO.
- **Solo?** Yes, with Alloy/TLA+ familiarity — highest rigor-per-effort move
  (~days for a first countermodel in Alloy).

## H4 — Provenance/temporal separation improves knowledge-update accuracy (empirical bridge)

- **Prediction:** A memory pipeline recording FMO-style provenance — separating
  a semantic claim (with validity time) from the episodic source event that
  produced it (with event/transaction time), and applying supersede-not-overwrite
  semantics — scores higher on
  [LongMemEval](https://github.com/xiaowu0162/longmemeval)'s **Knowledge-Updates**
  and **Temporal-Reasoning** splits than a matched baseline storing flat text
  with a single timestamp.
- **Test:** Two retrieval agents over `LongMemEval_S`, identical LLM/retriever,
  differing only in memory record schema (flat vs FMO-provenance). Report
  per-category accuracy; primary endpoint = Knowledge-Updates.
- **Confirms:** Meaningful gain on Knowledge-Updates (and/or Temporal) with no
  loss elsewhere → the distinction has held-out operational value.
- **Refutes:** No gain, or gains only on dev items → downgrade to a
  structural-only claim.
- **Solo?** Yes but heavier — a small implementation + benchmark run (est. 2–4
  weeks). This is the hypothesis that makes the work legible to the wider field.

## H5 — FMO deletion scope detects incomplete deletion a flat store misses (governance bridge)

- **Prediction:** Given a consolidation/derivation graph, `executeDelete` under a
  declared deletion scope returns `INCOMPLETE` exactly when an in-scope
  derivative or replica survives, whereas a naive "delete the row" reports
  success. (The field's acknowledged blind spot — CoALA §4.5; the
  poisoning/unlearning literature; GDPR Art. 17.)
- **Test:** Reference implementation (below) seeded with an
  admit→consolidate→delete trace; assert the result equals "verified within
  scope" iff the closure has no surviving in-scope targets.
- **Confirms:** The implementation distinguishes the deletion-result states on
  constructed traces.
- **Refutes:** The closure can't be computed finitely on a realistic graph →
  narrow the deletion postcondition.
- **Solo?** Yes, as part of the reference implementation.

## Recommended first experiment

**Run H1 (K vs R) on the already-built case set — a paper experiment, not code.**
The artifacts exist ([`cases/`](taxonomy/cases/),
[`category-evaluation-rules.json`](taxonomy/category-evaluation-rules.json)); it
needs no ML, API budget, or GPU; and the outcome is decisive — it either
justifies carrying two organizations forward or triggers the rejection
condition, saving weeks of downstream work. Rough effort: 1–2 focused weeks
(freeze + hash the cases, write the two coding rubrics, adjudicate blind,
tabulate divergences and agreement, report atomically including nulls).

## Benchmark options

| Benchmark | Tests | Link | Solo effort |
|---|---|---|---|
| **LongMemEval** | Info extraction, multi-session + temporal reasoning, knowledge updates, abstention | [github](https://github.com/xiaowu0162/longmemeval) · [paper](https://arxiv.org/pdf/2410.10813) | Low–moderate; best fit (has explicit knowledge-update + temporal splits) |
| **LongMemEval_Oracle** | Same questions, evidence-only (isolates reasoning from retrieval) | (in LongMemEval repo) | Lowest — pure API calls, no retrieval stack |
| **LoCoMo** | Long multi-session dialogue QA: single/multi-hop, temporal, adversarial | [project](https://snap-research.github.io/locomo/) · [paper](https://arxiv.org/abs/2402.17753) | Low–moderate; pin your scorer (known scoring critiques) |

## FMO → minimal reference implementation

The FMO forbids picking a storage/DB/model, so the reference implementation is a
thin, in-memory, **append-only interpreter of the operation contracts** — its
job is to witness the invariants and countermodels, not to be a product.

- **Immutable event log**: every op emits one append-only record; nothing is
  mutated. Transaction time = a monotonic counter.
- **Typed entities kept distinct**: events, candidates, object-versions,
  provenance assertions; admission mints a *new* object version (never relabels).
- **Provenance as reified edges** with `admitted-from / updated-from /
  consolidated-from / superseded-by` kinds; `trace(x)` = reachability closure.
- **Operations as guarded transitions**: `admit` (adds no truth/confidence),
  `retrieve` (mutates nothing), `update`→`supersede` (predecessor flips to
  superseded, identity preserved), `requestDelete`/`executeDelete` (returns
  "verified within scope" iff every non-excepted target is deleted and
  unreachable, else "incomplete").
- **Authority guard** gating every state change; a denial records a rejected op
  with no state change.
- **K/R switch**: compile-time flag between the kind-first and role-first
  extensions; feeding the H1 divergence cases through both is the executable
  form of the K-vs-R discriminator.

Tested with property-based tests over random legal op sequences (invariants),
unit tests constructing each countermodel, deletion-closure tests, and the H1
discriminator test. First version: ~1–2 weeks solo in Python (dataclasses +
pytest/Hypothesis); an Alloy/TLA+ encoding of the same core (H3) adds
machine-checked consistency for a few more days.

---

*Field grounding and links: [MemGPT/Letta](https://arxiv.org/abs/2310.08560),
[A-MEM](https://arxiv.org/abs/2502.12110), [CoALA](https://arxiv.org/abs/2309.02427),
[Generative Agents](https://dl.acm.org/doi/10.1145/3586183.3606763),
[HippoRAG](https://arxiv.org/abs/2405.14831). See also
[`taxonomy/M1_PRIOR_ART_AND_COMPETING_TAXONOMIES.md`](taxonomy/M1_PRIOR_ART_AND_COMPETING_TAXONOMIES.md).*

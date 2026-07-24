# FMO-0.1 minimal reference interpreter `[AI-assisted]`

A thin, in-memory, **append-only** interpreter of the FMO-0.1 operation
contracts (`docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md`). Its job is to
**witness** the candidate invariants and countermodels and to make the H1 (K vs
R) and H5 (deletion-scope) hypotheses *executable*. It is deliberately **not a
product**: per the FMO it selects no database, model, embedding, index,
serialization, or application schema.

## What it implements

- **Immutable append-only log.** Every operation appends exactly one
  `OperationRecord` — including rejected / failed ones (FMO-INV-16). Nothing is
  mutated in place. Lifecycle state is *derived* by folding `StateEvent` records
  (`Engine.object_state`), not stored on a mutable field.
- **Transaction time = a monotonic counter** (`Engine._tick`). No wall clock /
  `Date.now` is ever read; `≺` is the counter's order.
- **Distinct typed entities** as frozen dataclasses (`fmo/entities.py`): source
  events, candidates, object-versions, provenance assertions, operation records,
  confidence/uncertainty/assessment/conflict records, deletion scopes. Admission
  mints a **new** `ObjectVersion` — it never relabels a candidate (FMO-INV-01).
- **Provenance as reified edges** (`ProvenanceAssertion`) with
  `WAS_ENCODED_FROM / WAS_ADMITTED_FROM / WAS_UPDATED_FROM /
  WAS_CONSOLIDATED_FROM / WAS_SUPERSEDED_BY` kinds, plus `Engine.trace()` — the
  reachability closure over provenance edges.
- **Guarded operations** (`fmo/engine.py`): `encode`, `admit` (adds no
  truth/confidence), `retrieve` (mutates nothing), `update` → `supersede`
  (predecessor flips to `SUPERSEDED`, identity preserved), `consolidate`,
  `forget` / `archive` / `restore`, `assess_confidence` /
  `describe_uncertainty` / `assess_claim` / `detect_conflict`,
  `request_delete` / `execute_delete`.
- **Authority guard** (`fmo/authority.py`): default-permit with an ordered
  override list; `DENY` / `UNRESOLVED` cannot produce a state-changing success
  (FMO-INV-05). A denial records a `REJECTED` op with no state change.
- **K/R switch** (`Engine(organization="K"|"R")`): kind-first vs role-first
  functional classification, the discriminator for H1.

## How to run

Stdlib + `pytest` only (no `hypothesis`, no heavy deps). From the repo root:

```bash
python -m pytest impl/tests -q
```

Latest run: **74 passed**. Property-style tests use a deterministic PRNG with an
explicitly passed seed (`test_invariants.py`) — no `Math.random`-style
nondeterminism; a failing seed is reproducible and printed.

## Coverage — honest

**Invariants** (`fmo/checks.py::check_all`, asserted after *every* step of 50
random legal traces × {K, R}):

| Invariant | Covered | How |
|---|---|---|
| INV-01 type separation | yes | distinct classes + id-namespace disjointness check |
| INV-02 exact identity unique | yes | `(object_id, version_id)` uniqueness |
| INV-03 version immutability | yes | frozen dataclass + birth-snapshot compare |
| INV-04 legal transitions | yes | transition-relation membership; `DELETED` has no exit |
| INV-05 authority guard | yes | every successful state change carries `PERMIT` |
| INV-06 provenance presence | yes | exactly one `WAS_ADMITTED_FROM` per object |
| INV-07 derivation acyclicity | yes | derivation edges strictly increase tx time |
| INV-08 supersession preservation | yes | predecessor snapshot unchanged after supersede |
| INV-09 admission neutrality | partial | structural (admit never writes assessment logs); asserted, not adversarial |
| INV-10 retrieval neutrality | yes | no `StateEvent` shares a `retrieve` tx |
| INV-11 scoped assessments | yes | every CA/UA names target, assessor, context, time |
| INV-12 conflict preservation | yes | no `StateEvent` shares a conflict tx |
| INV-13 contextual access | partial | signature/smoke check only; no adversary model |
| INV-14 deletion closure | yes | via H5 tests (not in `check_all`) — see `test_deletion_h5.py` |
| INV-15 no resurrection | yes | no state assigned after `DELETED`; no id reuse |
| INV-16 failure retention | yes | rejected/failed ops remain, unique, in the log |

**Countermodels** — one unit test each, all 10 (`test_countermodels.py`):
CM-01 high-confidence≠correct · CM-02 retrieved≠used/relevant · CM-03
connected-trace≠authentic · CM-04 forgotten≠deleted · CM-05 disjoint-validity≠
conflict · CM-06 local-erasure≠verified-deletion · CM-07 same-content≠same-
governance · CM-08 role≠authority · CM-09 role-change-without-version · CM-10
independent-reacquisition≠resurrection.

**H5** (`test_deletion_h5.py`): closure pulls in derivatives; a flat "delete the
row" returns `INCOMPLETE`; full-closure erasure returns
`VERIFIED_WITHIN_SCOPE`; the verified-iff-no-surviving-target biconditional over
every proper subset of the closure; exceptions. One honest finding surfaced
while building: **excepting a surviving derivative of the root still blocks
verification**, because the derivative's lineage keeps the root reconstructable
(FMO deletion postcondition). Encoded as
`test_excepting_a_surviving_derivative_still_blocks_verification`.

**H1** (`test_discriminator_h1.py`): the four "genuinely compete" held-out cases
(reminder-after-trigger, signed-composite, source-sensitive-claim,
durable-policy-in-active-task) each yield **identity count 1 under R** and **≥2
under K**, a forced divergence in all four; a same-kind control does *not*
diverge (the divergence is not an artifact of always multiplying).

### Not covered (out of scope for this interpreter)

- No machine-checked satisfiability / independence of the FMO core — that is
  **H3** (Alloy/TLA+), not this code. Passing tests here show this interpreter
  *can host* the distinctions; they do not prove the FMO invariants jointly
  satisfiable in general.
- No adversary / observation model for `accessible`, reconstruction, caches,
  backups, replay/rollback, or audit-residue leakage (FMO "missing obligations"
  11, 18, 21).
- `abstract`, `reconsolidate`, `deduplicate` operations, numeric confidence
  calculus, and distributed/partial transaction order are not modeled.
- Content is an opaque id; no natural-language claim interpretation.

## Evidence framing

`[AI-assisted]` (AI materially drafted this code and tests). Per
[`METHOD.md`](../METHOD.md): passing tests **support H3/H5 structurally** — this
append-only interpreter can express the FMO distinctions, the 16 invariants as
implemented here, all 10 countermodels, and the K/R discriminator — **but are
not empirical validity and cannot self-assign above E2.** Machine-checked
semantic validity of the FMO core remains the H3 (Alloy/TLA+) obligation. A
successful test run is not a proof that the natural-language FMO is consistent.

### How to falsify / replicate

Add a random-trace seed that breaks an invariant; encode a countermodel whose
non-entailment the interpreter is forced to violate; or exhibit a legal K-case
where R is forced to multiply identity (or vice versa). Any of these narrows the
FMO or this interpreter.

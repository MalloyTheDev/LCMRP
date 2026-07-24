# FMO-0.1 in Alloy — machine-checking H3

**Study artifact E1 (candidate) — supports H3 iff the commands below produce the
documented outcomes. `[AI-assisted]`.**

> **Human-verification claim.** The single most important thing a reader must check
> for themselves is that `fmo.als` is *faithful to the FMO-0.1 prose*
> (`docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md`). Alloy only checks the model
> it is given. A green run confirms *the encoding*, not the paper. Faithfulness is a
> claim; the solver cannot grade it. This file is honest about where the encoding
> simplifies or omits the prose (see **Gaps** below).

This directory encodes the core of **FMO-0.1** in [Alloy](https://alloytools.org/)
to test **H3** (`docs/HYPOTHESES.md`): *"A finite model satisfying all 16 invariants
exists, and each `⇏` non-entailment admits a countermodel."*

- `fmo.als` — the model: typed entities, transaction-time ordering, object
  lifecycle, provenance edges, invariants as facts, and the `run`/`check` commands.
- `README.md` — this file.

---

## How to run

**Tool.** Alloy Analyzer. The model uses only classic relational Alloy plus
`util/ordering`; it deliberately avoids Alloy 6 temporal (`always`/`after`) syntax,
so it is intended to load in **Alloy Analyzer 5.x and 6.x** (developed against
6.1.0). Transaction time is an explicit ordered `Time` signature, not Alloy's
built-in mutable state.

**Steps.**
1. Open `fmo.als` in the Alloy Analyzer.
2. Use *Execute → Execute All*, or run each named command from the drop-down.
3. Read each result against the **Expected outcome** column below. For a `run`,
   "Instance found" is success. For a `check`, Alloy reports either
   "No counterexample found" (the assertion is valid within scope) or
   a counterexample (the assertion is invalid within scope) — **for the
   non-entailment checks a counterexample is the desired result.**

**Solver / scope.** Default SAT4J is fine at the small scopes given (≤ 8 `Time`,
≤ 6 `Object`). Every command carries an explicit scope; none should be slow.

---

## Commands and expected outcomes

### H3 (a) — satisfiability

| Command | Expected | Meaning |
|---|---|---|
| `run FMO_satisfiable` | **Instance found** | A non-trivial structure (object, candidate, event, provenance, operation, claim, deletion scope) satisfies **all** encoded invariants at once. This is the satisfiability witness H3(a) asks for. |
| `run FMO_minimal` | Instance found (may be the empty instance) | Sanity check that the facts are not jointly contradictory even trivially. Informative only in combination with `FMO_satisfiable`. |

### H3 (b) — countermodel witnesses (each should find an instance)

| Command | FMO CM | Non-entailment witnessed | Expected |
|---|---|---|---|
| `run CM01_highConf_not_correct` | CM-01 | `highConfidence(k) ⇏ correct(k)` | Instance found |
| `run CM02_retrieved_not_relevant_or_used` | CM-02 | `retrieved ⇏ relevant`, `retrieved ⇏ used` | Instance found |
| `run CM03_provenance_not_authentic` | CM-03 | `hasProvenance ⇏ authentic` | Instance found |
| `run CM04_forgotten_not_deleted` | CM-04 | `forgotten ⇏ deleted` | Instance found |
| `run CM06_incomplete_deletion` | CM-06 | `locallyErased ⇏ deletionVerifiedWithinScope` (the `INCOMPLETE` case) | Instance found |
| `run CM10_reacquire_not_resurrect` | CM-10 | independent reacquisition `⇏` resurrection | Instance found |

### H3 (c) — non-entailment checks (a counterexample is the *goal*)

| Command | Expected | Meaning |
|---|---|---|
| `check Retrieved_forces_Relevant` | **Counterexample found** | The core does not force `retrieved ⇒ relevant`. |
| `check Provenance_forces_Authentic` | **Counterexample found** | The core does not force `hasProvenance ⇒ authentic`. |
| `check Forgotten_forces_Deleted` | **Counterexample found** | The core does not force `forgotten ⇒ deleted`. |
| `check Access_one_tuple_forces_all_actors` | **Counterexample found** | Access for one `(actor,object,query,purpose,boundary,time)` tuple does not force access for another actor (FMO-INV-13 / cross-authority non-entailment). |

### Positive safety checks (no counterexample is the goal)

| Command | Expected | Invariant |
|---|---|---|
| `check DerivationAcyclic` | No counterexample | FMO-INV-07 / FMO-P01 |
| `check VerifiedImpliesAllTargetsDeleted` | No counterexample | FMO-INV-14 |
| `check DeletedIsTerminal` | No counterexample | FMO-INV-15 |
| `check SupersededPredecessorPreserved` | No counterexample | FMO-INV-08 |

---

## What maps to H3's confirm / refute criteria

- **Confirm H3** (per `HYPOTHESES.md`): a satisfying instance **+** the countermodels
  realized **+** no intended non-entailment forced. In this encoding that is:
  `FMO_satisfiable` finds an instance; every `CM*` run finds an instance; every
  non-entailment `check` returns a counterexample; and the positive safety `check`s
  return none.
- **Refute / narrow H3**: `FMO_satisfiable` is **unsat**, or one of the
  non-entailment `check`s returns **no counterexample** (the implication is forced),
  or a positive safety `check` returns a counterexample (an intended invariant fails).

Per `METHOD.md`, this is an **E2-eligible** confirmatory check only *after* a
preregistered study card runs it against the pinned file hash; as delivered it is
labelled **E1** and `[AI-assisted]`. A solo author may never self-assign E3, and an
AI review does not lift the label.

---

## Coverage: the 16 invariants

| Invariant | Status | How |
|---|---|---|
| FMO-INV-01 Type separation | **Encoded (structural), partial coverage** | The carrier sets present — `E`, `N`, `O`, `U`, `PT`, `CA`, `DS`, `K`, … — are distinct top-level sigs, so no atom inhabits two. Uncertainty records (`UA`) and versioned policy statements (`P`) are **not** declared as sigs (authority is abstracted to `Operation.opAuthz`); their type-distinctness is therefore not exercised. |
| FMO-INV-02 Exact identity uniqueness | **Encoded** | `ExactIdentityUniqueness`: `versionOf` unique per object; `object_id` uniqueness is automatic (distinct atoms). |
| FMO-INV-03 Version immutability | **Encoded (structural)** | Identity fields (`seriesOf/versionOf/contentID/admittedFrom/createdAtO`) are static functions of the atom — unchangeable by construction. Only `state` is time-indexed. |
| FMO-INV-04 Legal lifecycle transitions | **Encoded** | `LegalTransitions` (edge shapes) + `StateChangeJustifiedAndAuthorized` (each change justified by exactly one successful op). |
| FMO-INV-05 Authority guard | **Encoded** | Same fact requires `opAuthz = PERMIT` + `opResult = R_SUCCEEDED` for each state change; `AdmissionAuthorized` for admission. |
| FMO-INV-06 Provenance presence & attribution | **Partial** | `AdmissionProvenance` (each object → exactly one `WAS_ADMITTED_FROM` to an admitted candidate); attribution structural (`Prov.assertedBy: one Actor`). **Not** encoded: transform-output *input-completeness* (matches the FMO-P04 limit). |
| FMO-INV-07 Derivation acyclicity | **Encoded** | `DerivationOrder` forces input-before-output in strict `≺`; `check DerivationAcyclic` proves no cycle within scope. |
| FMO-INV-08 Supersession preservation | **Encoded** | `SupersessionMeaning` (same series, predecessor link, later time, predecessor→`SUPERSEDED`); identity preservation is structural (INV-03). |
| FMO-INV-09 Admission neutrality | **Encoded as absence + witness** | No fact attaches truth/relevance/confidence at admission; witnessed by `CM01` (admitted object asserting a `CHALLENGED` claim). |
| FMO-INV-10 Retrieval neutrality | **Encoded** | `Retrieve` ops carry no `toState` (mutate nothing); `relevant`/`used` are free relations not tied to `returns`. Witnessed by `CM02`; forced-implication ruled out by `check Retrieved_forces_Relevant`. |
| FMO-INV-11 Scoped assessments | **Encoded (structural)** | `ConfAssessment`/`Assessment` name target, assessor/actor, context, time as `one` fields. Aggregation-creates-new-record is **not** modelled (no aggregation op present). |
| FMO-INV-12 Conflict preservation | **Partial** | `ConflictWellFormed` (irreflexive + validity overlap) and symmetric `conflicts` fun. "Records no state change" is structural absence, not an explicit before/after check. |
| FMO-INV-13 Contextual access | **Encoded (structural)** | `Access` = one atom per exact 6-tuple; no closure axiom. `check Access_one_tuple_forces_all_actors` shows non-implication. |
| FMO-INV-14 Deletion closure | **Encoded** | `DeletionSuccessClosure`: `D_VERIFIED` requires every target `DELETED` at completion. Witnessed by `CM06`; `check VerifiedImpliesAllTargetsDeleted`. |
| FMO-INV-15 No resurrection | **Encoded** | `NoResurrection` (DELETED terminal for all later times) + `LegalTransitions` (DELETED self-loop only) + identity uniqueness. `check DeletedIsTerminal`. |
| FMO-INV-16 Failure retention | **Encoded (structural)** | `Operation` atoms are immutable and never removed; a `R_REJECTED/R_FAILED/R_HALTED/R_UNKNOWN` op persists. A later success adds a new atom, never edits the failure. |

## Coverage: the 10 countermodels

| CM | Status | Note |
|---|---|---|
| CM-01 high confidence ≠ correct | **Encoded** | `run CM01_highConf_not_correct` |
| CM-02 retrieved ≠ relevant/used | **Encoded** | `run CM02_retrieved_not_relevant_or_used` |
| CM-03 connected ≠ authentic provenance | **Encoded** | `run CM03_provenance_not_authentic` |
| CM-04 forgotten ≠ deleted | **Encoded** | `run CM04_forgotten_not_deleted` |
| CM-06 local erasure ≠ verified deletion | **Encoded** | `run CM06_incomplete_deletion` |
| CM-10 reacquisition ≠ resurrection | **Encoded** | `run CM10_reacquire_not_resurrect` |
| CM-05 disjoint validity ⇒ no conflict | **Encoded indirectly** | `ConflictWellFormed` forbids a `Conflict` between claims with non-overlapping validity, so the CM-05 structure is guaranteed rather than exhibited by its own `run`. |
| CM-07 same content ≠ same governance | **Not encoded** | Governance/deletion-duty per content is out of scope here (partly reachable via CM-10's `contentID` sharing). |
| CM-08 role ≠ authority | **Not encoded as its own run** | The mechanism *is* present: `opAuthz = DENY` yields no state change (INV-05). No dedicated actor-role relation was added. |
| CM-09 role change without version change | **Not encoded** | `playsRole` (contextual functional roles) and the K/R extensions are omitted — this is the taxonomy-neutrality question (FMO-C04), deliberately left to a separate study. |

The task asked for **≥ 3–4** countermodels including `retrieved ⇏ relevant`,
`hasProvenance ⇏ authentic`, `forgotten ⇏ deleted`, and the deletion `INCOMPLETE`
case. All four are present (CM-02, CM-03, CM-04, CM-06), plus CM-01 and CM-10.

---

## Gaps, simplifications, and honesty notes

These are the places the encoding is *narrower* than the FMO-0.1 prose. They are the
reason "faithful to the prose" needs a human check.

1. **Candidate lifecycle is a `reached: set CandidateState`, not time-indexed.** The
   full `candidateState : N × T` machine is collapsed to the set of states a
   candidate went through (with `PENDING` always present and `REJECTED`/`ADMITTED`
   mutually exclusive). Object lifecycle *is* time-indexed.
2. **INV-06 input-completeness is not enforced.** We constrain the provenance edges
   that exist (time order, attribution) and require the admission edge, but do not
   force a transform to declare *every* input. This mirrors the FMO's own FMO-P04
   limit ("neither undeclared-input completeness nor authenticity").
3. **INV-11 aggregation and the confidence *scale/value* are abstracted** to a
   two-point `ConfLevel = {HIGH, LOW}`; numeric intervals and aggregation rules are
   not modelled.
4. **INV-12 "conflict records no state change" is structural absence**, not an
   explicit pre/post comparison; the model simply has no operation that a `Conflict`
   could mutate.
5. **Retrieval order is abstracted to a set** (`returns: set Object`), not a
   `seq(O)`.
6. **Deletion `exceptions` are pre-subtracted into `DeletionScope.targets`**; the
   closure-rule / relation-snapshot machinery of `scope : DS` is not expanded. The
   deletion *postcondition* checked is "all in-scope targets DELETED at completion",
   which is the `materialized=false` core; reconstruction-dependency reasoning is not
   modelled (matches FMO-C01 / obligation 17).
7. **CM-07, CM-08 (own run), CM-09 not encoded** as noted above; the K/R
   functional-role extensions are out of scope (they belong to H1, not H3).
10. **No `UA` (uncertainty) or `P` (policy) signatures.** Authority is abstracted
    to the `AuthzDecision` a given `Operation` carries (`opAuthz ∈ {PERMIT, DENY,
    UNRESOLVED_A}`); the `governs`/`policyEffect`/`policyDomain` attachment machinery
    and the uncertainty-description records are not modelled. This means the FMO-INV-01
    type-distinctness of `UA` and `P`, and the policy-composition question (FMO-C02),
    are untested here.
8. **Event/validity time vs transaction time.** `Claim.vFrom/vTo` and the transaction
   `Time` order are separate, so the model *can* express `eventTime ⇏ transactionTime`;
   a dedicated check for that non-entailment was not added.
9. **Scope-bounded results.** Every `check` is bounded (small `Time`/`Object` scopes).
   Alloy's small-scope hypothesis makes these persuasive, not exhaustive proofs. A
   "no counterexample" result means *within the given scope*.

### Constructs I could not run here (verify on first load)

I do not have an Alloy Analyzer in this environment, so the model is written to be
correct-by-inspection. Two constructs are worth a first-load sanity check:

- **Transitive closure over a `fun`-valued relation:** `o.^derivEdges` in
  `DerivationAcyclic`. If your Alloy build objects, write `o.^(derivEdges)`.
- **`util/ordering` navigation:** `t.(TO/next)` for the successor and
  `TO/lt`/`TO/lte`/`TO/gte` for the order predicates (module opened as
  `open util/ordering[Time] as TO`). These are standard, but the exact `TO/…`
  qualification is the thing to eyeball.

Everything else is ordinary first-order relational Alloy (signatures, `fact`,
`pred`, `assert`, `run`, `check`, union field types like
`one (Event + Candidate + Object + Operation)`, and ternary state relations
`state: Time -> lone ObjectState`).

---

## How to replicate or falsify this

1. Pin the bytes: record the SHA-256 of `fmo.als` in a study card and note the Alloy
   Analyzer version used.
2. *Execute All* and record, per command, exactly what the analyzer reported
   (instance / no counterexample / counterexample) against the tables above.
3. **Falsify** by exhibiting any of: `FMO_satisfiable` unsat; a non-entailment
   `check` with **no** counterexample; a positive safety `check` **with** a
   counterexample; or — the human-only check — a place where a `fact` misreads the
   FMO-0.1 prose (that is a faithfulness bug, not an Alloy bug, and the solver will
   not catch it).

/*
 * fmo.als  --  Alloy encoding of the FMO-0.1 core (Formal Memory Object Model v0.1)
 *
 * Source of truth: docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md
 * Tests: hypothesis H3 (docs/HYPOTHESES.md) -- "FMO-0.1 is satisfiable and its
 *        non-entailments hold".
 *
 * Evidence label: E1 (candidate) -> supports H3 iff the commands below produce the
 *                 documented outcomes.  [AI-assisted].  See README.md.
 *
 * WARNING (must be human-verified): that this encoding is *faithful to the FMO-0.1
 * prose* is itself a claim, not a checked fact.  Alloy only checks the encoding it
 * is given.  A green run confirms the Alloy model, not the paper.
 *
 * Portability: uses only classic relational Alloy + util/ordering (no Alloy-6 LTL
 * `always`/`after`).  Intended to load in Alloy Analyzer 5.x and 6.x.  Transaction
 * time is modelled explicitly as an ordered `Time` signature, NOT as Alloy state.
 *
 * Each fact/predicate is tagged with the FMO-INV-NN invariant(s) it encodes.
 * Honest gaps and simplifications are documented in README.md.
 */
module fmo

open util/ordering[Time] as TO   // strict total order over transaction time  (the "≺" of FMO-0.1)

// ---------------------------------------------------------------------------
// Transaction time
// ---------------------------------------------------------------------------
// TO gives: TO/first, TO/last, TO/next (relation), TO/lt, TO/lte, TO/gt, TO/gte.
sig Time {}

// ---------------------------------------------------------------------------
// Enumerated state / result domains  (FMO-0.1 "Enumerated state and result domains")
// Names are prefixed where a bare name would clash across enums.
// ---------------------------------------------------------------------------
abstract sig CandidateState {}
one sig PENDING, REJECTED, ADMITTED extends CandidateState {}

abstract sig ObjectState {}
one sig ACTIVE, SUPPRESSED, ARCHIVED, SUPERSEDED, DELETE_PENDING, DELETED extends ObjectState {}

abstract sig AuthzDecision {}
one sig PERMIT, DENY, UNRESOLVED_A extends AuthzDecision {}

abstract sig OperationResult {}
one sig R_SUCCEEDED, R_REJECTED, R_FAILED, R_HALTED, R_UNKNOWN extends OperationResult {}

abstract sig TruthStatus {}
one sig T_SUPPORTED, T_CHALLENGED, T_UNRESOLVED, T_WITHDRAWN extends TruthStatus {}

abstract sig DeletionResult {}
one sig D_VERIFIED, D_INCOMPLETE, D_FAILED, D_UNVERIFIED extends DeletionResult {}

abstract sig OpKind {}
one sig Encode, Admit, Retrieve, Update, Consolidate, Abstract_, Reconsolidate,
        Forget, Archive, Restore, RequestDelete, ExecuteDelete extends OpKind {}

abstract sig RelKind {}
one sig WAS_ENCODED_FROM, WAS_DERIVED_FROM, USED_INPUT, WAS_GENERATED_BY,
        WAS_ATTRIBUTED_TO, WAS_ADMITTED_FROM, WAS_UPDATED_FROM,
        WAS_CONSOLIDATED_FROM, WAS_ABSTRACTED_FROM, WAS_RECONSOLIDATED_FROM,
        WAS_RETRIEVED_IN, WAS_SUPERSEDED_BY extends RelKind {}

abstract sig ConfLevel {}
one sig HIGH, LOW extends ConfLevel {}

// ---------------------------------------------------------------------------
// Uninterpreted carrier sets.  Kept as distinct top-level sigs so that
// FMO-INV-01 (type separation) is structural: no atom can inhabit two of them.
// ---------------------------------------------------------------------------
sig Actor {}
sig Event {}          // E   source events
sig Series {}         // S   stable series identity
sig Digest {}         // DIG abstract immutable-content identifier
sig Claim {           // K
  vFrom: one Time,    // validity interval start  (validity time, NOT transaction time)
  vTo:   one Time     // validity interval end
}
sig CX {}             // claim-comparison / interpretation context
sig Query {}          // Q
sig Purpose {}        // PR
sig Boundary {}       // B   declared governed system boundary

// ---------------------------------------------------------------------------
// Memory candidate  (N)
// Candidate lifecycle is simplified to a set of *reached* states (not time-indexed);
// see README "Simplifications".  Enough to express PENDING/ADMITTED/REJECTED and
// the admission contract.
// ---------------------------------------------------------------------------
sig Candidate {
  cContentID:     one Digest,
  proposedSeries: lone Series,
  createdAtN:     one Time,
  createdByN:     one Actor,
  reached:        set CandidateState
}

// ---------------------------------------------------------------------------
// Exact memory object version  (O)
// Identity-bearing fields are *static* Alloy functions of the atom, so they cannot
// change over time -- this is exactly how FMO-INV-03 (version immutability) is
// encoded.  Only `state` is time-indexed.
// ---------------------------------------------------------------------------
sig Object {
  seriesOf:     one Series,
  versionOf:    one Digest,          // version_id  (immutable)
  contentID:    one Digest,          // admitted content identity (immutable)
  admittedFrom: one Candidate,       // WAS_ADMITTED_FROM target (immutable)
  createdAtO:   one Time,            // transaction time of admission (immutable)
  predecessor:  lone Object,
  supersedes:   set Object,
  asserts:      set Claim,           // asserts ⊆ O × K
  state:        Time -> lone ObjectState   // objectState : O × T ⇀ ObjectState
}

// ---------------------------------------------------------------------------
// Immutable operation-event record  (U)
// Retrieval is folded in as kind = Retrieve with a `returns` set.  `relevant`/`used`
// are free relations, deliberately NOT tied to `returns` (that is the point of
// FMO-INV-10 / retrieved ⇏ relevant / retrieved ⇏ used).
// ---------------------------------------------------------------------------
sig Operation {
  opKind:     one OpKind,
  opActor:    one Actor,
  opAuthz:    one AuthzDecision,
  opTime:     one Time,
  opResult:   one OperationResult,
  targetObj:  lone Object,           // object whose state this op changes (if any)
  targetCand: lone Candidate,        // candidate acted on (e.g. Admit)
  toState:    lone ObjectState,      // resulting object state for a state-changing op
  returns:    set Object,            // Retrieve result sequence (order abstracted to a set)
  relevant:   set Object,            // free: not forced to equal `returns`
  used:       set Object,            // free: not forced to equal `returns`
  delScope:   lone DeletionScope,    // for RequestDelete / ExecuteDelete
  delResult:  lone DeletionResult
}

// ---------------------------------------------------------------------------
// Reified provenance assertion  (PT)  -- carries its own attribution & time so it
// can itself be challenged (see ProvAssessment).
// ---------------------------------------------------------------------------
sig Prov {
  relKind:    one RelKind,
  subj:       one (Event + Candidate + Object + Operation),
  obj:        one (Event + Candidate + Object + Operation),
  assertedBy: one Actor,             // attribution is structural (>= one accountable actor)
  pvTime:     one Time
}

// ---------------------------------------------------------------------------
// Assessment records
// ---------------------------------------------------------------------------
sig ConfAssessment {                 // confidence : CA
  cTarget: one (Claim + Object + Prov),
  cAssessor: one Actor,
  cCtx:    one CX,
  caTime:  one Time,
  level:   one ConfLevel
}

sig Assessment {                     // assessment ⊆ A × K × CX × T × TruthStatus
  aActor:  one Actor,
  aClaim:  one Claim,
  aCtx:    one CX,
  asTime:  one Time,
  status:  one TruthStatus
}

sig ProvAssessment {                 // authenticity assessment of a provenance edge
  paProv:   one Prov,
  paStatus: one TruthStatus,         // T_CHALLENGED == forgery suspected
  paTime:   one Time
}

// ---------------------------------------------------------------------------
// Conflict record  (conflicts ⊆ K × K × CX × T)
// ---------------------------------------------------------------------------
sig Conflict {
  k1:    one Claim,
  k2:    one Claim,
  cxOf:  one CX,
  cfTime: one Time
}

// ---------------------------------------------------------------------------
// Deletion scope  (DS)
// ---------------------------------------------------------------------------
sig DeletionScope {
  targets:  set Object,              // frozen closure minus exceptions
  dsBoundary: one Boundary
}

// ---------------------------------------------------------------------------
// Access tuple  (accessible = true for this exact 6-tuple)
// One Access atom == one true evaluation of accessible(a,o,q,pr,b,t).
// ---------------------------------------------------------------------------
sig Access {
  acActor:    one Actor,
  acObj:      one Object,
  acQuery:    one Query,
  acPurpose:  one Purpose,
  acBoundary: one Boundary,
  acTime:     one Time
}

// ===========================================================================
// LIFECYCLE HELPERS
// ===========================================================================

// Permitted object-lifecycle transition shapes (FMO-0.1 object lifecycle diagram).
// Self-loops (s1 = s2, "no change") are allowed; DELETED has only the self-loop,
// which gives terminality.
pred legalStep[s1, s2: ObjectState] {
  s1 = s2
  or (s1 = ACTIVE        and s2 in (SUPPRESSED + ARCHIVED + SUPERSEDED + DELETE_PENDING))
  or (s1 = SUPPRESSED     and s2 in (ACTIVE + ARCHIVED + SUPERSEDED + DELETE_PENDING))
  or (s1 = ARCHIVED       and s2 in (ACTIVE + SUPERSEDED + DELETE_PENDING))
  or (s1 = SUPERSEDED     and s2 in DELETE_PENDING)
  or (s1 = DELETE_PENDING and s2 in DELETED)
  // DELETED -> only DELETED (covered by s1 = s2)
}

// object-to-object derivation edge relation, read from provenance assertions
fun derivEdges: Object -> Object {
  { d: Object, s: Object |
      some p: Prov |
        p.relKind in (WAS_DERIVED_FROM + WAS_UPDATED_FROM + WAS_CONSOLIDATED_FROM
                      + WAS_ABSTRACTED_FROM + WAS_RECONSOLIDATED_FROM)
        and p.subj = d and p.obj = s }
}

// derived symmetric conflict relation over claims
fun conflicts: Claim -> Claim {
  { a: Claim, b: Claim |
      some c: Conflict | (c.k1 = a and c.k2 = b) or (c.k1 = b and c.k2 = a) }
}

// ===========================================================================
// FACTS  (candidate invariants)
// ===========================================================================

// -- FMO-INV-01  Type separation ------------------------------------------------
// Structural: E, N, O, U, PT, CA, UA(-), P(-), DS, ... are distinct top-level sigs,
// so no atom inhabits two carrier types.  Admission mints a fresh Object atom; it
// never relabels a Candidate atom as an Object.  (No fact needed.)

// -- FMO-INV-02  Exact identity uniqueness --------------------------------------
fact ExactIdentityUniqueness {
  // No two object versions share a version_id; object_id uniqueness is automatic
  // (distinct atoms).  versionOf therefore identifies at most one object, and its
  // per-object contentID is the single immutable admitted content identity.
  all disj o1, o2: Object | o1.versionOf != o2.versionOf
}

// -- FMO-INV-03  Version immutability -------------------------------------------
// Encoded structurally: seriesOf, versionOf, contentID, admittedFrom, createdAtO
// are static (time-independent) functions of the Object atom, hence unchangeable.
// (No fact needed; a metadata/content change must produce a NEW Object atom.)

// -- FMO-INV-04 (shape) + object state well-formedness --------------------------
fact ObjectStateDomain {
  // an object has a defined state exactly from its admission time onward
  all o: Object, t: Time | (some o.state[t]) iff TO/lte[o.createdAtO, t]
}
fact ObjectInitiallyActive {
  // admission creates the object in ACTIVE
  all o: Object | o.state[o.createdAtO] = ACTIVE
}
fact LegalTransitions {
  // FMO-INV-04: consecutive defined states follow a permitted lifecycle edge
  all o: Object, t: Time |
    (some t.(TO/next) and some o.state[t] and some o.state[t.(TO/next)])
      implies legalStep[o.state[t], o.state[t.(TO/next)]]
}

// -- FMO-INV-04 (justification) + FMO-INV-05 (authority guard) ------------------
fact StateChangeJustifiedAndAuthorized {
  // every object-state change is justified by exactly one successful, PERMITted
  // operation event recorded at the time the new state takes effect
  all o: Object, t: Time |
    let t2 = t.(TO/next) |
      (some t2 and some o.state[t] and some o.state[t2] and o.state[t] != o.state[t2])
        implies (one op: Operation |
                   op.targetObj = o
                   and op.toState = o.state[t2]
                   and op.opTime  = t2
                   and op.opResult = R_SUCCEEDED
                   and op.opAuthz  = PERMIT)
}
fact ToStateOnlyForStateChangingKinds {
  all op: Operation | some op.toState implies
    op.opKind in (Admit + Update + Forget + Archive + Restore + RequestDelete + ExecuteDelete)
}

// -- FMO-INV-05  Authority guard (candidate admission) --------------------------
fact AdmissionAuthorized {
  all n: Candidate | ADMITTED in n.reached implies
    (some op: Operation |
       op.opKind = Admit and op.targetCand = n
       and op.opResult = R_SUCCEEDED and op.opAuthz = PERMIT)
}

// -- FMO-INV-06  Provenance presence & attribution ------------------------------
fact AdmissionProvenance {
  // every admitted object traces to exactly one admitted candidate via WAS_ADMITTED_FROM
  all o: Object |
    (one p: Prov | p.relKind = WAS_ADMITTED_FROM and p.subj = o and p.obj = o.admittedFrom)
    and ADMITTED in o.admittedFrom.reached
}
// Attribution: every Prov carries `assertedBy: one Actor` structurally (>= one
// accountable actor identity).  NOTE: "every transform output links to *every*
// declared input" is only PARTIALLY encoded -- we constrain the edges that exist
// (time order + attribution) but do not force input-completeness.  See README.

// -- FMO-INV-07  Derivation acyclicity (via strict transaction order) -----------
fact DerivationOrder {
  all p: Prov |
    (p.relKind in (WAS_DERIVED_FROM + WAS_UPDATED_FROM + WAS_CONSOLIDATED_FROM
                   + WAS_ABSTRACTED_FROM + WAS_RECONSOLIDATED_FROM)
     and p.subj in Object and p.obj in Object)
      implies TO/lt[p.obj.createdAtO, p.subj.createdAtO]   // input older than output
}
fact PredecessorOrder {
  all o: Object | some o.predecessor implies {
    TO/lt[o.predecessor.createdAtO, o.createdAtO]
    o.predecessor.seriesOf = o.seriesOf
  }
}

// -- FMO-INV-08  Supersession preservation --------------------------------------
fact SupersessionMeaning {
  all n, old: Object | old in n.supersedes implies {
    n.seriesOf = old.seriesOf
    n.predecessor = old
    TO/lt[old.createdAtO, n.createdAtO]
    old.state[n.createdAtO] = SUPERSEDED       // predecessor flips to SUPERSEDED
  }
  // identity/content preservation is structural (INV-03): supersession never
  // mutates old.versionOf / old.contentID / old.admittedFrom / old.createdAtO.
}

// -- FMO-INV-11  Scoped epistemic assessments -----------------------------------
// Structural: every ConfAssessment names cTarget, cAssessor, cCtx, caTime (all
// multiplicity `one`); every Assessment names its actor, claim, context, time.
// Aggregation-creates-a-new-record is NOT modelled (no aggregation op here).

// -- FMO-INV-12  Conflict preservation ------------------------------------------
fact ConflictWellFormed {
  all c: Conflict {
    c.k1 != c.k2                                  // irreflexive
    // overlapping / unresolved validity required (CM-05: disjoint intervals cannot conflict)
    TO/lte[c.k1.vFrom, c.k2.vTo] and TO/lte[c.k2.vFrom, c.k1.vTo]
  }
  // `conflicts` (the fun) is symmetric by construction.
  // Conflict records carry no state-change effect: detecting a conflict does not
  // touch claims, objects, confidence, lifecycle or authority (structural absence).
}

// -- FMO-INV-13  Contextual access ----------------------------------------------
// Structural: accessibility is a per-6-tuple fact (one Access atom == one tuple).
// There is NO closure axiom making one tuple imply another actor/purpose.

// -- FMO-INV-14  Deletion closure -----------------------------------------------
fact DeletionSuccessClosure {
  // VERIFIED_WITHIN_SCOPE requires every non-excepted target DELETED at completion
  all op: Operation |
    (op.opKind = ExecuteDelete and op.delResult = D_VERIFIED) implies {
      some op.delScope
      all x: op.delScope.targets | x.state[op.opTime] = DELETED
    }
  // exceptions are pre-subtracted into `targets` (see README simplification).
}

// -- FMO-INV-15  No resurrection under one identity -----------------------------
fact NoResurrection {
  all o: Object, t: Time |
    o.state[t] = DELETED implies (all t2: Time | TO/gte[t2, t] implies o.state[t2] = DELETED)
  // reuse of an exact (object_id, version_id) is already impossible: distinct atoms
  // + FMO-INV-02 uniqueness of versionOf.
}

// -- FMO-INV-16  Failure retention ----------------------------------------------
// Structural: Operation atoms are immutable and never removed; a REJECTED/FAILED/
// HALTED/UNKNOWN op remains an atom.  A later success adds a new atom, never edits
// or deletes the failure record.  (No fact needed.)

// -- Candidate lifecycle well-formedness (support for INV-01/05/06) -------------
fact CandidateLifecycle {
  all n: Candidate {
    PENDING in n.reached                              // starts PENDING
    not (REJECTED in n.reached and ADMITTED in n.reached)   // terminal states exclusive
    // admission time ordering: candidate exists no later than its admitted object
  }
  all o: Object | TO/lte[o.admittedFrom.createdAtN, o.createdAtO]
}

// ===========================================================================
// H3 (a)  --  SATISFIABILITY of the whole core
// ===========================================================================
pred nontrivial {
  some Object
  some Candidate
  some Event
  some Prov
  some Operation
  some Claim
  some DeletionScope
}
// Expected: instance found  ->  the FMO-0.1 core (as encoded) is SATISFIABLE.
run FMO_satisfiable { nontrivial } for 6 but 8 Time, 6 Object, 12 Operation, 10 Prov

// A tiny sanity run with no extra pressure (should also find an instance).
run FMO_minimal {} for 4 but 6 Time

// ===========================================================================
// H3 (b)  --  COUNTERMODEL WITNESSES  (each `run` should find an instance)
// ===========================================================================

// CM-01  highConfidence(k) ⇏ correct(k)
pred CM01_highConf_not_correct {
  some o: Object, k: Claim, ca: ConfAssessment, ta: Assessment |
    k in o.asserts
    and ca.cTarget = k and ca.level = HIGH        // 0.99-ish confidence in support
    and ta.aClaim = k and ta.status = T_CHALLENGED // yet challenged
}
run CM01_highConf_not_correct for 5 but 6 Time, 3 Object, 8 Operation

// CM-02  retrieved(o,q) ⇏ relevant(o,q)  and  ⇏ used(o,q)
pred CM02_retrieved_not_relevant_or_used {
  some op: Operation, o1, o2: Object |
    op.opKind = Retrieve
    and o1 != o2
    and op.returns = o1 + o2       // both returned (both eligible/accessible)
    and op.used = o1               // only o1 used
    and o2 not in op.used          // o2 unused
    and o2 not in op.relevant      // and not relevant
}
run CM02_retrieved_not_relevant_or_used for 5 but 6 Time, 4 Object, 8 Operation

// CM-03  hasProvenance(o) ⇏ authenticProvenance(o)
pred CM03_provenance_not_authentic {
  some o: Object, p: Prov, pa: ProvAssessment |
    p.relKind = WAS_ADMITTED_FROM and p.subj = o    // connected admission trace
    and pa.paProv = p and pa.paStatus = T_CHALLENGED // yet the edge is challenged as forged
}
run CM03_provenance_not_authentic for 5 but 6 Time, 3 Object, 8 Prov, 8 Operation

// CM-04  forgotten(o) ⇏ deleted(o)
pred CM04_forgotten_not_deleted {
  some o: Object, t: Time |
    o.state[t] = SUPPRESSED                          // forgotten
    and (no t2: Time | o.state[t2] = DELETED)        // never deleted
}
run CM04_forgotten_not_deleted for 5 but 8 Time, 3 Object, 10 Operation

// CM-06  locallyErased(o1) ⇏ deletionVerifiedWithinScope(o1)   (the INCOMPLETE case)
pred CM06_incomplete_deletion {
  some op: Operation, ds: DeletionScope, root, deriv: Object |
    root != deriv
    and op.opKind = ExecuteDelete
    and op.delScope = ds
    and ds.targets = root + deriv                    // derivative is in the frozen closure
    and (some p: Prov | p.relKind = WAS_CONSOLIDATED_FROM and p.subj = deriv and p.obj = root)
    and some deriv.state[op.opTime]
    and deriv.state[op.opTime] != DELETED            // in-scope derivative survives
    and op.delResult = D_INCOMPLETE                  // so result MUST be INCOMPLETE, not VERIFIED
}
run CM06_incomplete_deletion for 6 but 8 Time, 4 Object, 10 Operation

// CM-10  independent reacquisition ⇏ resurrection  (bonus)
pred CM10_reacquire_not_resurrect {
  some o1, o2: Object, t: Time |
    o1 != o2
    and o1.state[t] = DELETED                        // o1 verified-deleted, terminal
    and o1.contentID = o2.contentID                  // equivalent content
    and o1.versionOf != o2.versionOf                 // but a NEW exact identity
    and o1.admittedFrom != o2.admittedFrom           // independent provenance
    and (all t2: Time | TO/gte[t2, t] implies o1.state[t2] = DELETED)  // o1 stays terminal
}
run CM10_reacquire_not_resurrect for 6 but 8 Time, 4 Object, 12 Operation

// ===========================================================================
// H3 (c)  --  NON-ENTAILMENT CHECKS
// For these, a COUNTEREXAMPLE FOUND is the *desired* result: it shows the core
// does NOT force the implication (the non-entailment holds).
// ===========================================================================

assert Retrieved_forces_Relevant {
  all op: Operation, o: Object |
    (op.opKind = Retrieve and o in op.returns) implies o in op.relevant
}
// Expected: COUNTEREXAMPLE FOUND  -> retrieved ⇏ relevant.
check Retrieved_forces_Relevant for 5 but 6 Time, 4 Object, 8 Operation

assert Provenance_forces_Authentic {
  all o: Object, p: Prov |
    (p.relKind = WAS_ADMITTED_FROM and p.subj = o)
      implies (no pa: ProvAssessment | pa.paProv = p and pa.paStatus = T_CHALLENGED)
}
// Expected: COUNTEREXAMPLE FOUND  -> hasProvenance ⇏ authentic.
check Provenance_forces_Authentic for 5 but 6 Time, 3 Object, 8 Prov, 8 Operation

assert Forgotten_forces_Deleted {
  all o: Object |
    (some t: Time | o.state[t] = SUPPRESSED)
      implies (some t2: Time | o.state[t2] = DELETED)
}
// Expected: COUNTEREXAMPLE FOUND  -> forgotten ⇏ deleted.
check Forgotten_forces_Deleted for 5 but 8 Time, 3 Object, 10 Operation

assert Access_one_tuple_forces_all_actors {
  all x: Access, a2: Actor |
    some x2: Access |
      x2.acActor = a2 and x2.acObj = x.acObj and x2.acQuery = x.acQuery
      and x2.acPurpose = x.acPurpose and x2.acBoundary = x.acBoundary and x2.acTime = x.acTime
}
// Expected: COUNTEREXAMPLE FOUND  -> access for one tuple ⇏ access for another actor
// (FMO-INV-13 / cross-authority leakage non-entailment).
check Access_one_tuple_forces_all_actors for 4 but 4 Time

// ===========================================================================
// POSITIVE SAFETY CHECKS
// For these, NO COUNTEREXAMPLE is the desired result: they should be *valid*
// consequences of the facts (sanity that the model is not vacuously broken).
// ===========================================================================

assert DerivationAcyclic {                     // FMO-INV-07 / FMO-P01
  no o: Object | o in o.^derivEdges
}
// Expected: NO COUNTEREXAMPLE (valid, given DerivationOrder + strict time order).
check DerivationAcyclic for 6 but 8 Time, 6 Object, 10 Prov

assert VerifiedImpliesAllTargetsDeleted {      // FMO-INV-14
  all op: Operation |
    (op.opKind = ExecuteDelete and op.delResult = D_VERIFIED)
      implies (all x: op.delScope.targets | x.state[op.opTime] = DELETED)
}
// Expected: NO COUNTEREXAMPLE (directly enforced by DeletionSuccessClosure).
check VerifiedImpliesAllTargetsDeleted for 6 but 8 Time, 5 Object, 10 Operation

assert DeletedIsTerminal {                     // FMO-INV-15
  all o: Object, t: Time |
    o.state[t] = DELETED implies (all t2: Time | TO/gte[t2, t] implies o.state[t2] = DELETED)
}
// Expected: NO COUNTEREXAMPLE (enforced by NoResurrection + LegalTransitions).
check DeletedIsTerminal for 6 but 8 Time, 5 Object, 10 Operation

assert SupersededPredecessorPreserved {        // FMO-INV-08 (structural identity preservation)
  all n, old: Object | old in n.supersedes implies {
    old.seriesOf = n.seriesOf
    old.createdAtO != n.createdAtO             // distinct exact versions
    n.predecessor = old
  }
}
// Expected: NO COUNTEREXAMPLE (enforced by SupersessionMeaning + PredecessorOrder).
check SupersededPredecessorPreserved for 6 but 8 Time, 5 Object, 10 Operation

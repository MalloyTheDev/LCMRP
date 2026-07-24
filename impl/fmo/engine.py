"""Append-only interpreter of the FMO-0.1 operation contracts.

This is a *witness*, not a product. It picks no database, model, embedding, or
schema; it only interprets the operation contracts and their invariants /
non-entailments so they can be exercised by tests.

Design commitments:
  * Immutable event log. Every operation appends exactly one OperationRecord
    (even rejected / failed ones, FMO-INV-16). Nothing is mutated.
  * Transaction time is a monotonic counter (`_tick`). No wall clock is read.
  * Object lifecycle state is DERIVED by folding StateEvent records, never
    stored as a mutable field on the object (keeps append-only honest).
  * Guarded transitions: state changes require an authz PERMIT (FMO-INV-05).
"""

from typing import Dict, List, Optional, Sequence, Set, Tuple

from .authority import Authority
from .entities import (
    Assessment,
    Candidate,
    ConfidenceAssessment,
    ConflictAssessment,
    DeletionScope,
    Event,
    ObjectVersion,
    OperationRecord,
    ProvenanceAssertion,
    RoleAssignment,
    StateEvent,
    UncertaintyRecord,
)
from .enums import (
    AuthzDecision,
    CandidateState,
    DeletionResult,
    FunctionalRole,
    ObjectState,
    OperationResult,
    ProvKind,
    TruthStatus,
    PRIMARY_KINDS,
)

# Legal object lifecycle transitions (from the object state diagram).
_OBJECT_TRANSITIONS = {
    ("ACTIVE", "SUPPRESSED"),
    ("SUPPRESSED", "ACTIVE"),
    ("ACTIVE", "ARCHIVED"),
    ("SUPPRESSED", "ARCHIVED"),
    ("ARCHIVED", "ACTIVE"),
    ("ACTIVE", "SUPERSEDED"),
    ("SUPPRESSED", "SUPERSEDED"),
    ("ARCHIVED", "SUPERSEDED"),
    ("ACTIVE", "DELETE_PENDING"),
    ("SUPPRESSED", "DELETE_PENDING"),
    ("ARCHIVED", "DELETE_PENDING"),
    ("SUPERSEDED", "DELETE_PENDING"),
    ("DELETE_PENDING", "DELETED"),
    ("DELETE_PENDING", "DELETE_PENDING"),
}


class OpOutcome:
    """Return value of every operation: the record plus any produced entity."""

    def __init__(self, record: OperationRecord, value=None):
        self.record = record
        self.value = value

    @property
    def ok(self) -> bool:
        return self.record.result == OperationResult.SUCCEEDED


class Engine:
    def __init__(self, authority: Optional[Authority] = None, organization: str = "R"):
        assert organization in ("K", "R"), "organization must be 'K' or 'R'"
        self.organization = organization
        self.authority = authority or Authority()

        self._tx = 0  # monotonic transaction-time counter (NOT wall clock)
        self._seq = 0  # id disambiguator

        # append-only logs
        self.events: List[Event] = []
        self.candidates: List[Candidate] = []
        self.objects: List[ObjectVersion] = []
        self.prov: List[ProvenanceAssertion] = []
        self.ops: List[OperationRecord] = []
        self.state_events: List[StateEvent] = []
        self.confidences: List[ConfidenceAssessment] = []
        self.uncertainties: List[UncertaintyRecord] = []
        self.assessments: List[Assessment] = []
        self.conflicts: List[ConflictAssessment] = []
        self.roles: List[RoleAssignment] = []
        self.scopes: Dict[str, DeletionScope] = {}

        # objects the interpreter still considers materialized in the boundary
        self._materialized: Set[str] = set()
        # primaryKind per series (Organization K only)
        self._primary_kind: Dict[str, FunctionalRole] = {}

    # ------------------------------------------------------------------ ids
    def _tick(self) -> int:
        self._tx += 1
        return self._tx

    def _id(self, prefix: str) -> str:
        self._seq += 1
        return f"{prefix}{self._seq}"

    def _okey(self, o: ObjectVersion) -> str:
        return f"{o.object_id}:{o.version_id}"

    def _record(self, kind, actor, decision, basis, inputs, outputs, purpose,
                tx, result, failure=None) -> OperationRecord:
        rec = OperationRecord(
            operation_id=self._id("op"),
            operation_kind=kind,
            actor=actor,
            authority_decision=decision,
            authority_basis=basis,
            inputs=tuple(inputs),
            outputs=tuple(outputs),
            purpose=purpose,
            transaction_time=tx,
            result=result,
            failure=failure,
        )
        self.ops.append(rec)
        return rec

    # --------------------------------------------------------- derived state
    def object_state(self, o: ObjectVersion, at: Optional[int] = None) -> ObjectState:
        key = self._okey(o)
        state = ObjectState.ACTIVE  # every admitted object starts ACTIVE
        for ev in self.state_events:
            if ev.subject_id != key:
                continue
            if at is not None and ev.transaction_time > at:
                continue
            state = ObjectState(ev.to_state)
        return state

    def candidate_state(self, n: Candidate, at: Optional[int] = None) -> CandidateState:
        key = f"cand:{n.candidate_id}"
        state = CandidateState.PENDING
        for ev in self.state_events:
            if ev.subject_id != key:
                continue
            if at is not None and ev.transaction_time > at:
                continue
            state = CandidateState(ev.to_state)
        return state

    def materialized(self, o: ObjectVersion) -> bool:
        return self._okey(o) in self._materialized

    def accessible(self, actor, o: ObjectVersion, query, purpose, boundary,
                   at: Optional[int] = None) -> bool:
        """Contextual accessibility (FMO-INV-13): evaluated for an exact tuple.
        A DELETED or unmaterialized object is never accessible; otherwise ACTIVE
        objects are accessible in this minimal model. The point is that the
        signature is per-(actor, object, query, purpose, boundary, time)."""
        st = self.object_state(o, at)
        if st in (ObjectState.DELETED, ObjectState.DELETE_PENDING):
            return False
        if not self.materialized(o):
            return False
        return st == ObjectState.ACTIVE

    def _emit_state(self, key, to_state, op_id, tx, from_state=None):
        self.state_events.append(
            StateEvent(key, from_state, to_state, op_id, tx)
        )

    def _guard(self, actor, op_kind, target, purpose, domain, tx):
        return self.authority.decide(actor, op_kind, target, purpose, domain, tx)

    # ------------------------------------------------------------ operations
    def encode(self, content_id, actor, transform=None, purpose="encode",
               domain="d", event_time=None, series=None, origin_refs=()) -> OpOutcome:
        tx = self._tick()
        ev = Event(
            event_id=self._id("e"),
            source_actor=actor,
            event_time=event_time,
            receipt_time=tx,
            content_id=content_id,
            authority_domain=domain,
        )
        self.events.append(ev)
        decision, basis = self._guard(actor, "encode", ev.event_id, purpose, domain, tx)
        if decision != AuthzDecision.PERMIT:
            rec = self._record("encode", actor, decision, basis, [ev.event_id],
                               [], purpose, tx, OperationResult.REJECTED,
                               failure="authorization not PERMIT")
            return OpOutcome(rec)
        cand = Candidate(
            candidate_id=self._id("n"),
            content_id=content_id,
            proposed_series=series,
            origin_refs=tuple(origin_refs) + (ev.event_id,),
            transform_ref=transform,
            created_by=actor,
            created_at=tx,
            authority_domain=domain,
        )
        self.candidates.append(cand)
        rec = self._record("encode", actor, decision, basis, [ev.event_id],
                           [cand.candidate_id], purpose, tx, OperationResult.SUCCEEDED)
        self._prov(ProvKind.WAS_ENCODED_FROM, cand.candidate_id, ev.event_id,
                   actor, rec.operation_id, tx, domain)
        return OpOutcome(rec, cand)

    def _prov(self, kind, subject, obj, actor, op_id, tx, domain):
        pa = ProvenanceAssertion(
            prov_id=self._id("pt"),
            relation_kind=kind,
            subject=subject,
            object=obj,
            asserted_by=actor,
            operation=op_id,
            transaction_time=tx,
            authority_domain=domain,
        )
        self.prov.append(pa)
        return pa

    def admit(self, cand: Candidate, actor, purpose="admit", domain="d") -> OpOutcome:
        tx = self._tick()
        if self.candidate_state(cand) != CandidateState.PENDING:
            rec = self._record("admit", actor, AuthzDecision.PERMIT, "n/a",
                               [cand.candidate_id], [], purpose, tx,
                               OperationResult.REJECTED, failure="candidate not PENDING")
            return OpOutcome(rec)
        decision, basis = self._guard(actor, "admit", cand.candidate_id, purpose, domain, tx)
        if decision != AuthzDecision.PERMIT:
            rec = self._record("admit", actor, decision, basis, [cand.candidate_id],
                               [], purpose, tx, OperationResult.REJECTED,
                               failure="authorization not PERMIT")
            self._emit_state(f"cand:{cand.candidate_id}", "REJECTED",
                             rec.operation_id, tx, "PENDING")
            return OpOutcome(rec)
        series = cand.proposed_series or self._id("s")
        obj = ObjectVersion(
            object_id=self._id("o"),
            series_id=series,
            version_id=self._id("v"),
            content_id=cand.content_id,
            admitted_from=cand.candidate_id,
            created_at=tx,
            authority_domain=domain,
        )
        self.objects.append(obj)
        self._materialized.add(self._okey(obj))
        rec = self._record("admit", actor, decision, basis, [cand.candidate_id],
                           [obj.object_id], purpose, tx, OperationResult.SUCCEEDED)
        # candidate becomes ADMITTED; object born ACTIVE (implicit start state)
        self._emit_state(f"cand:{cand.candidate_id}", "ADMITTED", rec.operation_id,
                         tx, "PENDING")
        self._prov(ProvKind.WAS_ADMITTED_FROM, obj.object_id, cand.candidate_id,
                   actor, rec.operation_id, tx, domain)
        return OpOutcome(rec, obj)

    def retrieve(self, objs: Sequence[ObjectVersion], actor, query="q",
                 purpose="retrieve", boundary="b") -> OpOutcome:
        """Retrieval mutates nothing (FMO-INV-10): no state events, no new
        candidates/objects. It only reads and records a decision."""
        tx = self._tick()
        results = [
            o for o in objs
            if self.accessible(actor, o, query, purpose, boundary, tx)
        ]
        rec = self._record("retrieve", actor, AuthzDecision.PERMIT, "read-only",
                           [self._okey(o) for o in objs],
                           [self._okey(o) for o in results], purpose, tx,
                           OperationResult.SUCCEEDED)
        return OpOutcome(rec, results)

    def update(self, o: ObjectVersion, new_content_id, actor, purpose="update",
               domain="d") -> OpOutcome:
        """update -> (pending candidate). On admission of the successor the
        predecessor flips to SUPERSEDED with identity preserved (FMO-INV-08)."""
        tx = self._tick()
        if self.object_state(o) == ObjectState.DELETED:
            rec = self._record("update", actor, AuthzDecision.PERMIT, "n/a",
                               [o.object_id], [], purpose, tx,
                               OperationResult.REJECTED, failure="predecessor DELETED")
            return OpOutcome(rec)
        decision, basis = self._guard(actor, "update", o.object_id, purpose, domain, tx)
        if decision != AuthzDecision.PERMIT:
            rec = self._record("update", actor, decision, basis, [o.object_id],
                               [], purpose, tx, OperationResult.REJECTED,
                               failure="authorization not PERMIT")
            return OpOutcome(rec)
        cand = Candidate(
            candidate_id=self._id("n"),
            content_id=new_content_id,
            proposed_series=o.series_id,
            origin_refs=(o.object_id,),
            transform_ref="update",
            created_by=actor,
            created_at=tx,
            authority_domain=domain,
        )
        self.candidates.append(cand)
        rec = self._record("update", actor, decision, basis, [o.object_id],
                           [cand.candidate_id], purpose, tx, OperationResult.SUCCEEDED)
        self._prov(ProvKind.WAS_UPDATED_FROM, cand.candidate_id, o.object_id,
                   actor, rec.operation_id, tx, domain)
        return OpOutcome(rec, cand)

    def supersede(self, predecessor: ObjectVersion, successor_candidate: Candidate,
                  actor, purpose="supersede", domain="d") -> OpOutcome:
        """Admit the update-successor, flipping the predecessor to SUPERSEDED."""
        tx = self._tick()
        st = self.object_state(predecessor)
        if st in (ObjectState.SUPERSEDED, ObjectState.DELETED, ObjectState.DELETE_PENDING):
            rec = self._record("supersede", actor, AuthzDecision.PERMIT, "n/a",
                               [predecessor.object_id], [], purpose, tx,
                               OperationResult.REJECTED, failure=f"predecessor {st.value}")
            return OpOutcome(rec)
        out = self.admit(successor_candidate, actor, purpose="admit-successor", domain=domain)
        if not out.ok:
            return out
        successor = out.value
        tx2 = self._tick()
        rec = self._record("supersede", actor, AuthzDecision.PERMIT, "successor-admitted",
                           [predecessor.object_id], [successor.object_id], purpose, tx2,
                           OperationResult.SUCCEEDED)
        self._emit_state(self._okey(predecessor), "SUPERSEDED", rec.operation_id,
                         tx2, st.value)
        self._prov(ProvKind.WAS_SUPERSEDED_BY, predecessor.object_id,
                   successor.object_id, actor, rec.operation_id, tx2, domain)
        return OpOutcome(rec, successor)

    def consolidate(self, inputs: Sequence[ObjectVersion], actor, transform="consolidate",
                    purpose="consolidate", domain="d") -> OpOutcome:
        tx = self._tick()
        if len(inputs) < 2:
            rec = self._record("consolidate", actor, AuthzDecision.PERMIT, "n/a",
                               [o.object_id for o in inputs], [], purpose, tx,
                               OperationResult.REJECTED, failure="need >=2 inputs")
            return OpOutcome(rec)
        decision, basis = self._guard(actor, "consolidate", None, purpose, domain, tx)
        if decision != AuthzDecision.PERMIT:
            rec = self._record("consolidate", actor, decision, basis,
                               [o.object_id for o in inputs], [], purpose, tx,
                               OperationResult.REJECTED, failure="authorization not PERMIT")
            return OpOutcome(rec)
        cand = Candidate(
            candidate_id=self._id("n"),
            content_id=self._id("c"),
            proposed_series=None,
            origin_refs=tuple(o.object_id for o in inputs),
            transform_ref=transform,
            created_by=actor,
            created_at=tx,
            authority_domain=domain,
        )
        self.candidates.append(cand)
        rec = self._record("consolidate", actor, decision, basis,
                           [o.object_id for o in inputs], [cand.candidate_id],
                           purpose, tx, OperationResult.SUCCEEDED)
        # a consolidation edge for EVERY input (cannot hide a contributor)
        for o in inputs:
            self._prov(ProvKind.WAS_CONSOLIDATED_FROM, cand.candidate_id,
                       o.object_id, actor, rec.operation_id, tx, domain)
        return OpOutcome(rec, cand)

    def _state_op(self, kind, o, to_state, allowed_from, actor, purpose, domain):
        tx = self._tick()
        st = self.object_state(o)
        if st.value not in allowed_from:
            rec = self._record(kind, actor, AuthzDecision.PERMIT, "n/a",
                               [o.object_id], [], purpose, tx,
                               OperationResult.REJECTED, failure=f"state {st.value}")
            return OpOutcome(rec)
        decision, basis = self._guard(actor, kind, o.object_id, purpose, domain, tx)
        if decision != AuthzDecision.PERMIT:
            rec = self._record(kind, actor, decision, basis, [o.object_id], [],
                               purpose, tx, OperationResult.REJECTED,
                               failure="authorization not PERMIT")
            return OpOutcome(rec)
        rec = self._record(kind, actor, decision, basis, [o.object_id],
                           [o.object_id], purpose, tx, OperationResult.SUCCEEDED)
        self._emit_state(self._okey(o), to_state, rec.operation_id, tx, st.value)
        return OpOutcome(rec, o)

    def forget(self, o, actor, purpose="forget", domain="d") -> OpOutcome:
        return self._state_op("forget", o, "SUPPRESSED", {"ACTIVE"}, actor, purpose, domain)

    def archive(self, o, actor, purpose="archive", domain="d") -> OpOutcome:
        return self._state_op("archive", o, "ARCHIVED", {"ACTIVE", "SUPPRESSED"},
                              actor, purpose, domain)

    def restore(self, o, actor, purpose="restore", domain="d") -> OpOutcome:
        return self._state_op("restore", o, "ACTIVE", {"SUPPRESSED", "ARCHIVED"},
                              actor, purpose, domain)

    # --------------------------------------------------- epistemic records
    def assess_confidence(self, target, assessor, value, method="declared",
                          scale="numeric-unit-interval", context="cx") -> ConfidenceAssessment:
        tx = self._tick()
        ca = ConfidenceAssessment(self._id("ca"), target, assessor, method, scale,
                                  tuple(value), context, tx)
        self.confidences.append(ca)
        return ca

    def describe_uncertainty(self, target, assessor_or_method, kind,
                             context="cx") -> UncertaintyRecord:
        tx = self._tick()
        ua = UncertaintyRecord(self._id("ua"), target, assessor_or_method, kind,
                               context, tx)
        self.uncertainties.append(ua)
        return ua

    def assess_claim(self, claim_id, assessor, status: TruthStatus,
                     context="cx") -> Assessment:
        tx = self._tick()
        a = Assessment(self._id("as"), claim_id, assessor, context, status, tx)
        self.assessments.append(a)
        return a

    def detect_conflict(self, claim_a, claim_b, context, valid_overlap) -> Optional[ConflictAssessment]:
        """Symmetric, irreflexive. Records an assessment only; changes nothing
        (FMO-INV-12). Returns None when the claims are identical or validity does
        not overlap (non-overlap is not conflict)."""
        tx = self._tick()
        if claim_a == claim_b:
            return None
        if not valid_overlap:
            # different claims over disjoint validity: no conflict is required
            return None
        ca = ConflictAssessment(self._id("cf"), claim_a, claim_b, context,
                                valid_overlap, tx)
        self.conflicts.append(ca)
        return ca

    # ----------------------------------------------------- functional roles
    def assign_role(self, o: ObjectVersion, role: FunctionalRole, query, actor,
                    purpose="classify") -> OpOutcome:
        """Contextual role assignment.

        Under Organization R (role-first): always records a playsRole edge; one
        identity may play many roles across contexts with no version change.

        Under Organization K (kind-first): the series carries a single, invariant
        primaryKind drawn from PRIMARY_KINDS. Assigning a role whose kind differs
        from an already-fixed primaryKind is REJECTED on this identity -- K must
        mint a *separate* identity to carry the other kind."""
        tx = self._tick()
        if self.organization == "R":
            ra = RoleAssignment(self._id("r"), o.object_id, role, query, actor,
                                purpose, tx)
            self.roles.append(ra)
            rec = self._record("assign_role", actor, AuthzDecision.PERMIT, "role-first",
                               [o.object_id], [ra.role_id], purpose, tx,
                               OperationResult.SUCCEEDED)
            return OpOutcome(rec, ra)
        # Organization K
        if role not in PRIMARY_KINDS:
            # e.g. WORKING is not a primaryKind: K cannot classify a durable
            # object as WORKING on its stable identity.
            rec = self._record("assign_role", actor, AuthzDecision.PERMIT, "kind-first",
                               [o.object_id], [], purpose, tx,
                               OperationResult.REJECTED,
                               failure=f"{role.value} is not a primaryKind")
            return OpOutcome(rec)
        existing = self._primary_kind.get(o.series_id)
        if existing is None:
            self._primary_kind[o.series_id] = role
            rec = self._record("assign_role", actor, AuthzDecision.PERMIT, "kind-first",
                               [o.object_id], [o.series_id], purpose, tx,
                               OperationResult.SUCCEEDED)
            return OpOutcome(rec, role)
        if existing == role:
            rec = self._record("assign_role", actor, AuthzDecision.PERMIT, "kind-first",
                               [o.object_id], [o.series_id], purpose, tx,
                               OperationResult.SUCCEEDED)
            return OpOutcome(rec, role)
        rec = self._record("assign_role", actor, AuthzDecision.PERMIT, "kind-first",
                           [o.object_id], [], purpose, tx, OperationResult.REJECTED,
                           failure=f"primaryKind already {existing.value}, invariant")
        return OpOutcome(rec)

    # ------------------------------------------------------------- deletion
    def declare_scope(self, root_targets, closure_kinds, actor, boundary="b",
                      exceptions=(), verification_method="closure-check") -> DeletionScope:
        ds = DeletionScope(
            ds_id=self._id("ds"),
            root_targets=tuple(root_targets),
            boundary=boundary,
            closure_kinds=tuple(k.value for k in closure_kinds),
            exceptions=tuple(exceptions),
            verification_method=verification_method,
            authority_basis=actor,
        )
        self.scopes[ds.ds_id] = ds
        return ds

    def _closure(self, ds: DeletionScope) -> Set[str]:
        """Targets(d) = closure over the declared provenance relations from the
        roots, minus exceptions. Objects reachable as derivatives/successors of a
        root along an in-scope edge are pulled in."""
        kinds = set(ds.closure_kinds)
        targets: Set[str] = set(ds.root_targets)
        frontier = list(ds.root_targets)
        while frontier:
            cur = frontier.pop()
            for pa in self.prov:
                if pa.relation_kind.value not in kinds:
                    continue
                # follow edges whose *source* (object endpoint) is cur, to reach
                # the derived candidate, then map candidate -> admitted object.
                if pa.object == cur:
                    derived = self._object_for_candidate(pa.subject)
                    if derived and derived.object_id not in targets:
                        targets.add(derived.object_id)
                        frontier.append(derived.object_id)
                # superseded-by edges point predecessor -> successor object
                if pa.subject == cur and pa.relation_kind == ProvKind.WAS_SUPERSEDED_BY:
                    if pa.object not in targets:
                        targets.add(pa.object)
                        frontier.append(pa.object)
        return targets - set(ds.exceptions)

    def _object_for_candidate(self, candidate_id) -> Optional[ObjectVersion]:
        for o in self.objects:
            if o.admitted_from == candidate_id:
                return o
        return None

    def _obj_by_id(self, object_id) -> Optional[ObjectVersion]:
        for o in self.objects:
            if o.object_id == object_id:
                return o
        return None

    def request_delete(self, ds: DeletionScope, actor, purpose="delete", domain="d") -> OpOutcome:
        tx = self._tick()
        decision, basis = self._guard(actor, "requestDelete", ds.ds_id, purpose, domain, tx)
        if decision == AuthzDecision.DENY:
            rec = self._record("requestDelete", actor, decision, basis,
                               list(ds.root_targets), [], purpose, tx,
                               OperationResult.REJECTED, failure="DENY")
            return OpOutcome(rec)
        targets = self._closure(ds)
        rec = self._record("requestDelete", actor, decision, basis,
                           list(ds.root_targets), sorted(targets), purpose, tx,
                           OperationResult.SUCCEEDED
                           if decision == AuthzDecision.PERMIT else OperationResult.UNKNOWN)
        if decision == AuthzDecision.PERMIT:
            for oid in targets:
                o = self._obj_by_id(oid)
                if o is None:
                    continue
                st = self.object_state(o)
                if (st.value, "DELETE_PENDING") in _OBJECT_TRANSITIONS:
                    self._emit_state(self._okey(o), "DELETE_PENDING",
                                     rec.operation_id, tx, st.value)
        return OpOutcome(rec, targets)

    def execute_delete(self, ds: DeletionScope, actor, erased_ids=None,
                       purpose="delete", domain="d") -> OpOutcome:
        """Attempt deletion. `erased_ids` = the object ids the executor actually
        manages to erase (defaults to the full closure = a complete deletion). A
        flat "delete the row" caller passes erased_ids = {root} only; the scoped
        closure check then catches the surviving derivative and returns
        INCOMPLETE (FMO-INV-14, H5)."""
        tx = self._tick()
        decision, basis = self._guard(actor, "executeDelete", ds.ds_id, purpose, domain, tx)
        if decision != AuthzDecision.PERMIT:
            rec = self._record("executeDelete", actor, decision, basis,
                               list(ds.root_targets), [], purpose, tx,
                               OperationResult.REJECTED, failure="authorization not PERMIT")
            return OpOutcome(rec, DeletionResult.UNVERIFIED)

        targets = self._closure(ds)
        erased = set(targets) if erased_ids is None else set(erased_ids)

        # apply erasure: move erased targets to DELETED, drop materialization
        for oid in erased:
            o = self._obj_by_id(oid)
            if o is None:
                continue
            st = self.object_state(o)
            if st == ObjectState.DELETED:
                continue
            # must pass through DELETE_PENDING (request_delete) then DELETED
            if st != ObjectState.DELETE_PENDING:
                self._emit_state(self._okey(o), "DELETE_PENDING", "auto", tx, st.value)
            de_rec = self._record("executeDelete.erase", actor, AuthzDecision.PERMIT,
                                  basis, [oid], [oid], purpose, tx,
                                  OperationResult.SUCCEEDED)
            self._emit_state(self._okey(o), "DELETED", de_rec.operation_id, tx,
                             "DELETE_PENDING")
            self._materialized.discard(self._okey(o))

        # verify EVERY non-excepted target
        result = DeletionResult.VERIFIED_WITHIN_SCOPE
        survivors = []
        for oid in targets:
            o = self._obj_by_id(oid)
            if o is None:
                result = DeletionResult.INCOMPLETE
                survivors.append(oid)
                continue
            deleted = self.object_state(o) == ObjectState.DELETED
            reconstructable = self._reconstructable(oid, targets)
            if not (deleted and not self.materialized(o) and not reconstructable):
                result = DeletionResult.INCOMPLETE
                survivors.append(oid)

        rec = self._record("executeDelete", actor, decision, basis,
                           sorted(targets), sorted(erased), purpose, tx,
                           OperationResult.SUCCEEDED if result == DeletionResult.VERIFIED_WITHIN_SCOPE
                           else OperationResult.HALTED,
                           failure=None if result == DeletionResult.VERIFIED_WITHIN_SCOPE
                           else f"surviving in-scope targets: {survivors}")
        return OpOutcome(rec, result)

    def _reconstructable(self, oid, targets) -> bool:
        """True if a SURVIVING (non-deleted, in-boundary) object's lineage
        depends on `oid` -- i.e. a derivative that is NOT itself being deleted
        could reconstruct content whose lineage depends on the target."""
        for pa in self.prov:
            if pa.relation_kind not in (ProvKind.WAS_CONSOLIDATED_FROM,
                                        ProvKind.WAS_UPDATED_FROM):
                continue
            if pa.object != oid:
                continue
            derived = self._object_for_candidate(pa.subject)
            if derived is None:
                continue
            if derived.object_id in targets:
                continue  # the derivative is itself in scope, fine
            if self.object_state(derived) != ObjectState.DELETED and self.materialized(derived):
                return True
        return False

    # -------------------------------------------------------------- trace()
    def trace(self, root_id) -> Tuple[Set[str], Set[str]]:
        """Reachability closure over provenance edges rooted at `root_id`.
        Returns (visited provenance-assertion ids, visited endpoint ids)."""
        seen_pt: Set[str] = set()
        seen_nodes: Set[str] = {root_id}
        frontier = [root_id]
        while frontier:
            cur = frontier.pop()
            for pa in self.prov:
                if pa.subject == cur or pa.object == cur:
                    if pa.prov_id not in seen_pt:
                        seen_pt.add(pa.prov_id)
                        for endpoint in (pa.subject, pa.object):
                            if endpoint not in seen_nodes:
                                seen_nodes.add(endpoint)
                                frontier.append(endpoint)
        return seen_pt, seen_nodes

"""One unit test per encoded countermodel CM-01 .. CM-10.

Each asserts the intended *non-entailment* holds in the interpreter: the
antecedent structure exists, yet the consequent does not follow. These witness
the FMO's "explicit non-entailments" list; they are structural, not a machine
check of the FMO core.
"""

from fmo import (
    Engine,
    Authority,
    AuthzDecision,
    DeletionResult,
    FunctionalRole,
    ObjectState,
    ProvKind,
    TruthStatus,
)


def _admit(eng, content="c", actor="alice", series=None):
    c = eng.encode(content, actor, series=series).value
    return eng.admit(c, actor).value


# CM-01 -- high confidence does not establish correctness -----------------
def test_cm01_high_confidence_not_correct():
    eng = Engine()
    o = _admit(eng)
    claim = f"k:{o.object_id}"
    eng.assess_confidence(claim, "alice", (0.99, 1.00))          # high confidence
    a = eng.assess_claim(claim, "bob", TruthStatus.CHALLENGED)   # yet challenged
    # both records coexist; nothing equates confidence with truth
    assert any(ca.value == (0.99, 1.00) for ca in eng.confidences)
    assert a.status == TruthStatus.CHALLENGED
    # no support/correctness predicate is derivable from the confidence record
    assert not any(x.status == TruthStatus.SUPPORTED for x in eng.assessments)


# CM-02 -- retrieved does not entail use or relevance ----------------------
def test_cm02_retrieved_not_used_or_relevant():
    eng = Engine()
    o1 = _admit(eng, "c1")
    o2 = _admit(eng, "c2")
    out = eng.retrieve([o1, o2], "alice")
    assert {r.object_id for r in out.value} == {o1.object_id, o2.object_id}
    # a separate "use" cites only o1; a relevance assessment challenges o2
    used = {o1.object_id}
    eng.assess_claim(f"relevance:{o2.object_id}", "alice", TruthStatus.CHALLENGED)
    assert o2.object_id in {r.object_id for r in out.value}  # returned
    assert o2.object_id not in used                          # but not used
    # retrieval itself emitted no state change
    assert all(op.operation_kind != "retrieve" or op.outputs is not None
               for op in eng.ops)


# CM-03 -- connected provenance need not be authentic ----------------------
def test_cm03_connected_trace_not_authentic():
    eng = Engine()
    o = _admit(eng)
    pt_ids, nodes = eng.trace(o.object_id)
    assert len(pt_ids) >= 1 and o.admitted_from in nodes  # connected trace
    # challenge the encoding assertion as forged
    enc = next(p for p in eng.prov if p.relation_kind == ProvKind.WAS_ENCODED_FROM)
    eng.assess_claim(f"authentic:{enc.prov_id}", "auditor", TruthStatus.CHALLENGED)
    # the trace is still structurally connected, yet flagged non-authentic
    pt_ids2, _ = eng.trace(o.object_id)
    assert pt_ids2 == pt_ids
    assert any(a.status == TruthStatus.CHALLENGED for a in eng.assessments)


# CM-04 -- forgotten is not deleted ----------------------------------------
def test_cm04_forgotten_not_deleted():
    eng = Engine()
    o = _admit(eng)
    assert eng.forget(o, "alice").ok
    assert eng.object_state(o) == ObjectState.SUPPRESSED
    assert eng.object_state(o) != ObjectState.DELETED
    # restoration remains available -> recoverable, not erased
    assert eng.restore(o, "alice").ok
    assert eng.object_state(o) == ObjectState.ACTIVE


# CM-05 -- different claims without conflict over disjoint validity --------
def test_cm05_disjoint_validity_no_conflict():
    eng = Engine()
    # k1 valid [t0,t1], k2 valid [t2,t3], t1 < t2 -> no overlap
    conflict = eng.detect_conflict("k1", "k2", "cx", valid_overlap=False)
    assert conflict is None
    assert eng.conflicts == []
    # with overlap the same distinct claims DO record a conflict
    assert eng.detect_conflict("k1", "k2", "cx", valid_overlap=True) is not None


# CM-06 -- local erasure with surviving derivative -> INCOMPLETE -----------
def test_cm06_local_erasure_incomplete():
    eng = Engine()
    o1 = _admit(eng, "c1")
    o2src = _admit(eng, "c2")
    cand = eng.consolidate([o1, o2src], "alice").value      # derivative candidate
    o_deriv = eng.admit(cand, "alice").value                # o_deriv derived from o1
    ds = eng.declare_scope([o1.object_id], [ProvKind.WAS_CONSOLIDATED_FROM], "alice")
    eng.request_delete(ds, "alice")
    # flat "delete the row": erase ONLY the root, leave the derivative
    out = eng.execute_delete(ds, "alice", erased_ids={o1.object_id})
    assert out.value == DeletionResult.INCOMPLETE
    # the derivative is in the closure and still materialized
    assert o_deriv.object_id in eng._closure(ds)
    assert eng.materialized(o_deriv)


# CM-07 -- same content, different governance ------------------------------
def test_cm07_same_content_different_governance():
    # o1 in domain d1 gets deleted; o2 with identical content in d2 does not.
    eng = Engine()
    c1 = eng.encode("SAME", "alice", domain="d1").value
    o1 = eng.admit(c1, "alice", domain="d1").value
    c2 = eng.encode("SAME", "bob", domain="d2").value
    o2 = eng.admit(c2, "bob", domain="d2").value
    assert o1.content_id == o2.content_id          # same content id
    assert o1.object_id != o2.object_id            # distinct identities
    assert o1.authority_domain != o2.authority_domain
    ds = eng.declare_scope([o1.object_id], [], "alice", boundary="d1")
    eng.request_delete(ds, "alice")
    eng.execute_delete(ds, "alice")
    assert eng.object_state(o1) == ObjectState.DELETED
    assert eng.object_state(o2) == ObjectState.ACTIVE   # o2 unaffected


# CM-08 -- actor role without authority ------------------------------------
def test_cm08_role_without_authority():
    auth = Authority()
    auth.deny(actor="op", op_kind="executeDelete")   # OPERATOR role, but DENY
    eng = Engine(authority=auth)
    o = _admit(eng)
    ds = eng.declare_scope([o.object_id], [], "op")
    out = eng.execute_delete(ds, "op")
    assert out.value == DeletionResult.UNVERIFIED
    assert out.record.authority_decision == AuthzDecision.DENY
    assert eng.object_state(o) == ObjectState.ACTIVE   # no state change


# CM-09 -- contextual role change without object change (role-first) --------
def test_cm09_role_change_without_version_change():
    eng = Engine(organization="R")
    o = _admit(eng)
    r1 = eng.assign_role(o, FunctionalRole.PROSPECTIVE, "q1", "alice")
    r2 = eng.assign_role(o, FunctionalRole.EPISODIC, "q2", "alice")
    assert r1.ok and r2.ok
    # one identity, two roles, no new object version
    assert len([x for x in eng.objects if x.object_id == o.object_id]) == 1
    assert {ra.role for ra in eng.roles} == {
        FunctionalRole.PROSPECTIVE, FunctionalRole.EPISODIC}
    # under K the SAME move is forbidden on one identity (discriminator)
    engK = Engine(organization="K")
    oK = _admit(engK)
    assert engK.assign_role(oK, FunctionalRole.PROSPECTIVE, "q1", "alice").ok
    assert not engK.assign_role(oK, FunctionalRole.EPISODIC, "q2", "alice").ok


# CM-10 -- new independent source does not resurrect a deleted identity -----
def test_cm10_independent_reacquisition_not_resurrection():
    eng = Engine()
    o1 = _admit(eng, "FACT")
    ds = eng.declare_scope([o1.object_id], [], "alice")
    eng.request_delete(ds, "alice")
    assert eng.execute_delete(ds, "alice").value == DeletionResult.VERIFIED_WITHIN_SCOPE
    assert eng.object_state(o1) == ObjectState.DELETED
    # later, an independent event yields equivalent content but a NEW identity
    o2 = _admit(eng, "FACT")
    assert o2.content_id == o1.content_id
    assert (o2.object_id, o2.version_id) != (o1.object_id, o1.version_id)
    assert eng.object_state(o1) == ObjectState.DELETED   # o1 stays terminal
    assert eng.object_state(o2) == ObjectState.ACTIVE

"""H5 -- FMO deletion scope detects incomplete deletion a flat store misses.

Prediction (HYPOTHESES.md H5): executeDelete under a declared deletion scope
returns INCOMPLETE exactly when an in-scope derivative/replica survives, whereas
a naive "delete the row" reports success.

These tests exercise the deletion-closure (FMO-INV-14) directly.
"""

from fmo import Engine, DeletionResult, ProvKind, ObjectState


def _admit(eng, content, actor="alice"):
    return eng.admit(eng.encode(content, actor).value, actor).value


def build_derivation_graph():
    """admit o1, o2 ; consolidate -> o3 (derived from o1 and o2)."""
    eng = Engine()
    o1 = _admit(eng, "c1")
    o2 = _admit(eng, "c2")
    cand = eng.consolidate([o1, o2], "alice").value
    o3 = eng.admit(cand, "alice").value
    return eng, o1, o2, o3


def test_closure_includes_derivative():
    eng, o1, o2, o3 = build_derivation_graph()
    ds = eng.declare_scope([o1.object_id], [ProvKind.WAS_CONSOLIDATED_FROM], "alice")
    closure = eng._closure(ds)
    assert o1.object_id in closure
    assert o3.object_id in closure   # consolidated derivative pulled in


def test_flat_delete_the_row_is_incomplete():
    eng, o1, o2, o3 = build_derivation_graph()
    ds = eng.declare_scope([o1.object_id], [ProvKind.WAS_CONSOLIDATED_FROM], "alice")
    eng.request_delete(ds, "alice")
    # naive store erases only the root row
    out = eng.execute_delete(ds, "alice", erased_ids={o1.object_id})
    assert out.value == DeletionResult.INCOMPLETE


def test_full_closure_delete_is_verified():
    eng, o1, o2, o3 = build_derivation_graph()
    ds = eng.declare_scope([o1.object_id], [ProvKind.WAS_CONSOLIDATED_FROM], "alice")
    eng.request_delete(ds, "alice")
    # erase the whole closure (default) -> verified within scope
    out = eng.execute_delete(ds, "alice")
    assert out.value == DeletionResult.VERIFIED_WITHIN_SCOPE
    assert eng.object_state(o1) == ObjectState.DELETED
    assert eng.object_state(o3) == ObjectState.DELETED
    assert not eng.materialized(o1) and not eng.materialized(o3)


def test_verified_iff_no_surviving_in_scope_target():
    """The core H5 biconditional over the constructed graph: VERIFIED iff the
    closure has no surviving in-scope target."""
    eng, o1, o2, o3 = build_derivation_graph()
    ds = eng.declare_scope([o1.object_id], [ProvKind.WAS_CONSOLIDATED_FROM], "alice")
    eng.request_delete(ds, "alice")
    closure = eng._closure(ds)

    # partial erasures: every proper subset that misses a target -> INCOMPLETE
    for miss in closure:
        sub = closure - {miss}
        e2, a1, a2, a3 = build_derivation_graph()
        ds2 = e2.declare_scope([a1.object_id], [ProvKind.WAS_CONSOLIDATED_FROM], "alice")
        e2.request_delete(ds2, "alice")
        # translate ids from the fresh graph: same structure, map by role
        mapping = {o1.object_id: a1.object_id, o2.object_id: a2.object_id,
                   o3.object_id: a3.object_id}
        erased = {mapping[x] for x in sub}
        res = e2.execute_delete(ds2, "alice", erased_ids=erased)
        assert res.value == DeletionResult.INCOMPLETE

    # full erasure -> VERIFIED
    assert eng.execute_delete(ds, "alice").value == DeletionResult.VERIFIED_WITHIN_SCOPE


def test_exception_removes_id_from_closure():
    eng, o1, o2, o3 = build_derivation_graph()
    ds = eng.declare_scope([o1.object_id], [ProvKind.WAS_CONSOLIDATED_FROM],
                           "alice", exceptions=[o3.object_id])
    # the excepted id is no longer a member of the frozen target closure
    assert o3.object_id not in eng._closure(ds)


def test_excepting_a_surviving_derivative_still_blocks_verification():
    """Honest witness: excepting o3 (a derivative of o1) drops it from the
    closure, but o3 survives and its lineage depends on o1 -> o1 stays
    reconstructable, so the scoped postcondition still forbids
    VERIFIED_WITHIN_SCOPE (FMO deletion postcondition, INV-14)."""
    eng, o1, o2, o3 = build_derivation_graph()
    ds = eng.declare_scope([o1.object_id], [ProvKind.WAS_CONSOLIDATED_FROM],
                           "alice", exceptions=[o3.object_id])
    eng.request_delete(ds, "alice")
    out = eng.execute_delete(ds, "alice", erased_ids={o1.object_id})
    assert out.value == DeletionResult.INCOMPLETE


def test_exception_of_independent_replica_verifies():
    """A clean exception: an INDEPENDENT object (no lineage link to the root) is
    excepted; deleting the root alone then verifies within scope."""
    eng = Engine()
    o1 = _admit(eng, "c1")
    ox = _admit(eng, "cx")          # independent, not derived from o1
    ds = eng.declare_scope([o1.object_id, ox.object_id],
                           [ProvKind.WAS_CONSOLIDATED_FROM], "alice",
                           exceptions=[ox.object_id])
    assert ox.object_id not in eng._closure(ds)
    eng.request_delete(ds, "alice")
    out = eng.execute_delete(ds, "alice", erased_ids={o1.object_id})
    assert out.value == DeletionResult.VERIFIED_WITHIN_SCOPE
    assert eng.object_state(ox) == ObjectState.ACTIVE   # excepted, untouched

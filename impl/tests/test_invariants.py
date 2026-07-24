"""Property-style tests: over many random *legal* operation sequences, the FMO
invariants must never break.

No hypothesis dependency: we drive a deterministic PRNG with an explicitly
passed seed (Math.random-style nondeterminism is discouraged by the project).
Each seed produces a reproducible trace; failures print the seed.
"""

import random

import pytest

from fmo import Engine, Authority, AuthzDecision, FunctionalRole
from fmo.checks import check_all


def _snapshot(o):
    return (o.object_id, o.series_id, o.version_id, o.content_id,
            o.admitted_from, o.created_at)


def run_random_trace(seed, steps=60, organization="R"):
    rng = random.Random(seed)
    auth = Authority()
    # occasionally an actor is denied a state change (still legal: the op is
    # recorded REJECTED, no state change) -- exercises INV-05.
    if rng.random() < 0.5:
        auth.deny(actor="mallory")
    eng = Engine(authority=auth, organization=organization)
    snapshots = {}
    live_objects = []
    live_candidates = []

    actors = ["alice", "bob", "mallory"]

    for _ in range(steps):
        actor = rng.choice(actors)
        choice = rng.random()
        if choice < 0.25 or not live_candidates and choice < 0.5:
            out = eng.encode(f"c{rng.randint(0, 5)}", actor)
            if out.ok:
                live_candidates.append(out.value)
        elif choice < 0.5 and live_candidates:
            cand = live_candidates.pop(rng.randrange(len(live_candidates)))
            out = eng.admit(cand, actor)
            if out.ok:
                snapshots[out.value.object_id] = _snapshot(out.value)
                live_objects.append(out.value)
        elif choice < 0.62 and live_objects:
            eng.retrieve(live_objects, actor)
        elif choice < 0.74 and live_objects:
            o = rng.choice(live_objects)
            up = eng.update(o, f"c{rng.randint(0, 5)}", actor)
            if up.ok:
                sup = eng.supersede(o, up.value, actor)
                if sup.ok:
                    snapshots[sup.value.object_id] = _snapshot(sup.value)
                    live_objects.append(sup.value)
        elif choice < 0.82 and len(live_objects) >= 2:
            picks = rng.sample(live_objects, 2)
            eng.consolidate(picks, actor)
        elif choice < 0.88 and live_objects:
            eng.forget(rng.choice(live_objects), actor)
        elif choice < 0.93 and live_objects:
            eng.archive(rng.choice(live_objects), actor)
        elif choice < 0.97 and live_objects:
            eng.restore(rng.choice(live_objects), actor)
        elif live_objects:
            o = rng.choice(live_objects)
            eng.assess_confidence(o.object_id, actor, (0.1, 0.9))

        # invariants must hold after every single step
        check_all(eng, snapshots)

    return eng


@pytest.mark.parametrize("seed", list(range(25)))
@pytest.mark.parametrize("organization", ["K", "R"])
def test_invariants_hold_over_random_legal_traces(seed, organization):
    eng = run_random_trace(seed, steps=60, organization=organization)
    # final sanity: some work actually happened
    assert len(eng.ops) > 0


def test_denied_state_change_records_but_does_not_transition():
    auth = Authority()
    auth.deny(actor="mallory", op_kind="forget")
    eng = Engine(authority=auth)
    c = eng.encode("c1", "alice").value
    o = eng.admit(c, "alice").value
    out = eng.forget(o, "mallory")
    assert not out.ok
    assert out.record.authority_decision == AuthzDecision.DENY
    # no state event, object still ACTIVE, but the rejected op IS retained
    from fmo import ObjectState
    assert eng.object_state(o) == ObjectState.ACTIVE
    assert any(op.operation_kind == "forget" and op.result.value == "REJECTED"
               for op in eng.ops)

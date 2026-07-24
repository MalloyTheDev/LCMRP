"""H1 (executable form) -- Organizations K and R genuinely diverge.

The four "genuinely compete" held-out cases each use ONE unchanged object across
two contexts that demand two different functional classifications:

  CASE-HOLD-001 reminder-after-trigger    : PROSPECTIVE then EPISODIC
  CASE-HOLD-002 signed composite          : PROCEDURAL + EPISODIC
  CASE-HOLD-003 source-sensitive claim    : SEMANTIC + EPISODIC
  CASE-HOLD-004 durable-policy-in-task     : PROCEDURAL + WORKING

Under Organization R (role-first) one identity plays both roles -> identity
count 1. Under Organization K (kind-first) primaryKind is single-valued and
invariant per series, so the two required kinds force TWO identities. The test
asserts the counts differ for every one of the four cases (the discriminator).
"""

import pytest

from fmo import Engine, FunctionalRole

FR = FunctionalRole

CASES = {
    "CASE-HOLD-001-reminder-after-trigger": [FR.PROSPECTIVE, FR.EPISODIC],
    "CASE-HOLD-002-signed-composite": [FR.PROCEDURAL, FR.EPISODIC],
    "CASE-HOLD-003-source-sensitive-claim": [FR.SEMANTIC, FR.EPISODIC],
    "CASE-HOLD-004-durable-policy-in-active-task": [FR.PROCEDURAL, FR.WORKING],
}


def identity_count(required_kinds, organization):
    """Drive the same object through the required contextual classifications and
    count how many distinct object identities the organization is forced to
    mint to represent them."""
    eng = Engine(organization=organization)
    base = eng.admit(eng.encode("content", "alice").value, "alice").value
    identities = {base.object_id}

    for kind in required_kinds:
        out = eng.assign_role(base, kind, f"q:{kind.value}", "alice")
        if out.ok:
            continue
        # organization K refused this kind on the stable identity -> it must
        # carry that kind on a SEPARATE admitted identity.
        extra = eng.admit(eng.encode("content", "alice").value, "alice").value
        identities.add(extra.object_id)
        forced = eng.assign_role(extra, kind, f"q:{kind.value}", "alice")
        # WORKING is not a primaryKind at all under K: it still needs its own
        # identity even though K cannot label it a primaryKind.
        assert forced.ok or kind not in eng._primary_kind.values()
    return len(identities)


@pytest.mark.parametrize("case_id", list(CASES))
def test_k_and_r_diverge_on_each_case(case_id):
    kinds = CASES[case_id]
    r_count = identity_count(kinds, "R")
    k_count = identity_count(kinds, "K")
    assert r_count == 1, f"{case_id}: R should keep one identity, got {r_count}"
    assert k_count >= 2, f"{case_id}: K should multiply identity, got {k_count}"
    assert k_count != r_count, f"{case_id}: no divergence (K={k_count}, R={r_count})"


def test_at_least_one_forced_divergence_overall():
    """H1 confirm condition: >=1 case with a forced K/R divergence."""
    divergences = [
        cid for cid, kinds in CASES.items()
        if identity_count(kinds, "K") != identity_count(kinds, "R")
    ]
    assert len(divergences) >= 1
    # in fact all four diverge
    assert len(divergences) == len(CASES)


def test_r_single_kind_case_does_not_diverge():
    """Control: when both contexts demand the SAME kind, K and R agree (the
    divergence is not an artifact of always multiplying)."""
    same = [FR.SEMANTIC, FR.SEMANTIC]
    assert identity_count(same, "K") == identity_count(same, "R") == 1

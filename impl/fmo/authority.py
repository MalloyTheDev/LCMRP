"""Authority guard (FMO-INV-05).

`authz : A x OpKind x target x PR x AD x T -> AuthzDecision`

State-changing success requires PERMIT. DENY and UNRESOLVED cannot produce a
successful state-changing event. This module does NOT implement a policy
calculus (FMO leaves that open); it is a pluggable decision function with an
explicit rule list so tests can inject DENY / UNRESOLVED for exact
(actor, op_kind) combinations (e.g. CM-08).
"""

from dataclasses import dataclass
from typing import Callable, List

from .enums import AuthzDecision


@dataclass
class AuthorityRule:
    predicate: Callable[..., bool]
    decision: AuthzDecision
    basis: str


class Authority:
    """Default-permit guard with an ordered override rule list (first match
    wins). Default-permit keeps the interpreter's happy path short; the tests
    that matter for FMO-INV-05 install explicit DENY / UNRESOLVED rules."""

    def __init__(self, default: AuthzDecision = AuthzDecision.PERMIT):
        self.default = default
        self.rules: List[AuthorityRule] = []

    def add_rule(self, predicate, decision, basis="explicit-rule"):
        self.rules.append(AuthorityRule(predicate, decision, basis))
        return self

    def deny(self, actor=None, op_kind=None, basis="denied"):
        return self.add_rule(_match(actor, op_kind), AuthzDecision.DENY, basis)

    def unresolved(self, actor=None, op_kind=None, basis="unresolved"):
        return self.add_rule(
            _match(actor, op_kind), AuthzDecision.UNRESOLVED, basis
        )

    def decide(self, actor, op_kind, target, purpose, domain, tx):
        ctx = dict(
            actor=actor,
            op_kind=op_kind,
            target=target,
            purpose=purpose,
            domain=domain,
            tx=tx,
        )
        for rule in self.rules:
            if rule.predicate(ctx):
                return rule.decision, rule.basis
        return self.default, "default"


def _match(actor, op_kind):
    def predicate(ctx):
        if actor is not None and ctx["actor"] != actor:
            return False
        if op_kind is not None and ctx["op_kind"] != op_kind:
            return False
        return True

    return predicate

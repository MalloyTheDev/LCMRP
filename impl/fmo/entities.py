"""Typed, immutable entities for the FMO-0.1 reference interpreter.

Every entity is a frozen dataclass so that, once appended to the log, its
identity-bearing fields cannot be mutated in place (FMO-INV-03). Dynamic
lifecycle state is NOT stored on the entity; it is derived by folding the
append-only log of StateEvent records (see engine.py). This keeps the store
genuinely append-only rather than mutating a status field.

Type separation (FMO-INV-01) is enforced structurally: source events,
candidates, object-versions, provenance assertions, operation records and
deletion scopes are distinct classes with distinct id prefixes.
"""

from dataclasses import dataclass, field
from typing import Optional

from .enums import (
    AuthzDecision,
    CandidateState,
    FunctionalRole,
    ObjectState,
    OperationResult,
    ProvKind,
    TruthStatus,
)


@dataclass(frozen=True)
class Event:
    """Source event (type E)."""

    event_id: str
    source_actor: Optional[str]
    event_time: Optional[int]  # asserted occurrence time; may be unknown (None)
    receipt_time: int  # transaction time of receipt
    content_id: str
    authority_domain: str


@dataclass(frozen=True)
class Candidate:
    """Memory candidate (type N) -- an immutable proposal, not yet admitted."""

    candidate_id: str
    content_id: str
    proposed_series: Optional[str]
    origin_refs: tuple  # ids of source events / objects this derives from
    transform_ref: Optional[str]
    created_by: Optional[str]
    created_at: int
    authority_domain: str


@dataclass(frozen=True)
class ObjectVersion:
    """Exact admitted memory object version (type O).

    identity-bearing fields (immutable, FMO-INV-03): object_id, series_id,
    version_id, content_id, admitted_from, created_at.
    """

    object_id: str
    series_id: str
    version_id: str
    content_id: str
    admitted_from: str  # candidate_id
    created_at: int
    authority_domain: str


@dataclass(frozen=True)
class ProvenanceAssertion:
    """Reified provenance edge (type PT). Carries its own attribution and can
    itself be challenged."""

    prov_id: str
    relation_kind: ProvKind
    subject: str  # id of the derived/target entity
    object: str  # id of the source/origin entity
    asserted_by: Optional[str]
    operation: Optional[str]
    transaction_time: int
    authority_domain: str


@dataclass(frozen=True)
class OperationRecord:
    """Immutable operation-event record (type U). Emitted for EVERY attempt,
    including rejected/failed ones (FMO-INV-16)."""

    operation_id: str
    operation_kind: str
    actor: Optional[str]
    authority_decision: AuthzDecision
    authority_basis: Optional[str]
    inputs: tuple
    outputs: tuple
    purpose: Optional[str]
    transaction_time: int
    result: OperationResult
    failure: Optional[str] = None


@dataclass(frozen=True)
class StateEvent:
    """An immutable record of one lifecycle transition, justified by exactly one
    operation (FMO-INV-04). Object state is derived by folding these."""

    subject_id: str  # candidate_id or (object_id, version_id) key
    from_state: Optional[str]
    to_state: str
    operation_id: str
    transaction_time: int


@dataclass(frozen=True)
class ConfidenceAssessment:
    """Scoped confidence assessment (type CA, FMO-INV-11)."""

    ca_id: str
    target: str
    assessor: str
    method: str
    scale: str
    value: tuple  # (lower, upper) for the numeric unit-interval scale
    context: str
    transaction_time: int


@dataclass(frozen=True)
class UncertaintyRecord:
    """Scoped uncertainty description (type UA, FMO-INV-11)."""

    ua_id: str
    target: str
    assessor_or_method: str
    uncertainty_kind: str
    context: str
    transaction_time: int


@dataclass(frozen=True)
class Assessment:
    """A TruthStatus assessment of a claim (assessment relation)."""

    assessment_id: str
    claim_id: str
    assessor: str
    context: str
    status: TruthStatus
    transaction_time: int


@dataclass(frozen=True)
class ConflictAssessment:
    """Symmetric, irreflexive inter-claim conflict assessment (FMO-INV-12)."""

    conflict_id: str
    claim_a: str
    claim_b: str
    context: str
    valid_overlap: bool
    transaction_time: int


@dataclass(frozen=True)
class RoleAssignment:
    """Contextual playsRole edge (role-first extension)."""

    role_id: str
    object_id: str
    role: FunctionalRole
    query: str
    actor: str
    purpose: str
    transaction_time: int


@dataclass(frozen=True)
class DeletionScope:
    """A deletion-scope declaration (type DS)."""

    ds_id: str
    root_targets: tuple
    boundary: str
    closure_kinds: tuple  # which ProvKind edges the closure follows
    exceptions: tuple
    verification_method: str
    authority_basis: Optional[str]

"""Enumerated state and result domains for FMO-0.1.

Mirrors the domains declared in
docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md (section "Enumerated state and
result domains"). These are plain string enums; no ordering or truth-value
semantics is implied by any label.
"""

from enum import Enum


class CandidateState(str, Enum):
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    ADMITTED = "ADMITTED"


class ObjectState(str, Enum):
    ACTIVE = "ACTIVE"
    SUPPRESSED = "SUPPRESSED"
    ARCHIVED = "ARCHIVED"
    SUPERSEDED = "SUPERSEDED"
    DELETE_PENDING = "DELETE_PENDING"
    DELETED = "DELETED"


class AuthzDecision(str, Enum):
    PERMIT = "PERMIT"
    DENY = "DENY"
    UNRESOLVED = "UNRESOLVED"


class OperationResult(str, Enum):
    SUCCEEDED = "SUCCEEDED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"
    HALTED = "HALTED"
    UNKNOWN = "UNKNOWN"


class TruthStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    CHALLENGED = "CHALLENGED"
    UNRESOLVED = "UNRESOLVED"
    WITHDRAWN = "WITHDRAWN"


class DeletionResult(str, Enum):
    VERIFIED_WITHIN_SCOPE = "VERIFIED_WITHIN_SCOPE"
    INCOMPLETE = "INCOMPLETE"
    FAILED = "FAILED"
    UNVERIFIED = "UNVERIFIED"


class ProvKind(str, Enum):
    """Reified provenance relation kinds (subset used by this interpreter)."""

    WAS_ENCODED_FROM = "WAS_ENCODED_FROM"
    WAS_ADMITTED_FROM = "WAS_ADMITTED_FROM"
    WAS_UPDATED_FROM = "WAS_UPDATED_FROM"
    WAS_CONSOLIDATED_FROM = "WAS_CONSOLIDATED_FROM"
    WAS_SUPERSEDED_BY = "WAS_SUPERSEDED_BY"
    WAS_ATTRIBUTED_TO = "WAS_ATTRIBUTED_TO"
    WAS_RETRIEVED_IN = "WAS_RETRIEVED_IN"


class FunctionalRole(str, Enum):
    EPISODIC = "EPISODIC"
    SEMANTIC = "SEMANTIC"
    PROCEDURAL = "PROCEDURAL"
    PROSPECTIVE = "PROSPECTIVE"
    WORKING = "WORKING"


# The four kinds the stable-kind extension (Organization K) treats as an
# invariant primaryKind of a series. WORKING is deliberately excluded from
# primaryKind per the model (primaryKind : S -> {EPISODIC, SEMANTIC,
# PROCEDURAL, PROSPECTIVE}); under K a WORKING use of a durable object therefore
# still forces a distinct identity.
PRIMARY_KINDS = frozenset(
    {
        FunctionalRole.EPISODIC,
        FunctionalRole.SEMANTIC,
        FunctionalRole.PROCEDURAL,
        FunctionalRole.PROSPECTIVE,
    }
)

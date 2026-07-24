"""FMO-0.1 minimal reference interpreter.

A thin, in-memory, append-only interpreter of the FMO-0.1 operation contracts
(docs/taxonomy/FORMAL_MEMORY_OBJECT_MODEL_v0.1.md). It exists to *witness*
invariants and countermodels, not to be a product: it selects no database,
model, embedding, index, or schema.

[AI-assisted]. Evidence: passing tests support H3/H5 *structurally* (this
interpreter can host the distinctions and non-entailments); they are not
empirical validity and do not machine-check the FMO core (that is the Alloy/TLA+
work in H3).
"""

from .authority import Authority
from .engine import Engine, OpOutcome
from .enums import (
    AuthzDecision,
    CandidateState,
    DeletionResult,
    FunctionalRole,
    ObjectState,
    OperationResult,
    ProvKind,
    TruthStatus,
)

__all__ = [
    "Engine",
    "OpOutcome",
    "Authority",
    "AuthzDecision",
    "CandidateState",
    "DeletionResult",
    "FunctionalRole",
    "ObjectState",
    "OperationResult",
    "ProvKind",
    "TruthStatus",
]

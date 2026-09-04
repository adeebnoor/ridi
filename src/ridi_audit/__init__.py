"""RIDI: allocation-identity auditing for capacity-limited AI."""

from .api import AllocationReport, AuditReport, audit, compare_allocations
from .core import (
    audit_scores,
    changed_slots,
    deterministic_topk,
    margin_certificate,
    ridi,
)
from .selector import (
    Frontier,
    deterministic_percentiles,
    identity_utility_frontier,
    select_identity_control,
)

__all__ = [
    "AllocationReport",
    "AuditReport",
    "Frontier",
    "audit",
    "audit_scores",
    "changed_slots",
    "compare_allocations",
    "deterministic_percentiles",
    "deterministic_topk",
    "identity_utility_frontier",
    "margin_certificate",
    "ridi",
    "select_identity_control",
]

__version__ = "1.1.0"

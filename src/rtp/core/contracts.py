from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

Json = Dict[str, Any]

@dataclass(frozen=True)
class DecisionRequest:
    facts: Json
    features: Json = field(default_factory=dict)
    metadata: Json = field(default_factory=dict)  # tenant_id, trace_id, ts, policy_version, etc.

@dataclass(frozen=True)
class DecisionResult:
    action: str
    score: Optional[float] = None
    reasons: list[str] = field(default_factory=list)  # stable reason codes
    constraints_applied: list[str] = field(default_factory=list)
    payload: Json = field(default_factory=dict)  # explainability, debug, chosen candidate, etc.

@dataclass(frozen=True)
class Policy:
    rules: Json = field(default_factory=dict)
    limits: Json = field(default_factory=dict)
    version: str = "v0"

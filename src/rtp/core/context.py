from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional
from .contracts import DecisionRequest, Policy

@dataclass
class DecisionContext:
    request: DecisionRequest
    policy: Policy
    runtime: Dict[str, Any]  # logger, metrics, tracer, clock, etc.

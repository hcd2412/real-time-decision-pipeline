from __future__ import annotations

from abc import ABC, abstractmethod

from rtp.core.context import DecisionContext
from rtp.core.contracts import DecisionResult


class DecidePattern(ABC):
    """
    Decide patterns choose an action, using the request + policy + runtime context.

    They may use heuristics, rules, optimization, or ranking.
    They MUST NOT weaken constraints (constraints are applied in the constrain stage).
    """

    name: str  # unique identifier, e.g. "decide.threshold_action"

    @abstractmethod
    def decide(self, ctx: DecisionContext) -> DecisionResult:
        """Return the decision result."""
        raise NotImplementedError

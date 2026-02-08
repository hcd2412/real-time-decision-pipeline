from abc import ABC, abstractmethod
from typing import Any


class Decider(ABC):
    """
    Deciders choose actions *within* the constrained action space.

    They may use heuristics, rules, optimization, or ranking.
    But they MUST NOT expand constraints.
    """

    @abstractmethod
    def decide(self, constrained_space: Any) -> Any:
        """
        Given a constrained action space (bounds/options),
        return a concrete decision (one or more actions).
        """
        raise NotImplementedError


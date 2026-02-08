from abc import ABC, abstractmethod
from typing import Any


class Constraint(ABC):
    """
    Constraints define what actions are allowed
    in the current context.

    They do NOT decide actions.
    They restrict the decision space.
    """

    @abstractmethod
    def apply(self, evaluated_state: Any) -> Any:
        """
        Given evaluated system state, return
        a constrained action space or bounds.
        """
        raise NotImplementedError


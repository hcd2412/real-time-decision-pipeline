from abc import ABC, abstractmethod
from typing import Any


class Evaluator(ABC):
    """
    Evaluators transform raw signals into
    interpreted system state.

    This is where forecasting, scoring,
    and estimation live — but not decisions.
    """

    @abstractmethod
    def evaluate(self, raw_input: Any) -> Any:
        """
        Convert raw inputs into evaluated state
        (e.g. demand estimates, risk scores).
        """
        raise NotImplementedError

from abc import ABC, abstractmethod
from typing import Any


class Observer(ABC):
    """
    Observers record and analyze what happened
    after a decision was exposed and acted upon.

    This is where feedback, metrics, and audits live.
    """

    @abstractmethod
    def observe(self, decision: Any, outcome: Any) -> None:
        """
        Record decision + outcome for monitoring,
        auditability, and learning.
        """
        raise NotImplementedError


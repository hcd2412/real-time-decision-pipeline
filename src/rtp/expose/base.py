from abc import ABC, abstractmethod
from typing import Any


class Exposer(ABC):
    """
    Exposers publish decisions to the outside world.

    Examples:
    - HTTP API response
    - message bus publish
    - writing to a decision log store
    """

    @abstractmethod
    def expose(self, decision: Any) -> Any:
        """
        Publish/serialize the decision.
        Returns an external representation (e.g. response payload).
        """
        raise NotImplementedError


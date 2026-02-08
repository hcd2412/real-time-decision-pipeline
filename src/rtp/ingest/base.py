from abc import ABC, abstractmethod
from typing import Any


class IngestSource(ABC):
    """
    Base class for all ingestion sources.

    Ingest is responsible only for capturing
    what the world says — not interpreting it.
    """

    @abstractmethod
    def read(self) -> Any:
        """Return raw input data with minimal transformation."""
        raise NotImplementedError

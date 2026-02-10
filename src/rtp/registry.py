from __future__ import annotations
from typing import Callable, Dict, Type, TypeVar, Any

T = TypeVar("T")

class Registry:
    def __init__(self) -> None:
        self._items: Dict[str, Any] = {}

    def register(self, name: str, obj: Any) -> None:
        if name in self._items:
            raise ValueError(f"Duplicate registration: {name}")
        self._items[name] = obj

    def get(self, name: str) -> Any:
        try:
            return self._items[name]
        except KeyError as e:
            raise KeyError(f"Unknown registered item: {name}") from e

    def items(self) -> Dict[str, Any]:
        return dict(self._items)

from __future__ import annotations
from dataclasses import dataclass
from typing import List

from rtp.core.context import DecisionContext
from rtp.core.contracts import DecisionResult
from rtp.registry import Registry


@dataclass
class EngineConfig:
    ingest: List[str]
    evaluate: List[str]
    constrain: List[str]
    decide: str
    observe: List[str] | None = None


class DecisionEngine:
    def __init__(self, registry: Registry, config: EngineConfig) -> None:
        self.registry = registry
        self.config = config
        if self.config.observe is None:
            self.config.observe = []

    def run(self, ctx: DecisionContext) -> DecisionResult:
        # INGEST
        for name in self.config.ingest:
            self.registry.get(name).ingest(ctx)

        # EVALUATE
        for name in self.config.evaluate:
            evidence = self.registry.get(name).evaluate(ctx)
            ctx.runtime.setdefault("evidence", {})[name] = evidence

        # DECIDE
        result: DecisionResult = self.registry.get(self.config.decide).decide(ctx)

        # CONSTRAIN (post-decision)
        for name in self.config.constrain:
            result = self.registry.get(name).constrain(ctx, result)

        # OBSERVE
        for name in self.config.observe:
            self.registry.get(name).observe(ctx, result)

        return result

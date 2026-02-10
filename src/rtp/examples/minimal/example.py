from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from rtp.ingest.base import IngestSource
from rtp.evaluate.base import Evaluator
from rtp.constrain.base import Constraint
from rtp.expose.base import Exposer
from rtp.observe.base import Observer


# -----------------------------
# Domain-neutral action + state
# -----------------------------
@dataclass(frozen=True)
class TransferAction:
    from_node: str
    to_node: str
    units: int


@dataclass(frozen=True)
class WorldState:
    # current measured inventory per node
    inventory: Dict[str, int]


@dataclass(frozen=True)
class EvaluatedState:
    # excess = inventory - baseline
    excess: Dict[str, float]


@dataclass(frozen=True)
class ConstrainedSpace:
    donors: List[str]
    receivers: List[str]
    max_units_per_move: int


# -----------------------------
# Ingest → Evaluate → Constrain → Decide → Expose → Observe
# -----------------------------
class DictIngest(IngestSource):
    def __init__(self, payload: Dict[str, Any]) -> None:
        self.payload = payload

    def read(self) -> WorldState:
        inv = self.payload["inventory"]
        # normalize to str->int
        inventory = {str(k): int(v) for k, v in inv.items()}
        return WorldState(inventory=inventory)


class MeanBaselineEvaluator(Evaluator):
    def evaluate(self, raw_input: WorldState) -> EvaluatedState:
        values = list(raw_input.inventory.values())
        baseline = sum(values) / max(len(values), 1)
        excess = {k: v - baseline for k, v in raw_input.inventory.items()}
        return EvaluatedState(excess=excess)


class BasicTransferConstraint(Constraint):
    def __init__(self, max_units_per_move: int = 5) -> None:
        self.max_units_per_move = int(max_units_per_move)

    def apply(self, evaluated_state: EvaluatedState) -> ConstrainedSpace:
        donors = [k for k, x in evaluated_state.excess.items() if x > 0]
        receivers = [k for k, x in evaluated_state.excess.items() if x < 0]
        return ConstrainedSpace(
            donors=donors,
            receivers=receivers,
            max_units_per_move=self.max_units_per_move,
        )


class GreedyDecider:
    def decide(self, constrained_space: ConstrainedSpace) -> List[TransferAction]:
        actions: List[TransferAction] = []
        if not constrained_space.donors or not constrained_space.receivers:
            return actions

        # minimal: one move from first donor to first receiver
        actions.append(
            TransferAction(
                from_node=constrained_space.donors[0],
                to_node=constrained_space.receivers[0],
                units=constrained_space.max_units_per_move,
            )
        )
        return actions


class DictExposer(Exposer):
    def expose(self, decision: List[TransferAction]) -> Dict[str, Any]:
        return {
            "actions": [
                {"from": a.from_node, "to": a.to_node, "units": a.units} for a in decision
            ]
        }


class PrintObserver(Observer):
    def observe(self, decision: Any, outcome: Any) -> None:
        # For now: just demonstrate the contract
        print("DECISION:", decision)
        print("OUTCOME:", outcome)


def main() -> None:
    payload = {"inventory": {"A": 2, "B": 8, "C": 4}}

    pipeline = DecisionPipeline(
        ingest=DictIngest(payload),
        evaluate=MeanBaselineEvaluator(),
        constrain=BasicTransferConstraint(max_units_per_move=3),
        decide=GreedyDecider(),
        expose=DictExposer(),
        observe=PrintObserver(),
    )

    result = pipeline.run(outcome=None)
    print(result)


# -----------------------------
# New: Engine + named pattern demo
# -----------------------------
def engine_demo() -> None:
    from rtp.core.contracts import DecisionRequest, Policy
    from rtp.core.context import DecisionContext
    from rtp.registry import Registry
    from rtp.engine import DecisionEngine, EngineConfig
    from rtp.patterns.decide.threshold_action import ThresholdAction

    registry = Registry()
    registry.register("decide.threshold_action", ThresholdAction(threshold=0.75))

    engine = DecisionEngine(
        registry=registry,
        config=EngineConfig(
            ingest=[],
            evaluate=[],
            constrain=[],
            decide="decide.threshold_action",
            observe=[],
        ),
    )

    req = DecisionRequest(
        facts={"user_id": "u1"},
        features={"score": 0.8},
        metadata={"trace_id": "t1", "policy_version": "v0"},
    )
    ctx = DecisionContext(request=req, policy=Policy(version="v0"), runtime={})

    result = engine.run(ctx)
    print("ENGINE RESULT:", result)


# if __name__ == "__main__":
#     engine_demo()

from typing import Dict, Any

from rtp.pipeline.pipeline import DecisionPipeline
from rtp.examples.minimal.example import (
    DictIngest,
    MeanBaselineEvaluator,
    BasicTransferConstraint,
    GreedyDecider,
    DictExposer,
    PrintObserver,
)


def build_transfer_pipeline(
    *,
    inventory: Dict[str, int],
    max_units_per_move: int = 3,
) -> DecisionPipeline:
    """
    Factory for a simple surplus–deficit transfer decision pipeline.

    This keeps API, batch, and tests consistent.
    """
    payload: Dict[str, Any] = {"inventory": inventory}

    return DecisionPipeline(
        ingest=DictIngest(payload),
        evaluate=MeanBaselineEvaluator(),
        constrain=BasicTransferConstraint(max_units_per_move=max_units_per_move),
        decide=GreedyDecider(),
        expose=DictExposer(),
        observe=PrintObserver(),
    )

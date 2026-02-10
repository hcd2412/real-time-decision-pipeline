from __future__ import annotations
from dataclasses import dataclass

from rtp.core.context import DecisionContext
from rtp.core.contracts import DecisionResult
from rtp.decide.base import DecidePattern


@dataclass
class ThresholdAction(DecidePattern):
    """
    Decide APPROVE / REJECT based on a numeric score threshold.
    """

    name: str = "decide.threshold_action"

    threshold: float = 0.8
    approve_action: str = "APPROVE"
    reject_action: str = "REJECT"

    def decide(self, ctx: DecisionContext) -> DecisionResult:
        score = float(ctx.request.features.get("score", 0.0))

        if score >= self.threshold:
            return DecisionResult(
                action=self.approve_action,
                score=score,
                reasons=["SCORE_GE_THRESHOLD"],
            )

        return DecisionResult(
            action=self.reject_action,
            score=score,
            reasons=["SCORE_LT_THRESHOLD"],
        )

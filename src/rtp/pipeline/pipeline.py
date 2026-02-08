from typing import Any, Iterable

from rtp.ingest.base import IngestSource
from rtp.evaluate.base import Evaluator
from rtp.constrain.base import Constraint
from rtp.decide.base import Decider
from rtp.expose.base import Exposer
from rtp.observe.base import Observer


class DecisionPipeline:
    """
    Orchestrates the full decision flow:

    ingest → evaluate → constrain → decide → expose → observe
    """

    def __init__(
        self,
        *,
        source: IngestSource,
        evaluator: Evaluator,
        constraints: Iterable[Constraint],
        decider: Decider,
        exposer: Exposer,
        observer: Observer,
    ):
        self.source = source
        self.evaluator = evaluator
        self.constraints = list(constraints)
        self.decider = decider
        self.exposer = exposer
        self.observer = observer

    def run(self) -> Any:
        raw = self.source.read()
        evaluated = self.evaluator.evaluate(raw)

        constrained = evaluated
        for constraint in self.constraints:
            constrained = constraint.apply(constrained)

        decision = self.decider.decide(constrained)
        exposed = self.exposer.expose(decision)

        # Outcome may be async or external; placeholder for now
        self.observer.observe(decision=decision, outcome=None)

        return exposed


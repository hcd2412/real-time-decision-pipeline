from __future__ import annotations

from typing import Any, Iterable, Optional, Union

from rtp.ingest.base import IngestSource
from rtp.evaluate.base import Evaluator
from rtp.constrain.base import Constraint
from rtp.decide.base import Decider
from rtp.expose.base import Exposer
from rtp.observe.base import Observer


ConstraintOrMany = Union[Constraint, Iterable[Constraint]]


class DecisionPipeline:
    """
    Orchestrates the full decision flow:

    ingest → evaluate → constrain → decide → expose → observe

    Supports ergonomic stage naming (ingest/evaluate/constrain/decide/expose/observe),
    while keeping backward-compatible aliases:
      - ingest  OR source
      - evaluate OR evaluator
      - constrain OR constraints
      - decide OR decider
      - expose OR exposer
      - observe OR observer
    """

    def __init__(
        self,
        *,
        # Ingest
        ingest: Optional[IngestSource] = None,
        source: Optional[IngestSource] = None,
        # Evaluate
        evaluate: Optional[Evaluator] = None,
        evaluator: Optional[Evaluator] = None,
        # Constrain (accept single or many)
        constrain: Optional[ConstraintOrMany] = None,
        constraints: Optional[ConstraintOrMany] = None,
        # Decide
        decide: Optional[Decider] = None,
        decider: Optional[Decider] = None,
        # Expose
        expose: Optional[Exposer] = None,
        exposer: Optional[Exposer] = None,
        # Observe
        observe: Optional[Observer] = None,
        observer: Optional[Observer] = None,
    ):
        # --------
        # Ingest
        # --------
        if ingest is None and source is None:
            raise ValueError("Provide either ingest=... or source=...")
        self.source: IngestSource = ingest if ingest is not None else source  # type: ignore[assignment]

        # --------
        # Evaluate
        # --------
        if evaluate is None and evaluator is None:
            raise ValueError("Provide either evaluate=... or evaluator=...")
        self.evaluator: Evaluator = evaluate if evaluate is not None else evaluator  # type: ignore[assignment]

        # --------
        # Constrain
        # --------
        chosen = constrain if constrain is not None else constraints
        if chosen is None:
            self.constraints: list[Constraint] = []
        elif isinstance(chosen, Constraint):
            self.constraints = [chosen]
        else:
            self.constraints = list(chosen)

        # --------
        # Decide
        # --------
        if decide is None and decider is None:
            raise ValueError("Provide either decide=... or decider=...")
        self.decider: Decider = decide if decide is not None else decider  # type: ignore[assignment]

        # --------
        # Expose
        # --------
        if expose is None and exposer is None:
            raise ValueError("Provide either expose=... or exposer=...")
        self.exposer: Exposer = expose if expose is not None else exposer  # type: ignore[assignment]

        # --------
        # Observe
        # --------
        if observe is None and observer is None:
            raise ValueError("Provide either observe=... or observer=...")
        self.observer: Observer = observe if observe is not None else observer  # type: ignore[assignment]

    def run(self, *, outcome: Any = None) -> Any:
        raw = self.source.read()
        evaluated = self.evaluator.evaluate(raw)

        constrained = evaluated
        for constraint in self.constraints:
            constrained = constraint.apply(constrained)

        decision = self.decider.decide(constrained)
        exposed = self.exposer.expose(decision)

        # Outcome may be async/external; caller can pass it when available.
        self.observer.observe(decision, outcome)

        return exposed

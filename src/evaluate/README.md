# Evaluate

The evaluate stage transforms raw inputs into **interpretable signals**
that can be used by downstream decision logic.

This stage answers questions like:
- What does the data *mean*?
- Is the situation normal, degraded, or critical?
- How confident are we in what we see?

Typical responsibilities:
- feature computation
- aggregation and summarization
- scoring, classification, or forecasting
- uncertainty estimation

Design principles:
- evaluation produces **signals, not actions**
- evaluation may use ML, statistics, or rules
- evaluation results are **versioned and observable**
- evaluation can be recomputed or audited

This stage answers only one question:
**“How should we interpret what we know?”**


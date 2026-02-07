# Expose

The expose stage is responsible for **making decisions visible and usable**
by external systems and humans.

This typically includes:
- APIs (HTTP / gRPC)
- message queues or streams
- dashboards or operator UIs
- audit logs

Key idea:
**Exposure is not execution.**

Design principles:
- decisions are exposed with **context**
- decisions are **versioned**
- decisions are **reviewable**
- decisions can be **replayed or simulated**

The expose stage does NOT:
- make decisions
- change constraints
- hide uncertainty

This stage answers only one question:
**“How do others see and interact with the decision?”**


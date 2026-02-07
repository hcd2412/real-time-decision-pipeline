# Decide

The decide stage selects **one or more actions** from the set of
allowed actions defined by upstream constraints.

This stage may use:
- heuristics
- rules
- optimization
- ranking or scoring
- human input

Key idea:
**Decision logic operates only within constraints.**

Design principles:
- decisions are **bounded**, not free-form
- decisions are **explainable**
- decisions can be **overridden by humans**
- optimality is secondary to safety and stability

The decide stage does NOT:
- ingest raw data
- infer meaning from signals
- relax constraints

This stage answers only one question:
**“Given what is allowed, what should we do now?”**


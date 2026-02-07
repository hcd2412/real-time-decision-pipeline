# Constrain

The constrain stage defines **what decisions are allowed** before any
optimization or selection occurs.

This stage encodes:
- physical limits
- safety rules
- policy requirements
- cost ceilings
- fairness or ethical boundaries

Constraints may come from:
- regulation
- operations teams
- contracts or SLAs
- risk management

Design principles:
- constraints are **explicit and reviewable**
- constraints are **separate from decision logic**
- violating a constraint is a system error, not a trade-off
- constraints may evolve independently of models

This stage answers only one question:
**“What actions are forbidden or limited?”**


# Ingest

The ingest stage is responsible for bringing **raw signals from the real world**
into the decision system in a controlled, observable way.

Examples of inputs:
- events (rides, transactions, sensor readings)
- state snapshots (inventory, capacity, availability)
- external signals (weather, prices, policy changes)

Design principles:
- ingestion is **loss-aware** (we know what we missed)
- ingestion is **time-aware** (late data is handled explicitly)
- ingestion does **no decision logic**
- ingestion does **no optimization**

This stage answers only one question:
**“What do we know right now?”**


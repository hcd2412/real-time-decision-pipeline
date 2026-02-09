from __future__ import annotations

from typing import Dict, List

from fastapi import APIRouter
from pydantic import BaseModel, Field, ConfigDict

from rtp.pipeline.factory import build_transfer_pipeline

router = APIRouter()


class DecideRequest(BaseModel):
    inventory: Dict[str, int] = Field(..., description="Current inventory per node/station")
    max_units_per_move: int = Field(3, ge=1, le=100, description="Upper bound per transfer action")


class TransferActionOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_node: str = Field(..., alias="from")
    to_node: str = Field(..., alias="to")
    units: int


class DecideResponse(BaseModel):
    actions: List[TransferActionOut]


@router.post(
    "/decide",
    response_model=DecideResponse,
    summary="Make a constrained transfer decision",
    description="Runs ingest → evaluate → constrain → decide → expose (observe is internal).",
)
def decide(req: DecideRequest) -> DecideResponse:
    pipeline = build_transfer_pipeline(
        inventory=req.inventory,
        max_units_per_move=req.max_units_per_move,
    )

    result = pipeline.run()
    return DecideResponse.model_validate(result)

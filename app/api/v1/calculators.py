from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import success_response
from app.database.session import get_db
from app.schemas.calculator import (
    CalculatorResultRead,
    DeltaVRequest,
    MassRatioRequest,
    PayloadFractionRequest,
    TwrRequest,
)
from app.services.calculator_service import CalculatorService


router = APIRouter()


@router.post("/delta-v")
def calculate_delta_v(payload: DeltaVRequest, db: Session = Depends(get_db)) -> dict:
    result = CalculatorService.calculate_delta_v(payload)
    stored = CalculatorService.store_result_if_requested(db, payload, result)
    if stored is not None:
        result["stored_result_id"] = stored.id
    return success_response(message="Delta-V calculated successfully", data=result)


@router.post("/twr")
def calculate_twr(payload: TwrRequest, db: Session = Depends(get_db)) -> dict:
    result = CalculatorService.calculate_twr(payload)
    stored = CalculatorService.store_result_if_requested(db, payload, result)
    if stored is not None:
        result["stored_result_id"] = stored.id
    return success_response(message="TWR calculated successfully", data=result)


@router.post("/payload-fraction")
def calculate_payload_fraction(payload: PayloadFractionRequest, db: Session = Depends(get_db)) -> dict:
    result = CalculatorService.calculate_payload_fraction(payload)
    stored = CalculatorService.store_result_if_requested(db, payload, result)
    if stored is not None:
        result["stored_result_id"] = stored.id
    return success_response(message="Payload fraction calculated successfully", data=result)


@router.post("/mass-ratio")
def calculate_mass_ratio(payload: MassRatioRequest, db: Session = Depends(get_db)) -> dict:
    result = CalculatorService.calculate_mass_ratio(payload)
    stored = CalculatorService.store_result_if_requested(db, payload, result)
    if stored is not None:
        result["stored_result_id"] = stored.id
    return success_response(message="Mass ratio calculated successfully", data=result)


@router.get("/results")
def list_calculator_results(
    mission_id: str | None = None,
    rocket_id: str | None = None,
    db: Session = Depends(get_db),
) -> dict:
    results = CalculatorService.list_results(db, mission_id=mission_id, rocket_id=rocket_id)
    return success_response(
        message="Calculator results retrieved successfully",
        data=[CalculatorResultRead.model_validate(result).model_dump(mode="json") for result in results],
    )

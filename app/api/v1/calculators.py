from fastapi import APIRouter

from app.core.responses import success_response
from app.schemas.calculator import (
    DeltaVRequest,
    MassRatioRequest,
    PayloadFractionRequest,
    TwrRequest,
)
from app.services.calculator_service import CalculatorService


router = APIRouter()


@router.post("/delta-v")
def calculate_delta_v(payload: DeltaVRequest) -> dict:
    result = CalculatorService.calculate_delta_v(payload)
    return success_response(message="Delta-V calculated successfully", data=result)


@router.post("/twr")
def calculate_twr(payload: TwrRequest) -> dict:
    result = CalculatorService.calculate_twr(payload)
    return success_response(message="TWR calculated successfully", data=result)


@router.post("/payload-fraction")
def calculate_payload_fraction(payload: PayloadFractionRequest) -> dict:
    result = CalculatorService.calculate_payload_fraction(payload)
    return success_response(message="Payload fraction calculated successfully", data=result)


@router.post("/mass-ratio")
def calculate_mass_ratio(payload: MassRatioRequest) -> dict:
    result = CalculatorService.calculate_mass_ratio(payload)
    return success_response(message="Mass ratio calculated successfully", data=result)

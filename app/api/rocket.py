from fastapi import APIRouter

from app.core.responses import success_response
from app.schemas.rocket import RocketInput
from app.services.calculator_service import CalculatorService
from app.schemas.calculator import DeltaVRequest, TwrRequest


router = APIRouter()


@router.post("/calculate")
def calculate(data: RocketInput) -> dict:
    delta_v = CalculatorService.calculate_delta_v(
        DeltaVRequest(isp=data.isp, wet_mass=data.wet_mass, dry_mass=data.dry_mass)
    )
    twr = CalculatorService.calculate_twr(
        TwrRequest(thrust=data.thrust, mass=data.wet_mass)
    )

    return success_response(
        message="Rocket calculation completed successfully",
        data={
            "delta_v": delta_v["result"],
            "twr": twr["result"],
        },
    )

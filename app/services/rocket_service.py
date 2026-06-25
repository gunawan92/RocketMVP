from app.schemas.calculator import DeltaVRequest, TwrRequest
from app.services.calculator_service import CalculatorService


class RocketService:
    @staticmethod
    def calculate_delta_v(wet_mass, dry_mass, isp):
        result = CalculatorService.calculate_delta_v(
            DeltaVRequest(isp=isp, wet_mass=wet_mass, dry_mass=dry_mass)
        )
        return result["result"]["delta_v"]

    @staticmethod
    def calculate_twr(thrust, wet_mass):
        result = CalculatorService.calculate_twr(TwrRequest(thrust=thrust, mass=wet_mass))
        return result["result"]["twr"]

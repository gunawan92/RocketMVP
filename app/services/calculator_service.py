import math

from app.core.constants import G0
from app.core.exceptions import BusinessRuleError
from app.schemas.calculator import (
    DeltaVRequest,
    MassRatioRequest,
    PayloadFractionRequest,
    TwrRequest,
)


class CalculatorService:
    @staticmethod
    def calculate_delta_v(payload: DeltaVRequest) -> dict:
        if payload.wet_mass <= payload.dry_mass:
            raise BusinessRuleError(
                "Wet mass must be greater than dry mass",
                details=[
                    {
                        "field": "wet_mass",
                        "message": "Wet mass must be greater than dry mass",
                    }
                ],
            )

        delta_v = payload.isp * G0 * math.log(payload.wet_mass / payload.dry_mass)
        return {
            "calculator_type": "delta_v",
            "input": {
                "isp": payload.isp,
                "wet_mass": payload.wet_mass,
                "dry_mass": payload.dry_mass,
                "g0": G0,
            },
            "result": {
                "delta_v": round(delta_v, 2),
                "unit": "m/s",
            },
            "interpretation": "Estimated ideal velocity change without drag, gravity loss, or steering loss.",
        }

    @staticmethod
    def calculate_twr(payload: TwrRequest) -> dict:
        twr = payload.thrust / (payload.mass * G0)
        return {
            "calculator_type": "twr",
            "input": {
                "thrust": payload.thrust,
                "mass": payload.mass,
                "g0": G0,
            },
            "result": {
                "twr": round(twr, 2),
                "unit": "dimensionless",
            },
            "interpretation": CalculatorService._twr_interpretation(twr),
        }

    @staticmethod
    def calculate_payload_fraction(payload: PayloadFractionRequest) -> dict:
        if payload.payload_mass > payload.total_mass:
            raise BusinessRuleError(
                "Payload mass cannot be greater than total mass",
                details=[
                    {
                        "field": "payload_mass",
                        "message": "Payload mass cannot be greater than total mass",
                    }
                ],
            )

        ratio = payload.payload_mass / payload.total_mass
        return {
            "calculator_type": "payload_fraction",
            "input": {
                "payload_mass": payload.payload_mass,
                "total_mass": payload.total_mass,
            },
            "result": {
                "payload_fraction": round(ratio, 4),
                "payload_fraction_percentage": round(ratio * 100, 2),
                "unit": "percent",
            },
            "interpretation": f"Payload represents {round(ratio * 100, 2)}% of total rocket mass.",
        }

    @staticmethod
    def calculate_mass_ratio(payload: MassRatioRequest) -> dict:
        if payload.wet_mass <= payload.dry_mass:
            raise BusinessRuleError(
                "Wet mass must be greater than dry mass",
                details=[
                    {
                        "field": "wet_mass",
                        "message": "Wet mass must be greater than dry mass",
                    }
                ],
            )

        ratio = payload.wet_mass / payload.dry_mass
        return {
            "calculator_type": "mass_ratio",
            "input": {
                "wet_mass": payload.wet_mass,
                "dry_mass": payload.dry_mass,
            },
            "result": {
                "mass_ratio": round(ratio, 2),
                "unit": "dimensionless",
            },
            "interpretation": f"Wet mass is {round(ratio, 2)} times the dry mass.",
        }

    @staticmethod
    def _twr_interpretation(twr: float) -> str:
        if twr < 1:
            return "Rocket cannot lift off. TWR is below 1."
        if twr == 1:
            return "Rocket is in hover condition. TWR equals 1."
        return "Rocket can ascend. TWR is greater than 1."

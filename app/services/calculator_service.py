import math

from app.core.constants import G0
from app.core.exceptions import BusinessRuleError
from app.core.ids import normalize_uuid
from app.models.calculator_result import CalculatorResult
from app.models.mission import Mission
from app.models.rocket import Rocket
from app.schemas.calculator import (
    CalculatorStoreMixin,
    DeltaVRequest,
    MassRatioRequest,
    PayloadFractionRequest,
    TwrRequest,
)
from sqlalchemy import select
from sqlalchemy.orm import Session


class CalculatorService:
    @staticmethod
    def store_result_if_requested(db: Session, payload: CalculatorStoreMixin, calculation: dict) -> CalculatorResult | None:
        if not payload.store_result:
            return None

        mission_id = normalize_uuid(payload.mission_id, "mission_id") if payload.mission_id else None
        rocket_id = normalize_uuid(payload.rocket_id, "rocket_id") if payload.rocket_id else None

        if mission_id is not None and db.get(Mission, mission_id) is None:
            raise BusinessRuleError(
                "Mission does not exist",
                details=[{"field": "mission_id", "message": "Mission must exist before storing calculator result"}],
            )

        if rocket_id is not None:
            rocket = db.get(Rocket, rocket_id)
            if rocket is None:
                raise BusinessRuleError(
                    "Rocket configuration does not exist",
                    details=[{"field": "rocket_id", "message": "Rocket must exist before storing calculator result"}],
                )
            if mission_id is not None and rocket.mission_id != mission_id:
                raise BusinessRuleError(
                    "Rocket does not belong to mission",
                    details=[{"field": "rocket_id", "message": "Rocket must belong to the requested mission"}],
                )

        result = CalculatorResult(
            mission_id=mission_id,
            rocket_id=rocket_id,
            calculator_type=calculation["calculator_type"].upper(),
            input_data=calculation["input"],
            result_data={
                "result": calculation["result"],
                "interpretation": calculation["interpretation"],
            },
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return result

    @staticmethod
    def list_results(db: Session, mission_id: str | None = None, rocket_id: str | None = None) -> list[CalculatorResult]:
        statement = select(CalculatorResult).order_by(CalculatorResult.created_at.desc())

        if mission_id is not None:
            mission_id = normalize_uuid(mission_id, "mission_id")
            statement = statement.where(CalculatorResult.mission_id == mission_id)
        if rocket_id is not None:
            rocket_id = normalize_uuid(rocket_id, "rocket_id")
            statement = statement.where(CalculatorResult.rocket_id == rocket_id)

        return list(db.scalars(statement))

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

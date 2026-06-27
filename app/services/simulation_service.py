from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import BusinessRuleError, ResourceNotFoundError
from app.core.ids import normalize_uuid
from app.models.mission import Mission
from app.models.rocket import Rocket
from app.models.simulation_result import SimulationResult
from app.schemas.simulation import SimulationCompareRequest, SimulationRunRequest
from app.simulation.rocketpy_adapter import RocketPyAdapter


class SimulationService:
    @staticmethod
    def run_simulation(db: Session, payload: SimulationRunRequest) -> SimulationResult | dict:
        mission_id = normalize_uuid(payload.mission_id, "mission_id")
        rocket_id = normalize_uuid(payload.rocket_id, "rocket_id")
        SimulationService._ensure_mission_exists(db, mission_id)
        rocket = SimulationService._get_rocket_with_engine(db, rocket_id)

        if rocket.mission_id != mission_id:
            raise BusinessRuleError(
                "Rocket does not belong to mission",
                details=[{"field": "rocket_id", "message": "Rocket must belong to the requested mission"}],
            )
        if rocket.engine is None:
            raise BusinessRuleError(
                "Rocket must have engine data before simulation",
                details=[{"field": "engine_id", "message": "Rocket engine is required"}],
            )

        simulation_payload = RocketPyAdapter.run_basic_simulation(
            rocket=rocket,
            environment_input=payload.environment,
            include_time_series=payload.options.include_time_series,
        )

        if not payload.options.store_result:
            return simulation_payload

        result = SimulationResult(
            mission_id=mission_id,
            rocket_id=rocket_id,
            status="SUCCESS",
            apogee=simulation_payload["summary"]["apogee"],
            max_velocity=simulation_payload["summary"]["max_velocity"],
            max_acceleration=simulation_payload["summary"]["max_acceleration"],
            flight_duration=simulation_payload["summary"]["flight_duration"],
            summary=simulation_payload["summary"],
            time_series=simulation_payload["time_series"],
            raw_result=simulation_payload["raw_result"],
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return result

    @staticmethod
    def list_by_mission(db: Session, mission_id: str) -> list[SimulationResult]:
        mission_id = normalize_uuid(mission_id, "mission_id")
        SimulationService._ensure_mission_exists(db, mission_id)
        return list(
            db.scalars(
                select(SimulationResult)
                .where(SimulationResult.mission_id == mission_id)
                .order_by(SimulationResult.created_at.desc())
            )
        )

    @staticmethod
    def get_simulation(db: Session, simulation_id: str) -> SimulationResult:
        simulation_id = normalize_uuid(simulation_id, "simulation_id")
        result = db.get(SimulationResult, simulation_id)
        if result is None:
            raise ResourceNotFoundError("Simulation result not found")
        return result

    @staticmethod
    def delete_simulation(db: Session, simulation_id: str) -> None:
        result = SimulationService.get_simulation(db, simulation_id)
        db.delete(result)
        db.commit()

    @staticmethod
    def compare_simulations(db: Session, payload: SimulationCompareRequest) -> dict:
        normalized_ids = [normalize_uuid(simulation_id, "simulation_ids") for simulation_id in payload.simulation_ids]

        if len(set(normalized_ids)) != len(normalized_ids):
            raise BusinessRuleError(
                "Simulation IDs must be unique",
                details=[{"field": "simulation_ids", "message": "Duplicate simulation IDs are not allowed"}],
            )

        results = list(
            db.scalars(
                select(SimulationResult).where(SimulationResult.id.in_(normalized_ids))
            )
        )
        found_by_id = {result.id: result for result in results}
        missing_ids = [simulation_id for simulation_id in normalized_ids if simulation_id not in found_by_id]

        if missing_ids:
            raise ResourceNotFoundError("One or more simulation results were not found")

        ordered_results = [found_by_id[simulation_id] for simulation_id in normalized_ids]
        items = [SimulationService._comparison_item(result) for result in ordered_results]
        best_result = SimulationService._best_result(items)

        baseline = items[0]["summary"]
        differences = []
        for item in items[1:]:
            summary = item["summary"]
            differences.append(
                {
                    "simulation_id": item["simulation_id"],
                    "against_simulation_id": items[0]["simulation_id"],
                    "apogee_delta": round(summary["apogee"] - baseline["apogee"], 2),
                    "max_velocity_delta": round(summary["max_velocity"] - baseline["max_velocity"], 2),
                    "max_acceleration_delta": round(summary["max_acceleration"] - baseline["max_acceleration"], 2),
                    "flight_duration_delta": round(summary["flight_duration"] - baseline["flight_duration"], 2),
                }
            )

        return {
            "items": items,
            "best_result": best_result,
            "differences": differences,
        }

    @staticmethod
    def _ensure_mission_exists(db: Session, mission_id: str) -> None:
        if db.get(Mission, mission_id) is None:
            raise ResourceNotFoundError("Mission not found")

    @staticmethod
    def _get_rocket_with_engine(db: Session, rocket_id: str) -> Rocket:
        rocket = db.scalar(
            select(Rocket)
            .options(joinedload(Rocket.engine))
            .where(Rocket.id == rocket_id)
        )
        if rocket is None:
            raise ResourceNotFoundError("Rocket configuration not found")
        return rocket

    @staticmethod
    def _comparison_item(result: SimulationResult) -> dict:
        return {
            "simulation_id": result.id,
            "mission_id": result.mission_id,
            "rocket_id": result.rocket_id,
            "status": result.status,
            "summary": {
                "apogee": result.apogee or 0,
                "max_velocity": result.max_velocity or 0,
                "max_acceleration": result.max_acceleration or 0,
                "flight_duration": result.flight_duration or 0,
            },
        }

    @staticmethod
    def _best_result(items: list[dict]) -> dict:
        return {
            "highest_apogee_simulation_id": max(items, key=lambda item: item["summary"]["apogee"])["simulation_id"],
            "highest_velocity_simulation_id": max(items, key=lambda item: item["summary"]["max_velocity"])["simulation_id"],
            "highest_acceleration_simulation_id": max(items, key=lambda item: item["summary"]["max_acceleration"])["simulation_id"],
            "longest_flight_duration_simulation_id": max(items, key=lambda item: item["summary"]["flight_duration"])["simulation_id"],
        }

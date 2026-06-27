from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import success_response
from app.database.session import get_db
from app.schemas.simulation import SimulationCompareRequest, SimulationResultRead, SimulationRunRequest
from app.services.simulation_service import SimulationService


router = APIRouter()


def serialize_simulation(result) -> dict:
    return SimulationResultRead.model_validate(result).model_dump(mode="json")


@router.post("/simulations/run")
def run_simulation(payload: SimulationRunRequest, db: Session = Depends(get_db)) -> dict:
    result = SimulationService.run_simulation(db, payload)
    if isinstance(result, dict):
        return success_response(message="Simulation completed successfully", data=result)
    return success_response(message="Simulation completed successfully", data=serialize_simulation(result))


@router.post("/simulations/compare")
def compare_simulations(payload: SimulationCompareRequest, db: Session = Depends(get_db)) -> dict:
    comparison = SimulationService.compare_simulations(db, payload)
    return success_response(message="Simulation comparison generated successfully", data=comparison)


@router.get("/missions/{mission_id}/simulations")
def list_simulations_by_mission(mission_id: str, db: Session = Depends(get_db)) -> dict:
    results = SimulationService.list_by_mission(db, mission_id)
    return success_response(
        message="Simulation results retrieved successfully",
        data=[serialize_simulation(result) for result in results],
    )


@router.get("/simulations/{simulation_id}")
def get_simulation(simulation_id: str, db: Session = Depends(get_db)) -> dict:
    result = SimulationService.get_simulation(db, simulation_id)
    return success_response(message="Simulation result retrieved successfully", data=serialize_simulation(result))


@router.delete("/simulations/{simulation_id}")
def delete_simulation(simulation_id: str, db: Session = Depends(get_db)) -> dict:
    SimulationService.delete_simulation(db, simulation_id)
    return success_response(message="Simulation result deleted successfully", data=None)

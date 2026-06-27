from datetime import datetime

from pydantic import BaseModel


class BestApogeeSummary(BaseModel):
    value: float | None = None
    unit: str = "m"
    simulation_id: str | None = None


class LatestSimulationSummary(BaseModel):
    id: str | None = None
    status: str | None = None
    created_at: datetime | None = None


class DashboardSummary(BaseModel):
    total_missions: int
    total_engines: int
    total_rockets: int
    total_simulations: int
    total_calculator_results: int
    best_apogee: BestApogeeSummary
    latest_simulation: LatestSimulationSummary

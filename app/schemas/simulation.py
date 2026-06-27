from __future__ import annotations

from datetime import date as Date
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SimulationEnvironment(BaseModel):
    latitude: float = Field(default=0, ge=-90, le=90)
    longitude: float = Field(default=0, ge=-180, le=180)
    elevation: float = 0
    date: Date | None = None


class SimulationOptions(BaseModel):
    store_result: bool = True
    include_time_series: bool = True


class SimulationRunRequest(BaseModel):
    mission_id: str
    rocket_id: str
    environment: SimulationEnvironment = Field(default_factory=SimulationEnvironment)
    options: SimulationOptions = Field(default_factory=SimulationOptions)


class SimulationCompareRequest(BaseModel):
    simulation_ids: list[str] = Field(min_length=2, max_length=5)


class SimulationSummary(BaseModel):
    apogee: float
    max_velocity: float
    max_acceleration: float
    flight_duration: float


class SimulationResultRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    mission_id: str
    rocket_id: str
    status: str
    apogee: float | None = None
    max_velocity: float | None = None
    max_acceleration: float | None = None
    flight_duration: float | None = None
    summary: dict | None = None
    time_series: dict | None = None
    raw_result: dict | None = None
    error_message: str | None = None
    created_at: datetime

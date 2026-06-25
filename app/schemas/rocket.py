from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.engine import EngineRead


class RocketInput(BaseModel):
    wet_mass: float = Field(gt=0)
    dry_mass: float = Field(gt=0)
    isp: float = Field(gt=0)
    thrust: float = Field(gt=0)


class RocketCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    wet_mass: float = Field(gt=0)
    dry_mass: float = Field(gt=0)
    payload_mass: float = Field(ge=0)
    engine_id: str
    diameter: float | None = Field(default=None, gt=0)
    length: float | None = Field(default=None, gt=0)
    drag_coefficient: float | None = Field(default=None, gt=0)
    notes: str | None = None


class RocketUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    wet_mass: float | None = Field(default=None, gt=0)
    dry_mass: float | None = Field(default=None, gt=0)
    payload_mass: float | None = Field(default=None, ge=0)
    engine_id: str | None = None
    diameter: float | None = Field(default=None, gt=0)
    length: float | None = Field(default=None, gt=0)
    drag_coefficient: float | None = Field(default=None, gt=0)
    notes: str | None = None


class RocketRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    mission_id: str
    engine_id: str | None = None
    name: str
    wet_mass: float
    dry_mass: float
    payload_mass: float
    diameter: float | None = None
    length: float | None = None
    drag_coefficient: float | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class RocketDetailRead(RocketRead):
    engine: EngineRead | None = None

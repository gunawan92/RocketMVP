from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.engine import EngineRead


class RocketGeometry(BaseModel):
    diameter: float | None = Field(default=None, gt=0)
    length: float | None = Field(default=None, gt=0)
    drag_coefficient: float | None = Field(default=None, gt=0)
    center_of_mass_position: float | None = Field(default=None, ge=0)
    motor_position: float | None = Field(default=None, ge=0)
    nose_length: float | None = Field(default=None, gt=0)
    nose_kind: str | None = Field(default=None, max_length=80)
    fin_count: int | None = Field(default=None, gt=0)
    fin_root_chord: float | None = Field(default=None, gt=0)
    fin_tip_chord: float | None = Field(default=None, gt=0)
    fin_span: float | None = Field(default=None, gt=0)
    fin_position: float | None = Field(default=None, ge=0)


class RocketInput(BaseModel):
    wet_mass: float = Field(gt=0)
    dry_mass: float = Field(gt=0)
    isp: float = Field(gt=0)
    thrust: float = Field(gt=0)


class RocketCreate(RocketGeometry):
    name: str = Field(min_length=1, max_length=150)
    wet_mass: float = Field(gt=0)
    dry_mass: float = Field(gt=0)
    payload_mass: float = Field(ge=0)
    engine_id: str
    notes: str | None = None


class RocketUpdate(RocketGeometry):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    wet_mass: float | None = Field(default=None, gt=0)
    dry_mass: float | None = Field(default=None, gt=0)
    payload_mass: float | None = Field(default=None, ge=0)
    engine_id: str | None = None
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
    center_of_mass_position: float | None = None
    motor_position: float | None = None
    nose_length: float | None = None
    nose_kind: str | None = None
    fin_count: int | None = None
    fin_root_chord: float | None = None
    fin_tip_chord: float | None = None
    fin_span: float | None = None
    fin_position: float | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class RocketDetailRead(RocketRead):
    engine: EngineRead | None = None

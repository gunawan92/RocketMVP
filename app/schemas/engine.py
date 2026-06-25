from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EngineCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    thrust: float = Field(gt=0)
    isp: float = Field(gt=0)
    burn_time: float = Field(gt=0)
    propellant_mass: float | None = Field(default=None, ge=0)
    manufacturer: str | None = Field(default=None, max_length=150)
    notes: str | None = None


class EngineUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    thrust: float | None = Field(default=None, gt=0)
    isp: float | None = Field(default=None, gt=0)
    burn_time: float | None = Field(default=None, gt=0)
    propellant_mass: float | None = Field(default=None, ge=0)
    manufacturer: str | None = Field(default=None, max_length=150)
    notes: str | None = None


class EngineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    thrust: float
    isp: float
    burn_time: float | None = None
    propellant_mass: float | None = None
    manufacturer: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime

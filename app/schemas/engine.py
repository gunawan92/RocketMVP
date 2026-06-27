from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MotorCurvePoint(BaseModel):
    time: float = Field(ge=0)
    thrust: float = Field(ge=0)


class EngineBase(BaseModel):
    motor_curve: list[MotorCurvePoint] | None = None
    nozzle_radius: float | None = Field(default=None, gt=0)
    throat_radius: float | None = Field(default=None, gt=0)

    @field_validator("motor_curve")
    @classmethod
    def validate_motor_curve(cls, value: list[MotorCurvePoint] | None) -> list[MotorCurvePoint] | None:
        if value is None:
            return value
        if len(value) < 2:
            raise ValueError("motor_curve must contain at least two points")

        times = [point.time for point in value]
        if times != sorted(times) or len(set(times)) != len(times):
            raise ValueError("motor_curve time values must be strictly increasing")
        if value[0].time != 0:
            raise ValueError("motor_curve must start at time 0")
        if max(point.thrust for point in value) <= 0:
            raise ValueError("motor_curve must contain positive thrust")
        return value


class EngineCreate(EngineBase):
    name: str = Field(min_length=1, max_length=150)
    thrust: float = Field(gt=0)
    isp: float = Field(gt=0)
    burn_time: float = Field(gt=0)
    propellant_mass: float | None = Field(default=None, ge=0)
    manufacturer: str | None = Field(default=None, max_length=150)
    notes: str | None = None


class EngineUpdate(EngineBase):
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
    motor_curve: list[MotorCurvePoint] | None = None
    nozzle_radius: float | None = None
    throat_radius: float | None = None
    manufacturer: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime

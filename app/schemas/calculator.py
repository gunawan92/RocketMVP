from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CalculatorStoreMixin(BaseModel):
    mission_id: str | None = None
    rocket_id: str | None = None
    store_result: bool = False


class DeltaVRequest(CalculatorStoreMixin):
    isp: float = Field(gt=0)
    wet_mass: float = Field(gt=0)
    dry_mass: float = Field(gt=0)


class TwrRequest(CalculatorStoreMixin):
    thrust: float = Field(gt=0)
    mass: float = Field(gt=0)


class PayloadFractionRequest(CalculatorStoreMixin):
    payload_mass: float = Field(ge=0)
    total_mass: float = Field(gt=0)


class MassRatioRequest(CalculatorStoreMixin):
    wet_mass: float = Field(gt=0)
    dry_mass: float = Field(gt=0)


class CalculatorResultRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    mission_id: str | None = None
    rocket_id: str | None = None
    calculator_type: str
    input_data: dict
    result_data: dict
    created_at: datetime

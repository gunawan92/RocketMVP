from pydantic import BaseModel, Field


class DeltaVRequest(BaseModel):
    isp: float = Field(gt=0)
    wet_mass: float = Field(gt=0)
    dry_mass: float = Field(gt=0)


class TwrRequest(BaseModel):
    thrust: float = Field(gt=0)
    mass: float = Field(gt=0)


class PayloadFractionRequest(BaseModel):
    payload_mass: float = Field(ge=0)
    total_mass: float = Field(gt=0)


class MassRatioRequest(BaseModel):
    wet_mass: float = Field(gt=0)
    dry_mass: float = Field(gt=0)

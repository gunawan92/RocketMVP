from pydantic import BaseModel, Field


class RocketInput(BaseModel):
    wet_mass: float = Field(gt=0)
    dry_mass: float = Field(gt=0)
    isp: float = Field(gt=0)
    thrust: float = Field(gt=0)

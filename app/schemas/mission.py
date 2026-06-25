from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


MISSION_STATUSES = {"DRAFT", "READY", "SIMULATED", "ARCHIVED"}


class MissionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None


class MissionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    status: str | None = None


class MissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None = None
    status: str
    created_at: datetime
    updated_at: datetime

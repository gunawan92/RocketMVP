from pydantic import BaseModel, Field


class MissionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None


class MissionRead(MissionCreate):
    id: str
    status: str = "draft"

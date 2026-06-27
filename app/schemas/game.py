from typing import Literal

from pydantic import BaseModel, Field


NoseConeType = Literal["short", "medium", "sharp"]
FinSizeType = Literal["small", "medium", "large"]
EnginePresetId = Literal["A", "B", "C", "D"]
WeatherPresetId = Literal["clear", "cloudy", "windy", "storm"]
FuelStageType = Literal["single", "two", "three"]


class GameEnginePreset(BaseModel):
    id: EnginePresetId
    name: str
    description: str
    thrust: float
    isp: float
    burn_time: float
    propellant_mass: float
    unlock_level: int


class GameWeatherPreset(BaseModel):
    id: WeatherPresetId
    name: str
    description: str
    wind_speed: float
    turbulence: float
    difficulty_multiplier: float


class MissionChallenge(BaseModel):
    id: str
    title: str
    target_apogee: float
    reward: str
    level: int
    description: str


class SandboxRunRequest(BaseModel):
    mode: Literal["sandbox", "challenge"] = "sandbox"
    challenge_id: str | None = None
    rocket_height: float = Field(ge=5, le=50)
    rocket_diameter: float = Field(ge=0.5, le=5)
    nose_cone: NoseConeType = "medium"
    fin_size: FinSizeType = "medium"
    payload_mass: float = Field(ge=5, le=100)
    engine_preset: EnginePresetId = "A"
    fuel_stages: FuelStageType = "single"
    weather_preset: WeatherPresetId = "clear"


class GameScoreBreakdown(BaseModel):
    mission_success: float
    fuel_efficiency: float
    payload_delivery: float
    stability: float


class LearningFeedback(BaseModel):
    title: str
    message: str
    suggestions: list[str]


class SandboxRunResult(BaseModel):
    mode: str
    mission_success: bool
    mission_status: str
    score: int
    stars: int
    score_breakdown: GameScoreBreakdown
    failures: list[str]
    learning_feedback: LearningFeedback
    summary: dict
    selected_configuration: dict

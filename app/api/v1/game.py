from fastapi import APIRouter

from app.core.responses import success_response
from app.schemas.game import SandboxRunRequest
from app.services.game_service import GameService


router = APIRouter()


@router.get("/game/engine-presets")
def list_engine_presets() -> dict:
    return success_response(
        message="Engine presets retrieved successfully",
        data=[preset.model_dump(mode="json") for preset in GameService.list_engine_presets()],
    )


@router.get("/game/weather-presets")
def list_weather_presets() -> dict:
    return success_response(
        message="Weather presets retrieved successfully",
        data=[preset.model_dump(mode="json") for preset in GameService.list_weather_presets()],
    )


@router.get("/game/challenges")
def list_challenges() -> dict:
    return success_response(
        message="Mission challenges retrieved successfully",
        data=[challenge.model_dump(mode="json") for challenge in GameService.list_challenges()],
    )


@router.post("/game/sandbox/run")
def run_sandbox(payload: SandboxRunRequest) -> dict:
    result = GameService.run_sandbox(payload)
    return success_response(
        message="Sandbox simulation completed successfully",
        data=result.model_dump(mode="json"),
    )

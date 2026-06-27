from fastapi import APIRouter

from app.api.v1.calculators import router as calculators_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.engines import router as engines_router
from app.api.v1.game import router as game_router
from app.api.v1.health import router as health_router
from app.api.v1.missions import router as missions_router
from app.api.v1.rockets import router as rockets_router
from app.api.v1.simulations import router as simulations_router


api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(calculators_router, prefix="/calculators", tags=["calculators"])
api_router.include_router(missions_router, tags=["missions"])
api_router.include_router(engines_router, tags=["engines"])
api_router.include_router(game_router, tags=["game"])
api_router.include_router(rockets_router, tags=["rockets"])
api_router.include_router(simulations_router, tags=["simulations"])
api_router.include_router(dashboard_router, tags=["dashboard"])

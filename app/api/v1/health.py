from fastapi import APIRouter

from app.core.config import get_settings
from app.core.responses import success_response


router = APIRouter()


@router.get("/health")
def health() -> dict:
    settings = get_settings()
    return success_response(
        message="Service is healthy",
        data={
            "service": settings.app_name,
            "status": "healthy",
            "version": settings.app_version,
        },
    )

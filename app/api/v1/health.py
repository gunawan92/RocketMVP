from fastapi import APIRouter

from app.core.config import get_settings
from app.core.responses import success_response
from app.database.session import check_database_connection


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


@router.get("/health/db")
def database_health() -> dict:
    check_database_connection()
    return success_response(
        message="Database connection is healthy",
        data={
            "database": "postgresql",
            "status": "healthy",
        },
    )

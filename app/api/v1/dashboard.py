from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import success_response
from app.database.session import get_db
from app.services.dashboard_service import DashboardService


router = APIRouter()


@router.get("/dashboard/summary")
def get_dashboard_summary(db: Session = Depends(get_db)) -> dict:
    summary = DashboardService.get_summary(db)
    return success_response(
        message="Dashboard summary retrieved successfully",
        data=summary.model_dump(mode="json"),
    )

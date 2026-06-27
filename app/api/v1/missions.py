from math import ceil

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.responses import success_response
from app.database.session import get_db
from app.schemas.mission import MissionCreate, MissionRead, MissionUpdate
from app.services.mission_service import MissionService


router = APIRouter()


def serialize_mission(mission) -> dict:
    return MissionRead.model_validate(mission).model_dump(mode="json")


@router.post("/missions", status_code=status.HTTP_201_CREATED)
def create_mission(payload: MissionCreate, db: Session = Depends(get_db)) -> dict:
    mission = MissionService.create_mission(db, payload)
    return success_response(
        message="Mission created successfully",
        data=serialize_mission(mission),
    )


@router.get("/missions")
def list_missions(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    status_filter: str | None = Query(default=None, alias="status"),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    missions, total = MissionService.list_missions(db, page=page, limit=limit, status=status_filter, search=search)
    return success_response(
        message="Missions retrieved successfully",
        data=[serialize_mission(mission) for mission in missions],
        meta={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": ceil(total / limit) if total else 0,
        },
    )


@router.get("/missions/{mission_id}")
def get_mission(mission_id: str, db: Session = Depends(get_db)) -> dict:
    mission = MissionService.get_mission(db, mission_id)
    return success_response(
        message="Mission retrieved successfully",
        data=serialize_mission(mission),
    )


@router.put("/missions/{mission_id}")
def update_mission(mission_id: str, payload: MissionUpdate, db: Session = Depends(get_db)) -> dict:
    mission = MissionService.update_mission(db, mission_id, payload)
    return success_response(
        message="Mission updated successfully",
        data=serialize_mission(mission),
    )


@router.delete("/missions/{mission_id}")
def delete_mission(mission_id: str, db: Session = Depends(get_db)) -> dict:
    MissionService.delete_mission(db, mission_id)
    return success_response(message="Mission deleted successfully", data=None)

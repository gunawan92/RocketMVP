from math import ceil

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.responses import success_response
from app.database.session import get_db
from app.schemas.rocket import RocketCreate, RocketDetailRead, RocketRead, RocketUpdate
from app.services.rocket_service import RocketService


router = APIRouter()


def serialize_rocket(rocket) -> dict:
    return RocketRead.model_validate(rocket).model_dump(mode="json")


def serialize_rocket_detail(rocket) -> dict:
    return RocketDetailRead.model_validate(rocket).model_dump(mode="json")


@router.post("/missions/{mission_id}/rockets", status_code=status.HTTP_201_CREATED)
def create_rocket(mission_id: str, payload: RocketCreate, db: Session = Depends(get_db)) -> dict:
    rocket = RocketService.create_rocket(db, mission_id, payload)
    return success_response(
        message="Rocket configuration created successfully",
        data=serialize_rocket(rocket),
    )


@router.get("/missions/{mission_id}/rockets")
def list_rockets_by_mission(
    mission_id: str,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict:
    rockets, total = RocketService.list_rockets_by_mission(db, mission_id, page=page, limit=limit)
    return success_response(
        message="Rocket configurations retrieved successfully",
        data=[serialize_rocket(rocket) for rocket in rockets],
        meta={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": ceil(total / limit) if total else 0,
        },
    )


@router.get("/rockets/{rocket_id}")
def get_rocket(rocket_id: str, db: Session = Depends(get_db)) -> dict:
    rocket = RocketService.get_rocket(db, rocket_id)
    return success_response(
        message="Rocket configuration retrieved successfully",
        data=serialize_rocket_detail(rocket),
    )


@router.put("/rockets/{rocket_id}")
def update_rocket(rocket_id: str, payload: RocketUpdate, db: Session = Depends(get_db)) -> dict:
    rocket = RocketService.update_rocket(db, rocket_id, payload)
    return success_response(
        message="Rocket configuration updated successfully",
        data=serialize_rocket(rocket),
    )


@router.delete("/rockets/{rocket_id}")
def delete_rocket(rocket_id: str, db: Session = Depends(get_db)) -> dict:
    RocketService.delete_rocket(db, rocket_id)
    return success_response(message="Rocket configuration deleted successfully", data=None)

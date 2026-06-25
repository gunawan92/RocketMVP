from math import ceil

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.responses import success_response
from app.database.session import get_db
from app.schemas.engine import EngineCreate, EngineRead, EngineUpdate
from app.services.engine_service import EngineService


router = APIRouter()


def serialize_engine(engine) -> dict:
    return EngineRead.model_validate(engine).model_dump(mode="json")


@router.post("/engines", status_code=status.HTTP_201_CREATED)
def create_engine(payload: EngineCreate, db: Session = Depends(get_db)) -> dict:
    engine = EngineService.create_engine(db, payload)
    return success_response(
        message="Engine created successfully",
        data=serialize_engine(engine),
    )


@router.get("/engines")
def list_engines(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    engines, total = EngineService.list_engines(db, page=page, limit=limit, search=search)
    return success_response(
        message="Engines retrieved successfully",
        data=[serialize_engine(engine) for engine in engines],
        meta={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": ceil(total / limit) if total else 0,
        },
    )


@router.get("/engines/{engine_id}")
def get_engine(engine_id: str, db: Session = Depends(get_db)) -> dict:
    engine = EngineService.get_engine(db, engine_id)
    return success_response(
        message="Engine retrieved successfully",
        data=serialize_engine(engine),
    )


@router.put("/engines/{engine_id}")
def update_engine(engine_id: str, payload: EngineUpdate, db: Session = Depends(get_db)) -> dict:
    engine = EngineService.update_engine(db, engine_id, payload)
    return success_response(
        message="Engine updated successfully",
        data=serialize_engine(engine),
    )


@router.delete("/engines/{engine_id}")
def delete_engine(engine_id: str, db: Session = Depends(get_db)) -> dict:
    EngineService.delete_engine(db, engine_id)
    return success_response(message="Engine deleted successfully", data=None)

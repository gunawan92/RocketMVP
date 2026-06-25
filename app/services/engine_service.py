from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, ResourceNotFoundError
from app.core.ids import normalize_uuid
from app.models.engine import Engine
from app.models.rocket import Rocket
from app.schemas.engine import EngineCreate, EngineUpdate


class EngineService:
    @staticmethod
    def create_engine(db: Session, payload: EngineCreate) -> Engine:
        engine = Engine(**payload.model_dump())
        db.add(engine)
        db.commit()
        db.refresh(engine)
        return engine

    @staticmethod
    def list_engines(
        db: Session,
        page: int = 1,
        limit: int = 10,
        search: str | None = None,
    ) -> tuple[list[Engine], int]:
        page = max(page, 1)
        limit = min(max(limit, 1), 100)

        statement = select(Engine)
        count_statement = select(func.count()).select_from(Engine)

        if search:
            pattern = f"%{search}%"
            statement = statement.where(Engine.name.ilike(pattern))
            count_statement = count_statement.where(Engine.name.ilike(pattern))

        total = db.scalar(count_statement) or 0
        engines = list(
            db.scalars(
                statement.order_by(Engine.created_at.desc())
                .offset((page - 1) * limit)
                .limit(limit)
            )
        )
        return engines, total

    @staticmethod
    def get_engine(db: Session, engine_id: str) -> Engine:
        engine_id = normalize_uuid(engine_id, "engine_id")
        engine = db.get(Engine, engine_id)
        if engine is None:
            raise ResourceNotFoundError("Engine not found")
        return engine

    @staticmethod
    def update_engine(db: Session, engine_id: str, payload: EngineUpdate) -> Engine:
        engine = EngineService.get_engine(db, engine_id)
        data = payload.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(engine, field, value)

        db.commit()
        db.refresh(engine)
        return engine

    @staticmethod
    def delete_engine(db: Session, engine_id: str) -> None:
        engine_id = normalize_uuid(engine_id, "engine_id")
        engine = EngineService.get_engine(db, engine_id)
        used_count = db.scalar(select(func.count()).select_from(Rocket).where(Rocket.engine_id == engine_id)) or 0

        if used_count > 0:
            raise BusinessRuleError(
                "Engine cannot be deleted because it is used by rocket configuration",
                details=[
                    {
                        "field": "engine_id",
                        "message": "Engine is still used by one or more rocket configurations",
                    }
                ],
            )

        db.delete(engine)
        db.commit()

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, ResourceNotFoundError
from app.core.ids import normalize_uuid
from app.models.mission import Mission
from app.schemas.mission import MISSION_STATUSES, MissionCreate, MissionUpdate


class MissionService:
    @staticmethod
    def create_mission(db: Session, payload: MissionCreate) -> Mission:
        mission = Mission(name=payload.name, description=payload.description, status="DRAFT")
        db.add(mission)
        db.commit()
        db.refresh(mission)
        return mission

    @staticmethod
    def list_missions(db: Session, page: int = 1, limit: int = 10, status: str | None = None) -> tuple[list[Mission], int]:
        if status is not None:
            status = status.upper()
            MissionService._validate_status(status)

        page = max(page, 1)
        limit = min(max(limit, 1), 100)

        statement = select(Mission)
        count_statement = select(func.count()).select_from(Mission)

        if status is not None:
            statement = statement.where(Mission.status == status)
            count_statement = count_statement.where(Mission.status == status)

        total = db.scalar(count_statement) or 0
        missions = list(
            db.scalars(
                statement.order_by(Mission.created_at.desc())
                .offset((page - 1) * limit)
                .limit(limit)
            )
        )
        return missions, total

    @staticmethod
    def get_mission(db: Session, mission_id: str) -> Mission:
        mission_id = normalize_uuid(mission_id, "mission_id")
        mission = db.get(Mission, mission_id)
        if mission is None:
            raise ResourceNotFoundError("Mission not found")
        return mission

    @staticmethod
    def update_mission(db: Session, mission_id: str, payload: MissionUpdate) -> Mission:
        mission = MissionService.get_mission(db, mission_id)
        data = payload.model_dump(exclude_unset=True)

        if "status" in data and data["status"] is not None:
            data["status"] = data["status"].upper()
            MissionService._validate_status(data["status"])

        for field, value in data.items():
            setattr(mission, field, value)

        db.commit()
        db.refresh(mission)
        return mission

    @staticmethod
    def delete_mission(db: Session, mission_id: str) -> None:
        mission = MissionService.get_mission(db, mission_id)
        db.delete(mission)
        db.commit()

    @staticmethod
    def _validate_status(status: str) -> None:
        if status not in MISSION_STATUSES:
            raise BusinessRuleError(
                "Invalid mission status",
                details=[
                    {
                        "field": "status",
                        "message": f"Status must be one of: {', '.join(sorted(MISSION_STATUSES))}",
                    }
                ],
            )

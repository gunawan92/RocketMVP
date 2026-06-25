from app.schemas.calculator import DeltaVRequest, TwrRequest
from app.core.exceptions import BusinessRuleError, ResourceNotFoundError
from app.core.ids import normalize_uuid
from app.models.engine import Engine
from app.models.mission import Mission
from app.models.rocket import Rocket
from app.schemas.rocket import RocketCreate, RocketUpdate
from app.services.calculator_service import CalculatorService
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload


class RocketService:
    @staticmethod
    def calculate_delta_v(wet_mass, dry_mass, isp):
        result = CalculatorService.calculate_delta_v(
            DeltaVRequest(isp=isp, wet_mass=wet_mass, dry_mass=dry_mass)
        )
        return result["result"]["delta_v"]

    @staticmethod
    def calculate_twr(thrust, wet_mass):
        result = CalculatorService.calculate_twr(TwrRequest(thrust=thrust, mass=wet_mass))
        return result["result"]["twr"]

    @staticmethod
    def create_rocket(db: Session, mission_id: str, payload: RocketCreate) -> Rocket:
        mission_id = normalize_uuid(mission_id, "mission_id")
        engine_id = normalize_uuid(payload.engine_id, "engine_id")
        RocketService._ensure_mission_exists(db, mission_id)
        RocketService._ensure_engine_exists(db, engine_id)
        RocketService._validate_mass_relationship(
            wet_mass=payload.wet_mass,
            dry_mass=payload.dry_mass,
            payload_mass=payload.payload_mass,
        )

        data = payload.model_dump()
        data["engine_id"] = engine_id
        rocket = Rocket(mission_id=mission_id, **data)
        db.add(rocket)
        db.commit()
        db.refresh(rocket)
        return rocket

    @staticmethod
    def list_rockets_by_mission(
        db: Session,
        mission_id: str,
        page: int = 1,
        limit: int = 10,
    ) -> tuple[list[Rocket], int]:
        mission_id = normalize_uuid(mission_id, "mission_id")
        RocketService._ensure_mission_exists(db, mission_id)
        page = max(page, 1)
        limit = min(max(limit, 1), 100)

        statement = select(Rocket).where(Rocket.mission_id == mission_id)
        count_statement = select(func.count()).select_from(Rocket).where(Rocket.mission_id == mission_id)

        total = db.scalar(count_statement) or 0
        rockets = list(
            db.scalars(
                statement.order_by(Rocket.created_at.desc())
                .offset((page - 1) * limit)
                .limit(limit)
            )
        )
        return rockets, total

    @staticmethod
    def get_rocket(db: Session, rocket_id: str) -> Rocket:
        rocket_id = normalize_uuid(rocket_id, "rocket_id")
        rocket = db.scalar(
            select(Rocket)
            .options(joinedload(Rocket.engine))
            .where(Rocket.id == rocket_id)
        )
        if rocket is None:
            raise ResourceNotFoundError("Rocket configuration not found")
        return rocket

    @staticmethod
    def update_rocket(db: Session, rocket_id: str, payload: RocketUpdate) -> Rocket:
        rocket_id = normalize_uuid(rocket_id, "rocket_id")
        rocket = RocketService.get_rocket(db, rocket_id)
        data = payload.model_dump(exclude_unset=True)

        if "engine_id" in data and data["engine_id"] is not None:
            data["engine_id"] = normalize_uuid(data["engine_id"], "engine_id")
            RocketService._ensure_engine_exists(db, data["engine_id"])

        wet_mass = data.get("wet_mass", rocket.wet_mass)
        dry_mass = data.get("dry_mass", rocket.dry_mass)
        payload_mass = data.get("payload_mass", rocket.payload_mass)
        RocketService._validate_mass_relationship(
            wet_mass=wet_mass,
            dry_mass=dry_mass,
            payload_mass=payload_mass,
        )

        for field, value in data.items():
            setattr(rocket, field, value)

        db.commit()
        db.refresh(rocket)
        return RocketService.get_rocket(db, rocket.id)

    @staticmethod
    def delete_rocket(db: Session, rocket_id: str) -> None:
        rocket_id = normalize_uuid(rocket_id, "rocket_id")
        rocket = RocketService.get_rocket(db, rocket_id)
        db.delete(rocket)
        db.commit()

    @staticmethod
    def _ensure_mission_exists(db: Session, mission_id: str) -> None:
        mission_id = normalize_uuid(mission_id, "mission_id")
        if db.get(Mission, mission_id) is None:
            raise ResourceNotFoundError("Mission not found")

    @staticmethod
    def _ensure_engine_exists(db: Session, engine_id: str) -> None:
        engine_id = normalize_uuid(engine_id, "engine_id")
        if db.get(Engine, engine_id) is None:
            raise ResourceNotFoundError("Engine not found")

    @staticmethod
    def _validate_mass_relationship(wet_mass: float, dry_mass: float, payload_mass: float) -> None:
        if wet_mass <= dry_mass:
            raise BusinessRuleError(
                "Wet mass must be greater than dry mass",
                details=[{"field": "wet_mass", "message": "Wet mass must be greater than dry mass"}],
            )
        if payload_mass > dry_mass:
            raise BusinessRuleError(
                "Payload mass cannot be greater than dry mass",
                details=[{"field": "payload_mass", "message": "Payload mass cannot be greater than dry mass"}],
            )

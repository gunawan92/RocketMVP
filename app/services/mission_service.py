from app.core.exceptions import ResourceNotFoundError
from app.schemas.mission import MissionCreate, MissionRead


class MissionService:
    _missions: list[MissionRead] = []

    @classmethod
    def create_mission(cls, payload: MissionCreate) -> MissionRead:
        mission = MissionRead(
            id=f"mission-{len(cls._missions) + 1}",
            name=payload.name,
            description=payload.description,
        )
        cls._missions.append(mission)
        return mission

    @classmethod
    def list_missions(cls) -> list[MissionRead]:
        return cls._missions

    @classmethod
    def get_mission(cls, mission_id: str) -> MissionRead:
        for mission in cls._missions:
            if mission.id == mission_id:
                return mission
        raise ResourceNotFoundError("Mission not found")

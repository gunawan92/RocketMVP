from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, UUIDPrimaryKeyMixin, utc_now


class SimulationResult(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "simulation_results"
    __table_args__ = (
        Index("idx_simulation_results_mission_id", "mission_id"),
        Index("idx_simulation_results_rocket_id", "rocket_id"),
        Index("idx_simulation_results_status", "status"),
        Index("idx_simulation_results_created_at", "created_at"),
    )

    mission_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("missions.id", ondelete="CASCADE"), nullable=False)
    rocket_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("rockets.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="PENDING", nullable=False)
    apogee: Mapped[float | None]
    max_velocity: Mapped[float | None]
    max_acceleration: Mapped[float | None]
    flight_duration: Mapped[float | None]
    summary: Mapped[dict | None] = mapped_column(JSONB)
    time_series: Mapped[dict | None] = mapped_column(JSONB)
    raw_result: Mapped[dict | None] = mapped_column(JSONB)
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    mission: Mapped["Mission"] = relationship(back_populates="simulation_results")
    rocket: Mapped["Rocket"] = relationship(back_populates="simulation_results")

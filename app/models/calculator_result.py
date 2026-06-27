from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, GUID, JSONData, UUIDPrimaryKeyMixin, utc_now


class CalculatorResult(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "calculator_results"
    __table_args__ = (
        Index("idx_calculator_results_mission_id", "mission_id"),
        Index("idx_calculator_results_rocket_id", "rocket_id"),
        Index("idx_calculator_results_type", "calculator_type"),
    )

    mission_id: Mapped[str | None] = mapped_column(GUID(), ForeignKey("missions.id", ondelete="SET NULL"))
    rocket_id: Mapped[str | None] = mapped_column(GUID(), ForeignKey("rockets.id", ondelete="SET NULL"))
    calculator_type: Mapped[str] = mapped_column(String(100), nullable=False)
    input_data: Mapped[dict] = mapped_column(JSONData(), nullable=False)
    result_data: Mapped[dict] = mapped_column(JSONData(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    mission: Mapped["Mission | None"] = relationship(back_populates="calculator_results")
    rocket: Mapped["Rocket | None"] = relationship(back_populates="calculator_results")

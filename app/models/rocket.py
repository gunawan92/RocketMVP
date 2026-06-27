from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, GUID, TimestampMixin, UUIDPrimaryKeyMixin


class Rocket(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "rockets"
    __table_args__ = (
        CheckConstraint("wet_mass > 0", name="check_rocket_wet_mass_positive"),
        CheckConstraint("dry_mass > 0", name="check_rocket_dry_mass_positive"),
        CheckConstraint("payload_mass >= 0", name="check_rocket_payload_mass_non_negative"),
        CheckConstraint("wet_mass > dry_mass", name="check_rocket_wet_mass_greater_than_dry_mass"),
        CheckConstraint("payload_mass <= wet_mass", name="check_rocket_payload_not_greater_than_wet_mass"),
        CheckConstraint("diameter IS NULL OR diameter > 0", name="check_rocket_diameter_positive"),
        CheckConstraint("length IS NULL OR length > 0", name="check_rocket_length_positive"),
        CheckConstraint("drag_coefficient IS NULL OR drag_coefficient > 0", name="check_rocket_drag_coefficient_positive"),
        Index("idx_rockets_mission_id", "mission_id"),
        Index("idx_rockets_engine_id", "engine_id"),
    )

    mission_id: Mapped[str] = mapped_column(GUID(), ForeignKey("missions.id", ondelete="CASCADE"), nullable=False)
    engine_id: Mapped[str | None] = mapped_column(GUID(), ForeignKey("engines.id", ondelete="SET NULL"))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    wet_mass: Mapped[float] = mapped_column(nullable=False)
    dry_mass: Mapped[float] = mapped_column(nullable=False)
    payload_mass: Mapped[float] = mapped_column(nullable=False)
    diameter: Mapped[float | None]
    length: Mapped[float | None]
    drag_coefficient: Mapped[float | None]
    notes: Mapped[str | None] = mapped_column(Text)

    mission: Mapped["Mission"] = relationship(back_populates="rockets")
    engine: Mapped["Engine | None"] = relationship(back_populates="rockets")
    calculator_results: Mapped[list["CalculatorResult"]] = relationship(back_populates="rocket")
    simulation_results: Mapped[list["SimulationResult"]] = relationship(back_populates="rocket", cascade="all, delete-orphan")
